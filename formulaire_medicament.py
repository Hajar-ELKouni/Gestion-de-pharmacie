import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

class FormulaireMedicament:
    def __init__(self, parent, bg_color, button_color, entry_bg_color):
        # Initialisation de la fenêtre et des couleurs
        self.frame = tk.Frame(parent, bg=bg_color)
        self.frame.pack(fill="both", expand=True)

        self.bg_color = bg_color
        self.button_color = button_color
        self.entry_bg_color = entry_bg_color

        # Titre
        self.label_title = tk.Label(
            self.frame, text="Gestion des Médicaments", font=("Helvetica", 16, "bold"), bg=bg_color
        )
        self.label_title.pack(pady=10)

        # Formulaire (centré)
        self.frame_form = tk.Frame(self.frame, bg=bg_color)
        self.frame_form.pack(pady=10, padx=20, fill="x", anchor="center")

        # Champs de saisie
        self.entry_code = self.create_input_field(self.frame_form, "Code Article :", 0, 0)
        self.entry_nom_generique = self.create_input_field(self.frame_form, "Nom Générique :", 1, 0)
        self.entry_nom_commercial = self.create_input_field(self.frame_form, "Nom Commercial :", 1, 1)

        formes = ["Comprimé", "Solution", "Injection", "Pommade"]
        self.combobox_forme = self.create_input_field(self.frame_form, "Forme Pharmaceutique :", 2, 0, "combobox", formes)

        self.entry_dosage = self.create_input_field(self.frame_form, "Dosage :", 2, 1)
        self.entry_prix = self.create_input_field(self.frame_form, "Prix Unitaire :", 3, 0)
        self.entry_seuil = self.create_input_field(self.frame_form, "Seuil d'Approvisionnement :", 3, 1)

        self.date_fab = self.create_input_field(self.frame_form, "Date de Fabrication :", 4, 0, "date")
        self.date_exp = self.create_input_field(self.frame_form, "Date d'Expiration :", 4, 1, "date")

        self.entry_emplacement = self.create_input_field(self.frame_form, "Emplacement :", 5, 0)

        self.combobox_fournisseur = self.create_input_field(
            self.frame_form, "Fournisseur :", 5, 1, "combobox"
        )
        self.load_fournisseurs()

        # Zone pour afficher les erreurs
        self.error_label_code = self.create_error_label(self.frame_form, 0, 2)
        self.error_label_nom_generique = self.create_error_label(self.frame_form, 1, 2)
        self.error_label_nom_commercial = self.create_error_label(self.frame_form, 1, 3)
        self.error_label_prix = self.create_error_label(self.frame_form, 3, 2)
        self.error_label_seuil = self.create_error_label(self.frame_form, 3, 3)
        self.error_label_dates = self.create_error_label(self.frame_form, 4, 2)

        # Boutons
        self.frame_buttons = tk.Frame(self.frame, bg=bg_color)
        self.frame_buttons.pack(pady=10)

        self.button_ajouter = tk.Button(
            self.frame_buttons, text="Ajouter", command=self.ajouter, bg=button_color, fg="#FFFFFF"
        )
        self.button_ajouter.grid(row=0, column=0, padx=5, pady=5)

        # Tableau
        self.frame_table = tk.Frame(self.frame, bg=bg_color)
        self.frame_table.pack(fill="both", expand=True, pady=10)

        self.table = ttk.Treeview(
            self.frame_table,
            columns=("code", "nom_generique", "nom_commercial", "forme", "dosage", "prix", "seuil"),
            show="headings",
        )
        self.table.heading("code", text="Code")
        self.table.heading("nom_generique", text="Nom Générique")
        self.table.heading("nom_commercial", text="Nom Commercial")
        self.table.heading("forme", text="Forme")
        self.table.heading("dosage", text="Dosage")
        self.table.heading("prix", text="Prix")
        self.table.heading("seuil", text="Seuil")
        self.table.pack(fill="both", expand=True)

        self.load_table()

    def create_input_field(self, frame, label_text, row, col, widget_type="entry", options=None):
        # Fonction utilitaire pour créer des champs d'entrée
        label = tk.Label(frame, text=label_text, bg=self.bg_color)
        label.grid(row=row, column=col * 2, padx=5, pady=5, sticky="w")

        if widget_type == "entry":
            entry = tk.Entry(frame, bg=self.entry_bg_color)
            entry.grid(row=row, column=col * 2 + 1, padx=5, pady=5)
            return entry
        elif widget_type == "combobox":
            combobox = ttk.Combobox(frame, values=options or [], state="readonly")
            combobox.grid(row=row, column=col * 2 + 1, padx=5, pady=5)
            return combobox
        elif widget_type == "date":
            date_picker = DateEntry(frame, background="darkblue", foreground="white", date_pattern="yyyy-MM-dd")
            date_picker.grid(row=row, column=col * 2 + 1, padx=5, pady=5)
            return date_picker

    def create_error_label(self, frame, row, col):
        error_label = tk.Label(frame, text="", fg="red", bg=self.bg_color)
        error_label.grid(row=row, column=col, padx=5, pady=5, sticky="w")
        return error_label

    def load_fournisseurs(self):
        try:
            connexion = sqlite3.connect("PharmacyManagement.db")
            curseur = connexion.cursor()
            curseur.execute("SELECT nom_F FROM Fournisseur")
            fournisseurs = curseur.fetchall()

            if self.combobox_fournisseur:
                self.combobox_fournisseur["values"] = [f[0] for f in fournisseurs]
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur de chargement des fournisseurs : {e}")
        finally:
            connexion.close()

    def load_table(self):
        # Charge les médicaments depuis la base de données dans le tableau
        for i in self.table.get_children():
            self.table.delete(i)

        try:
            connexion = sqlite3.connect("PharmacyManagement.db")
            curseur = connexion.cursor()
            curseur.execute("SELECT * FROM Medicament")
            rows = curseur.fetchall()
            for row in rows:
                self.table.insert("", "end", values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur de chargement des médicaments : {e}")
        finally:
            connexion.close()

    def ajouter(self):
        # Réinitialiser les messages d'erreur
        self.error_label_code.config(text="")
        self.error_label_nom_generique.config(text="")
        self.error_label_nom_commercial.config(text="")
        self.error_label_prix.config(text="")
        self.error_label_seuil.config(text="")
        self.error_label_dates.config(text="")

        # Vérification des champs
        errors = False

        if not self.entry_code.get():
            self.error_label_code.config(text="Le code article est obligatoire.")
            errors = True
        if not self.entry_nom_generique.get():
            self.error_label_nom_generique.config(text="Le nom générique est obligatoire.")
            errors = True
        if not self.entry_nom_commercial.get():
            self.error_label_nom_commercial.config(text="Le nom commercial est obligatoire.")
            errors = True

        # Vérification des types pour prix et seuil
        try:
            prix = float(self.entry_prix.get()) if self.entry_prix.get() else 0.0
            self.error_label_prix.config(text="")  # Si prix valide, effacer l'erreur
        except ValueError:
            self.error_label_prix.config(text="Le prix doit être un nombre valide.")
            errors = True

        try:
            seuil = int(self.entry_seuil.get()) if self.entry_seuil.get() else 0
            self.error_label_seuil.config(text="")  # Si seuil valide, effacer l'erreur
        except ValueError:
            self.error_label_seuil.config(text="Le seuil doit être un nombre entier.")
            errors = True

        # Validation des dates
        try:
            date_fab = self.date_fab.get_date()
            date_exp = self.date_exp.get_date()

            if date_exp <= date_fab:
                self.error_label_dates.config(text="La date d'expiration doit être après la date de fabrication.")
                errors = True
            else:
                self.error_label_dates.config(text="")  # Si dates valides, effacer l'erreur

        except Exception as e:
            self.error_label_dates.config(text="Erreur dans les dates.")
            errors = True

        # Si des erreurs, arrêter le processus
        if errors:
            return

        # Ajouter à la base de données si tout est valide
        try:
            connexion = sqlite3.connect("PharmacyManagement.db")
            curseur = connexion.cursor()

            code = self.entry_code.get()
            nom_generique = self.entry_nom_generique.get()
            nom_commercial = self.entry_nom_commercial.get()
            forme = self.combobox_forme.get()
            dosage = self.entry_dosage.get()
            emplacement = self.entry_emplacement.get()

            curseur.execute(""" 
            INSERT INTO Medicament (Code_Article, Nom_Generique, Nom_Commercial, Forme_Pharmaceutique, Dosage,
                                    Prix_Unitaire, Date_Fab, Date_Exp, Emplacement, Seuil_Approv, Statut, Avec_Ordonnance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (code, nom_generique, nom_commercial, forme, dosage, prix, date_fab, date_exp,
                  emplacement, seuil, "Disponible", 0))

            connexion.commit()
            messagebox.showinfo("Succès", "Médicament ajouté avec succès !")
            self.load_table()

            # Réinitialisation des champs après ajout
            self.entry_code.delete(0, tk.END)
            self.entry_nom_generique.delete(0, tk.END)
            self.entry_nom_commercial.delete(0, tk.END)
            self.entry_dosage.delete(0, tk.END)
            self.entry_prix.delete(0, tk.END)
            self.entry_seuil.delete(0, tk.END)
            self.entry_emplacement.delete(0, tk.END)

        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout : {e}")
        finally:
            connexion.close()

    def modifier(self):
        # Code pour la modification des médicaments
        pass

    def supprimer(self):
        # Code pour la suppression des médicaments
        pass

    def rechercher(self):
        # Code pour la recherche des médicaments
        pass

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()
