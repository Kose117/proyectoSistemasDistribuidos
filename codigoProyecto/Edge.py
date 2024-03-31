import threading
from SensorHumo import SensorHumo
from SensorHumedad import SensorHumedad
from SensorTemperatura import SensorTemperatura


def CrearSensores():
    print("Creando sensores")
    sensorHumo = SensorHumo("humo", "config/configFile1.txt")
    sensorTemperatura = SensorTemperatura(
        "temperatura", "config/configFile2.txt")
    sensorHumedad = SensorHumedad(
        "humedad", "config/configFile3.txt")

    # Crear hilos para cada sensor
    hiloHumo = threading.Thread(
        target=sensorHumo.tomarMuestra)
    hiloTemperatura = threading.Thread(
        target=sensorTemperatura.tomarMuestra)
    hiloHumedad = threading.Thread(
        target=sensorHumedad.tomarMuestra)

    # Iniciar hilos
    hiloHumo.start()
    hiloTemperatura.start()
    hiloHumedad.start()

    # Opcional: Esperar a que los hilos terminen
    hiloHumo.join()
    hiloTemperatura.join()
    hiloHumedad.join()


def CrearAspersor():
    print("Creando aspersor")


def CrearSistemaCalidad():
    print("Creando sistema de calidad")


if __name__ == "__main__":
    CrearAspersor()
    CrearSensores()
    CrearSistemaCalidad()
