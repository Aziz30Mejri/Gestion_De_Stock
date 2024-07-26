from subprocess import call
from tkinter import ttk,Tk
from tkinter import *
from tkinter import messagebox


#Ma fenetre
root = Tk()
root.title("GESTION DE STOCK")
root.geometry("600x200+450+260")
root.resizable(False, False)
root.config(background="#808080")

#Fonction Achats
def Achats():
    root.destroy()
    call(["python", "Achats.py"])
#Fonction Ventes
def Ventes():
    root.destroy()
    call(["python", "Ventes.py"])


#Ajouter le titre
lbltitre = Label(root,borderwidth = 3, relief = SUNKEN
                 ,text = "BIOSPHERE TUNIS", font=("Sans Serif", 25),background = "#483088", foreground = "white")
lbltitre.place(x=0,y=0,width=600)

#Bouton Achats
btnenregistrer = Button(root,text="ACHATS",font=("Arial",24),bg="#48308B",fg="white",command=Achats)
btnenregistrer.place(x=100,y=100,width=200)
#Bouton Ventes
btnenregistrer = Button(root,text="VENTES",font=("Arial",24),bg="#48308B",fg="white",command=Ventes)
btnenregistrer.place(x=300,y=100,width=200)


#Execution
root.mainloop()