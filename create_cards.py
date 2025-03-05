import os
import sys
import pandas as pd

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

# Importations pour Paragraph
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def draw_page1(c, data):
    """
    Dessine la première page avec les informations personnelles et la photo.
    Champs utilisés :
      - Nom, Prénom, Photo, Village, Age, Sexe, Métier, Partie politique
    """
    # Récupération des champs (conversion en chaîne pour éviter les NaN)
    nom = str(data.get("Nom", ""))
    prenom = str(data.get("Prénom", ""))
    photo_path = str(data.get("Photo", ""))
    village = str(data.get("Village", ""))
    age = str(data.get("Age", ""))
    sexe = str(data.get("Sexe", ""))
    metier = str(data.get("Métier", ""))
    partie_politique = str(data.get("Partie politique", ""))

    page_width, page_height = A4

    # -------------------------
    # Ajout d'une bordure double
    # -------------------------
    outer_margin = 1 * cm
    inner_margin = 0.7 * cm  # espace entre la première et la deuxième bordure

    c.setStrokeColor(colors.black)
    c.setLineWidth(2)
    # Bordure extérieure
    c.rect(outer_margin, outer_margin, page_width - 2 * outer_margin, page_height - 2 * outer_margin, stroke=1, fill=0)
    # Bordure intérieure
    c.rect(outer_margin + inner_margin, outer_margin + inner_margin,
           page_width - 2 * (outer_margin + inner_margin), page_height - 2 * (outer_margin + inner_margin),
           stroke=1, fill=0)

    # -------------------------
    # Titre (Nom complet)
    # -------------------------
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    title_text = f"{prenom} {nom}"
    c.drawCentredString(page_width / 2, page_height - 4 * cm, title_text)

    # -------------------------
    # Sous-titre (Métier)
    # -------------------------
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.black)
    c.drawCentredString(page_width / 2, page_height - 5 * cm, metier)

    # -------------------------
    # Insertion de la photo
    # -------------------------
    photo_w = 6 * cm
    photo_h = 6 * cm
    photo_x = (page_width - photo_w) / 2
    photo_y = page_height - 12 * cm

    try:
        c.drawImage(
            photo_path,
            photo_x,
            photo_y,
            width=photo_w,
            height=photo_h,
            preserveAspectRatio=True,
            mask='auto'
        )
    except Exception as e:
        print(f"Impossible de charger l'image '{photo_path}' : {e}")

    # -------------------------
    # Informations complémentaires
    # -------------------------
    text_x = 2 * cm
    text_y = photo_y - 1 * cm  # position juste en dessous de la photo
    line_spacing = 16

    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawString(text_x, text_y, f"Village : {village}")
    c.drawString(text_x, text_y - line_spacing, f"Âge : {age}")
    c.drawString(text_x, text_y - 2 * line_spacing, f"Sexe : {sexe}")
    c.drawString(text_x, text_y - 3 * line_spacing, f"Parti politique : {partie_politique}")

def draw_page2(c, data):
    """
    Dessine la deuxième page qui affiche l'alibi avec un retour à la ligne automatique.
    """
    alibi = str(data.get("Alibi", ""))

    page_width, page_height = A4

    # -------------------------
    # Ajout d'une bordure double (même style que la page 1)
    # -------------------------
    outer_margin = 1 * cm
    inner_margin = 0.7 * cm

    c.setStrokeColor(colors.black)
    c.setLineWidth(2)
    c.rect(outer_margin, outer_margin, page_width - 2 * outer_margin, page_height - 2 * outer_margin, stroke=1, fill=0)
    c.rect(outer_margin + inner_margin, outer_margin + inner_margin,
           page_width - 2 * (outer_margin + inner_margin), page_height - 2 * (outer_margin + inner_margin),
           stroke=1, fill=0)

    # -------------------------
    # Titre de la page 2
    # -------------------------
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(page_width / 2, page_height - 3 * cm, "Alibi")

    # -------------------------
    # Zone pour le texte de l'alibi
    # -------------------------
    text_x = 2 * cm
    text_y = page_height - 4 * cm  # début du bloc texte sous le titre
    text_width = page_width - 4 * cm  # marge de 2 cm de chaque côté
    text_height = text_y - 2 * cm  # marge en bas

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = 12
    style.leading = 16  # interligne augmenté pour une meilleure lisibilité
    style.alignment = 4  # Justification du texte (optionnel)

    # Conversion des retours à la ligne en balises <br/> pour que Paragraph gère les sauts de ligne
    alibi_html = alibi.replace("\n", "<br/>")

    p = Paragraph(alibi_html, style)
    w, h = p.wrap(text_width, text_height)
    p.drawOn(c, text_x, text_y - h)

def create_fullpage_card(data, output_dir):
    """
    Crée un PDF pour un personnage sur deux pages :
      - Page 1 : Informations personnelles et photo.
      - Page 2 : Alibi.
    """
    nom = str(data.get("Nom", ""))
    prenom = str(data.get("Prénom", ""))
    pdf_filename = os.path.join(output_dir, f"{nom}_{prenom}.pdf")
    c = canvas.Canvas(pdf_filename, pagesize=A4)

    # Page 1 : Infos personnelles et photo
    draw_page1(c, data)
    c.showPage()  # passe à la page suivante

    # Page 2 : Alibi
    draw_page2(c, data)
    c.showPage()
    c.save()

def main():
    if len(sys.argv) < 3:
        print("Usage : python create_fullpage_card.py <csv_file> <output_directory>")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Lecture du CSV en forçant les colonnes en str et en remplaçant NaN par ''
    df = pd.read_csv(csv_file, dtype=str).fillna('')

    for _, row in df.iterrows():
        create_fullpage_card(row, output_dir)

    print("La génération des cartes est terminée !")

if __name__ == "__main__":
    main()