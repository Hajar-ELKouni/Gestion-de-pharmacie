import tkinter as tk
from tkinter import ttk
from docxtpl import DocxTemplate

# Données pour la facture
data = {
    "client_name": "Jean Dupont",  # Nom du client
    "client_telephone": "06 17 72 76 38",  # Téléphone du client
    "items": [  # Liste des médicaments
        {"description": "Paracétamol 500mg", "quantity": 2, "unit_price": 3.50, "total_price": 7.00},
        {"description": "Ibuprofène 400mg", "quantity": 1, "unit_price": 5.00, "total_price": 5.00},
    ],
}

# Calculer le montant total TTC
total_amount = sum(item["total_price"] for item in data["items"])
data["total_amount"] = f"{total_amount:.2f}"  # Format to 2 decimal places (e.g., 12.34)

# Charger le modèle Word
template = DocxTemplate("facture_template_3.docx")  # Utilisez votre fichier modèle
template.render(data)  # Remplir les champs dynamiques avec les données
template.save("facture_finale.docx")  # Enregistrer la facture générée

print("Facture générée avec succès avec Montant Total TTC!")

