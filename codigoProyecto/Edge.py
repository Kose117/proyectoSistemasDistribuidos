import SensorHumedad
import SensorHumo
import SensorTemperatura

def CrearSensores():
    print("Creando sensores")
    sensorHumo = SensorHumo("humo", "configFile1")
    sensorTemperatura = SensorTemperatura("temperatura", "configFile2")
    sensorHumedad = SensorHumedad("humedad", "configFile3")
    return

def CrearAspersor():
    print("Creando aspersor")
    return

def CrearSistemaCalidad():
    print("Creando sistema de calidad")
    return


if __name__ == "__main__":
    # Llama a la función principal cuando el script se ejecute directamente
    CrearAspersor()
    CrearSensores()
    CrearSistemaCalidad()
