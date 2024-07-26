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
    clients = txtClients.get()
    telephone = txtTelephone.get()
    produit = comboproduit.get()
    prix_ventes = txtPrixVentes.get()
    vendu = txtVendu.get()

    if not all((matricule, clients, telephone, produit, prix_ventes, vendu)):
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return
    if not telephone.isdigit() or len(telephone) != 8:
        messagebox.showerror("Erreur", "Le numéro de téléphone doit être 8 chiffres.")
        return

    try:
        vendu = int(vendu)
    except ValueError:
        messagebox.showerror("Erreur", "La quantité vendue doit être un nombre entier.")
        return

    maBase = mysql.connector.connect(host="localhost", user="root", password="", database="achat")
    meConnect = maBase.cursor()

    try:
        # Vérifier la quantité en stock
        meConnect.execute("SELECT quantite FROM tb_stock WHERE produit = %s", (produit,))
        stock = meConnect.fetchone()

        if stock is None:
            messagebox.showerror("Erreur", "Le produit spécifié n'existe pas dans le stock.")
            return

        stock_quantite = stock[0]

        if vendu > stock_quantite:
            messagebox.showerror("Erreur", "La quantité vendue dépasse la quantité en stock.")
            return

        # Ajouter la vente
        sql = "INSERT INTO tb_vente (CODE_VENTE, clients, telephone, produit, prix_ventes, vendu) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (matricule, clients, telephone, produit, prix_ventes, vendu)
        meConnect.execute(sql, val)

        # Mettre à jour le stock
        sql_stock = "UPDATE tb_stock SET quantite = quantite - %s WHERE produit = %s"
        val_stock = (vendu, produit)
        meConnect.execute(sql_stock, val_stock)

        maBase.commit()
        messagebox.showinfo("Information", "Vente terminée et stock mis à jour.")
        root.destroy()
        call(["python", "Ventes.py"])
    except Exception as e:
        print(e)
        maBase.rollback()
    finally:
        maBase.close()


def Modifier():
    matricule = txtNumero.get()
    clients = txtClients.get()
    telephone = txtTelephone.get()
    produit = comboproduit.get()
    prix_ventes = txtPrixVentes.get()
    vendu = txtVendu.get()
    if not all((matricule, clients, telephone, produit, prix_ventes, vendu)):
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return
    maBase = mysql.connector.connect(host="localhost", user="root", password="", database="achat")
    meConnect = maBase.cursor()
    try:
        # Récupérer l'ancienne quantité vendue
        meConnect.execute("SELECT vendu FROM tb_vente WHERE CODE_VENTE = %s", (matricule,))
        old_vendu = meConnect.fetchone()[0]

        # Mettre à jour la vente
        sql = "UPDATE tb_vente SET clients=%s, telephone=%s, produit=%s, prix_ventes=%s, vendu=%s WHERE CODE_VENTE=%s"
        val = (clients, telephone, produit, prix_ventes, vendu, matricule)
        meConnect.execute(sql, val)

        # Mettre à jour le stock
        sql_stock = "UPDATE tb_stock SET quantite = quantite + %s - %s WHERE produit = %s"
        val_stock = (old_vendu, vendu, produit)
        meConnect.execute(sql_stock, val_stock)

        maBase.commit()
        messagebox.showinfo("Information", "Vente modifiée et stock mis à jour.")
        root.destroy()
        call(["python", "Ventes.py"])
    except Exception as e:
        print(e)
        maBase.rollback()
    finally:
        maBase.close()


def AjouterAchat():
    produit = comboproduit.get()
    quantite = txtVendu.get()
    if not all((produit, quantite)):
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return
    if not quantite.isdigit():
        messagebox.showerror("Erreur", "La quantité doit être un nombre entier.")
        return
    maBase = mysql.connector.connect(host="localhost", user="root", password="", database="achat")
    meConnect = maBase.cursor()
    try:
        # Ajouter l'achat à la table d'achats
        sql = "INSERT INTO tb_achat (produit, quantite) VALUES (%s, %s)"
        val = (produit, quantite)
        meConnect.execute(sql, val)

        # Mettre à jour le stock
        sql_stock = "UPDATE tb_stock SET quantite = quantite + %s WHERE produit = %s"
        val_stock = (quantite, produit)
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


