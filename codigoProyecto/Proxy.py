import zmq

class Proxy:
    
    def __init__ (self):
        print("Creando proxy")

    def recibirAlertas(self):
        print("Recibiendo alertas")
    
   

    def recibirMuestras(self):

        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.connect("tcp://*:5555")

        while True :
            datos = socket.recv_pyobj()
            self.enviarDatosServidor(datos)
            print(datos)
            
             
    def enviarDatosServidor(self, datos):

        print("Enviando datos servidor")
    
    def validarDatos(self):
        print("Validando datos")

    

    def enviarMensajesCloud(self):
        print("Enviando mensajes cloud")
        

