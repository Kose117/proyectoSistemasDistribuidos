from codigoProyecto.Sensor import Sensor

class SensorTemperatura(Sensor):
    def __init__(self, parametro1, parametro2):
        super().__init__(parametro1, parametro2)
        

    def tomarMuestra(self):
        # Código para el método tomarMuestra