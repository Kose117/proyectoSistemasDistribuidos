import zmq


class Proxy:

    def __init__(self):
        print("Creando proxy")

    def recibirAlertas(self):
        print("Recibiendo alertas")

    def recibirMuestras(self):

        context = zmq.Context()
        socket = context.socket(zmq.PULL)

        socket.bind("tcp://*:5556")
        try:
            while True:
                datos = socket.recv_pyobj()
                print("Muestra recibida en el Proxy:", datos)
                self.enviarDatosServidor(datos)
                print(datos)
        except zmq.ZMQError as e:
            print(f"Error al recibir la muestra: {e}")
        finally:
            socket.close()
            context.term()

    def enviarDatosServidor(self, datos):

        print("Enviando datos servidor")

    def validarDatos(self):
        print("Validando datos")

    def enviarMensajesCloud(self):
        print("Enviando mensajes cloud")
