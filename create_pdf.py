import os
import sys
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

# Importations pour Paragraph (texte long)
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Importations pour la fusion avec un template PDF existant
from PyPDF2 import PdfReader, PdfWriter

# Dimensions du template selon votre JSON
TEMPLATE_WIDTH = 1500.0
TEMPLATE_HEIGHT = 2100.0

# Format final : A4
PAGE_WIDTH, PAGE_HEIGHT = A4

# Facteurs d'échelle pour convertir les coordonnées du template en coordonnées A4
SCALE_X = PAGE_WIDTH / TEMPLATE_WIDTH
SCALE_Y = PAGE_HEIGHT / TEMPLATE_HEIGHT

def draw_page1(c, data):
    """
    Crée la première page d'overlay pour un PDF A4.
    On place dans les zones prévues par le template (coordonnées issues du JSON) :
      - "Title" : Nom et Prénom à (x=125, y=90, height=80, size=80)
      - "Type" : Métier à (x=125, y=1885, height=70, size=70) centré
      - "Art" : Zone photo à (x=40, y=203, width=1420, height=1048)
      - "Rules" : Zone d'infos complémentaires (Village, Âge, Sexe, Parti politique)
        à (x=160, y=1300, height=500, size=60)
    Les coordonnées JSON sont converties vers le système A4.
    """
    # Récupération des données du CSV
    prenom = str(data.get("Prénom", ""))
    nom = str(data.get("Nom", ""))
    photo_path = str(data.get("Photo", ""))
    metier = str(data.get("Métier", ""))
    village = str(data.get("Village", ""))
    age = str(data.get("Age", ""))
    sexe = str(data.get("Sexe", ""))
    parti = str(data.get("Parti politique", ""))

    # --- Zone Title ---
    # JSON : x=125, y=90, height=80, taille de police=80
    title_text = f"{prenom} {nom}"
    title_y = ((TEMPLATE_HEIGHT - 90 - 80) * SCALE_Y ) + 8 # conversion depuis le haut
    c.setFont("Helvetica-Bold", 80 * SCALE_Y)
    c.setFillColor(colors.white)
    c.drawCentredString(PAGE_WIDTH / 2, title_y, title_text)

    # --- Zone Type (Métier) ---
    type_text = metier
    type_x = 125 * SCALE_X
    type_width = 1250 * SCALE_X
    type_y = ((TEMPLATE_HEIGHT - 1885 - 70) * SCALE_Y) + 10

    # Définition de la marge de 20 px de chaque côté (on peut convertir en points si besoin, ici on suppose 20 pts)
    marge = 20
    max_text_width = type_width - 2 * marge

    # Taille de police initiale (en points) basée sur l'échelle
    font_name = "Helvetica-Bold"
    font_size = 50 * SCALE_Y

    # Ajustement de la taille de police jusqu'à ce que le texte tienne dans max_text_width
    while c.stringWidth(type_text, font_name, font_size) > max_text_width and font_size > 1:
        font_size -= 1

    c.setFont(font_name, font_size)
    c.setFillColor(colors.white)
    c.drawCentredString(type_x + type_width / 2, type_y, type_text)

    # --- Zone Photo ("Art") ---
    # JSON : x=40, y=203, width=1420, height=1048
    art_x = (40 * SCALE_X) + 40
    art_y = ((TEMPLATE_HEIGHT - 203 - 1048) * SCALE_Y ) +20
    art_w = 1420 * SCALE_X * 0.8
    art_h = 1048 * SCALE_Y * 0.8
    try:
        c.drawImage(photo_path, art_x, art_y, width=art_w, height=art_h, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print(f"Impossible de charger l'image '{photo_path}' : {e}")

    # --- Zone Rules (Infos complémentaires) ---
    # JSON : x=160, y=1300, width=1180, height=500, taille=60
    rules_x = 160 * SCALE_X
    rules_width = 1180 * SCALE_X
    rules_y = (TEMPLATE_HEIGHT - 1300 - 500) * SCALE_Y  # position basse de la zone
    # On compose les informations complémentaires avec un retour à la ligne après chaque valeur
    rules_text = (
        f"Village : {village}<br/>"
        f"Âge : {age}<br/>"
        f"Sexe : {sexe}<br/>"
        f"Parti politique : {parti}"
    )

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = 60 * SCALE_Y
    style.leading = 66 * SCALE_Y
    style.textColor = colors.white
    # Création d'un Paragraph pour gérer la mise en forme
    p = Paragraph(rules_text, style)
    w, h = p.wrap(rules_width, 500 * SCALE_Y)
    # On place le texte dans la zone en centrant verticalement dans la zone Rules
    p.drawOn(c, rules_x, rules_y + (500 * SCALE_Y - h)/2)


def draw_page2(c, data):
    """
    Crée la deuxième page d'overlay pour afficher les deux textes :
      - Le texte de la colonne "Alibi" en premier,
      - Puis, en dessous, le texte de la colonne "Alibi_en".
    """
    # Récupération des deux textes
    alibi1 = str(data.get("Alibi", "")).strip()
    alibi2 = str(data.get("Alibi_EN", "")).strip()

    # Titre de la page 2 : "Alibi"
    c.setFont("Helvetica-Bold", 50 * SCALE_Y)
    c.setFillColor(colors.white)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 50, "Keep this side secret - Alibi")

    # Combinaison des deux textes avec un double saut de ligne
    if alibi1 and alibi2:
        combined_alibi = f"{alibi1}<br/>***************************************************************<br/>{alibi2}"
    else:
        combined_alibi = alibi1 or alibi2

    # Zone pour le texte de l'alibi
    text_x = 100
    text_width = PAGE_WIDTH - 200
    text_height = 300
    text_y = (PAGE_HEIGHT - 150 ) +70 # à partir du haut

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = 40 * SCALE_Y  # taille augmentée
    style.leading = 45 * SCALE_Y
    style.alignment = 4  # texte justifié
    style.textColor = colors.white

    # Conversion des retours à la ligne en balises <br/> pour que le Paragraph les interprète
    alibi_html = combined_alibi.replace("\n", "<br/>")
    p = Paragraph(alibi_html, style)
    w, h = p.wrap(text_width, text_height)
    p.drawOn(c, text_x, text_y - h)
