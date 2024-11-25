import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from docxtpl import DocxTemplate
from datetime import datetime


class FormulaireFacture:
    def __init__(self, parent, bg_color="#F5F5F5", button_color="#007BFF"):
        self.frame = tk.Frame(parent, bg=bg_color)
        self.bg_color = bg_color
        self.button_color = button_color

        # Nouvelle frame centrée
        self.center_frame = tk.Frame(self.frame, bg=bg_color)
        self.center_frame.pack(expand=True, fill="both")

        # Section regroupant les champs
        section_frame = tk.LabelFrame(
            self.center_frame, text="Détails du Facture", bg=bg_color, font=("Arial", 10, "bold")
        )
        section_frame.pack(pady=10, padx=20, fill="x")

        # Rechercher Client par numéro d'inscription
        tk.Label(
            section_frame, text="Rechercher Client (Numéro d'Inscription) :", bg=bg_color
        ).grid(row=0, column=0, pady=5, sticky="w")
        self.num_inscription_entry = tk.Entry(section_frame, width=30)
        self.num_inscription_entry.grid(row=0, column=1, pady=5)
        self.search_client_button = tk.Button(
            section_frame, text="Rechercher", bg=button_color, fg="#FFF", command=self.search_client
        )
        self.search_client_button.grid(row=0, column=2, pady=5, padx=5)

        # Champs générés automatiquement pour Nom, Prénom et Téléphone
        tk.Label(section_frame, text="Nom et Prénom :", bg=bg_color).grid(row=1, column=0, pady=5, sticky="w")
        self.nom_prenom_entry = tk.Entry(section_frame, width=50, state="readonly")
        self.nom_prenom_entry.grid(row=1, column=1, columnspan=2, pady=5)

        tk.Label(section_frame, text="Téléphone :", bg=bg_color).grid(row=2, column=0, pady=5, sticky="w")
        self.telephone_entry = tk.Entry(section_frame, width=30, state="readonly")
        self.telephone_entry.grid(row=2, column=1, columnspan=2, pady=5)

        # Rechercher Médicament
        tk.Label(
            section_frame, text="Rechercher Médicament (Code Article) :", bg=bg_color
        ).grid(row=3, column=0, pady=5, sticky="w")
        self.med_entry = tk.Entry(section_frame, width=30)
        self.med_entry.grid(row=3, column=1, pady=5)
        self.search_med_button = tk.Button(
            section_frame, text="Rechercher", bg=button_color, fg="#FFF", command=self.search_med
        )
        self.search_med_button.grid(row=3, column=2, pady=5, padx=5)

        # Champs pour description, prix et quantité
        tk.Label(section_frame, text="Description :", bg=bg_color).grid(row=4, column=0, pady=5, sticky="w")
        self.med_desc = tk.Entry(section_frame, width=50, state="readonly")
        self.med_desc.grid(row=4, column=1, columnspan=2, pady=5)

        tk.Label(section_frame, text="Prix Unitaire :", bg=bg_color).grid(row=5, column=0, pady=5, sticky="w")
        self.med_price = tk.Entry(section_frame, width=20, state="readonly")
        self.med_price.grid(row=5, column=1, pady=5)

        tk.Label(section_frame, text="Quantité :", bg=bg_color).grid(row=6, column=0, pady=5, sticky="w")
        self.quantity_entry = tk.Entry(section_frame, width=20)
        self.quantity_entry.grid(row=6, column=1, pady=5)

        # Boutons centrés
        button_frame = tk.Frame(self.center_frame, bg=bg_color)
        button_frame.pack(pady=10)
        self.add_button = tk.Button(
            button_frame, text="Ajouter Ligne", bg=button_color, fg="#FFF", command=self.add_line, width=15
        )
        self.add_button.grid(row=0, column=0, padx=10)
        self.modify_button = tk.Button(
            button_frame, text="Modifier Ligne", bg=button_color, fg="#FFF", command=self.modify_line, width=15
        )
        self.modify_button.grid(row=0, column=1, padx=10)
        self.delete_button = tk.Button(
            button_frame, text="Supprimer Ligne", bg=button_color, fg="#FFF", command=self.delete_line, width=15
        )
        self.delete_button.grid(row=0, column=2, padx=10)

        # Tableau des lignes
        self.tree = ttk.Treeview(
            self.center_frame, columns=("code","desc", "qty", "unit_price", "total_price"), show="headings", height=10
        )
        self.tree.heading("code", text="Code Article")
        self.tree.heading("desc", text="Description")
        self.tree.heading("qty", text="Quantité")
        self.tree.heading("unit_price", text="Prix Unitaire")
        self.tree.heading("total_price", text="Prix Total")
        
        self.tree.pack(pady=10, padx=20, fill="x")
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

        # Frame pour Total et Bouton Générer Facture
        total_and_button_frame = tk.Frame(self.center_frame, bg=bg_color)
        total_and_button_frame.pack(side="bottom", pady=3, padx=400, fill="x")  # Placer au bas de la fenêtre

        # Total général
        tk.Label(total_and_button_frame, text="Total Général :", bg=bg_color, font=("Arial", 12, "bold")).grid(row=0, column=0, pady=10, sticky="e")
        self.total_label = tk.Label(total_and_button_frame, text="0.00", bg=bg_color, font=("Arial", 12, "bold"))
        self.total_label.grid(row=0, column=1, pady=10, sticky="e")  # Aligner à droite

        # Bouton Générer Facture
        self.generate_button = tk.Button(total_and_button_frame, text="Générer Facture", bg=button_color, fg="#FFF",command=self.generate_invoice, width=20)
        self.generate_button.grid(row=0, column=2, padx=10, sticky="e")  # Aligner à droite

    def search_client(self):
        """Recherche un client par son numéro d'inscription."""
        num_inscription = self.num_inscription_entry.get().strip()

        if not num_inscription:
            messagebox.showerror("Erreur", "Veuillez entrer un numéro d'inscription.")
            return

        try:
            connexion = sqlite3.connect("DB_Pharmacy.db")
            curseur = connexion.cursor()

            curseur.execute("SELECT Nom_C, Prenom_C, Telephone_C FROM Client WHERE id_C = ?", (num_inscription,))
            result = curseur.fetchone()

            if result:
                nom, prenom, telephone = result
                full_name = f"{prenom} {nom}"
                self.nom_prenom_entry.config(state="normal")
                self.nom_prenom_entry.delete(0, tk.END)
                self.nom_prenom_entry.insert(0, full_name)
                self.nom_prenom_entry.config(state="readonly")

                self.telephone_entry.config(state="normal")
                self.telephone_entry.delete(0, tk.END)
                self.telephone_entry.insert(0, telephone)
                self.telephone_entry.config(state="readonly")
            else:
                messagebox.showerror("Erreur", "Client introuvable.")

        except sqlite3.Error as e:
            messagebox.showerror("Erreur Base de Données", f"Une erreur est survenue : {e}")
        finally:
            if 'connexion' in locals():
                connexion.close()

    def search_med(self):
        """Recherche un médicament par son code article."""
        code_article = self.med_entry.get().strip()

        if not code_article:
            messagebox.showerror("Erreur", "Veuillez entrer un code article.")
            return

        try:
            conn = sqlite3.connect("DB_Pharmacy.db")
            cursor = conn.cursor()

            cursor.execute(
                "SELECT Nom_Commercial || ' ' || Dosage || ' ' || Forme_Pharmaceutique, Prix_Unitaire "
                "FROM Medicament WHERE LOWER(Code_Article) = LOWER(?)", (code_article,)
            )
            result = cursor.fetchone()

            if result:
                self.med_desc.config(state="normal")
                self.med_desc.delete(0, tk.END)
                self.med_desc.insert(0, result[0])
                self.med_desc.config(state="readonly")

                self.med_price.config(state="normal")
                self.med_price.delete(0, tk.END)
                self.med_price.insert(0, result[1])
                self.med_price.config(state="readonly")
            else:
                messagebox.showerror("Erreur", "Médicament introuvable.")

        except sqlite3.Error as e:
            messagebox.showerror("Erreur Base de Données", f"Une erreur est survenue : {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    def validate_quantity(self):
        """Valide la quantité saisie par l'utilisateur."""
        try:
            qty = int(self.quantity_entry.get())
            if qty <= 0:
                raise ValueError("Quantité doit être supérieure à 0.")
            return qty
        except ValueError:
            messagebox.showerror("Erreur", "Quantité invalide. Veuillez entrer un entier positif.")
            return None

    def add_line(self):
     """Ajoute une ligne au tableau en vérifiant si le code article existe déjà."""
     code = self.med_entry.get().strip()
     description = self.med_desc.get().strip()
     prix_unitaire = self.med_price.get().strip()
     quantite = self.quantity_entry.get().strip()
  
     if not (code and description and prix_unitaire and quantite):
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return
     try:
        quantite = int(quantite)
        if quantite <= 0:
            messagebox.showerror("Erreur", "La quantité doit être un entier positif.")
            return
     except ValueError:
        messagebox.showerror("Erreur", "La quantité doit être un entier positif.")
        return
     # Vérifier si le code article existe déjà dans le tableau
     for item in self.tree.get_children():
        existing_values = self.tree.item(item, "values")
        if existing_values[0] == code:
            messagebox.showerror("Erreur", "Ce code article existe déjà dans la liste.")
            return

     try:
        quantite = int(quantite)
        prix_unitaire = float(prix_unitaire)
        total_price = quantite * prix_unitaire

        # Ajouter la ligne si le code n'existe pas
        self.tree.insert("", "end", values=(code, description, quantite, prix_unitaire, total_price))
        self.clear_fields()
        self.update_total()

     except ValueError:
        messagebox.showerror("Erreur", "eereur d 'ajout.")



    def modify_line(self):
     """Modifie une ligne sélectionnée dans le tableau."""
     selected_item = self.tree.selection()
     if not selected_item:
        messagebox.showerror("Erreur", "Aucune ligne sélectionnée pour modification.")
        return

     code = self.med_entry.get().strip()
     description = self.med_desc.get().strip()
     unit_price = self.med_price.get().strip()
     quantity = self.quantity_entry.get().strip()

     if not (code and description and unit_price and quantity):
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs avant de modifier une ligne.")
        return

     try:
        unit_price = float(unit_price)
        quantity = int(quantity)
        total_price = unit_price * quantity

        # Mise à jour des valeurs dans la ligne sélectionnée
        self.tree.item(selected_item, values=(code, description, quantity, unit_price, total_price))
        self.clear_fields()
        self.update_total()
     except ValueError:
        messagebox.showerror("Erreur", "Prix ou quantité non valide.")


    def delete_line(self):
        """Supprime une ligne sélectionnée dans le tableau."""
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("Erreur", "Aucune ligne sélectionnée pour suppression.")
            return

        self.tree.delete(selected_item)
        
    def on_item_select(self, event):
        """Handle item selection in the Treeview."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        values = self.tree.item(selected_item, "values")
        self.med_entry.delete(0, tk.END)
        self.med_entry.insert(0, values[0])  # code
        self.search_med()


        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, values[2])
    def clear_fields(self):
        """Efface tous les champs du formulaire."""
        self.med_entry.delete(0, tk.END)
        self.med_desc.config(state="normal")
        self.med_desc.delete(0, tk.END)
        self.med_desc.config(state="readonly")

        self.med_price.config(state="normal")
        self.med_price.delete(0, tk.END)
        self.med_price.config(state="readonly")

        self.quantity_entry.delete(0, tk.END)
    def update_total(self):
      """Met à jour le total général en fonction des lignes dans le tableau."""
      total_general = 0.0
      for item in self.tree.get_children():
        total_price = float(self.tree.item(item, "values")[4])  # Index 4 correspond au prix total
        total_general += total_price
        self.total_label.config(text=f"{total_general:.2f}")


    def generate_invoice(self):
      """Génère une facture en utilisant un modèle Word."""
      # Enregistrer les ventes dans la base de données avant la génération
      if not self.save_sales_to_db():
        return  # Arrêter si l'enregistrement des ventes échoue
      # Vérifier si le tableau contient des articles
      if not self.tree.get_children():
         messagebox.showerror("Erreur", "Aucun article ajouté pour générer une facture.")
         return

     # Récupérer les informations du client
      client_name = self.nom_prenom_entry.get().strip()
      client_telephone = self.telephone_entry.get().strip()

      if not (client_name and client_telephone):
         messagebox.showerror("Erreur", "Veuillez rechercher un client avant de générer une facture.")
         return

     # Préparer les données pour le modèle Word
      items = []
      for item in self.tree.get_children():
         code, description, quantity, unit_price, total_price = self.tree.item(item, "values")
         items.append({
            "description": description,
            "quantity": int(quantity),
            "unit_price": float(unit_price),
            "total_price": float(total_price),
         })

      total_amount = sum(item["total_price"] for item in items)

      data = {
        "client_name": client_name,
        "client_telephone": client_telephone,
        "items": items,
        "total_amount": f"{total_amount:.2f}",
      }

     # Charger et remplir le modèle Word
      try:
         template = DocxTemplate("facture_template_3.docx")  # Remplacez par le chemin de votre modèle
         template.render(data)
         file_name = f"facture_{client_name.replace(' ', '_')}.docx"
         template.save(file_name)

         messagebox.showinfo("Succès", f"Facture générée avec succès : {file_name}")
      except Exception as e:
         messagebox.showerror("Erreur", f"Une erreur est survenue lors de la génération de la facture : {e}")
         
        
    def save_sales_to_db(self):
     """Enregistre les lignes de vente dans la table Vente."""
     # Vérifier si le tableau contient des articles
     if not self.tree.get_children():
         messagebox.showerror("Erreur", "Aucun article à enregistrer dans la base de données.")
         return False

     # Récupérer la date actuelle
     current_date = datetime.now().strftime("%Y-%m-%d")

     try:
         connexion = sqlite3.connect("DB_Pharmacy.db")
         curseur = connexion.cursor()

         # Parcourir les lignes du tableau
         for item in self.tree.get_children():
             code, _, quantity, _, _ = self.tree.item(item, "values")

             # Insérer dans la table Vente
             curseur.execute(
                '''
                INSERT INTO Vente (Code_Article, Quantite_Vendue, Date_Vente)
                VALUES (?, ?, ?)
                ''',
                (code, int(quantity), current_date)
             )

         # Valider les changements
         connexion.commit()
         connexion.close()
         return True

     except sqlite3.Error as e:
        messagebox.showerror("Erreur Base de Données", f"Une erreur est survenue : {e}")
        return False
    def hide(self):
        """Masque le frame principal."""
        self.frame.pack_forget()

    def show(self):
        """Affiche le frame principal."""
        self.frame.pack(expand=True, fill="both")
    
