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
    receiver.bind("tcp://10.43.100.67:5568")
    
    result = receiver.recv()
    print(f"PING RECIBIDO: {result}")
    receiver.send(b"Mensaje recibido por el SC")

    # request al principal
    sender = context.socket(zmq.REQ)
    sender.connect("tcp://10.43.103.83:5569")

    # Establecer un timeout de recepción de 5000 milisegundos (5 segundos)
    sender.setsockopt(zmq.RCVTIMEO, 5000)  # 5000 ms = 5 s
    
    push_socket = context.socket(zmq.PUSH)
    push_socket.connect("tcp://10.43.101.24:5590")

    global PrincipalActivo
    while True:
        try:
            sender.send_string("EXISTES?")
            message = sender.recv_string()
            print(f"Respuesta recibida: {message}")
            with lock:
                PrincipalActivo = True
            push_socket.send_string("10.43.103.83")
            print("Enviando ip 10.43.103.83")
            time.sleep(5)
        except zmq.error.Again:
            print("No se recibió respuesta en 5 segundos, reintentando...")
        except zmq.error.ZMQError as e:
            if e.errno == zmq.EFSM:  # Estado incorrecto del socket
                sender.close()
                sender = context.socket(zmq.REQ)
                sender.connect("tcp://10.43.103.83:5569")
                sender.setsockopt(zmq.RCVTIMEO, 5000)  # Timeout de 5 segundos para recibir
                with lock:
                    PrincipalActivo = False
                push_socket.send_string("10.43.100.67")
                print("Enviando ip 10.43.100.67")
                result = receiver.recv()
                print(f"PING RECIBIDO: {result}")
                receiver.send(b"Mensaje recibido por el SC")


def manejarSecundario():
    context = zmq.Context()
    # reply al secundario
    receiver = context.socket(zmq.REP)
    receiver.bind("tcp://10.43.100.67:5570")

    while True:
        result = receiver.recv()
        print(f"PROXY2: {result}")
        with lock:
            receiver.send_string(f"{PrincipalActivo}")


if __name__ == "__main__":
    main()
 