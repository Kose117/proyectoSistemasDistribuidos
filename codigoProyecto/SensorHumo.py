from Sensor import Sensor
from time import sleep
from Aspersor import Aspersor
import zmq




class SensorHumo(Sensor):
    def __init__(self, parametro1, parametro2):
        super().__init__(parametro1, parametro2)

    def tomarMuestra(self, aspersor):
        sleep(3)
        print("Tomando muestra de Humo")
        self.enviarMensajeAspersor(aspersor)
        self.generarSistemaCalidad()


    def generarSistemaCalidad(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")

        socket.send_string("Alerta: Sistema de Calidad")

        response = socket.recv_string()
        print(f"Sensor humo: recibe '{response}'del sistema de calidad")

        socket.close()
        context.term()


    def enviarMensajeAspersor(self, aspersor):
        aspersor.activarAspersor()

        # Código para el método enviarMensajeAspersor

    # def enviarAlertaProxy(self):
        # Código para el método enviarAlertaProxy
