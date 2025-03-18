# Générateur de Cartes PDF pour Murder Party

Ce projet est une application Python qui génère des cartes de jeu pour une murder party. Chaque carte est créée en fusionnant des données provenant d'un fichier CSV avec un template PDF existant. Le système génère une carte sur deux pages :

- **Page 1** : Affiche les informations principales (Nom, Prénom, Métier, Photo, Village, Âge, Sexe, Partie politique) en remplaçant les zones en rouge du template.
- **Page 2** : Affiche l'alibi avec deux colonnes : d'abord le texte de "Alibi", puis, en dessous, celui de "Alibi_en".

Le projet utilise ReportLab pour créer les overlays PDF et PyPDF2 pour fusionner ces overlays avec un template PDF.

## Table des Matières

- [Installation](#installation)
- [Utilisation](#utilisation)
- [Dépendances](#dépendances)
- [Structure du CSV](#structure-du-csv)
- [Fonctionnalités](#fonctionnalités)
- [Contribuer](#contribuer)
- [Licence](#licence)
- [Contact](#contact)

## Installation

1. **Cloner le dépôt :**

   ```bash
   git clone https://github.com/gateanbarras/cardGenerator.git
   cd cardGenerator
   ```

2. **Installer les dépendances :**

   Vous pouvez installer les dépendances avec :

   ```bash
   pip install -r requirements.txt
   ```

   Si le fichier requirements.txt n'existe pas, installez-les manuellement :

   ```bash
   pip install pandas reportlab PyPDF2
   ```

## Utilisation

Le script principal s'appelle `create_pdf.py` et prend trois arguments :

1. Le fichier CSV contenant vos données.
2. Le répertoire de sortie où seront générées les cartes.
3. Le fichier template PDF (par exemple, `template.pdf`).

Exemple d'exécution :

```bash
python create_pdf.py personnages.csv output_cards template.pdf
```

Chaque ligne du CSV génère un PDF nommé `Nom_Prénom.pdf` dans le dossier `output_cards`.

## Dépendances

- **pandas** : Pour lire et manipuler le fichier CSV.
- **ReportLab** : Pour générer et formater les PDF.
- **PyPDF2** : Pour fusionner les overlays PDF avec un template PDF existant.

## Structure du CSV

Le fichier CSV doit contenir au minimum les colonnes suivantes :

- **Nom** : Nom du personnage.
- **Prénom** : Prénom du personnage.
- **Photo** : Chemin vers l'image à intégrer.
- **Métier** : Métier ou rôle du personnage.
- **Village** : Village d'origine.
- **Âge** : Âge du personnage.
- **Sexe** : Sexe du personnage.
- **Partie politique** : Parti politique associé.
- **Alibi** : Texte d'alibi en français.
- **Alibi_en** : Texte d'alibi en anglais.

Exemple de ligne CSV :

```
Nom,Prénom,Photo,Métier,Village,Âge,Sexe,Partie politique,Alibi,Alibi_en
Nanchen,Tristan,photo/gee_me_020.jpg,Stay-at-home dad,Icogne,35,M,PLR,"Alibi en français ici","Alibi in English here"
```

## Fonctionnalités

- **Génération de cartes PDF sur deux pages** : La première page contient les informations principales et la photo, et la deuxième page affiche les alibis.
- **Overlay personnalisé** : Les données du CSV sont placées dans des zones précises du template PDF.
- **Fusion avec template PDF** : L'overlay est fusionné avec un template PDF existant pour créer un design final.
- **Auto-ajustement du texte** : La taille du texte est ajustée automatiquement pour tenir dans les zones définies.
- **Support pour deux colonnes d'alibi** : Affichage du texte de "Alibi" suivi du texte de "Alibi_en" sur la deuxième page.

## Contribuer

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez ce dépôt.
2. Créez une branche pour votre fonctionnalité :
   ```bash
   git checkout -b feature/nom-fonctionnalite
   ```
3. Commitez vos changements :
   ```bash
   git commit -am 'Ajout d\'une fonctionnalité'
   ```
4. Poussez votre branche :
   ```bash
   git push origin feature/nom-fonctionnalite
   ```
5. Ouvrez une Pull Request sur GitHub.

## Contact

Gaëtan Barras – gaetan.barras@regentschool.ch

Lien du projet : https://github.com/gateanbarras/cardGenerator