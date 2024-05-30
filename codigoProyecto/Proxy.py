import datetime
import re
import zmq
from Alerta import Alerta
from datetime import datetime
from ServidorLocal import ServidorLocal

class Proxy:
    
    promedio = {
        'tipo': '',
        'valor': ''
    }

    def __init__(self, servidor):
        print("Creando proxy") 
        self.servidor:ServidorLocal = servidor
        self.temperaturas = []
        self.humedades = []
        # Límites establecidos para los sensores
        self.TEMP_MAX = 29.4
        
    def recibirAlertasServidor(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5559")

        while True:
            alert = socket.recv_pyobj()
            print("Alerta recibida en el Proxy:", alert)
            print(f"Se va a mandar al cloud: {alert}")
            self.enviarAlerta(alert)
            socket.send_string("Enviando alerta al cloud")

    def recibirMuestras(self):
        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.bind("tcp://*:5556")
        try:
            while True:
                datos = socket.recv_pyobj()
                print("Muestra recibida en el Proxy:", datos)
                if self.validarDatos(datos):
                    self.enviarMuestrasCloud(datos)
                    if datos['tipo'] == "temperatura":
                        self.temperaturas.append(datos['valor'])
                    elif datos['tipo'] == "humedad":
                        self.humedades.append(datos['valor'])
                    self.pedirPromedioServidor()
                    print("Datos válidos enviados al Cloud.")
                else:
                    self.enviarAlerta(datos)
                    print("Alerta enviada al sistema de calidad y al Cloud.")
        except zmq.ZMQError as e:
            print(f"Error al recibir la muestra: {e}")
        finally:
            socket.close()
            context.term()

    # def enviarDatosServidor(self, datos):
    #     context = zmq.Context()
    #     socket = context.socket(zmq.REQ)
    #     socket.connect("tcp://localhost:5558")

    #     socket.send_pyobj(datos)
    #     print("Enviando datos servidor")

    #     response = socket.recv_string()
    #     print(f"Proxy: recibe '{response}'del servidor")

    #     socket.close()
    #     context.term()

    def validarDatos(self, datos):
        print("Validando datos")
        if re.search("humo", datos['tipo']):
            if datos['valor'] == True or datos['valor'] == False:
                print("Datos correctos")
                return True
            print("Datos Incorrectos: Valor no es True ni False")
            return False
        elif re.search("temperatura", datos['tipo']):
            if float(datos['valor']) < 0:
                print("Datos Incorrectos: Valor de temperatura negativo")
                return False
            elif float(datos['valor']) < 11 or float(datos['valor']) > 29.4:
                print("Datos fuera de rango: Generando alerta")
                return False
            print("Datos correctos")
            return True
        elif re.search("humedad", datos['tipo']):
            if float(datos['valor']) < 0:
                print("Datos Incorrectos: Valor de humedad negativo")
                return False
            print("Datos correctos")
            return True
        else:
            print("Tipo de datos desconocido")
            return False
        
    # def enviarAlerta(self, datos):
    #     tipo_alerta = f"Alerta: {datos['tipo']} fuera de rango" if float(datos['valor']) < 11 or float(datos['valor']) > 29.4 else "Datos Incorrectos"
    #     alerta = Alerta(origen_sensor=datos['tipo'], tipo_alerta=tipo_alerta, fecha=datetime.datetime.now())
    #     try:
    #         context = zmq.Context()
    #         socket = context.socket(zmq.REQ)
    #         socket.connect("tcp://localhost:5560")
    #         socket.send_pyobj(alerta)
    #         print("Alerta enviada al Cloud.")
    #     except zmq.ZMQError as e:
    #         print(f"Error al enviar la alerta: {e}")
    #     self.enviarMensajesCloud(alerta)
    def enviarAlerta(self, datos):
        try:
            valor = float(datos['valor'])
            tipo_alerta = f"Alerta: {datos['tipo']} fuera de rango" if valor < 11 or valor > 29.4 else "Datos Correctos"
        except ValueError:
            tipo_alerta = "Datos Incorrectos"
        
        alerta = Alerta(origen_sensor=datos['tipo'], tipo_alerta=tipo_alerta, fecha=datetime.now())
        
        try:
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://localhost:5560")
            socket.send_pyobj(alerta)
            print("Alerta enviada al Cloud.")
        except zmq.ZMQError as e:
            print(f"Error al enviar la alerta: {e}")
        
    # self.enviarMensajesCloud(alerta)
    
    
    def pedirPromedioServidor(self):
        
        if len(self.temperaturas) >= 10:
            promedioTemp = self.servidor.enviarPromedio(self.temperaturas)
            print(f"Promedio de Temperatura: {promedioTemp} - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
            promedioTemp = 35
            if promedioTemp > self.TEMP_MAX:
                alerta = Alerta("Promedio temperatura elevado", promedioTemp, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                self.generarSistemaCalidad()
                self.enviarAlerta(alerta)
            print(f"Promedio de temperatura recibido en el Proxy: {promedioTemp}")
            self.enviarMensajesCloud(promedioTemp, "temperatura")
            self.temperaturas = []  # Resetear la lista para el próximo cálculo

        if len(self.humedades) == 10:
            promedioHumedad = self.servidor.enviarPromedio(self.humedades)
            print(f"Promedio de Humedad: {promedioHumedad} - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
            # enviar promedio al proxy
            print(f"Promedio de humedad recibido en el Proxy: {promedioHumedad}")
            self.enviarMensajesCloud(promedioHumedad, "humedad")
            self.humedades = []  # Resetear la lista para el próximo cálculo    

    def enviarMensajesCloud(self, datos, tipo):

        print("Enviando promedio cloud")
        # Usando Request Reply
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5557")

        self.promedio['tipo']=tipo
        self.promedio['valor']=datos
        socket.send_pyobj(self.promedio)
        
        response = socket.recv_string()
        print(f"Proxy: recibe '{response}' de la capa cloud")

        socket.close()
        context.term()
    
    def enviarMuestrasCloud(self, datos):
        
        print("Enviando muestras cloud")
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5557")

        socket.send_pyobj(datos)
        
        response = socket.recv_string()
        print(f"Proxy: recibe '{response}' de la capa cloud")

        socket.close()
        
    def generarSistemaCalidad(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5565")

        alerta = Alerta(origen_sensor=self.__class__.__name__, tipo_alerta="Alerta: Sistema de Calidad", fecha=datetime.now())
        socket.send_pyobj(alerta)

        response = socket.recv_string()
        print(f"Proxy: recibe '{response}' del sistema de calidad")

        socket.close()
        context.term()
