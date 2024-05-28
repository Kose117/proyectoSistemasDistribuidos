from datetime import time
import zmq
from Alerta import Alerta

class Cloud:
    def __init__(self):
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.SUB)
            self.socket.bind("tcp://*:5560")  
            self.socket.setsockopt_string(zmq.SUBSCRIBE, "")  
            self.sumatoriahumedad = 0
            self.minimo_humedad = 70

    def recibirAlertas(self):
        while True:
            alerta_data = self.socket.recv_json()   
            alerta = Alerta(**alerta_data)  
            self.escribirEnArchivo(alerta)

    def escribirEnArchivo(self, alerta):
        with open("Alertas.txt", "a") as file:
            file.write(f"Fecha: {alerta.fecha}, Origen del sensor: {alerta.origen_sensor}, Tipo de alerta: {alerta.tipo_alerta}\n")

    def recibirInfoProxy(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5557")

        while True :
            message = socket.recv_pyobj()
            print(f"{message}")
            
            socket.send_string("Datos recibidos impresos")
            
    def calcularHumedadMensual():
        while True:
                time.sleep(20)
                valorCalculado = 0
                #hace falta que se calcule todo, NO ENTIENDO LA PERRA FORMULA. Sophia tampoco la entendio, asi que es a la de dios
                #if valorCalculado < self.minimo_humedad:
                    #alerta=Alerta("Humedad", "Alta", "El valor de humedad es inferior al minimo permitido")
                    #self.escribirEnArchivo(alerta)

if __name__ == "__main__":
    cloud = Cloud()    
    cloud.recibirInfoProxy()
