import zmq
import json
from datetime import datetime

temperaturas = []
humedades = []

# Límites establecidos para los sensores
TEMP_MAX = 29,4


# HACE FALTA HACER QUE SE HAGA POR TIEMPO
def procesarDatosSensor(tipo, valor, timestamp):
    global temperaturas, humedades

    if tipo == "temperatura":
        temperaturas.append(valor)
    elif tipo == "humedad":
        humedades.append(valor)

   
    if len(temperaturas) >= 10:
        promedioTemp = sum(temperaturas) / len(temperaturas)
        print(f"Promedio de Temperatura: {promedioTemp} - {timestamp}")
        if promedioTemp > TEMP_MAX:
            enviarAlerta("temperatura", promedioTemp, timestamp)
        temperaturas = []  # Resetear la lista para el próximo cálculo

    if len(humedades) >= 10:
        promedioHumedad = sum(humedades) / len(humedades)
        print(f"Promedio de Humedad: {promedioHumedad} - {timestamp}")
        humedades = []  # Resetear la lista para el próximo cálculo

def enviarAlerta(tipo, valor, timestamp):
    pass


context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5556")  

while True:
    mensaje = socket.recv_string()
    datos = json.loads(mensaje)
    procesarDatosSensor(datos['tipo'], datos['valor'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
