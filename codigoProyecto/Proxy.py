import re
import zmq


class Proxy:

    def __init__(self):
        print("Creando proxy")

    def recibirAlertasServidor(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5559") 

       # while True :
        alert = socket.recv_pyobj()
        print("Alerta recibida en el Proxy:", alert)
        print(f"se va a mandar al cloud: {alert}")
        self.enviarMensajesCloud()#mandar con la alerta
        socket.send_string("Enviando alerta al cloud")

    def recibirMuestras(self):
        context = zmq.Context()
        socket = context.socket(zmq.PULL)

        socket.bind("tcp://*:5556")
        try:
            while True:
                datos = socket.recv_pyobj()
                print("Muestra recibida en el Proxy:", datos)
                self.enviarDatosServidor(datos)
                print(datos)
                if(self.validarDatos(datos)):
                    self.enviarMensajesCloud(datos)
                
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
        if(re.search("humo", datos['tipo'])):
            if datos['valor'] == True or datos['valor'] == False:
                print("Datos correctos")
                return True
            
            print("Datos INcorrectos")
            return False
        elif(re.search("temperatura", datos['tipo']) or re.search("humedad", datos['tipo'])):
            if float(datos['valor']) < 0:
                print("Datos INcorrectos")
                return False
            # Poner condicion en caso de que sea fuera de rango para mandar alerta
            print("Datos correctos")
            return True
        


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
        
