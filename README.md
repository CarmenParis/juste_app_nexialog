# ESEFIRIUS - Assistant Réseau SFR <img src="images/SFR.png" alt="Logo SFR" width="100" height="100" align="right">

## Prérequis

- Python 3.11+
- Poetry
- Git

## Installation

1. Cloner le dépôt
```bash
git clone https://github.com/CarmenParis/juste_app_nexialog.git
cd juste_app_nexialog
```

2. Installer Poetry (si pas déjà installé)
```bash
pip install poetry
```

3. Installer les dépendances
```bash
poetry install
```

4. Activer l'environnement virtuel
```bash
poetry shell
```

## Configuration

1. Assurez-vous d'avoir les fichiers de données requis :
   - `donnees.parquet`
   - `lof.csv`

## Lancement de l'application

```bash
python app.py
```

L'application sera accessible à l'adresse : `http://127.0.0.1:8050`

## Structure du Projet

- `app.py` : Point d'entrée principal de l'application
- `components/` : Composants de l'interface
- `callbacks/` : Logique de callback Dash
- `styles/` : Feuilles de style et thèmes
- `data/` : Fichiers de données

