from ServidorLocal import ServidorLocal
from SistemaCalidad import SistemaCalidad
from Proxy import Proxy
class Fog:

    def crearProxy(self):
        self.proxy = Proxy()

    def crearServidor(self):
         self.servidor_local = ServidorLocal()
    
    def crearSistemaCalidad(self):
        self.sistema_calidad = SistemaCalidad()
    
    if __name__ == "__main__":
       crearProxy()
       crearServidor()




