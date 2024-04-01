from Sensor import Sensor
from time import sleep
import zmq


class SensorHumedad(Sensor):
    def __init__(self, parametro1, parametro2):
        super().__init__(parametro1, parametro2)

    def tomarMuestra(self):
        sleep(5)
        print("Tomando muestra de Humedad")
        self.muestra['tipo'] = "humedad"
        self.muestra['valor'] = "20"
        self.muestra['hora'] = "3:49"

        self.enviarMuestraProxy()

    
    def enviarMuestraProxy(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.bind("tcp://localhost:5555")

        socket.send_pyobj(self.muestra)

        socket.close()
        context.term()
