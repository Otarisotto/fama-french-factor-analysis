# Guide de démarrage (à faire une seule fois)

Ce guide t'amène du dossier téléchargé à un dépôt GitHub qui fonctionne. Compte 30 à 45 minutes la première fois.

## 1. Installer les outils

- **Python 3.10 ou plus** : <https://www.python.org/downloads/> (sous Windows, coche « Add Python to PATH »).
- **Git** : <https://git-scm.com/downloads>.
- **Un éditeur** : VS Code (<https://code.visualstudio.com/>) avec l'extension Python est un bon choix.
- **Un compte GitHub** : <https://github.com/signup>.

Vérifie dans un terminal :

```bash
python --version      # ou python3 --version
git --version
```

## 2. Configurer Git (une seule fois)

```bash
git config --global user.name "Ton Nom"
git config --global user.email "ton-email@exemple.com"
```

Utilise la même adresse que celle de ton compte GitHub (ou l'adresse « noreply » que GitHub te propose dans Settings > Emails, si tu veux ne pas exposer ton adresse).

## 3. Mettre en place l'environnement Python

Dans un terminal, place-toi dans le dossier du projet (`cd fama-french-factor-analysis`), puis :

```bash
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\activate             # Windows (PowerShell)

pip install -r requirements.txt
pip install -e .
pytest
```

À la fin, `pytest` doit afficher que tous les tests passent. Un environnement virtuel isole les bibliothèques de ce projet : c'est ce qui rend le dépôt reproductible par quelqu'un d'autre.

À chaque nouvelle session de travail, réactive-le (`source .venv/bin/activate`).

## 4. Créer le dépôt sur GitHub

1. Sur github.com, clique sur **New repository**.
2. Nom : `fama-french-factor-analysis`. Visibilité : **Public** (c'est un portfolio).
3. **Ne coche rien** (ni README, ni .gitignore, ni licence) : ils existent déjà.

## 5. Envoyer le projet

Dans le dossier du projet :

```bash
git init -b main
git add .
git commit -m "Initial commit: project skeleton, data loading and regression code"
git remote add origin https://github.com/TON-PSEUDO/fama-french-factor-analysis.git
git push -u origin main
```

GitHub te demandera de t'authentifier : le plus simple est d'installer **GitHub Desktop** (<https://desktop.github.com/>) ou le **GitHub CLI** (`gh auth login`). Les mots de passe classiques ne fonctionnent plus pour `git push`.

## 6. Le rythme de travail ensuite

Fais des commits **petits et fréquents**, avec un message qui dit ce qui a changé :

```bash
git add -A
git commit -m "Add Newey-West standard errors to FF3 regression"
git push
```

Un historique régulier montre ta progression, et c'est ce que les recruteurs regardent. Évite les commits géants du type « update ».

Règles utiles :
- Ne commite jamais de données brutes ni de mots de passe (le `.gitignore` s'en occupe déjà pour `data/raw/`).
- Avant de pousser, lance `pytest`.
- Si un notebook est cassé, relance-le entièrement (Kernel > Restart & Run All) avant de le commiter.

## 7. Première session (jeudi)

1. Ouvre `notebooks/01_capm_one_asset.ipynb` et exécute-le cellule par cellule.
2. Change le ticker, regarde comment alpha et bêtas bougent.
3. Lis `src/factor_analysis/regression.py` et assure-toi de comprendre chaque ligne.
4. Commit : `git commit -am "First CAPM/FF3 run on one stock"`.

## En cas de problème

- `yfinance` renvoie un tableau vide : vérifie le ticker et ta connexion, puis réessaie plus tard.
- Le téléchargement des facteurs échoue : le site de Kenneth French est parfois lent ; relance, ou télécharge le CSV à la main et place-le dans `data/raw/`.
- `ModuleNotFoundError: factor_analysis` : tu as oublié `pip install -e .` ou l'environnement virtuel n'est pas activé.
