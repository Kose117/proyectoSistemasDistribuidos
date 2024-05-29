from time import sleep
import zmq
import json
from datetime import datetime

from Alerta import Alerta


class ServidorLocal:
    
    def __init__(self):
        self.temperaturas = []
        self.humedades = []
    # Límites establecidos para los sensores
        self.TEMP_MAX = 29.4
        print("Creando servidor local")

    # HACE FALTA HACER QUE SE HAGA POR TIEMPO
    def procesarDatosSensor(self, tipo, valor, timestamp):
        if tipo == "temperatura":
            self.temperaturas.append(valor)
        elif tipo == "humedad":
            self.humedades.append(valor)

        if len(self.temperaturas) >= 10:
            promedioTemp = sum(self.temperaturas) / len(self.temperaturas)
            print(f"Promedio de Temperatura: {promedioTemp} - {timestamp}")
            promedioTemp = 35
            if promedioTemp > self.TEMP_MAX:
                self.enviarAlertaProxy("temperatura", promedioTemp, timestamp)
            self.temperaturas = []  # Resetear la lista para el próximo cálculo

        if len(self.humedades) == 10:
            sleep(5)
            promedioHumedad = sum(self.humedades) / len(self.humedades)
            print(f"Promedio de Humedad: {promedioHumedad} - {timestamp}")
            # enviar promedio al proxy
            self.enviarPromedioHumedad(promedioHumedad)
            self.humedades = []  # Resetear la lista para el próximo cálculo

    # def enviarAlertaSistemaCalidad(tipo, valor, timestamp):
    #     context = zmq.Context()
    #     socket = context.socket(zmq.REQ)
    #     socket.connect("tcp://localhost:5555")

    #     socket.send_string("Alerta: Sistema de Calidad")

    #     response = socket.recv_string()
    #     print(f"Sensor humo: recibe '{response}'del sistema de calidad")

    #     socket.close()
    #     context.term()
    def enviarPromedioHumedad(self, promedioHumedad):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5561")

        socket.send_string(str(promedioHumedad))

        response = socket.recv_string()
        print(f"Servidor local: recibe '{response}'del proxy")

        socket.close()
        context.term()

    def enviarAlertaProxy(self,tipo, valor, timestamp):
        #crear alerta antes
        alerta = Alerta(tipo, valor, timestamp)
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5559")

        print(f"Enviando alerta al proxy {tipo} {valor} - {timestamp}")
        socket.send_pyobj(alerta)
        
        response = socket.recv_string()
        print(f"Servidor local: recibe '{response}'del proxy")

        socket.close()
        context.term()

    def recibirDatos(self):
        print("servidor local activo")
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5558") 

        while True :
            datos = socket.recv_pyobj()
            print(f"Datos recibidos: {datos}")
           # datos = json.loads(mensaje)
            self.procesarDatosSensor(
            datos['tipo'], datos['valor'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            socket.send_string("Datos recibidos correctamente por el servidor")

    # def recibirDatos(self):
    #     context = zmq.Context()
    #     socket = context.socket(zmq.PULL)
    #     socket.bind("tcp://*:5556")

    #     while True:
    #         mensaje = socket.recv_string()
    #         datos = json.loads(mensaje)
    #         self.procesarDatosSensor(
    #             datos['tipo'], datos['valor'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
