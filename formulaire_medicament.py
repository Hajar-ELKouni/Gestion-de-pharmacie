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

        # Organisation des champs en sections
        self.frame_info_generale = tk.LabelFrame(self.frame, text="Informations Générales", bg=bg_color, fg="black")
        self.frame_info_generale.pack(fill="x", padx=10, pady=5)

        self.frame_details = tk.LabelFrame(self.frame, text="Détails Pharmaceutiques", bg=bg_color, fg="black")
        self.frame_details.pack(fill="x", padx=10, pady=5)

        self.frame_dates = tk.LabelFrame(self.frame, text="Dates et Emplacement", bg=bg_color, fg="black")
        self.frame_dates.pack(fill="x", padx=10, pady=5)

        # Champs dans la section "Informations Générales"
        self.entry_code = self.create_input_field(self.frame_info_generale, "Code Article :", 0, 0)
        self.entry_nom_generique = self.create_input_field(self.frame_info_generale, "Nom Générique :", 0, 1)
        self.entry_nom_commercial = self.create_input_field(self.frame_info_generale, "Nom Commercial :", 1, 0)

        # Champs dans la section "Détails Pharmaceutiques"
        formes = ["Comprimé", "Solution", "Injection", "Pommade"]
        self.combobox_forme = self.create_input_field(self.frame_details, "Forme Pharmaceutique :", 0, 0, "combobox", formes)
        self.entry_dosage = self.create_input_field(self.frame_details, "Dosage :", 0, 1)
        self.entry_prix = self.create_input_field(self.frame_details, "Prix Unitaire :", 1, 0)
        self.entry_seuil = self.create_input_field(self.frame_details, "Seuil d'Approvisionnement :", 1, 1)

        # Champs dans la section "Dates et Emplacement"
        self.date_fab = self.create_input_field(self.frame_dates, "Date de Fabrication :", 0, 0, "date")
        self.date_exp = self.create_input_field(self.frame_dates, "Date d'Expiration :", 0, 1, "date")
        self.entry_emplacement = self.create_input_field(self.frame_dates, "Emplacement :", 1, 0)

        self.combobox_fournisseur = self.create_input_field(self.frame_dates, "Fournisseur :", 1, 1, "combobox")
        self.load_fournisseurs()

        # Label global pour les erreurs
        self.error_label = tk.Label(self.frame, text="", fg="red", bg=bg_color, wraplength=400, justify="left")
        self.error_label.pack(pady=5)

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
        errors = []

        if not self.entry_code.get():
            errors.append("Le code article est obligatoire.")
        if not self.entry_nom_generique.get():
            errors.append("Le nom générique est obligatoire.")
        if not self.entry_nom_commercial.get():
            errors.append("Le nom commercial est obligatoire.")

        try:
            float(self.entry_prix.get())
        except ValueError:
            errors.append("Le prix doit être un nombre valide.")

        try:
            int(self.entry_seuil.get())
        except ValueError:
            errors.append("Le seuil doit être un nombre entier.")

        try:
            date_fab = self.date_fab.get_date()
            date_exp = self.date_exp.get_date()
            if date_exp <= date_fab:
                errors.append("La date d'expiration doit être après la date de fabrication.")
        except Exception:
            errors.append("Erreur dans les dates.")

        if errors:
            self.error_label.config(text="\n".join(errors))
            return

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
            """, (code, nom_generique, nom_commercial, forme, dosage, float(self.entry_prix.get()), date_fab, date_exp,
                  emplacement, int(self.entry_seuil.get()), "Disponible", 0))

            connexion.commit()
            messagebox.showinfo("Succès", "Médicament ajouté avec succès !")
            self.load_table()

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
    def show(self):
        """Affiche le formulaire."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Cache le formulaire."""
        self.frame.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestion des Médicaments")
    app = FormulaireMedicament(root, bg_color="#F5F5F5", button_color="#4CAF50", entry_bg_color="#FFFFFF")
    root.mainloop()
