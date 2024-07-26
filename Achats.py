import tkinter
from cProfile import label
from distutils.util import execute
from tkinter import ttk,Tk
from tkinter import *
from subprocess import call
from tkinter import messagebox
import mysql.connector
#import tk as tk


def sort_treeview(treeview, col, reverse):
    data = [(treeview.set(child, col), child) for child in treeview.get_children('')]
    data.sort(reverse=reverse)
    for index, (val, child) in enumerate(data):
        treeview.move(child,'', index)
        treeview.heading(col, command=lambda: sort_treeview(treeview, col, not reverse))

def Retour():
    root.destroy()
    call(["python","Main.py"])


def Ajouter():
    matricule = txtNumero.get()
    fournisseur = txtfournisseur.get()
    telephone = txtTelephone.get()
    produit = comboproduit.get()
    prix_achat = txtPrix.get()
    quantite_achte = txtQuantite.get()

    if not all((matricule, fournisseur, telephone, produit, prix_achat, quantite_achte)):
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return
    if not telephone.isdigit() or len(telephone) != 8:
        messagebox.showerror("Erreur", "Le numéro de téléphone doit être 8 chiffres.")
        return
    maBase = mysql.connector.connect(host="localhost", user="root", password="", database="achat")
    meConnect = maBase.cursor()

    try:
        # Ajouter l'achat
        sql = "INSERT INTO tb_achat (CODE_ACHAT, fournisseur, telephone, produit, prix, quantite) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (matricule, fournisseur, telephone, produit, prix_achat, quantite_achte)
        meConnect.execute(sql, val)

        # Mettre à jour le stock
        sql_stock = "INSERT INTO tb_stock (produit, quantite) VALUES (%s, %s) ON DUPLICATE KEY UPDATE quantite = quantite + %s"
        val_stock = (produit, quantite_achte, quantite_achte)
        meConnect.execute(sql_stock, val_stock)

        maBase.commit()
        messagebox.showinfo("Information", "Achat ajouté et stock mis à jour.")
        root.destroy()
        call(["python", "Achats.py"])
    except Exception as e:
        print(e)
        maBase.rollback()
    finally:
        maBase.close()


def Modifier():
    matricule = txtNumero.get()
    fournisseur = txtfournisseur.get()
    telephone = txtTelephone.get()
    produit = comboproduit.get()
    prix_achat = txtPrix.get()
    quantite_achte = txtQuantite.get()

    if not all((matricule, fournisseur, telephone, produit, prix_achat, quantite_achte)):
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return

    maBase = mysql.connector.connect(host="localhost", user="root", password="", database="achat")
    meConnect = maBase.cursor()

    try:
        # Récupérer l'ancienne quantité
        meConnect.execute("SELECT quantite FROM tb_achat WHERE CODE_ACHAT = %s", (matricule,))
        old_quantite = meConnect.fetchone()[0]

        # Mettre à jour l'achat
        sql = "UPDATE tb_achat SET fournisseur=%s, telephone=%s, produit=%s, prix=%s, quantite=%s WHERE CODE_ACHAT=%s"
        val = (fournisseur, telephone, produit, prix_achat, quantite_achte, matricule)
        meConnect.execute(sql, val)

        # Mettre à jour le stock
        sql_stock = "UPDATE tb_stock SET quantite = quantite + %s - %s WHERE produit = %s"
        val_stock = (quantite_achte, old_quantite, produit)
        meConnect.execute(sql_stock, val_stock)

        maBase.commit()
        messagebox.showinfo("Information", "Achat modifié et stock mis à jour.")
        root.destroy()
        call(["python", "Achats.py"])
    except Exception as e:
        print(e)
        maBase.rollback()
    finally:
        maBase.close()


def Supprimer():
    matricule = txtNumero.get()
    if messagebox.askyesno("Confirmation", "Seriez-vous d'accord pour supprimer cet élément ?"):
        maBase = mysql.connector.connect(host="localhost", user="root", password="", database="achat")
        meConnect = maBase.cursor()
        try:
            # Récupérer les détails de l'achat à supprimer
            meConnect.execute("SELECT produit, quantite FROM tb_achat WHERE CODE_ACHAT = %s", (matricule,))
            achat = meConnect.fetchone()
            produit = achat[0]
            quantite = achat[1]

            # Supprimer l'achat
            sql = "DELETE FROM tb_achat WHERE CODE_ACHAT = %s"
            val = (matricule,)
            meConnect.execute(sql, val)

            # Mettre à jour le stock
            sql_stock = "UPDATE tb_stock SET quantite = quantite - %s WHERE produit = %s"
            val_stock = (quantite, produit)
            meConnect.execute(sql_stock, val_stock)

            maBase.commit()
            messagebox.showinfo("Information", "Achat supprimé et stock mis à jour.")
            root.destroy()
            call(["python", "Achats.py"])
        except Exception as e:
            print(e)
            maBase.rollback()
        finally:
            maBase.close()

