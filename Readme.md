# airQmap

Le but de ce projet est de visualiser en temps réél les mesures en concentration des polluants sur le territoire français. Les données sont issues du portail françaisde la données data.gouv.fr, et sont relevées toutes les heures par des stations de mesures réparties sur le territoire français avant d'être aggrégées par le Laboratoire Central de Surveillance de la Qualité de l'Air (LCSQA).

---

## Contexte

Suite à la directive européenne de Décembre 2011 sur les échanges d'informations vis à vis de la qualité de l'air ambiant, les état membres sont tenus d'entretenir un flux de données régulier suivant un format standardisé pour reporter les mesures de concentrations en polluants atmosphériques sur le territoire français. Cette standardisation des flux de données en open-data permet en principe une meilleure transparence sur la qualité de l'air en france, mais la complexité des flux de données échangés en rend la visualisation difficile. Ce projet propose une méthode d'aggrégation en temps réel du flux de données avant de le visualiser sur un carte interactive.

---

## Architecture

Le projet se divise en 3 composants principaux :
- L'api de visualisation, qui permet de contruire des cartes interactives puis de les visualiser dans le navigateur.
- La base de données (MongoDB), qui stocke les données du LCSQA et les renvoie à l'API de visualisation
- L'aggrégateur de données, qui parse les documents du LCSQA et permet de mettre à jour la base de données

---

## Installation

### API et base de donnée

Ces composant sont conteneurisés. Il suffit d'installer [docker](https://docs.docker.com/get-docker/) et [docker-compose](https://docs.docker.com/compose/install/), l'installation et le lancement des composants est ensuite automatisé avec la commande :
```
docker-compose up --build
```

### Aggrégateur de données

Pour garder les données à jour, ce composant devrait être lui aussi conteneurisé et s'éxécuter périodiquement (avec un cron job par exemple), mais pour la simplicité de la démonstration. J'ai souhaité laisser la possibilité d'éxécuter le raffrachissement manuellement. 

Il faut donc installer python et ses dépendances :
```
pip install -r requirements.txt
```

---

## Utilisation

### Remplissement et raffraichissement de la base

Avant la première utilisation de l'application, il faut utiliser le script d'aggrégation pour obtenir les premières données. Ce script peut ensuite être utilisé périodiquement pour mettre à jour la base avec les dernières données (des données sont produites toutes les heures).

Le raffraichissement de la base de données se fait en éxécutant le script `refresh.py`. Ce script parse les derniers relevés qui n'ont pas encore été insérés dans la base.

### Utilisation de l'API

lorsque la base de donnée et l'API sont lancés avec docker-compose, l'API est disponible à l'adresse http://localhost:5000. les ressources disponibles sont les suivantes : 
- `/api/heatmap?pollutant=<nom du polluant>` : visualisation sous forme de heatmap du polluant choisi les polluants répertoriés sont les suivants : 
   - NO2 : dioxyde d'azote
   - SO2 : dioxyde de souffre
   - PM10 : particules fines < 10 µm
   - O3 : Ozone
   - NOX : Oxydes d'azote
   - CO : Monoxyde de carbone
   - H2S : Sulfure d'hydrogène
   - PM25 : particules fines < 25 µm
- `/api/value?pollutant=<nom du polluant> :` visualisation en couleur des concentrations aux points de mesure. Les polluants référencés sont les mêmes.
- `/api/blank` : une carte interactive vide

---

## Remarques et conclusion

La visualisation sous forme de heatmap, bien que particulièrement esthétique, souffre d'un défaut majeur, la coloration change en fonction du nombre de points de mesures dans le voisinage. Dans notre cas d'utilisation, de nouveaux points de mesure peuvent apparaître et disparaître au fil du temps, ce qui fausse la représentation. La représentation par valeur au points de mesure est plus précise et permet un meilleur suivi en fonction du temps.

La visualisation sur une journée permet d'observer la variation de polluants atmosphériques due à l'activité humaine en journée. Cette variation est d'autant plus flagrante en visualisant les valeurs pour l'O3 au fil de la journée.

Cette visualisation est encore une première version, et elle souffre de problèmes de performance de la carte due au grand nombre de points de données. Pour aller plus loin, un pré calcul des moyennes par zones pourrait être effectué par un autre service, ce qui permettrait d'alléger le nombre de points sur la carte et d'exploiter d'autre visualisations (affichage de type choropleth).
