#Importaciones de Modulos
from tkinter import *
from tkinter import ttk
import os
from PIL import ImageTk, Image
from model import Abmc, Evolucion
from tkinter import messagebox
import tkinter as tk


class Vista: 
    #Metodo constructor e instanciacion de bbdd
    def __init__(self, vent_ppal):   
        self.objeto_base = Abmc()
        self.objeto_base_2 = Evolucion()
        self.vent_ppal = vent_ppal
        self.ruta = os.path.join(
            os.path.dirname((os.path.abspath(__file__))),
            "Mancuernas.jpg"
        )
        self.vent_ppal.geometry("605x450")
        self.vent_ppal.title("ENTRENAMIENTOS PERSONALIZADOS")
        self.imagen = ImageTk.PhotoImage(Image.open(self.ruta))
        self.background_label = ttk.Label(vent_ppal, image=self.imagen)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=0.5)

        
        #Variables de la ig
        self.nombre = StringVar()
        self.apellido = StringVar()
        self.edad = DoubleVar()
        self.peso = DoubleVar()
        self.estatura = DoubleVar()
        self.genero = StringVar()
        

        #Entradas
        self.l1 = Label(vent_ppal, text="Nombre")
        self.l1.place(x=20, y=10)
        self.e1 = Entry(vent_ppal, textvariable=self.nombre, width=10)
        self.e1.place(x=75, y=10)

        self.l2 = Label(vent_ppal, text="Apellido")
        self.l2.place(x=20, y=40)
        self.e2 = Entry(vent_ppal, textvariable=self.apellido, width=10)
        self.e2.place(x=75, y=40)  

        self.l3 = Label(vent_ppal, text="Edad")
        self.l3.place(x=20, y=70)
        self.e3 = Entry(vent_ppal, textvariable=self.edad, width=10)
        self.e3.place(x=75, y=70)

        self.l4 = Label(vent_ppal, text="Peso")
        self.l4.place(x=500, y=10)
        self.e4 = Entry(vent_ppal, textvariable=self.peso, width=5)
        self.e4.place(x=550, y=10)

        self.l5 = Label(vent_ppal, text="Estatura")
        self.l5.place(x=500, y=40)
        self.e5 = Entry(vent_ppal, textvariable=self.estatura, width=5)
        self.e5.place(x=550, y=40)

        self.l6 = Label(vent_ppal, text="Género")
        self.l6.place(x=500, y=70)
        self.e6 = Entry(vent_ppal, textvariable=self.genero, width=5)
        self.e6.place(x=550, y=70)

        
        #Tabla 
        self.tree = ttk.Treeview(self.vent_ppal)
        self.tree.place(x=18, y=160)
        self.tree["columns"] = ("nombre", "apellido", "edad", "peso", "estatura", "genero")
        self.tree.column("#0", width=60)
        self.tree.column("nombre", width=100)
        self.tree.column("apellido", width=100)
        self.tree.column("edad", width=76)
        self.tree.column("peso", width=76)
        self.tree.column("estatura", width=76)
        self.tree.column("genero", width=76)

        self.tree.heading("#0", text="ID")
        self.tree.heading("nombre", text="NOMBRE")
        self.tree.heading("apellido", text="APELLIDO")
        self.tree.heading("edad", text="EDAD")
        self.tree.heading("peso", text="PESO")
        self.tree.heading("estatura", text="ESTATURA")
        self.tree.heading("genero", text="GENERO")


        #Limita el caracter de variable genero a 1
        def limitador(genero):
            genero = self.genero
            if len(genero.get()) > 0:   
                genero.set(genero.get()[:1])


        #Aplica solo mayusculas a variable genero
        def gen_case(genero):
            genero = self.genero
            genero.set(genero.get().upper())
                      
        self.genero.trace("w", lambda *args: (limitador(self.genero), gen_case(self.genero)))

        self.tree.bind("<Button-1>", self.seleccionar_click)


        #Limpia el tree al arrancar la App
        self.limpiar()


        #Botones
        self.b1 = Button(vent_ppal, text="Agendar Alumno", command=lambda: self.agendar())
        self.b1.place(x=50, y=130)
        self.b2 = Button(vent_ppal, text="Editar Alumno", command=lambda: self.editar())
        self.b2.place(x=190, y=130)
        self.b3 = Button(vent_ppal, text="Mostrar la lista", command=lambda: self.mostrar())
        self.b3.place(x=325, y=130)
        self.b4 = Button(vent_ppal, text="BORRAR ALUMNO", bg="red", command=lambda: self.borrar())
        self.b4.place(x=455, y=130)
        
        
        self.b5 = Button(vent_ppal, text="EVOLUCIONAR", bg="black", fg="white", command=lambda: self.evolucionar())
        self.b5.place(x=20, y=400)
        self.b6 = Button(vent_ppal, text="Acerca de la App", command=lambda: self.acerca())
        self.b6.place(x=440 , y=400)
        self.b7 = Button(vent_ppal, text="Salir", command=self.salir)
        self.b7.place(x=550, y=400)
    
   
    def seleccionar_click(self, event):
        try:
            item = self.tree.identify('item', event.x, event.y)
            
            self.nombre.set(self.tree.item(item, 'values')[0])
            self.apellido.set(self.tree.item(item, 'values')[1])
            self.edad.set(self.tree.item(item, 'values')[2])
            self.peso.set(self.tree.item(item, 'values')[3])
            self.estatura.set(self.tree.item(item, 'values')[4])
            self.genero.set(self.tree.item(item, 'values')[5])
        except: 
            self.objeto_base.mensaje("No ha seleccionado ningun campo")

    def agendar(self):
        if self.objeto_base.validar(
            self.e1.get(), 
            self.e2.get()
            ):
            self.objeto_base.agendar(
            self.nombre.get(), 
            self.apellido.get(),
            self.edad.get(),
            self.peso.get(),
            self.estatura.get(),
            self.genero.get()
            )   
        self.mostrar()
           
    def borrar(self):
        seleccion = self.tree.focus()
        id = self.tree.item(seleccion)
        pregunta = messagebox.askquestion(message="Desea eliminar el Alumno", title="Advertencia")
        if pregunta == messagebox.NO:
            Abmc.mensaje(self,"ALUMNO GUARDADO") 
        else:
            self.objeto_base.borrar_definitivamente(id["text"])
            self.mostrar()
        
    def editar(self):
        seleccion = self.tree.focus()
        id = self.tree.item(seleccion)
        if self.objeto_base.validar(
            self.e1.get(),
            self.e2.get()
            ):
            self.objeto_base.editar(
                self.nombre.get(),
                self.apellido.get(),
                self.edad.get(),
                self.peso.get(),
                self.estatura.get(),
                self.genero.get(),
                id["text"]
            )
            self.mostrar()
    
    def mostrar(self):  
        self.objeto_base.mostrar(self.tree)
        self.limpiar()
        self.e1.focus()

    def acerca(self):
        self.objeto_base.acerca()
    
    def limpiar(self):
        self.e1.delete(0, END)
        self.e2.delete(0, END)  
        self.e3.delete(0, END)
        self.e4.delete(0, END)
        self.e5.delete(0, END)
        self.e6.delete(0, END)

    def salir(self):
        self.vent_ppal.destroy()

    def evolucionar(self):
        try:
            self.tree.item(self.tree.selection())['values'][0]
            self.tree.item(self.tree.selection())['values'][1]
        except IndexError as e:
            self.objeto_base.mensaje("No ha seleccionado Alumno")
            return

        nombre = self.tree.item(self.tree.selection())['values'][0]  
        apellido = self.tree.item(self.tree.selection())['values'][1]
        self.v_evo = Toplevel()
        self.v_evo.title("EVOLUCIONES")
        
        
        #Frames
        frame_ppal = Frame(self.v_evo)
        frame_ppal.pack(side="left", anchor="nw")

        self.background_label_2 = ttk.Label(frame_ppal, image=self.imagen, justify= "center")
        self.background_label_2.place(x=0, y=0, relwidth=5, relheight=1.0)
      
        frame_2 = Frame(self.v_evo)
        frame_2.pack(fill="x")


        #Etiquetas y Entradas
        self.e7 = Entry(frame_ppal, textvariable = StringVar(frame_ppal, value=nombre), fg='#C70039', width=10, justify=tk.CENTER, state= 'readonly')
        self.e7.grid(row=0, column=0, sticky="w", padx= 10, pady= 10)
        self.e8 = Entry(frame_ppal, textvariable = StringVar(frame_ppal, value=apellido), fg='#C70039', width=10, justify=tk.CENTER, state= 'readonly')
        self.e8.grid(row=0, column=1, padx= 10, pady= 10)

        #Etiqueta tmb
        self.texto_label = IntVar()
        self.texto_label.set('0000')
        self.result_tmb = Label(frame_ppal, textvariable=self.texto_label)
        self.result_tmb.grid(row=10, column=1)
        

        #Cuadro de Texto
        self.l6 = Label(frame_2, text="EVOLUCION",  font='bold')
        self.l6.grid(row=0, column=0)

        self.texto = Text(frame_2)
        self.texto.grid(row=1, column=0, padx=10, pady=10)
        self.scroll = Scrollbar(frame_2, command=self.texto.yview)
        self.scroll.grid(row=1, column=0, padx=10, pady=10, sticky="nse")
        self.texto.config(yscrollcommand=self.scroll.set)


        #Botones 
        b_rutina = Button(frame_ppal, text="Rutina Ejercicios", command=lambda:rutina())
        b_rutina.grid(row=6, column=0,  sticky = "w", padx= 10, pady= 10)
       
        b_guardar = Button(frame_ppal, text="GUARDAR", bg="red", fg="white", command=lambda:archivar())
        b_guardar.grid(row=7, column=0, sticky = "w", padx= 10, pady= 10)

        b_mostrar_2 = Button(frame_ppal, text="MOSTRAR", bg="black", fg="white", command=lambda:mostrar_2())
        b_mostrar_2.grid(row=8, column=0, sticky = "w", padx= 10, pady= 10)

        b_metabolismo = Button(frame_ppal, text="Tasa M Basal", command=lambda:t_m_b())
        b_metabolismo.grid(row=10, column=0, sticky = "w", padx= 10, pady= 10)


        #Metodos Clase Evolucion
        def archivar():
            self.objeto_base_2.archivar(
                self.texto.get('1.0', 'end'), apellido,
                )

        def mostrar_2():
            self.objeto_base_2.mostrar_2(apellido, self.texto)

        def rutina():
            self.objeto_base_2.rutina()

        def t_m_b():
            edad = self.tree.item(self.tree.selection())['values'][2]
            peso = self.tree.item(self.tree.selection())['values'][3]
            estatura = self.tree.item(self.tree.selection())['values'][4]
            genero = self.tree.item(self.tree.selection())['values'][5]
        
            self.objeto_base_2.calculo_tmb(edad, peso,
            estatura, genero, self.texto_label)
            
     
            