#Ma fenetre
root = Tk()
root.title("MENU DES ACHATS")
root.geometry("1550x790+0+0")
#root.geometry("1350x700+0+0")
root.resizable(False, False)
root.config(background="#808080")

#Ajouter le titre
lbltitre = Label(root,borderwidth = 3, relief = SUNKEN
                 ,text = "GESTION DES ACHATS", font=("Sans Serif", 25, "bold"),background = "#483088", foreground = "#FFFAFA")
lbltitre.place(x=0,y=0,width=1550, height=100)

#Detail des achats
#Matricule
lblNumero = Label(root, text="MATRICULE", font=("Arial",18), bg="#808080", fg="white")
lblNumero.place(x=70, y=150, width=150)
txtNumero = Entry(root,bd=4, font=("Arial",14))
txtNumero.place(x=250, y=150, width=150)
#Fournisseur
lblfournisseur = Label(root, text="FOURNISSEUR", font=("Arial",18), bg="#808080", fg="white")
lblfournisseur.place(x=50, y=200, width=200)
txtfournisseur = Entry(root,bd=4, font=("Arial",14))
txtfournisseur.place(x=250, y=200, width=300)
#Telephone
lblTelephone = Label(root, text="TELEPHONE", font=("Arial",18), bg="#808080", fg="white")
lblTelephone.place(x=70, y=250, width=150)
txtTelephone = Entry(root,bd=4, font=("Arial",14))
txtTelephone.place(x=250, y=250, width=300)
#Achats
lblproduit = Label(root, text="PRODUIT", font=("Arial",18), bg="#808080", fg="white")
lblproduit.place(x=550, y=150, width=150)

comboproduit = ttk.Combobox(root, font=("Arial",14))
comboproduit['values'] = ['Boite Pétri', 'Lamelle Couvre Objet' , 'Portoir Pour Tube', 'Eprouvette En Plastique', 'Tube Sous Vide', 'Seringue', 'Coton', 'Bavette', 'Electrode ECG','AUTRES....']
comboproduit.place(x=700, y=150, width=230)
#Prix
lblPrix = Label(root, text="PRIX", font=("Arial",18), bg="#808080", fg="white")
lblPrix.place(x=550, y=200, width=150)
txtPrix = Entry(root,bd=4, font=("Arial",14))
txtPrix.place(x=700, y=200, width=150)
#Quantite
lblQuantite = Label(root, text="QUANTITE", font=("Arial",18), bg="#808080", fg="white")
lblQuantite.place(x=550, y=250, width=150)
txtQuantite = Entry(root,bd=4, font=("Arial",14))
txtQuantite.place(x=700, y=250, width=150)

#Enregistrer
btnenregistrer = Button(root,text="Enregistrer",font=("Arial",16),bg="#48308B",fg="white",command=Ajouter)
btnenregistrer.place(x=1000,y=140,width=200)

#Modifier
btnmodifier = Button(root,text="Modifier",font=("Arial",16),bg="#48308B",fg="white",command=Modifier)
btnmodifier.place(x=1000,y=190,width=200)

#Supprimer
btnSupprimer = Button(root,text="Supprimer",font=("Arial",16),bg="#48308B",fg="white",command=Supprimer)
btnSupprimer.place(x=1000,y=240,width=200)

#Retour
btnRetour = Button(root,text="Retour",font=("Arial",16),bg="#B22222",fg="white",command=Retour)
btnRetour.place(x=1260,y=240,width=200)

#Table
table = ttk.Treeview(root, columns=(1,2,3,4,5,6), height=10, show="headings")
table.place(x=0, y=290, width=1550, height=700)

#Entete
table.heading(1, text="CODE_ACHAT" ,command=lambda: sort_treeview(table, 1, False))
table.heading(2, text="FOURNISSEUR" ,command=lambda: sort_treeview(table, 2, False))
table.heading(3, text="TELEPHONE" ,command=lambda: sort_treeview(table, 3, False))
table.heading(4, text="PRODUIT" ,command=lambda: sort_treeview(table, 4, False))
table.heading(5, text="PRIX" ,command=lambda: sort_treeview(table, 5, False))
table.heading(6, text="QUANTITE" ,command=lambda: sort_treeview(table, 6, False))


#definir les dimentions des colonnes
table.column(1, width=50 ,anchor="center")
table.column(2, width=150 ,anchor="center")
table.column(3, width=150 ,anchor="center")
table.column(4, width=100 ,anchor="center")
table.column(5, width=50 ,anchor="center")
table.column(6, width=50 ,anchor="center")

#afficher les informations de la table
maBase = mysql.connector.connect(host="localhost", user="root", password="", database="achat")
meConnect = maBase.cursor()
meConnect.execute("select * from tb_achat")
for row in meConnect:
    table.insert('', END, value=row)
maBase.close()

#Execution
root.mainloop()