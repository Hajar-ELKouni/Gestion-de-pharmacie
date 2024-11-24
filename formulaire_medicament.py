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
        self.frame_visible = False  # Indique si l'interface est affichée

        # Connexion à la base de données
        self.connexion = sqlite3.connect("DB_Pharmacy.db")
        self.curseur = self.connexion.cursor()

        # Frame principale
        self.main_frame = None

    def create_widgets(self):
        if self.main_frame is None:
            # Frame principale
            self.main_frame = tk.Frame(self.parent, bg=self.bg_color)
            self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Section formulaire
            self.form_frame = tk.LabelFrame(self.main_frame, text="Formulaire Médicament", bg="#ffffff", fg="black", padx=10, pady=10)
            self.form_frame.pack(side="top", fill="x", pady=5)

            # Champs de formulaire
            self.fields = {}
            self.add_form_field("Code Article :", "code_article", 0, "entry")
            self.add_form_field("Nom Générique :", "nom_generique", 1, "entry")
            self.add_form_field("Nom Commercial :", "nom_commercial", 2, "entry")
            self.add_form_field("Forme Pharmaceutique :", "forme", 3, "combobox", ["Comprimé", "Solution", "Injection", "Pommade"])
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

            self.btn_ajouter = tk.Button(self.buttons_frame, text="Ajouter", command=self.ajouter_medicament, bg=self.button_color, fg="white")
            self.btn_ajouter.pack(side="left", padx=5)

            self.btn_modifier = tk.Button(self.buttons_frame, text="Modifier", command=self.modifier_medicament, bg=self.button_color, fg="white")
            self.btn_modifier.pack(side="left", padx=5)

            self.btn_supprimer = tk.Button(self.buttons_frame, text="Supprimer", command=self.supprimer_medicament, bg=self.button_color, fg="white")
            self.btn_supprimer.pack(side="left", padx=5)

            # Tableau des médicaments avec scrollbar
            self.table_frame = tk.Frame(self.main_frame, bg=self.bg_color)
            self.table_frame.pack(fill="both", expand=True, pady=10)

            self.table = ttk.Treeview(
                self.table_frame,
                columns=("Code_Article", "Nom_Generique", "Nom_Commercial", "Forme_Pharmaceutique", "Dosage",
                         "Prix_Unitaire", "Date_Fab", "Date_Exp", "Emplacement", "Seuil_Approv", "Statut", "Avec_Ordonnance"),
                show="headings",
                height=15  # Nombre de lignes affichées par défaut
            )

            # Configuration des colonnes
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

            # Charger les données
            self.load_table()

    def add_form_field(self, label, field, row, widget_type, options=None):
        label = tk.Label(self.form_frame, text=label, bg="#ffffff")
        label.grid(row=row, column=0, sticky="w", pady=5)

        if widget_type == "entry":
            entry = tk.Entry(self.form_frame, bg=self.entry_color)
            entry.grid(row=row, column=1, pady=5, sticky="ew")
            self.fields[field] = entry
        elif widget_type == "combobox":
            combobox = ttk.Combobox(self.form_frame, values=options or [], state="readonly", style="TCombobox")
            combobox.grid(row=row, column=1, pady=5, sticky="ew")
            self.fields[field] = combobox
        elif widget_type == "date":
            date_entry = DateEntry(self.form_frame, background="darkblue", foreground="white", date_pattern="yyyy-MM-dd")
            date_entry.grid(row=row, column=1, pady=5, sticky="ew")
            self.fields[field] = date_entry

    def load_table(self):
        for row in self.table.get_children():
            self.table.delete(row)
        try:
            self.curseur.execute("SELECT * FROM Medicament")
            rows = self.curseur.fetchall()
            for row in rows:
                # Conversion des données pour affichage
                display_row = list(row)
                display_row[-1] = "Oui" if display_row[-1] == 1 else "Non"  # Convertir Avec_Ordonnance en texte
                self.table.insert("", "end", values=display_row)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données : {e}")

    def ajouter_medicament(self):
        try:
            data = {key: field.get() for key, field in self.fields.items()}
            data["ordonnance"] = 1 if data["ordonnance"] == "Oui" else 0

            self.curseur.execute('''
                INSERT INTO Medicament (Code_Article, Nom_Generique, Nom_Commercial, Forme_Pharmaceutique, Dosage, Prix_Unitaire, Date_Fab, Date_Exp, Emplacement, Seuil_Approv, Statut, Avec_Ordonnance)
                VALUES (:code_article, :nom_generique, :nom_commercial, :forme, :dosage, :prix_unitaire, :date_fab, :date_exp, :emplacement, :seuil, :statut, :ordonnance)
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
            code_article = self.table.item(selected)["values"][0]  # Récupérer le code article sélectionné

            data = {key: field.get() for key, field in self.fields.items()}
            data["ordonnance"] = 1 if data["ordonnance"] == "Oui" else 0

            self.curseur.execute('''
                UPDATE Medicament
                SET Nom_Generique = :nom_generique, Nom_Commercial = :nom_commercial, Forme_Pharmaceutique = :forme, Dosage = :dosage,
                    Prix_Unitaire = :prix_unitaire, Date_Fab = :date_fab, Date_Exp = :date_exp, Emplacement = :emplacement, 
                    Seuil_Approv = :seuil, Statut = :statut, Avec_Ordonnance = :ordonnance
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
            self.curseur.execute("DELETE FROM Medicament WHERE Code_Article=?", (code_article,))
            self.connexion.commit()
            self.load_table()
            messagebox.showinfo("Succès", "Médicament supprimé avec succès.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")

    def remplir_formulaire(self, event):
        selected = self.table.selection()
        if not selected:
            return
        item = self.table.item(selected)
        values = item["values"]
        for field, value in zip(self.fields.values(), values):
            field.delete(0, tk.END)
            field.insert(0, value)

    def show(self):
        if not self.frame_visible:
            self.create_widgets()
            self.main_frame.pack(fill="both", expand=True)
            self.frame_visible = True

    def hide(self):
        if self.frame_visible:
            self.main_frame.pack_forget()
            self.frame_visible = False
