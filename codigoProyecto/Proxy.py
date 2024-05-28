import datetime
import re
import zmq
from Alerta import Alerta

class Proxy:

    def __init__(self):
        print("Creando proxy")

    def recibirAlertasServidor(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5559")

        while True:
            alert = socket.recv_pyobj()
            print("Alerta recibida en el Proxy:", alert)
            print(f"Se va a mandar al cloud: {alert}")
            self.enviarMensajesCloud(alert)
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
                    self.enviarDatosServidor(datos)
                    print("Datos válidos enviados al Cloud.")
                else:
                    self.enviarAlerta(datos)
                    print("Alerta enviada al sistema de calidad y al Cloud.")
        except zmq.ZMQError as e:
            print(f"Error al recibir la muestra: {e}")
        finally:
            socket.close()
            context.term()

    def enviarDatosServidor(self, datos):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5558")

        socket.send_pyobj(datos)
        print("Enviando datos servidor")

        response = socket.recv_string()
        print(f"Proxy: recibe '{response}'del servidor")

        socket.close()
        context.term()

       
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
        
    def enviarAlerta(self, datos):
        tipo_alerta = f"Alerta: {datos['tipo']} fuera de rango" if float(datos['valor']) < 11 or float(datos['valor']) > 29.4 else "Datos Incorrectos"
        alerta = Alerta(origen_sensor=datos['tipo'], tipo_alerta=tipo_alerta, fecha=datetime.datetime.now())
        try:
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://localhost:5560")
            socket.send_pyobj(alerta)
            print("Alerta enviada al Cloud.")
        except zmq.ZMQError as e:
            print(f"Error al enviar la alerta: {e}")
        self.enviarMensajesCloud(alerta)


    def enviarMensajesCloud(self, datos):

        print("Enviando mensajes cloud")
        # Usando Request Reply
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5557")

        socket.send_pyobj(datos)

        response = socket.recv_string()
        print(f"Proxy: recibe '{response}'de la capa cloud")

        socket.close()
        context.term()
        
