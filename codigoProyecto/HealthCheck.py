import threading
import time
import zmq

PrincipalActivo = False
lock = threading.Lock()


def main():
    threading.Thread(target=manejarPrincipal).start()
    threading.Thread(target=manejarSecundario).start()


def manejarPrincipal():
    context = zmq.Context()
    # para primera respuesta del fog
    receiver = context.socket(zmq.REP)
    receiver.bind(
        f"tcp://10.43.100.67:5568"
    )
    result = receiver.recv()
    print("PING RECIBIDO: {result}")
    print(result)
    receiver.send(b"Mensaje recibido por el SC")

    # request al principal
    sender = context.socket(zmq.REQ)
    sender.connect(
        f"tcp://10.43.103.83:5569" 
    )

    # Establecer un timeout de recepción de 5000 milisegundos (5 segundos)
    sender.setsockopt(zmq.RCVTIMEO, 5000)  # 5000 ms = 5 s
    global PrincipalActivo
    while True:
        try:
            sender.send_string("EXISTES?")
            message = sender.recv_string()
            print(f"Respuesta recibida: {message}")
            with lock:
                PrincipalActivo = True
                context = zmq.Context()
                socket = context.socket(zmq.REQ)
                socket.connect("tcp://10.43.101.24:5590")
                socket.send_string("10.43.103.83")
                resp = socket.recv_string()
                print(f"mensaje del sensor: {resp}")

            time.sleep(5)
        except zmq.error.Again:
            print("No se recibió respuesta en 5 segundos, reintentando...")
        except zmq.error.ZMQError as e:
            if e.errno == zmq.EFSM:  # Estado incorrecto del socket
                sender.close()
                sender = context.socket(zmq.REQ)
                sender.connect(
                    f"tcp://10.43.103.83:5569" 
                )
                sender.setsockopt(
                    zmq.RCVTIMEO, 5000
                )  # Timeout de 5 segundos para recibir
                with lock:
                    PrincipalActivo = False
                    context = zmq.Context()
                    socket = context.socket(zmq.REQ)
                    socket.connect("tcp://10.43.101.24:5590")
                    socket.send_string("10.43.100.67")
                    resp = socket.recv_string()
                    print(f"mensaje del sensor: {resp}")

                result = receiver.recv()
                print("PING RECIBIDO: {result}")
                print(result)
                receiver.send(b"Mensaje recibido por el SC")


def manejarSecundario():
    context = zmq.Context()
    # reply al secundario
    receiver = context.socket(zmq.REP)
    receiver.bind(
        f"tcp://10.43.100.67:5570"
    )

    while True:
        result = receiver.recv()
        print("PROXY2: {result}")
        print(result)
        with lock:
            receiver.send_string(f"{PrincipalActivo}")


if __name__ == "__main__":
    main()
