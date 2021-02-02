# Rendu mini-projet BDA : Courses de tortues suite

Membres du projet : 
BERTHAUD Baptiste  p2009410
BESSON Florian p1504727

L'objectif de ce projet était d'implémenter, à partir des données issues du serveur c, un programme permettant de récupérer les catégories et les paramètres associés à chaque tortue.

Pour cela, nous avons choisi de travailler sur **Python**, pour l'acquisition et le traitement des données.

On retrouvera alors 3 fichiers : 
* *scrapper.py* : pour l'acquisition des données sur le serveur Web,
* *parser.py* : pour les parser et créer un dictionnaire de données associé, puis effectuer les calculs de vitesses et accélérations,
* *category.py* : pour attribuer une catégorie à chaque tortue.

## Phase 1 : Acquisition des données 

Disponibles sur le serveur *tortues.ecoquery.os.univ-lyon1.fr* au format JSON et actualisées toutes les 3 secondes, il nous a fallu commencer par créer un programme **scrapper.py** permettant de récupérer les données pour chaque course.

Pour cela, nous avons utilisé les librairies *urllib.request* (pour les requêtes sur le serveur Web), *time* (pour le délai (*sleep*) entre les requêtes), et *json* (pour la mise au bon format).

On définit tout d'abord un nombre de tops à acquérir. Ce choix de tops est délicat à déterminer, car si l'on prend une valeur trop faible alors on manquera certaines périodicités (pour la catégorie *cycliques* par exemple) ou une décroissance de la vitesse jusqu'à 0 (pour les *fatiguées*). A l'inverse, une valeur de tops trop élevée va engendrer un temps de calcul important, et un stockage des séquences qui va alourdir notre environnement.

# TODO : n tops ? 

On introduit une variable *course*, permettant de naviguer entre les 4 courses différentes.

Ensuite, on va requêter le serveur Web un certain de nombre de fois (suivant valeur de *nb_tops*), en attendant 3 secondes entre chaque requête.
A noter que le délai de 3 secondes est compté à partir du moment où l'on a terminé la précédente requête (et non commencé), car sinon un décalage va se créer en raison du délai de requêtage (peu élevé mais peut avoir des conséquences tout de même).

## Phase 2 : Parsage des données

On a ensuite implémenté le programme **parser.py**. 
L'objectif de celui-ci était de créer un nouveau dictionnaire de données, *tortues*, comprenant :
* l'id de chaque tortue
* pour chaque tortue, les positions, vitesses et accélérations associées à chaque top.


## Phase 3 : Attributuion des catégories

selon l'id 

# Note : cycles de taille 24!
