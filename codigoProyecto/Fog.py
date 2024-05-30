from Proxy import Proxy
from ServidorLocal import ServidorLocal
from SistemaCalidad import SistemaCalidad
import threading


class Fog:

    def crearProxy(servidor):
        print("Creando proxy")
        return Proxy(servidor)

    def crearServidor():
        print("Creando servidor")
        return ServidorLocal()
        # return ServidorLocal()

    def crearSistemaCalidad():
        print("Creando sistema de calidad")
        return SistemaCalidad("5565")

    if __name__ == "__main__":
        print("Creando fog")
        servidor = crearServidor()
        sistemaCalidad = crearSistemaCalidad()
        proxy = crearProxy(servidor)
        hiloProxy = threading.Thread(target=proxy.recibirMuestras)
        hiloSistemaCalidad = threading.Thread(
            target=sistemaCalidad.EsperarAlerta)

        print("Creando hilos")
        hiloProxy.start()
        hiloSistemaCalidad.start()

        hiloProxy.join()
        hiloSistemaCalidad.join()
