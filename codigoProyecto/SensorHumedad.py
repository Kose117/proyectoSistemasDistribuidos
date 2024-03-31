from Sensor import Sensor
from time import sleep


class SensorHumedad(Sensor):
    def __init__(self, parametro1, parametro2):
        super().__init__(parametro1, parametro2)

    def tomarMuestra(self):
        sleep(5)
        print("Tomando muestra de Humedad")
