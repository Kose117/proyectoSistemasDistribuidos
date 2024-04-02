from Sensor import Sensor
from time import sleep


class SensorTemperatura(Sensor):
    def __init__(self, parametro1, parametro2):
        super().__init__(parametro1, parametro2)

    def tomarMuestra(self):
        sleep(6)
        print("Tomando muestra de temperatura")
        self.muestra['tipo'] = "temperatura"
        self.muestra['valor'] = "19.4"
        self.muestra['hora'] = "2:35"

        self.enviarMuestraProxy()
