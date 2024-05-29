from Proxy import Proxy
from ServidorLocal import ServidorLocal
from SistemaCalidad import SistemaCalidad
import threading
class Fog:

    def crearProxy():
        print("Creando proxy")
        return Proxy()

    def crearServidor():
        print("Creando servidor")
        return ServidorLocal()
        # return ServidorLocal()

    def crearSistemaCalidad():
        print("Creando sistema de calidad")
        return SistemaCalidad()

    if __name__ == "__main__":
        print("Creando fog")
        proxy = crearProxy()
        servidor = crearServidor()
        hiloProxy = threading.Thread(target= proxy.recibirMuestras)
        hiloServ = threading.Thread(target= servidor.recibirDatos)
        hiloProxyAlerta = threading.Thread(target= proxy.recibirAlertasServidor)
        hiloProxyProm = threading.Thread(target= proxy.recibirPromedioHumedad)

        print("Creando hilos")
        hiloProxy.start()
        hiloServ.start()
        hiloProxyAlerta.start()
        hiloProxyProm.start()
        
        hiloProxy.join()
        hiloServ.join()
        hiloProxyAlerta.join()
        hiloProxyProm.join()