def create_overlay_pdf(data, overlay_pdf_path):
    """
    Crée un PDF overlay sur deux pages au format A4.
      - Page 1 : remplit les zones du template (Title, Type, Art, Rules)
      - Page 2 : affiche l'alibi
    """
    c = canvas.Canvas(overlay_pdf_path, pagesize=A4)
    draw_page1(c, data)
    c.showPage()
    draw_page2(c, data)
    c.showPage()
    c.save()

def merge_with_template(template_pdf_path, overlay_pdf_path, output_pdf_path):
    """
    Fusionne l'overlay PDF avec le template PDF existant.
    Chaque page de l'overlay est fusionnée avec la page correspondante du template.
    """
    template_reader = PdfReader(template_pdf_path)
    overlay_reader = PdfReader(overlay_pdf_path)
    writer = PdfWriter()

    for i, page in enumerate(template_reader.pages):
        if i < len(overlay_reader.pages):
            page.merge_page(overlay_reader.pages[i])
        writer.add_page(page)

    with open(output_pdf_path, "wb") as out_file:
        writer.write(out_file)

def create_fullpage_card(data, output_dir, template_pdf_path):
    """
    Crée un PDF A4 sur deux pages en fusionnant l'overlay (contenant les valeurs placées
    selon le template) avec le template PDF existant.
    La première page contient Title, Type, Photo et Rules, la deuxième l'alibi.
    """
    nom = str(data.get("Nom", ""))
    prenom = str(data.get("Prénom", ""))
    output_pdf = os.path.join(output_dir, f"{nom}_{prenom}.pdf")

    overlay_pdf = os.path.join(output_dir, f"overlay_{nom}_{prenom}.pdf")
    create_overlay_pdf(data, overlay_pdf)
    merge_with_template(template_pdf_path, overlay_pdf, output_pdf)
    os.remove(overlay_pdf)

def main():
    if len(sys.argv) < 4:
        print("Usage: python create_fullpage_card.py <csv_file> <output_directory> <template_pdf>")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_dir = sys.argv[2]
    template_pdf = sys.argv[3]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv(csv_file, dtype=str).fillna('')
    for _, row in df.iterrows():
        create_fullpage_card(row, output_dir, template_pdf)
    print("La génération des cartes est terminée !")

if __name__ == "__main__":
    main()