import tkinter as tk
from tkinter import ttk


class FormulaireFacture:
    def __init__(self, parent, bg_color, button_color):
        self.frame = tk.Frame(parent, bg=bg_color)
        self.bg_color = bg_color
        self.button_color = button_color

        # Nouvelle frame centrée
        self.center_frame = tk.Frame(self.frame, bg=bg_color)
        self.center_frame.pack(expand=True, fill="both")  # S'assure que la frame est visible et remplie

        # Section regroupant les champs
        section_frame = tk.LabelFrame(self.center_frame, text="Détails du Facture", bg=bg_color, font=("Arial", 10, "bold"))
        section_frame.pack(pady=10, padx=20, fill="x")

        # Rechercher Client par numéro d'inscription
        tk.Label(section_frame, text="Rechercher Client (Numéro d'Inscription) :", bg=bg_color).grid(row=0, column=0, pady=5, sticky="w")
        self.num_inscription_entry = tk.Entry(section_frame, width=30)
        self.num_inscription_entry.grid(row=0, column=1, pady=5)
        self.search_client_button = tk.Button(section_frame, text="Rechercher", bg=button_color, fg="#FFF", command=self.search_client)
        self.search_client_button.grid(row=0, column=2, pady=5, padx=5)

        # Champs générés automatiquement pour Nom, Prénom et Téléphone
        tk.Label(section_frame, text="Nom et Prénom :", bg=bg_color).grid(row=1, column=0, pady=5, sticky="w")
        self.nom_prenom_entry = tk.Entry(section_frame, width=50, state="readonly")
        self.nom_prenom_entry.grid(row=1, column=1, columnspan=2, pady=5)

        tk.Label(section_frame, text="Téléphone :", bg=bg_color).grid(row=2, column=0, pady=5, sticky="w")
        self.telephone_entry = tk.Entry(section_frame, width=30, state="readonly")
        self.telephone_entry.grid(row=2, column=1, columnspan=2, pady=5)

        # Rechercher Médicament
        tk.Label(section_frame, text="Rechercher Médicament (Code Article) :", bg=bg_color).grid(row=3, column=0, pady=5, sticky="w")
        self.med_entry = tk.Entry(section_frame, width=30)
        self.med_entry.grid(row=3, column=1, pady=5)
        self.search_med_button = tk.Button(section_frame, text="Rechercher", bg=button_color, fg="#FFF", command=self.search_med)
        self.search_med_button.grid(row=3, column=2, pady=5, padx=5)

        # Champs pour description, prix et quantité
        tk.Label(section_frame, text="Description :", bg=bg_color).grid(row=4, column=0, pady=5, sticky="w")
        self.med_desc = tk.Entry(section_frame, width=50, state="readonly")  # Non modifiable
        self.med_desc.grid(row=4, column=1, columnspan=2, pady=5)

        tk.Label(section_frame, text="Prix Unitaire :", bg=bg_color).grid(row=5, column=0, pady=5, sticky="w")
        self.med_price = tk.Entry(section_frame, width=20, state="readonly")  # Non modifiable
        self.med_price.grid(row=5, column=1, pady=5)

        tk.Label(section_frame, text="Quantité :", bg=bg_color).grid(row=6, column=0, pady=5, sticky="w")
        self.quantity_entry = tk.Entry(section_frame, width=20)
        self.quantity_entry.grid(row=6, column=1, pady=5)

        # Boutons centrés
        button_frame = tk.Frame(self.center_frame, bg=bg_color)
        button_frame.pack(pady=10)
        self.add_button = tk.Button(button_frame, text="Ajouter Ligne", bg=button_color, fg="#FFF", command=self.add_line, width=15)
        self.add_button.grid(row=0, column=0, padx=10)
        self.modify_button = tk.Button(button_frame, text="Modifier Ligne", bg=button_color, fg="#FFF", command=self.modify_line, width=15)
        self.modify_button.grid(row=0, column=1, padx=10)
        self.delete_button = tk.Button(button_frame, text="Supprimer Ligne", bg=button_color, fg="#FFF", command=self.delete_line, width=15)
        self.delete_button.grid(row=0, column=2, padx=10)


        # Tableau des lignes
        self.tree = ttk.Treeview(self.center_frame, columns=("desc", "qty", "unit_price", "total_price"), show="headings", height=10)
        self.tree.heading("desc", text="Description")
        self.tree.heading("qty", text="Quantité")
        self.tree.heading("unit_price", text="Prix Unitaire")
        self.tree.heading("total_price", text="Prix Total")
        self.tree.pack(pady=10, padx=20, fill="x")
        
        # Frame pour Total et Bouton Générer Facture
        total_and_button_frame = tk.Frame(self.center_frame, bg=bg_color)
        total_and_button_frame.pack(side="bottom", pady=3, padx=400,fill="x")  # Placer au bas de la fenêtre

        # Total général
        tk.Label(total_and_button_frame, text="Total Général :", bg=bg_color, font=("Arial", 12, "bold")).grid(row=0, column=0, pady=10, sticky="e")
        self.total_label = tk.Label(total_and_button_frame, text="0.00", bg=bg_color, font=("Arial", 12, "bold"))
        self.total_label.grid(row=0, column=1, pady=10, sticky="e")  # Aligner à droite

        # Bouton Générer Facture
        self.generate_button = tk.Button(total_and_button_frame, text="Générer Facture", bg=button_color, fg="#FFF", width=20)
        self.generate_button.grid(row=0, column=2, padx=10, sticky="e")  # Aligner à droite



    def show(self):
        """Affiche le formulaire."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Masque le formulaire."""
        self.frame.pack_forget()
        
    def search_med(self):
        pass

    def search_client(self):
        """Recherche un client par numéro d'inscription."""
        num_inscription = self.num_inscription_entry.get()
        database = {"12345": {"nom": "Dupont", "prenom": "Jean", "telephone": "0601020304"}}
        client = database.get(num_inscription)
        if client:
            full_name = f"{client['nom']} {client['prenom']}"
            self.nom_prenom_entry.config(state="normal")
            self.nom_prenom_entry.delete(0, tk.END)
            self.nom_prenom_entry.insert(0, full_name)
            self.nom_prenom_entry.config(state="readonly")

            self.telephone_entry.config(state="normal")
            self.telephone_entry.delete(0, tk.END)
            self.telephone_entry.insert(0, client["telephone"])
            self.telephone_entry.config(state="readonly")
        else:
            self.nom_prenom_entry.config(state="normal")
            self.nom_prenom_entry.delete(0, tk.END)
            self.nom_prenom_entry.insert(0, "Non trouvé")
            self.nom_prenom_entry.config(state="readonly")
            self.telephone_entry.config(state="normal")
            self.telephone_entry.delete(0, tk.END)
            self.telephone_entry.insert(0, "Non trouvé")
            self.telephone_entry.config(state="readonly")

    def add_line(self):
        pass

    def modify_line(self):
        pass

    def delete_line(self):
        pass
