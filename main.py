import tkinter as tk
from formulaire_medicament import FormulaireMedicament
from formulaire_fournisseur import FormulaireFournisseur
from formulaire_Client import Formulaireclient
from formulaire_facture import FormulaireFacture
from formulaire_ligne_ventes import FormulaireLigneVentes

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Médicaments, Fournisseurs, Clients et Ventes")
        self.root.geometry("1200x600")

        # Couleurs
        self.sidebar_bg_color = "#2F4F4F"
        self.main_bg_color = "#F7F9F9"
        self.button_bg_color = "#5D6D72"
        self.entry_bg_color = "#FBFCFC"

        # Barre latérale
        self.sidebar = tk.Frame(root, width=200, bg=self.sidebar_bg_color)
        self.sidebar.pack(side="left", fill="y")

        # Boutons
        self.button_medecaments = tk.Button(
            self.sidebar,
            text="Gestion des Médicaments",
            command=self.show_medecaments,
            width=20,
            pady=10,
            bg=self.button_bg_color,
            fg="#FDFEFE",
        )
        self.button_medecaments.pack(pady=15)

        self.button_fournisseurs = tk.Button(
            self.sidebar,
            text="Gestion des Fournisseurs",
            command=self.show_fournisseurs,
            width=20,
            pady=10,
            bg=self.button_bg_color,
            fg="#FDFEFE",
        )
        self.button_fournisseurs.pack(pady=15)

        self.button_clients = tk.Button(
            self.sidebar,
            text="Gestion des Clients",
            command=self.show_clients,
            width=20,
            pady=10,
            bg=self.button_bg_color,
            fg="#FDFEFE",
        )
        self.button_clients.pack(pady=15)

        self.button_facture = tk.Button(
            self.sidebar,
            text="Gestion des Factures",
            command=self.show_facture,
            width=20,
            pady=10,
            bg=self.button_bg_color,
            fg="#FDFEFE",
        )
        self.button_facture.pack(pady=15)

        self.button_ligne_vente = tk.Button(
            self.sidebar,
            text="Gestion des Lignes de Vente",
            command=self.show_ligne_vente,
            width=20,
            pady=10,
            bg=self.button_bg_color,
            fg="#FDFEFE",
        )
        self.button_ligne_vente.pack(pady=15)

        # Main frame
        self.main_frame = tk.Frame(root, bg=self.main_bg_color)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Pages
        self.page_medecaments = FormulaireMedicament(
            self.main_frame, self.main_bg_color, self.button_bg_color, self.entry_bg_color
        )
        self.page_fournisseurs = FormulaireFournisseur(
            self.main_frame, self.main_bg_color, self.button_bg_color
        )
        self.page_clients = Formulaireclient(
            self.main_frame, self.main_bg_color, self.button_bg_color
        )
        self.page_facture = FormulaireFacture(
            self.main_frame, self.main_bg_color, self.button_bg_color
        )
        self.page_ligne_vente = FormulaireLigneVentes(
            self.main_frame, self.main_bg_color, self.button_bg_color
        )  # Nouvelle page pour les lignes de vente

        # Page par défaut
        self.show_medecaments()

    def show_medecaments(self):
        self.hide_all_pages()
        self.page_medecaments.show()

    def show_fournisseurs(self):
        self.hide_all_pages()
        self.page_fournisseurs.show()

    def show_clients(self):
        self.hide_all_pages()
        self.page_clients.show()

    def show_facture(self):
        self.hide_all_pages()
        self.page_facture.show()

    def show_ligne_vente(self):
        self.hide_all_pages()
        self.page_ligne_vente.show()  # Afficher la page des lignes de vente

    def hide_all_pages(self):
        self.page_medecaments.hide()
        self.page_fournisseurs.hide()
        self.page_clients.hide()
        self.page_facture.hide()
        self.page_ligne_vente.hide()  # Cacher la page des lignes de vente


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
