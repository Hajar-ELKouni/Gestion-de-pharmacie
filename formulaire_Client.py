import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import re
from datetime import datetime
from tkcalendar import DateEntry

# Connexion à la base de données SQLite
def get_db_connection():
    """Retourner une connexion à la base de données."""
    return sqlite3.connect("DB_Pharmacy.db")

# Validation du téléphone marocain
def is_valid_phone(telephone):
    phone_regex = r'^(0[5-7]|(\+212))[0-9]{8}$'
    return re.match(phone_regex, telephone) is not None

class Formulaireclient:
    def __init__(self, parent, bg_color, button_color):
        self.frame = tk.Frame(parent, bg=bg_color)
        self.frame.pack(fill="both", expand=True)

        # Titre
        tk.Label(
            self.frame, text="Gestion des Clients", bg=bg_color,
            fg="#000000", font=("Arial", 16, "bold")
        ).pack(pady=20)

        self.bg_color = bg_color
        self.button_color = button_color
        self.entry_bg_color = "lightgray"  # Couleur de fond par défaut pour les champs

        # Cadre des champs de saisie
        self.frame_form = tk.Frame(self.frame, bg=bg_color)
        self.frame_form.pack(pady=10, padx=20, fill="x")

        self.entry_nom = self.create_input_field(self.frame_form, "Nom :", 0)
        self.entry_prenom = self.create_input_field(self.frame_form, "Prénom :", 1)
        self.entry_telephone = self.create_input_field(self.frame_form, "Téléphone :", 2)
        self.entry_date_naissance = self.create_date_picker(self.frame_form, "Date de Naissance :", 3)

        self.error_labels = [self.create_error_label(self.frame_form, row) for row in range(4)]

        # Boutons
        self.button_frame = tk.Frame(self.frame, bg=bg_color)
        self.button_frame.pack(pady=10)
        self.create_button(self.button_frame, "Ajouter", self.ajouter).grid(row=0, column=0, padx=5)
        self.create_button(self.button_frame, "Supprimer", self.supprimer).grid(row=0, column=1, padx=5)
        self.create_button(self.button_frame, "Modifier", self.modifier).grid(row=0, column=2, padx=5)
        self.create_button(self.button_frame, "Rechercher", self.rechercher).grid(row=0, column=3, padx=5)

        # Tableau (Treeview)
        self.table_frame = tk.Frame(self.frame, bg=bg_color)
        self.table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.table = ttk.Treeview(
            self.table_frame,
            columns=("id", "nom", "prenom", "telephone", "date_naissance"),
            show="headings",
        )
        self.table.heading("id", text="ID")
        self.table.heading("nom", text="Nom")
        self.table.heading("prenom", text="Prénom")
        self.table.heading("telephone", text="Téléphone")
        self.table.heading("date_naissance", text="Date de Naissance")
        self.table.pack(fill="both", expand=True)

        # Charger les données
        self.afficher_clients()

        # Sélection dans le tableau
        self.table.bind("<<TreeviewSelect>>", self.on_item_select)

    def create_input_field(self, frame, label_text, row):
        label = tk.Label(frame, text=label_text, bg=self.bg_color, fg="#000000", font=("Arial", 10))
        label.grid(row=row, column=0, pady=5, padx=5, sticky="ew")
        entry = tk.Entry(frame)
        entry.grid(row=row, column=1, pady=5, padx=5)
        return entry

    def create_date_picker(self, frame, label_text, row):
        label = tk.Label(frame, text=label_text, bg=self.bg_color, fg="#000000", font=("Arial", 10))
        label.grid(row=row, column=0, pady=5, padx=5, sticky="ew")
        date_picker = DateEntry(frame, width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
        date_picker.grid(row=row, column=1, pady=5, padx=5)
        return date_picker

    def create_error_label(self, frame, row):
        error_label = tk.Label(frame, text="", bg=self.bg_color, fg="red", font=("Arial", 8))
        error_label.grid(row=row, column=2, pady=5, padx=5, sticky="ew")
        return error_label

    def create_button(self, frame, text, command):
        return tk.Button(frame, text=text, bg=self.button_color, fg="white", font=("Arial", 10, "bold"), command=command)

    def vider_champs(self):
        self.entry_nom.delete(0, tk.END)
        self.entry_prenom.delete(0, tk.END)
        self.entry_telephone.delete(0, tk.END)
        self.entry_date_naissance.delete(0, tk.END)

    def ajouter(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        telephone = self.entry_telephone.get()
        date_naissance = self.entry_date_naissance.get()

        # Validation des champs
        for label in self.error_labels:
            label.config(text="")

        erreurs = False
        if not nom:
            self.error_labels[0].config(text="Le nom est requis.")
            erreurs = True
        if not prenom:
            self.error_labels[1].config(text="Le prénom est requis.")
            erreurs = True
        if not telephone:
            self.error_labels[2].config(text="Le téléphone est requis.")
            erreurs = True
        elif not is_valid_phone(telephone):
            self.error_labels[2].config(text="Format de téléphone invalide.")
            erreurs = True
        try:
            datetime.strptime(date_naissance, "%Y-%m-%d")
        except ValueError:
            self.error_labels[3].config(text="Format de date invalide (YYYY-MM-DD).")
            erreurs = True

        if erreurs:
            return

        try:
            with get_db_connection() as connexion:
                curseur = connexion.cursor()
                curseur.execute(
                    """
                    INSERT INTO Client (Nom_C, Prenom_C, Telephone_C, Date_Naissance)
                    VALUES (?, ?, ?, ?)
                    """,
                    (nom, prenom, telephone, date_naissance),
                )
                connexion.commit()
                self.afficher_clients()
                messagebox.showinfo("Succès", f"Client {nom} {prenom} ajouté avec succès.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout : {e}")

        self.vider_champs()

    def supprimer(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un client à supprimer.")
            return

        client_id = self.table.item(selected_item[0])["values"][0]
        confirmation = messagebox.askyesno("Confirmer la suppression", f"Supprimer le client ID {client_id} ?")
        if confirmation:
            try:
                with get_db_connection() as connexion:
                    curseur = connexion.cursor()
                    curseur.execute("DELETE FROM Client WHERE id_C = ?", (client_id,))
                    connexion.commit()
                    self.afficher_clients()
                    messagebox.showinfo("Succès", "Client supprimé.")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", f"Erreur : {e}")

        self.vider_champs()

    def modifier(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un client à modifier.")
            return

        client_id = self.table.item(selected_item[0])["values"][0]
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        telephone = self.entry_telephone.get()
        date_naissance = self.entry_date_naissance.get()

        # Réinitialiser les messages d'erreur
        for label in self.error_labels:
            label.config(text="")

        # Validation des champs
        erreurs = False
        if not nom:
            self.error_labels[0].config(text="Le nom est requis.")
            erreurs = True
        if not prenom:
            self.error_labels[1].config(text="Le prénom est requis.")
            erreurs = True
        if not telephone:
            self.error_labels[2].config(text="Le téléphone est requis.")
            erreurs = True
        elif not is_valid_phone(telephone):
            self.error_labels[2].config(text="Format de téléphone invalide.")
            erreurs = True
        try:
            datetime.strptime(date_naissance, "%Y-%m-%d")
        except ValueError:
            self.error_labels[3].config(text="Format de date invalide (YYYY-MM-DD).")
            erreurs = True

        if erreurs:
            return

        try:
            with get_db_connection() as connexion:
                curseur = connexion.cursor()
                curseur.execute(
                    """
                    UPDATE Client
                    SET Nom_C = ?, Prenom_C = ?, Telephone_C = ?, Date_Naissance = ?
                    WHERE id_C = ?
                    """,
                    (nom, prenom, telephone, date_naissance, client_id),
                )
                connexion.commit()
                self.afficher_clients()
                messagebox.showinfo("Succès", "Client modifié avec succès.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur : {e}")

        self.vider_champs()

    def rechercher(self):
        nom = self.entry_nom.get().lower()
        prenom = self.entry_prenom.get().lower()

        try:
            with get_db_connection() as connexion:
                curseur = connexion.cursor()
                curseur.execute(
                    """
               SELECT * FROM Client
                WHERE Nom_C COLLATE NOCASE LIKE ? AND Prenom_C COLLATE NOCASE LIKE ?
               """,
               (f"%{nom}%", f"%{prenom}%"),
                )
                clients = curseur.fetchall()

            if clients:
                self.table.delete(*self.table.get_children())
                for client in clients:
                    self.table.insert("", "end", values=client)
            else:
                messagebox.showinfo("Aucun résultat", "Aucun client trouvé avec ces critères.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")

    def afficher_clients(self):
        try:
            with get_db_connection() as connexion:
                curseur = connexion.cursor()
                curseur.execute("SELECT * FROM Client")
                clients = curseur.fetchall()

            self.table.delete(*self.table.get_children())
            for client in clients:
                self.table.insert("", "end", values=client)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des clients : {e}")

    def on_item_select(self, event):
     selected_item = self.table.selection()
     if selected_item:
        # Extraire l'ID du client sélectionné (index 0)
        client_id = self.table.item(selected_item)["values"][0]

        # Requête pour récupérer les informations du client depuis la base de données
        try:
            connexion = sqlite3.connect("PharmacyManagement.db")
            curseur = connexion.cursor()

            # Effectuer la requête pour récupérer les détails du client basé sur l'ID
            curseur.execute('''
                SELECT Nom_C, Prenom_C, Telephone_C, Date_Naissance
                FROM Client
                WHERE id_C = ?
            ''', (client_id,))

            # Récupérer les résultats de la requête
            client = curseur.fetchone()
            if client:
                # Si un client est trouvé, récupérer ses informations
                nom, prenom, telephone, date_naissance = client

                # Remplir les champs avec les données récupérées
                self.entry_nom.delete(0, tk.END)
                self.entry_nom.insert(0, nom)
                self.entry_prenom.delete(0, tk.END)
                self.entry_prenom.insert(0, prenom)
                self.entry_telephone.delete(0, tk.END)
                self.entry_telephone.insert(0, telephone)
                self.entry_date_naissance.delete(0, tk.END)
                self.entry_date_naissance.insert(0, date_naissance)
            else:
                print(f"Aucun client trouvé avec l'ID {client_id}")

        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des informations : {e}")
        finally:
            connexion.close()




    def show(self):
       """Afficher la page des clients."""
       self.frame.pack(fill="both", expand=True)
       self.afficher_clients()  # Assurez-vous que la fonction est bien appelée

    def hide(self):
       """Cacher la page des clients."""
       self.frame.pack_forget()