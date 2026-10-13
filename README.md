# Analyse factorielle Fama-French par régression

Les facteurs Fama-French (marché, taille, value, profitabilité, investissement) expliquent-ils les rendements d'un échantillon d'actions ? Ce pouvoir explicatif est-il stable dans le temps ?

> **Statut : en cours.** Ce README est complété au fil du projet (voir la feuille de route).

## Méthode

Pour chaque actif, on estime par moindres carrés ordinaires :

```
r_t - rf_t = α + β₁ F₁,t + … + β_k F_k,t + ε_t
```

pour trois modèles emboîtés : CAPM (1 facteur), Fama-French 3 facteurs, Fama-French 5 facteurs.

- **Inférence robuste** : erreurs standard de Newey-West (HAC), car les résidus sont souvent hétéroscédastiques et autocorrélés.
- **Comparaison de modèles** : R² ajusté, AIC, BIC.
- **Stabilité** : régressions sur fenêtre glissante (60 mois) et test de rupture structurelle.

## Données

- Facteurs : [bibliothèque de données de Kenneth French](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) (mensuel).
- Prix : Yahoo Finance via `yfinance` (prix ajustés des dividendes et splits).

Les données ne sont pas versionnées : elles sont téléchargées et mises en cache à la première exécution.

## Reproduire les résultats

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
pytest                           # vérifie que le code fonctionne
jupyter notebook notebooks/
```

## Structure

```
src/factor_analysis/   code réutilisable (données, régressions)
tests/                 tests unitaires sur données synthétiques
notebooks/             exploration et figures
report/                rapport LaTeX avec les dérivations
```

## Feuille de route

- [ ] Semaine 1 : données + CAPM / FF3 sur un actif
- [ ] Semaine 2 : erreurs robustes, tous les actifs, comparaison CAPM / FF3 / FF5
- [ ] Semaine 3 : bêtas glissants, test de rupture structurelle
- [ ] Semaine 4 : tests, README final, rapport LaTeX

## Résultats

*À compléter.*

## Limites

*À compléter : biais de survie (univers d'actions actuelles), période d'échantillon, absence de coûts de transaction, risque de data snooping si plusieurs modèles sont testés.*
