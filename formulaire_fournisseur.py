import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import re

# Connexion à la base de données SQLite
def get_db_connection():
    """Retourner une connexion à la base de données."""
    return sqlite3.connect("DB_Pharmacy.db")

# Fonction pour valider le format de l'email
def is_valid_email(email):
    """Vérifie si l'email est dans un format valide."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Fonction pour valider le format du téléphone marocain
def is_valid_phone(telephone):
    """Vérifie si le téléphone est dans un format valide marocain (commence par 06, 05, ou +212)."""
    phone_regex = r'^(0[5-7]|(\+212))[0-9]{8}$'
    return re.match(phone_regex, telephone) is not None

# Formulaire Fournisseur
class FormulaireFournisseur:
    def __init__(self, parent, bg_color, button_color):
        self.bg_color = bg_color
        self.button_color = button_color

        self.frame = tk.Frame(parent, bg=bg_color)
        self.frame.pack(fill="both", expand=True)

        # Titre
        tk.Label(
            self.frame,
            text="Gestion des Fournisseurs",
            bg=bg_color,
            fg="#000000",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        # Cadre pour les champs de saisie
        self.input_frame = tk.Frame(self.frame, bg=bg_color)
        self.input_frame.pack(pady=10)

        self.entry_nom = self.create_input_field(self.input_frame, "Nom :", 0)
        self.entry_email = self.create_input_field(self.input_frame, "Email :", 1)
        self.entry_telephone = self.create_input_field(self.input_frame, "Téléphone :", 2)
        self.entry_adresse = self.create_input_field(self.input_frame, "Adresse :", 3)

        # Labels d'erreur
        self.error_nom = self.create_error_label(self.input_frame, 0)
        self.error_email = self.create_error_label(self.input_frame, 1)
        self.error_telephone = self.create_error_label(self.input_frame, 2)
        self.error_adresse = self.create_error_label(self.input_frame, 3)

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
            columns=("numéro", "nom", "email", "telephone", "adresse"),
            show="headings",
        )
        self.table.heading("numéro", text="Numéro")
        self.table.heading("nom", text="Nom")
        self.table.heading("email", text="Email")
        self.table.heading("telephone", text="Téléphone")
        self.table.heading("adresse", text="Adresse")
        self.table.pack(fill="both", expand=True)

        # Mettre à jour l'affichage des fournisseurs à l'initialisation
        self.afficher_fournisseurs()

        # Ajouter un événement de sélection sur le tableau
        self.table.bind("<<TreeviewSelect>>", self.on_item_select)

    def create_input_field(self, frame, label_text, row):
        label = tk.Label(frame, text=label_text, bg=self.bg_color, fg="#000000", font=("Arial", 10))
        label.grid(row=row, column=0, pady=5, padx=5, sticky="w")
        entry = tk.Entry(frame)
        entry.grid(row=row, column=1, pady=5, padx=5)
        return entry

    def create_error_label(self, frame, row):
        error_label = tk.Label(frame, text="", bg=self.bg_color, fg="red", font=("Arial", 8))
        error_label.grid(row=row, column=2, pady=5, padx=5, sticky="w")
        return error_label

    def create_button(self, frame, text, command):
        return tk.Button(
            frame,
            text=text,
            bg=self.button_color,
            fg="#FFFFFF",
            font=("Arial", 10, "bold"),
            command=command,
        )

    def vider_champs(self):
        """Vider les champs de saisie."""
        self.entry_nom.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telephone.delete(0, tk.END)
        self.entry_adresse.delete(0, tk.END)

    def ajouter(self):
        nom = self.entry_nom.get()
        email = self.entry_email.get()
        telephone = self.entry_telephone.get()
        adresse = self.entry_adresse.get()

        # Réinitialiser les erreurs
        self.error_nom.config(text="")
        self.error_email.config(text="")
        self.error_telephone.config(text="")
        self.error_adresse.config(text="")

        erreurs = False

        if not nom:
            self.error_nom.config(text="Le nom est requis.")
            erreurs = True

        if not email:
            self.error_email.config(text="L'email est requis.")
            erreurs = True
        elif not is_valid_email(email):
            self.error_email.config(text="L'email n'est pas valide.")
            erreurs = True

        if not telephone:
            self.error_telephone.config(text="Le téléphone est requis.")
            erreurs = True
        elif not is_valid_phone(telephone):
            self.error_telephone.config(text="Le téléphone n'est pas valide. Format marocain requis.")
            erreurs = True

        if not adresse:
            self.error_adresse.config(text="L'adresse est requise.")
            erreurs = True

        if erreurs:
            return

        try:
            connexion = get_db_connection()
            curseur = connexion.cursor()
            curseur.execute('''
                INSERT INTO Fournisseur (Nom_F, Email_F, Telephone_F, Address_F)
                VALUES (?, ?, ?, ?)
            ''', (nom, email, telephone, adresse))
            connexion.commit()
            self.afficher_fournisseurs()
            messagebox.showinfo("Succès", f"Fournisseur {nom} ajouté avec succès.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout du fournisseur: {e}")
        finally:
            connexion.close()

        self.vider_champs()

    def supprimer(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un fournisseur à supprimer.")
            return

        fournisseur_numero = self.table.item(selected_item)["values"][0]

        confirmation = messagebox.askyesno("Confirmer la suppression", f"Voulez-vous vraiment supprimer le fournisseur avec numéro {fournisseur_numero}?")
        if confirmation:
            try:
                connexion = get_db_connection()
                curseur = connexion.cursor()
                curseur.execute("DELETE FROM Fournisseur WHERE id_F=?", (fournisseur_numero,))
                connexion.commit()
                self.afficher_fournisseurs()
                messagebox.showinfo("Succès", f"Fournisseur avec numéro {fournisseur_numero} supprimé avec succès.")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression du fournisseur: {e}")
            finally:
                connexion.close()

        self.vider_champs()

    def modifier(self):
        nom = self.entry_nom.get()
        email = self.entry_email.get()
        telephone = self.entry_telephone.get()
        adresse = self.entry_adresse.get()

        # Réinitialiser les erreurs
        self.error_nom.config(text="")
        self.error_email.config(text="")
        self.error_telephone.config(text="")
        self.error_adresse.config(text="")

        erreurs = False

        if not nom:
            self.error_nom.config(text="Le nom est requis.")
            erreurs = True

        if not email:
            self.error_email.config(text="L'email est requis.")
            erreurs = True
        elif not is_valid_email(email):
            self.error_email.config(text="L'email n'est pas valide.")
            erreurs = True

        if not telephone:
            self.error_telephone.config(text="Le téléphone est requis.")
            erreurs = True
        elif not is_valid_phone(telephone):
            self.error_telephone.config(text="Le téléphone n'est pas valide. Format marocain requis.")
            erreurs = True

        if not adresse:
            self.error_adresse.config(text="L'adresse est requise.")
            erreurs = True

        if erreurs:
            return

        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un fournisseur à modifier.")
            return

        fournisseur_numero = self.table.item(selected_item)["values"][0]

        try:
            connexion = get_db_connection()
            curseur = connexion.cursor()
            curseur.execute('''
                UPDATE Fournisseur
                SET Nom_F = ?, Email_F = ?, Telephone_F = ?, Address_F = ?
                WHERE id_F = ?
            ''', (nom, email, telephone, adresse, fournisseur_numero))
            connexion.commit()
            self.afficher_fournisseurs()
            messagebox.showinfo("Succès", f"Fournisseur avec numéro {fournisseur_numero} modifié avec succès.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification du fournisseur: {e}")
        finally:
            connexion.close()

        self.vider_champs()

    def rechercher(self):
        nom_recherche = self.entry_nom.get()

        if nom_recherche == "":
            self.afficher_fournisseurs()
            messagebox.showinfo("Recherche", "Liste complète des fournisseurs affichée.")
        else:
            try:
                connexion = get_db_connection()
                curseur = connexion.cursor()
                curseur.execute('''
                    SELECT id_F, Nom_F, Email_F, Telephone_F, Address_F
                    FROM Fournisseur
                    WHERE Nom_F LIKE ?
                ''', (f"%{nom_recherche}%",))
                resultats = curseur.fetchall()

                for row in self.table.get_children():
                    self.table.delete(row)
                for fournisseur in resultats:
                    self.table.insert("", "end", values=fournisseur)

                messagebox.showinfo("Recherche", f"{len(resultats)} résultat(s) trouvé(s) pour '{nom_recherche}'.")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")
            finally:
                connexion.close()

    def on_item_select(self, event):
     selected_item = self.table.selection()
     if selected_item:
        # Extraire l'ID du fournisseur sélectionné (index 0)
        fournisseur_id = self.table.item(selected_item)["values"][0]

        # Requête pour récupérer les informations du fournisseur depuis la base de données
        try:
            connexion = sqlite3.connect("PharmacyManagement.db")
            curseur = connexion.cursor()

            # Effectuer la requête pour récupérer les détails du fournisseur basé sur l'ID
            curseur.execute('''
                SELECT Nom_F, Email_F, Telephone_F, Address_F
                FROM Fournisseur
                WHERE id_F = ?
            ''', (fournisseur_id,))

            # Récupérer les résultats de la requête
            fournisseur = curseur.fetchone()
            if fournisseur:
                # Si un fournisseur est trouvé, récupérer ses informations
                nom, email, telephone, adresse = fournisseur

                # Remplir les champs avec les données récupérées
                self.entry_nom.delete(0, tk.END)
                self.entry_nom.insert(0, nom)
                self.entry_email.delete(0, tk.END)
                self.entry_email.insert(0, email)
                self.entry_telephone.delete(0, tk.END)
                self.entry_telephone.insert(0, telephone)
                self.entry_adresse.delete(0, tk.END)
                self.entry_adresse.insert(0, adresse)
            else:
                print(f"Aucun fournisseur trouvé avec l'ID {fournisseur_id}")

        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des informations : {e}")
        finally:
            connexion.close()


    def afficher_fournisseurs(self):
        for row in self.table.get_children():
            self.table.delete(row)

        try:
            connexion = get_db_connection()
            curseur = connexion.cursor()
            curseur.execute("SELECT id_F, Nom_F, Email_F, Telephone_F, Address_F FROM Fournisseur")
            fournisseurs = curseur.fetchall()
            for fournisseur in fournisseurs:
                self.table.insert("", "end", values=fournisseur)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des fournisseurs: {e}")
        finally:
            connexion.close()

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()
