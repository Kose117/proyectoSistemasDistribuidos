from time import sleep
from datetime import time
import zmq
from Alerta import Alerta
import threading

class Cloud:
    def __init__(self): 
            self.sumatoriahumedad = 0
            self.minimo_humedad = 70

    def recibirAlertasProxy(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5560")  
        #self.socket.setsockopt_string(zmq.SUBSCRIBE, "") 
        while True:
           alerta = socket.recv_pyobj()  # Recibimos directamente la instancia de Alerta
           if isinstance(alerta, Alerta):
                self.escribirEnArchivo(alerta)
           else:
                print("Recibido objeto no esperado:", alerta)

           socket.send_string("Datos recibidos impresos")

    def escribirEnArchivo(self, alerta):
        with open("Alertas.txt", "a") as file:
            file.write(f"Fecha: {alerta.fecha}, Origen del sensor: {alerta.origen_sensor}, Tipo de alerta: {alerta.tipo_alerta}\n")

    def recibirInfoProxy(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5557")

        while True :
            message = socket.recv_string()
            self.calcularHumedadMensual(message)
            print(f"{message}")
            
            socket.send_string("Datos recibidos impresos")
            
    def calcularHumedadMensual(self, promedioHumedad):
        humedadesArray = []
        while True:
                humedadesArray.append(float(promedioHumedad))
                sleep(20)
                n = 4
                if(len(humedadesArray) == n):
                    self.sumatoriahumedad = sum(humedadesArray) / 4
                    print("Sumatoria de humedad: ",self.sumatoriahumedad)
                    if self.sumatoriahumedad  < self.minimo_humedad:
                        alerta=Alerta("Humedad", "Alta", "El valor de humedad es inferior al minimo permitido")
                        self.escribirEnArchivo(alerta)
                #hace falta que se calcule todo, NO ENTIENDO LA PERRA FORMULA. Sophia tampoco la entendio, asi que es a la de dios
                #if valorCalculado < self.minimo_humedad:
                    #alerta=Alerta("Humedad", "Alta", "El valor de humedad es inferior al minimo permitido")
                    #self.escribirEnArchivo(alerta)

if __name__ == "__main__":
    cloud = Cloud()  
    hiloCloud = threading.Thread(target= cloud.recibirInfoProxy)  
    hiloCloudAlert = threading.Thread(target= cloud.recibirAlertasProxy)

    hiloCloud.start()
    hiloCloudAlert.start()

    hiloCloud.join()
    hiloCloudAlert.join()