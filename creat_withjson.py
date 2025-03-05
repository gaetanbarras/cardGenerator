import os
import sys
import json
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors


def load_template(json_path):
    """Charge le template depuis le fichier JSON."""
    with open(json_path, 'r') as f:
        template = json.load(f)
    return template


def draw_template(c, template, data):
    """
    Parcourt les éléments du template (ici, uniquement le groupe 'Text')
    et écrit sur le PDF les valeurs correspondantes.
    Le JSON doit contenir des objets avec des propriétés comme :
      - type (doit être "text")
      - name (nom de la zone, qui servira d'index pour récupérer la donnée)
      - x, y, width, height
      - size (taille de police)
      - color (code couleur, par exemple "#ffffff")
    """
    # On suppose que le template contient une clé "data" avec une structure
    # similaire à celle du fichier fourni.
    # Nous parcourons les enfants du groupe nommé "Text".
    groups = template.get("data", {}).get("children", [])
    for group in groups:
        if group.get("type") == "group" and group.get("name") == "Text":
            for element in group.get("children", []):
                if element.get("type") == "text":
                    # On récupère la valeur à afficher :
                    # soit on prend le texte déjà défini dans le template,
                    # soit on tente de récupérer la donnée via le nom de l'élément
                    text = element.get("text", "")
                    key = element.get("name", "")
                    if not text and key in data:
                        text = data.get(key, "")
                    # Récupération des coordonnées et de la taille
                    x = element.get("x", 0)
                    y = element.get("y", 0)
                    size = element.get("size", 12)
                    color_hex = element.get("color", "#000000")

                    # Configurer la police et la couleur
                    c.setFont("Helvetica", size)
                    c.setFillColor(colors.HexColor(color_hex))
                    # Pour simplifier, on affiche le texte tel quel.
                    # Vous pouvez adapter (centrer, etc.) en fonction des besoins.
                    c.drawString(x, y, text)


def create_card_using_template(data, output_pdf, template):
    """
    Crée un PDF en se basant sur le template JSON.
    Pour cet exemple, nous créons une seule page A4 et nous y inscrivons
    les éléments texte définis dans le template.
    """
    c = canvas.Canvas(output_pdf, pagesize=A4)
    draw_template(c, template, data)
    c.showPage()
    c.save()


def main():
    if len(sys.argv) < 4:
        print("Usage: python create_card_template.py <csv_file> <output_directory> <template_json>")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_dir = sys.argv[2]
    template_json = sys.argv[3]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Lecture du CSV (toutes les colonnes en str et remplacement des NaN)
    df = pd.read_csv(csv_file, dtype=str).fillna('')
    # Charge le template JSON
    template = load_template(template_json)

    # Pour chaque ligne du CSV, on crée un PDF
    for _, row in df.iterrows():
        nom = row.get("Nom", "")
        prenom = row.get("Prénom", "")
        output_pdf = os.path.join(output_dir, f"{nom}_{prenom}.pdf")
        create_card_using_template(row, output_pdf, template)

    print("Les cartes ont été générées !")


if __name__ == "__main__":
    main()