import zmq
from Alerta import Alerta

class Cloud:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.bind("tcp://*:5555")  
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")  
        self.sumatoriahumedad = 0

    def receive_alerts(self):
        while True:
            alerta_data = self.socket.recv_json()  
            alerta = Alerta(**alerta_data) 
            self.write_to_file(alerta)

    def write_to_file(self, alerta):
        with open("Alertas.txt", "a") as file:
            file.write(f"Fecha: {alerta.fecha}, Origen del sensor: {alerta.origen_sensor}, Tipo de alerta: {alerta.tipo_alerta}\n")

    
            

if __name__ == "__main__":
    cloud = Cloud()
    cloud.receive_alerts()