def Supprimer():
    matricule = txtNumero.get()
    if messagebox.askyesno("Confirmation", "Seriez-vous d'accord pour supprimer cet élément ?"):
        maBase = mysql.connector.connect(host="localhost", user="root", password="", database="achat")
        meConnect = maBase.cursor()
        try:
            # Récupérer les détails de la vente à supprimer
            meConnect.execute("SELECT produit, vendu FROM tb_vente WHERE CODE_VENTE = %s", (matricule,))
            vente = meConnect.fetchone()
            produit = vente[0]
            vendu = vente[1]

            # Supprimer la vente
            sql = "DELETE FROM tb_vente WHERE CODE_VENTE = %s"
            val = (matricule,)
            meConnect.execute(sql, val)

            # Mettre à jour le stock
            sql_stock = "UPDATE tb_stock SET quantite = quantite + %s WHERE produit = %s"
            val_stock = (vendu, produit)
            meConnect.execute(sql_stock, val_stock)

            maBase.commit()
            messagebox.showinfo("Information", "Vente supprimée et stock mis à jour.")
            root.destroy()
            call(["python", "Ventes.py"])
        except Exception as e:
            print(e)
            maBase.rollback()
        finally:
            maBase.close()

#Ma fenetre
root = Tk()
root.title("MENU DES VENTES")
root.geometry("1550x790+0+0")
#root.geometry("1350x700+0+0")
root.resizable(False, False)
root.config(background="#808080")

#Ajouter le titre
lbltitre = Label(root,borderwidth = 3, relief = SUNKEN
                 ,text = "GESTION DES VENTES", font=("Sans Serif", 25, "bold"),background = "#483088", foreground = "#FFFAFA")
lbltitre.place(x=0,y=0,width=1550, height=100)

#Detail des achats
#Matricule
lblNumero = Label(root, text="MATRICULE", font=("Arial",18), bg="#808080", fg="white")
lblNumero.place(x=70, y=150, width=150)
txtNumero = Entry(root,bd=4, font=("Arial",14))
txtNumero.place(x=250, y=150, width=150)
#Fournisseur
lblClients = Label(root, text="CLIENTS", font=("Arial",18), bg="#808080", fg="white")
lblClients.place(x=50, y=200, width=200)
txtClients = Entry(root,bd=4, font=("Arial",14))
txtClients.place(x=250, y=200, width=300)
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
lblPrixVentes = Label(root, text="PRIX", font=("Arial",18), bg="#808080", fg="white")
lblPrixVentes.place(x=550, y=200, width=150)
txtPrixVentes = Entry(root,bd=4, font=("Arial",14))
txtPrixVentes.place(x=700, y=200, width=150)
#Quantite
lblVendu = Label(root, text="QUANTITE", font=("Arial",18), bg="#808080", fg="white")
lblVendu.place(x=550, y=250, width=150)
txtVendu = Entry(root,bd=4, font=("Arial",14))
txtVendu.place(x=700, y=250, width=150)


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

#Ajouter le titre
lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="TABLE DES STOCKS", font=("Sans Serif", 20, "bold"), background="#483088", foreground="#FFFAFA")
lbltitre.place(x=60,y=300,width=400)

#Table Stocks
table = ttk.Treeview(root, columns=(1, 2) ,height=10 ,show="headings")
table.place(x=60, y=330, width=400, height=600 )

#Entete
table.heading(1, text="PRODUIT" ,command=lambda: sort_treeview(table, 1, False))
table.heading(2, text="QUANTITE" ,command=lambda: sort_treeview(table, 1, False))

#definir les dimentions des colonnes
table.column(1, width=200 ,anchor="center")
table.column(2, width=100 ,anchor="center")

#afficher les informations de la table
maBase = mysql.connector.connect(host="localhost", user="root", password="", database="achat")
meConnect = maBase.cursor()
meConnect.execute("select produit, quantite from tb_stock")
for row in meConnect:
    table.insert('', END, value=row)
maBase.close()


#Ajouter le titre
lbltitre = Label(root,borderwidth = 3, relief = SUNKEN
                 ,text = "GESTION DES VENTES", font=("Sans Serif", 18, "bold"),background = "#483088", foreground = "#FFFAFA")
lbltitre.place(x=580,y=300,width=900)

#Table Ventes
table = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6) ,height=10 ,show="headings")
table.place(x=580, y=330, width=900, height=600 )

#Entete
table.heading(1, text="CODE_VENTE" ,command=lambda: sort_treeview(table, 1, False))
table.heading(2, text="CLIENTS" ,command=lambda: sort_treeview(table, 2, False))
table.heading(3, text="TELEPHONE" ,command=lambda: sort_treeview(table, 3, False))
table.heading(4, text="PRODUIT" ,command=lambda: sort_treeview(table, 4, False))
table.heading(5, text="PRIX_VENTES" ,command=lambda: sort_treeview(table, 5, False))
table.heading(6, text="VENDU" ,command=lambda: sort_treeview(table, 6, False))

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
meConnect.execute("select * from tb_vente")
for row in meConnect:
    table.insert('', END, value=row)
maBase.close()


#Execution
root.mainloop()