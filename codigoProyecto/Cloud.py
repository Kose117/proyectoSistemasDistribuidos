import zmq

class Cloud:
        
    def recibirInfoProxy(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5557")

        while True :
            message = socket.recv_pyobj()
            print(f"{message}")
            
            socket.send_string("Datos recibidos impresos")
            


if __name__ == "__main__":
    cloud = Cloud()    
    cloud.recibirInfoProxy()