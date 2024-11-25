import tkinter as tk
from tkinter import ttk
import sqlite3

class FormulaireLigneVentes:
    def __init__(self, parent_frame, bg_color, button_color):
        self.parent_frame = parent_frame
        self.bg_color = bg_color
        self.button_color = button_color
        
        # Création du cadre principal
        self.frame = tk.Frame(self.parent_frame, bg=self.bg_color)
        
        # Titre
        self.title_label = tk.Label(
            self.frame, text="Ventes par Client", bg=bg_color, font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=10)

        # Champ de recherche par ID Client
        self.search_frame = tk.Frame(self.frame, bg=bg_color)
        self.search_frame.pack(pady=10)

        tk.Label(self.search_frame, text="ID Client:", bg=bg_color).grid(row=0, column=0, padx=5, pady=5)
        self.entry_id_client = tk.Entry(self.search_frame)
        self.entry_id_client.grid(row=0, column=1, padx=5, pady=5)

        # Bouton de recherche
        self.search_button = tk.Button(
            self.search_frame,
            text="Rechercher Ventes",
            bg=button_color,
            fg="white",
            command=self.search_ventes,
        )
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        # Bouton pour afficher toutes les ventes
        self.show_all_button = tk.Button(
            self.frame,
            text="Afficher Toutes les Ventes",
            bg=button_color,
            fg="white",
            command=self.show_all_ventes,
        )
        self.show_all_button.pack(pady=10)

        # Tableau des ventes
        self.table_frame = tk.Frame(self.frame, bg=bg_color)
        self.table_frame.pack(pady=10)

        self.scrollbar_y = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.scrollbar_x = ttk.Scrollbar(self.table_frame, orient="horizontal")

        self.table = ttk.Treeview(
            self.table_frame,
            columns=("id_vente", "id_article", "id_client", "nom_complet", "date_vente", "quantite_vendue", "prix_total"),
            show="headings",
            yscrollcommand=self.scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set,
        )
        self.scrollbar_y.config(command=self.table.yview)
        self.scrollbar_x.config(command=self.table.xview)

        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.table.pack(fill="both", expand=True)

        # Configuration des colonnes
        self.table.heading("id_vente", text="ID Vente")
        self.table.heading("id_article", text="ID Article")
        self.table.heading("id_client", text="ID Client")
        self.table.heading("nom_complet", text="Nom Complet")
        self.table.heading("date_vente", text="Date Vente")
        self.table.heading("quantite_vendue", text="Quantité Vendue")
        self.table.heading("prix_total", text="Prix Total")

        # Agrandir les colonnes pour une meilleure lisibilité
        self.table.column("id_vente", width=100)
        self.table.column("id_article", width=120)
        self.table.column("id_client", width=120)
        self.table.column("nom_complet", width=200)
        self.table.column("date_vente", width=150)
        self.table.column("quantite_vendue", width=120)
        self.table.column("prix_total", width=150)

    def search_ventes(self):
        """Rechercher les ventes par ID Client et afficher dans le tableau."""
        id_client = self.entry_id_client.get()

        if not id_client:
            print("Veuillez entrer un ID client.")
            return

        try:
            connexion = sqlite3.connect("DB_Pharmacy.db")
            curseur = connexion.cursor()

            # Sélectionner les ventes du client spécifié
            rows = curseur.execute(
                '''
                SELECT v.id_Vente, v.Code_Article, v.id_C AS id_client, c.Prenom_C || ' ' || c.Nom_C AS nom_complet, v.Date_Vente, v.Quantite_Vendue, NULL AS prix_total
                FROM Vente v
                JOIN Client c ON v.id_C = c.id_C
                WHERE v.id_C = ?
                ''', (id_client,)
            ).fetchall()

            connexion.close()

            # Effacer les anciennes données du tableau
            for row in self.table.get_children():
                self.table.delete(row)

            # Charger les nouvelles données dans le tableau
            for row in rows:
                self.table.insert("", "end", values=row)

        except sqlite3.Error as e:
            print("Erreur lors de la recherche des ventes :", e)

    def show_all_ventes(self):
        """Afficher toutes les ventes de tous les clients."""
        try:
            connexion = sqlite3.connect("DB_Pharmacy.db")
            curseur = connexion.cursor()

            # Sélectionner toutes les ventes
            rows = curseur.execute(
                '''
                SELECT v.id_Vente, v.Code_Article, v.id_C AS id_client, c.Prenom_C || ' ' || c.Nom_C AS nom_complet, v.Date_Vente, v.Quantite_Vendue, NULL AS prix_total
                FROM Vente v
                JOIN Client c ON v.id_C = c.id_C
                ''').fetchall()

            connexion.close()

            # Effacer les anciennes données du tableau
            for row in self.table.get_children():
                self.table.delete(row)

            # Charger les nouvelles données dans le tableau
            for row in rows:
                self.table.insert("", "end", values=row)

        except sqlite3.Error as e:
            print("Erreur lors de la récupération des ventes :", e)

    def show(self):
        """Afficher le formulaire."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Cacher le formulaire."""
        self.frame.pack_forget()
