import zmq

class SistemaCalidad:

    def __init__(self):
        print("Creando sistema de calidad")
    
    def EsperarAlerta(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5555")

        while True :
            message = socket.recv_string()
            self.ImprimirAlerta(message)
           
            socket.send_string("Alerta impresa en pantalla")

    def ImprimirAlerta(self, message):
         print(f"Sistema de Calidad: recibe '{message}'")
    
   