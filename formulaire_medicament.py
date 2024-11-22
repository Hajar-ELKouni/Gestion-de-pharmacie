import tkinter as tk
from tkinter import ttk

class FormulaireMedicament:
    def __init__(self, parent, bg_color, button_color, entry_bg_color):
        self.frame = tk.Frame(parent, bg=bg_color)
        self.frame.pack(fill="both", expand=True)

        self.bg_color = bg_color
        self.button_color = button_color
        self.entry_bg_color = entry_bg_color

        # Cadre des champs de saisie
        self.frame_form = tk.Frame(self.frame, bg=bg_color)
        self.frame_form.pack(pady=10, padx=20, fill="x")

        # Champs de saisie
        self.entry_code = self.create_input_field(self.frame_form, "Code de l'article :", 0, 0)
        self.entry_nom_generique = self.create_input_field(self.frame_form, "Nom générique :", 1, 0)
        self.entry_nom_commercial = self.create_input_field(self.frame_form, "Nom commercial :", 1, 1)

        formes_pharmaceutiques = ["Comprimé", "Solution", "Injection", "Pommade"]
        self.combobox_forme_pharmaceutique = self.create_input_field(
            self.frame_form, "Forme pharmaceutique :", 2, 0, "combobox", formes_pharmaceutiques
        )
        self.entry_dosage = self.create_input_field(self.frame_form, "Dosage :", 2, 1)

        conditionnements = ["Boîte de 10", "Flacon", "Pack de 30"]
        self.combobox_conditionnement = self.create_input_field(
            self.frame_form, "Conditionnement :", 3, 0, "combobox", conditionnements
        )
        self.entry_prix_unitaire = self.create_input_field(self.frame_form, "Prix unitaire :", 3, 1)

        # Ajouter des boutons d'action
        self.frame_buttons = tk.Frame(self.frame, bg=bg_color)
        self.frame_buttons.pack(pady=10)

        self.button_ajouter = tk.Button(
            self.frame_buttons, text="Ajouter", command=self.ajouter, bg=button_color, fg="#FFFFFF", width=10
        )
        self.button_ajouter.grid(row=0, column=0, padx=10)

        # Tableau (Treeview)
        self.frame_table = tk.Frame(self.frame, bg=bg_color)
        self.frame_table.pack(pady=20, padx=20, fill="both", expand=True)

        self.table = ttk.Treeview(
            self.frame_table,
            columns=("code", "nom_generique", "nom_commercial", "forme", "dosage", "prix"),
            show="headings",
        )
        self.table.heading("code", text="Code")
        self.table.heading("nom_generique", text="Nom Générique")
        self.table.heading("nom_commercial", text="Nom Commercial")
        self.table.heading("forme", text="Forme")
        self.table.heading("dosage", text="Dosage")
        self.table.heading("prix", text="Prix Unitaire")
        self.table.pack(fill="both", expand=True)

    def create_input_field(self, frame, label_text, row, col, widget_type="entry", options=None):
        label = tk.Label(frame, text=label_text, bg=self.bg_color, font=("Arial", 10))
        label.grid(row=row, column=col * 2, pady=5, padx=5, sticky="w")
        if widget_type == "entry":
            entry = tk.Entry(frame, bg=self.entry_bg_color)
            entry.grid(row=row, column=col * 2 + 1, pady=5, padx=5)
            return entry
        elif widget_type == "combobox" and options:
            combobox = ttk.Combobox(frame, values=options)
            combobox.grid(row=row, column=col * 2 + 1, pady=5, padx=5)
            return combobox

    def ajouter(self):
        pass

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()
