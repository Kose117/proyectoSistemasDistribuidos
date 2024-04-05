import datetime
import random
from Sensor import Sensor
from time import sleep
from Aspersor import Aspersor
import zmq


class SensorHumo(Sensor):
    def __init__(self, parametro1, parametro2):
        super().__init__(parametro1, parametro2)
        self.valores_booleanos = (True, False, "Error")

    def tomarMuestra(self, aspersor):
        while True:
            probabilidades = {
                "humo_detectado": self.pCorrecto,
                "error": self.pError,
            }
            eleccion = random.choices(
                list(probabilidades.keys()), probabilidades.values())[0]

            if eleccion == "humo_detectado":
                self.muestra['valor'] = random.choice([True, False])
            else:
                self.muestra['valor'] = "error"

            self.muestra['tipo'] = "alerta humo"
            self.muestra['hora'] = str(datetime.datetime.now())

            self.enviarAlertaProxy()
            if self.muestra['valor'] == True:
                self.enviarMensajeAspersor(aspersor)
                self.generarSistemaCalidad()
            sleep(3)

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

    def enviarAlertaProxy(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        # socket.bind("tcp://localhost:5555")
        socket.connect("tcp://localhost:5556")
        try:
            socket.send_pyobj(self.muestra)
            print("Muestra enviada al Proxy.")
        except zmq.ZMQError as e:
            print(f"Error al enviar la muestra: {e}")
        finally:
            socket.close()
            context.term()
