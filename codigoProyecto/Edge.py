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
        sensoresHumo = [SensorHumo(f"humo_{i}", f"config/configFile1.txt") for i in range(10)]
        sensoresTemperatura = [SensorTemperatura(f"temperatura_{i}", f"config/configFile2.txt") for i in range(10)]
        sensoresHumedad = [SensorHumedad(f"humedad_{i}", f"config/configFile3.txt") for i in range(10)]

        # Crear hilos para cada sensor y sistema de calidad
        hiloSC = threading.Thread(target=sistemaCalidad.EsperarAlerta)
<<<<<<< HEAD
        
        hiloHumo = threading.Thread(target=lambda: sensorHumo.tomarMuestra(aspersor))
        hiloTemperatura = threading.Thread(target=sensorTemperatura.tomarMuestra)
        hiloHumedad = threading.Thread(target=sensorHumedad.tomarMuestra)
=======

        hilosHumo = [threading.Thread(target=lambda sensor=sensor: sensor.tomarMuestra(aspersor)) for sensor in sensoresHumo]
        hilosTemperatura = [threading.Thread(target=sensor.tomarMuestra) for sensor in sensoresTemperatura]
        hilosHumedad = [threading.Thread(target=sensor.tomarMuestra) for sensor in sensoresHumedad]
>>>>>>> ba4c3709b1d2389dad47e1bfbdf21afaabd09e12

        # Iniciar hilos
        hiloSC.start()
        for hilo in hilosHumo + hilosTemperatura + hilosHumedad:
            hilo.start()

        # Opcional: Esperar a que los hilos terminen
        hiloSC.join()
        for hilo in hilosHumo + hilosTemperatura + hilosHumedad:
            hilo.join()

    def CrearAspersor():
        print("Creando aspersor")
        return Aspersor()

    if __name__ == "__main__":
        aspersor = CrearAspersor()
<<<<<<< HEAD
        CrearSensores(aspersor)

=======
        CrearSensores(aspersor)
>>>>>>> ba4c3709b1d2389dad47e1bfbdf21afaabd09e12
