class SensorHumo:
    def __init__(self, parametro1, parametro2):
        self.tipo:str = parametro1
        self.configFile: str = parametro2
        self.pCorrecto: float = -1
        self.pFueraRango:float = -1
        self.pError:float = -1

    def tomarMuestra(self):
        print("Muestra de humo tomada")

    def enviarMuestraProxy(self):
        print("Muestra de humo enviada")
   