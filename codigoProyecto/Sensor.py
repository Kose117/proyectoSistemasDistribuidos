import zmq


class Sensor:

    muestra = {
        'tipo': '',
        'valor': '',
        'tiempo': ''
    }

    def __init__(self, parametro1, parametro2):
        self.tipo: str = parametro1
        self.configFile: str = parametro2
        self.pCorrecto: float = -1
        self.pFueraRango: float = -1
        self.pError: float = -1
        self.PUERTO_PROXY = 5556

        self.leerArchivo()

    def tomarMuestra(self):
        print("Muestra de humo tomada")

    def enviarMuestraProxy(self):
        print("Muestra de humo enviada")

    def leerArchivo(self):
        # Abrir el archivo para lectura ('r')
        with open(self.configFile, 'r') as archivo:
            # Leer todas las líneas del archivo
            lineas = archivo.readlines()

            # Procesar cada línea
            for linea in lineas:
                # Dividir la línea por el delimitador ';'
                partes = linea.strip().split(';')

                # Convertir cada parte a entero (o flotante si fuera necesario)
                numeros = [float(parte) for parte in partes]

                # Hacer algo con los números (aquí simplemente los imprimo)
                print(numeros)
                self.pCorrecto = numeros[0]
                self.pFueraRango = numeros[1]
                self.pError = numeros[2]

    def enviarMuestraProxy(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        # socket.bind("tcp://localhost:5555")
        socket.connect("tcp://localhost:5556")

        try:
            socket.send_pyobj(self.muestra)
            print("Muestra enviada al Proxy.")
        except zmq.ZMQError as e:
            print(f"Error al enviar la muestra: {e}")
        finally:
            socket.close()
            context.term()
