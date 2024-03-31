from Sensor import Sensor
from time import sleep


class SensorHumo(Sensor):
    def __init__(self, parametro1, parametro2):
        super().__init__(parametro1, parametro2)

    def tomarMuestra(self):
        sleep(3)
        print("Tomando muestra de Humo")

    # def generarSistemaCalidad(self):
        # Código para el método generarSistemaCalidad
        # Tiene que hacerse con request. reply

    # def enviarMensajeAspersor(self):
        # Código para el método enviarMensajeAspersor

    # def enviarAlertaProxy(self):
        # Código para el método enviarAlertaProxy
