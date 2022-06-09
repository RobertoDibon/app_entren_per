#Creo un patron observador que recuerda al entrenador los datos del ultimo alumno creado, creando un archivo txt


#Importaciones
from datetime import datetime


class Sujeto():
    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def notificar(self, *args):
        for observador in self.observadores:
            observador.update(args)


class ConcreteObserver():
    def __init__(self, obj):
        self.objeto_observado = obj
        self.objeto_observado.agregar(self)

    def update(self, *args):
        txt = ('alumnos_nuevos.txt')
        archivo = open(txt, 'a')
        fecha = datetime.now()
        formato_fecha = fecha.strftime('%m/%d/%Y, %H:%M:%S ')
        valores = 'Nombre y Apellido : {0}'.format(
                args[0]    
            )
            
        print(formato_fecha + valores, file=archivo)



        
    
        
      