from tkinter import Tk
import view
import observ


class Controller:
    def __init__(self, root):
        self.root_controller = root         
        self.objeto_vista = view.Vista(self.root_controller)
        self.observ = observ.ConcreteObserver(self.objeto_vista.objeto_base)


if __name__ == "__main__":
    vent_ppal = Tk()
    app = Controller(vent_ppal)
    vent_ppal.mainloop()