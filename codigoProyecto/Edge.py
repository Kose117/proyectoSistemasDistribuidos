import threading
from SensorHumo import SensorHumo
from SensorHumedad import SensorHumedad
from SensorTemperatura import SensorTemperatura
from Aspersor import Aspersor
from SistemaCalidad import SistemaCalidad

class Edge:   
    def CrearSensores(aspersor):
        print("Creando sistema de calidad")
        sistemaCalidad = SistemaCalidad()

        print("Creando sensores")
        sensorHumo = SensorHumo("humo", "config/configFile1.txt")
        sensorTemperatura = SensorTemperatura("temperatura", "config/configFile2.txt")
        sensorHumedad = SensorHumedad("humedad", "config/configFile3.txt")

        # Crear hilos para cada sensor y sistema de calidad
        hiloSC = threading.Thread(target=sistemaCalidad.EsperarAlerta)
        
        hiloHumo = threading.Thread(target=lambda: sensorHumo.tomarMuestra(aspersor))
        hiloTemperatura = threading.Thread(target=sensorTemperatura.tomarMuestra)
        hiloHumedad = threading.Thread(target=sensorHumedad.tomarMuestra)

        # Iniciar hilos
        hiloSC.start()
        hiloHumo.start()
        hiloTemperatura.start()
        hiloHumedad.start()

        # Opcional: Esperar a que los hilos terminen
        hiloSC.join()
        hiloHumo.join()
        hiloTemperatura.join()
        hiloHumedad.join()

    def CrearAspersor():
        print("Creando aspersor")
        return Aspersor()
        

    if __name__ == "__main__":
        aspersor = CrearAspersor()
        CrearSensores(aspersor)

