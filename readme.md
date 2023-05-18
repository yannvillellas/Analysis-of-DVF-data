# Analyse des données DVF
## Projet de fin de semestre en Python
![Arrondissements de paris](./images/illustration.png)

**Elias TOURNEUX** et **Yann VILLELLAS**
TD I, étudiant à l'ESILV en A3, promo 2025
### Installation
Vous devez mettre à la racine de votre projet les valeurs foncières de 2019 et 2022, disponibles sur l'[open data du gouvernement](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/).

#### Django
Pour lancer notre site fait sur Django, vous devez [installer django](https://docs.djangoproject.com/fr/4.2/intro/install/). Après avoir suivi le tutoriel d'installation, rendez-vous à la racine du projet, mettez les valeurs foncières de 2022 et exécutez la commande suivante :
- `python mysite/mysite/manage.py runserver`
- Et voilà, votre site est disponible à l'adresse [http://127.0.0.1:8000](http://127.0.0.1:8000).

#### Notebook au format HTML
Vous pouvez ouvrir la dernière version du notebook en allant [ici](https://yannvillellas.github.io/Analysis-of-DVF-data/).
Pour build la dernière version du notebook, vous devez installer [Jupyter](https://jupyter.org/install) et [nbconvert](https://nbconvert.readthedocs.io/en/latest/install.html). Après avoir suivi les tutoriels d'installation, rendez-vous à la racine du projet et exécutez la commande suivante :
- `jupyter nbconvert --to html --template pj ./rapport.ipynb --output-dir ./_build --output index.html`
Et voilà, votre notebook est disponible dans le dossier `_build` à la racine du projet.

### Mini-rapport :
#### Avancement et difficultés :
Nous avons eu beaucoup de problèmes lors du tri des données. Certaines valeurs étaient faussés, comme par exemple la surface inférieur à 1 m² par exemple, ou encore des noms de ville avec un tiret parfois sans espace, parfois avec un espace. Nous avons donc du faire beaucoup de tests pour pouvoir trier les données correctement. Nous avons aussi eu des problèmes avec les graphiques, car nous n'avions pas compris comment les utiliser. Nous avons donc du faire des recherches pour pouvoir les utiliser correctement.
Nous avons souhaités faire des cartes dynamiques à l'aide de Folium, et cela nous a aussi pris beaucoup de temps pour comprendre le concept de geojson.
#### Ratio de contribution:
 - Elias TOURNEUX : 50 %
 - Yann VILLELLAS : 50 %
