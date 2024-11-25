import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3


class FormulaireMedicament:
    def __init__(self, parent, bg_color, button_color, entry_color):
        self.parent = parent
        self.bg_color = bg_color
        self.button_color = button_color
        self.entry_color = entry_color
        self.frame_visible = False

        # Connexion à la base de données
        self.connexion = sqlite3.connect("DB_Pharmacy.db")
        self.curseur = self.connexion.cursor()

 
        self.connexion.commit()

        # Frame principale
        self.main_frame = None

    def create_widgets(self):
        if self.main_frame is None:
            self.main_frame = tk.Frame(self.parent, bg=self.bg_color)
            self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

            self.form_frame = tk.LabelFrame(
                self.main_frame, text="Formulaire Médicament", bg="#ffffff", fg="black", padx=10, pady=10
            )
            self.form_frame.pack(side="top", fill="x", pady=5)

            # Champs du formulaire
            self.fields = {}
            self.add_form_field("Code Article :", "code_article", 0, "entry")
            self.add_form_field("Nom Générique :", "nom_generique", 1, "entry")
            self.add_form_field("Nom Commercial :", "nom_commercial", 2, "entry")
            self.add_form_field(
                "Forme Pharmaceutique :", "forme", 3, "combobox", ["Comprimé", "Solution", "Injection", "Pommade"]
            )
            self.add_form_field("Dosage :", "dosage", 4, "entry")
            self.add_form_field("Prix Unitaire :", "prix_unitaire", 5, "entry")
            self.add_form_field("Date de Fabrication :", "date_fab", 6, "date")
            self.add_form_field("Date d'Expiration :", "date_exp", 7, "date")
            self.add_form_field("Emplacement :", "emplacement", 8, "entry")
            self.add_form_field("Seuil Approvisionnement :", "seuil", 9, "entry")
            self.add_form_field("Statut :", "statut", 10, "combobox", ["Disponible", "Indisponible"])
            self.add_form_field("Avec Ordonnance :", "ordonnance", 11, "combobox", ["Oui", "Non"])

            # Boutons d'action
            self.buttons_frame = tk.Frame(self.main_frame, bg=self.bg_color)
            self.buttons_frame.pack(fill="x", pady=5)

            buttons = [
                ("Ajouter", self.ajouter_medicament),
                ("Modifier", self.modifier_medicament),
                ("Supprimer", self.supprimer_medicament),
                ("Rechercher", self.rechercher_medicament),
                ("Réinitialiser", self.reinitialiser_formulaire),
            ]

            for text, command in buttons:
                tk.Button(
                    self.buttons_frame, text=text, command=command, bg=self.button_color, fg="white"
                ).pack(side="left", padx=5)

            # Tableau des médicaments
            self.table_frame = tk.Frame(self.main_frame, bg=self.bg_color)
            self.table_frame.pack(fill="both", expand=True, pady=10)

            self.table = ttk.Treeview(
                self.table_frame,
                columns=(
                    "Code_Article", "Nom_Generique", "Nom_Commercial", "Forme_Pharmaceutique", "Dosage",
                    "Prix_Unitaire", "Date_Fab", "Date_Exp", "Emplacement", "Seuil_Approv", "Statut", "Avec_Ordonnance"
                ),
                show="headings",
                height=15
            )

            column_widths = {
                "Code_Article": 100,
                "Nom_Generique": 150,
                "Nom_Commercial": 150,
                "Forme_Pharmaceutique": 130,
                "Dosage": 80,
                "Prix_Unitaire": 100,
                "Date_Fab": 100,
                "Date_Exp": 100,
                "Emplacement": 120,
                "Seuil_Approv": 100,
                "Statut": 100,
                "Avec_Ordonnance": 120,
            }

            for col, width in column_widths.items():
                self.table.heading(col, text=col.replace("_", " ").capitalize())
                self.table.column(col, width=width, anchor="center")

            self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
            self.table.configure(yscroll=self.scrollbar.set)
            self.scrollbar.pack(side="right", fill="y")
            self.table.pack(fill="both", expand=True)

            self.table.bind("<<TreeviewSelect>>", self.remplir_formulaire)

            self.load_table()

    def add_form_field(self, label, field, row, widget_type, options=None):
        tk.Label(self.form_frame, text=label, bg="#ffffff").grid(row=row, column=0, sticky="w", pady=5)

        if widget_type == "entry":
            widget = tk.Entry(self.form_frame, bg=self.entry_color)
        elif widget_type == "combobox":
            widget = ttk.Combobox(self.form_frame, values=options or [], state="readonly")
        elif widget_type == "date":
            widget = DateEntry(self.form_frame, background="darkblue", foreground="white", date_pattern="yyyy-MM-dd")
        else:
            return

        widget.grid(row=row, column=1, pady=5, sticky="ew")
        self.fields[field] = widget

    def load_table(self):
        """Charge les données de la base dans le tableau."""
        for row in self.table.get_children():
            self.table.delete(row)
        try:
            self.curseur.execute("SELECT * FROM Medicament")
            rows = self.curseur.fetchall()
            for row in rows:
                display_row = list(row)
                display_row[-1] = "Oui" if display_row[-1] == 1 else "Non"
                self.table.insert("", "end", values=display_row)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données : {e}")

    def ajouter_medicament(self):
       try:
        # Récupérer les données des champs
        data = {key: field.get() for key, field in self.fields.items()}
        data["ordonnance"] = 1 if data["ordonnance"] == "Oui" else 0

        # Supprimer les anciens labels d'erreur
        for field, widget in self.fields.items():
            if hasattr(widget, "error_label"):
                widget.error_label.destroy()

        errors = {}

        # Validation des champs obligatoires
        champs_obligatoires = [
            "code_article", "nom_generique", "nom_commercial", "forme",
            "dosage", "prix_unitaire", "date_fab", "date_exp",
            "emplacement", "seuil", "statut","ordonnance"
        ]

        for champ in champs_obligatoires:
            if not data[champ]:
                errors[champ] = "Ce champ est obligatoire."

        # Validation du prix unitaire
        # Validation du prix unitaire
        try:
          prix = float(data["prix_unitaire"])  # Conversion en float
          if prix <= 0:
           errors["prix_unitaire"] = "Doit être un nombre positif."  # Vérifie que le prix est positif
        except ValueError:
           errors["prix_unitaire"] = "Doit être un nombre réel valide." 

        # Validation du seuil d'approvisionnement
        try:
            seuil = int(data["seuil"])
            if seuil < 0:
                errors["seuil"] = "Doit être un entier non négatif."
        except ValueError:
            errors["seuil"] = "Doit être un entier valide."

        # Validation des dates
        from datetime import datetime
        try:
            date_fab = datetime.strptime(data["date_fab"], "%Y-%m-%d")
            date_exp = datetime.strptime(data["date_exp"], "%Y-%m-%d")
            if date_fab >= date_exp:
                errors["date_fab"] = "Doit précéder la date d'expiration."
                errors["date_exp"] = "Doit suivre la date de fabrication."
        except ValueError:
            errors["date_fab"] = "Format AAAA-MM-JJ requis."
            errors["date_exp"] = "Format AAAA-MM-JJ requis."

        # Afficher les erreurs à côté des champs
        for champ, message in errors.items():
            widget = self.fields[champ]
            error_label = tk.Label(self.form_frame, text=message, fg="red", bg="#ffffff", font=("Arial", 8))
            error_label.grid(row=list(self.fields.keys()).index(champ), column=2, sticky="w", padx=5)
            widget.error_label = error_label

        # Si des erreurs existent, ne pas insérer dans la base
        if errors:
            return

        # Ajout dans la base de données
        self.curseur.execute('''
            INSERT INTO Medicament (Code_Article, Nom_Generique, Nom_Commercial, Forme_Pharmaceutique, Dosage,
            Prix_Unitaire, Date_Fab, Date_Exp, Emplacement, Seuil_Approv, Statut, Avec_Ordonnance)
            VALUES (:code_article, :nom_generique, :nom_commercial, :forme, :dosage, :prix_unitaire, :date_fab,
            :date_exp, :emplacement, :seuil, :statut, :ordonnance)
        ''', data)
        self.connexion.commit()
        self.load_table()
        messagebox.showinfo("Succès", "Médicament ajouté avec succès.")
       except sqlite3.Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'ajout : {e}")



    def modifier_medicament(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner un médicament à modifier.")
            return

        try:
            code_article = self.table.item(selected)["values"][0]
            data = {key: field.get() for key, field in self.fields.items()}
            data["ordonnance"] = 1 if data["ordonnance"] == "Oui" else 0

            self.curseur.execute('''
                UPDATE Medicament
                SET Nom_Generique = :nom_generique, Nom_Commercial = :nom_commercial, Forme_Pharmaceutique = :forme,
                Dosage = :dosage, Prix_Unitaire = :prix_unitaire, Date_Fab = :date_fab, Date_Exp = :date_exp,
                Emplacement = :emplacement, Seuil_Approv = :seuil, Statut = :statut, Avec_Ordonnance = :ordonnance
                WHERE Code_Article = :code_article
            ''', {**data, "code_article": code_article})
            self.connexion.commit()
            self.load_table()
            messagebox.showinfo("Succès", "Médicament modifié avec succès.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification : {e}")

    def supprimer_medicament(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner un médicament à supprimer.")
            return

        try:
            code_article = self.table.item(selected)["values"][0]
            self.curseur.execute("DELETE FROM Medicament WHERE Code_Article = ?", (code_article,))
            self.connexion.commit()
            self.load_table()
            messagebox.showinfo("Succès", "Médicament supprimé avec succès.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")

    def rechercher_medicament(self):
        query = self.fields["nom_commercial"].get()
        if not query:
            messagebox.showerror("Erreur", "Veuillez entrer un nom commercial pour la recherche.")
            return

        try:
            self.curseur.execute("SELECT * FROM Medicament WHERE Nom_Commercial = ?", (query,))
            rows = self.curseur.fetchall()
            for row in self.table.get_children():
                self.table.delete(row)
            for row in rows:
                display_row = list(row)
                display_row[-1] = "Oui" if display_row[-1] == 1 else "Non"
                self.table.insert("", "end", values=display_row)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")

    def reinitialiser_formulaire(self):
        for field in self.fields.values():
            if isinstance(field, (tk.Entry, ttk.Combobox)):
                field.delete(0, tk.END)
            elif isinstance(field, DateEntry):
                field.set_date("")

        self.load_table()

    def remplir_formulaire(self, event):
        selected = self.table.selection()
        if not selected:
            return
        item = self.table.item(selected)
        values = item["values"]
        for field, value in zip(self.fields.values(), values):
            if isinstance(field, tk.Entry):
                field.delete(0, tk.END)
                field.insert(0, value)
            elif isinstance(field, ttk.Combobox):
                field.set(value)
            elif isinstance(field, DateEntry):
                field.set_date(value)

    def show(self):
        if not self.frame_visible:
            self.create_widgets()
            self.frame_visible = True

    def hide(self):
        if self.frame_visible:
            self.main_frame.pack_forget()
            self.frame_visible = False