import re
import zmq
from Muestra  import Muestra 

def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.bind("tcp://*:5555")  
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")  
        self.sumatoriahumedad = 0

def receive_alerts(self, muestra_data):
        muestra = Muestra(**muestra_data)  
        if muestra.tipo == "alerta":
            self.write_to_file(muestra)

def write_to_file(self, muestra):
        with open("Alertas.txt", "a") as file:
            file.write(f"Fecha: {muestra.fecha}, Origen del sensor: {muestra.origen_sensor}, Tipo de muestra: {muestra.tipo}\n")


def recibirInfoProxy(self):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5557")

    while True :
        message = socket.recv_pyobj()
        print(f"{message}")
        
        if re.search("alerta", message['tipo']):
            self.receive_alerts(message)
        
        socket.send_string("Datos recibidos impresos")
        


if __name__ == "__main__":
    cloud = Cloud()    
    cloud.recibirInfoProxy()
