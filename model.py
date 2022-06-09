#Importaciones de modulos
from peewee import *
import re
from tkinter import messagebox
from datetime import datetime
from io import open
from observ import Sujeto
import pickle
from tkinter import filedialog


#Variables
archivo_txt = open('registro_log.txt', 'a')
fecha = datetime.now()
fecha_formato_a = fecha.strftime('%m/%d/%Y, %H:%M:%S '+'Se produjo un Alta \n')
fecha_formato_m = fecha.strftime('%m/%d/%Y, %H:%M:%S '+'Se Edito un registro \n')
fecha_formato_b = fecha.strftime('%m/%d/%Y, %H:%M:%S '+'Se produjo una Baja \n')


#Conexion con peewee 
db = SqliteDatabase('bbdd.db')

class BaseModel(Model):
    class Meta:
        database = db

class Alumnos(BaseModel):
    id = AutoField()
    nombre = CharField()
    apellido = CharField()
    edad = DecimalField()
    peso = DecimalField()
    estatura = DecimalField()
    genero = CharField()
db.connect()
db.create_tables([Alumnos])


#Decorador
def decorador(funcion_decorada):
    operacion = funcion_decorada.__name__
    if operacion == 'agendar':
        def archivo_registro(*args):
            archivo_txt.write(fecha_formato_a)
            funcion_decorada(*args)

    elif operacion == 'editar':
        def archivo_registro(*args):
            archivo_txt.write(fecha_formato_m)
            funcion_decorada(*args)

    elif operacion == 'borrar_definitivamente':
            def archivo_registro(*args):
                archivo_txt.write(fecha_formato_b)
                funcion_decorada(*args)

    return archivo_registro


#Abmc, Metodos
class Abmc(Sujeto):
    def validar(self, nombre, apellido):
        patron = re.compile("^[A-Za-z]+$")   
        if (patron.match(nombre)) is not None and (patron.match(apellido)) is not None:
            return True
            
        else:    
            self.mensaje("SOLO se permiten caracteres ALFABETICOS")
            return False

    @decorador                 
    def agendar(self, nombre, apellido, edad, peso, estatura, genero):
        tabla = Alumnos()
        tabla.nombre = nombre
        tabla.apellido = apellido
        tabla.edad = edad
        tabla.peso = peso
        tabla.estatura = estatura
        tabla.genero = genero
        tabla.save()
        self.notificar(nombre, apellido)
   
    @decorador
    def borrar_definitivamente(self, id):
        eliminar = Alumnos.get(Alumnos.id == id)
        eliminar.delete_instance()
        self.mensaje("ALUMNO BORRADO")    
            
    @decorador             
    def editar(self, nombre, apellido, edad, peso, estatura, genero, id):
        actualizar = Alumnos.update(
            nombre = nombre,
            apellido = apellido,
            edad = edad,
            peso = peso,
            estatura = estatura,
            genero = genero
        ).where(Alumnos.id == id)
        actualizar.execute()

    def mostrar(self, mitreeview):
        #Limpieza tabla
        records = mitreeview.get_children()
        for element in records:
            mitreeview.delete(element)

        #Consiguiendo datos
        resultado = Alumnos.select().order_by(Alumnos.id.desc())
        for fila in resultado:       
            mitreeview.insert(
                "", 
                0, 
                text=fila.id, 
                values=(fila.nombre, fila.apellido, fila.edad,
                fila.peso, fila.estatura, fila.genero, fila)
                ) 
           
    def acerca(self):
        acerca='''
        Aplicacion CRUD
        Version 2.0 (2022)
        Tecnologia Python 3.10.0 / Tkinter/ PeeWee
        Creado por Roberto Dibón
        '''
        messagebox.showinfo(title="INFORMACION APP", message=acerca)

    def mensaje(self, texto): 
        messagebox.showinfo("Atencion", texto)


class Evolucion():
    def archivar(self, texto, apellido):
        self.contenido_entry=texto
        #archivo en memoria
        archivo_evolucion=open(apellido, 'wb')
        
        pickle.dump(texto, archivo_evolucion)
        archivo_evolucion.close()
            
    def mostrar_2(self, apellido, text_entry):
        try:
            archivo_evolucion = open(apellido, 'rb')
            contenido = pickle.load(archivo_evolucion)
            text_entry.insert('end', contenido)
        except FileNotFoundError as e:
            mensaje = ("No se evolucinó al alumnx "+apellido)
            messagebox.showinfo(title="Error",
                message = mensaje)
            return
    
    def rutina(self):
        archivo = filedialog.askopenfilename(title= "Abrir archivo" , 
            initialdir = "C:/", 
            filetypes = (("Archivos de Word", "*.docx"), ("Archivos Pdf", "*.pdf")))
        

    def calculo_tmb(self, edad, peso, estatura, genero, texto_label):
        peso = float(peso)
        estatura = float(estatura)
        edad = float(edad)
        if genero == ('M') or genero == ('H'):
            t_m_b_hombre = ((10*peso)+(6.25*estatura)-(5*edad)+5)
            texto_label.set(t_m_b_hombre)
        
        else:
            t_m_b_mujer = ((10*peso)+(6.25*estatura)-(5*edad)-161)
            texto_label.set(t_m_b_mujer)
        
        
        
        