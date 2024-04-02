from Proxy import Proxy
from ServidorLocal import ServidorLocal
from SistemaCalidad import SistemaCalidad

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
        crearServidor()
        
        proxy.recibirMuestras()