# Rendu mini-projet BDA : Courses de tortues suite

Membres du projet : 

BERTHAUD Baptiste  p2009410

BESSON Florian p1504727

L'objectif de ce projet est d'implémenter, à partir des données issues du serveur `tortues.ecoquery.os.univ-lyon1.fr`, un programme permettant de récupérer les catégories et les paramètres associés à chaque tortue. Le sujet est ici : http://emmanuel.coquery.pages.univ-lyon1.fr/enseignement/tiw6/mini_projet_storm/

Pour cela, nous avons choisi de travailler sur **Python**, pour l'acquisition et le traitement des données.

On retrouvera alors 3 fichiers : 
* *scrapper.py* : pour l'acquisition des données sur le serveur Web,
* *parser.py* : pour les parser et créer un dictionnaire de données associé, puis effectuer les calculs de vitesses et accélérations,
* *category.py* : pour attribuer une catégorie à chaque tortue, ainsi que leurs paramètres.


## Phase 1 : Acquisition des données 

Disponibles sur le serveur `tortues.ecoquery.os.univ-lyon1.fr` au format JSON et actualisées toutes les 3 secondes, il nous a fallu commencer par créer un programme **scrapper.py** permettant de récupérer les données pour chaque course.

Pour cela, nous avons utilisé les librairies *urllib.request* (pour les requêtes sur le serveur Web), *time* (pour le délai (*sleep*) entre les requêtes), et *json* (pour la mise au bon format).

On définit tout d'abord un nombre de tops à acquérir. Ce choix de tops est délicat à déterminer, car si l'on prend une valeur trop faible alors on manquera certaines périodicités (pour la catégorie *cycliques* par exemple) ou une décroissance de la vitesse jusqu'à 0 (pour les *fatiguées*). A l'inverse, une valeur de tops trop élevée va engendrer un temps de calcul important, et un stockage des séquences qui va alourdir notre environnement. La valeur finale de tops est discutée dans la phase 3 sur les tortues cycliques.


On introduit une variable *course*, permettant de naviguer entre les 4 courses différentes.

Ensuite, on va requêter le serveur Web un certain de nombre de fois (suivant valeur de *nb_tops*), en attendant 3 secondes entre chaque requête.
A noter que le délai de 3 secondes est compté à partir du moment où l'on a terminé la précédente requête (et non commencé), car sinon un décalage va se créer en raison du délai de requêtage (peu élevé mais peut avoir des conséquences tout de même).


Enfin, on introduit une fonction **verification_top** qui va vérifier si le nombre de tops recueillis est bien celui souhaité.


## Phase 2 : Parsage des données

On a ensuite implémenté le programme **parser.py**. 
L'objectif de celui-ci est de créer un nouveau dictionnaire de données, *tortues*, comprenant :
* l'id de chaque tortue
* pour chaque tortue, les positions, vitesses et accélérations associées à chaque top. Ces vitesses et accélérations sont faites en calculant les dérivées (taux d'accroissement successifs pour être plus précis) des positions et vitesses pour chaque top.


## Phase 3 : Attribution des catégories

Enfi, on opère la phase d'attribution des catégories pour chaque tortue. 
En effet, 4 classes existent : les tortues *fatiguées*, *cycliques*, *régulières* et *distraites*. 

La définition des tortues *distraites* nous oblige à attribuer cette catégorie par élimination par rapport aux 3 autres.

On commence par les tortues *régulières*, qui sont les plus faciles à détecter. En effet, celles-ci on une vitesse constante. On implémente donc une fonction *est_reguliere*, qui retourne *None* si deux vitesses pour 2 tops successifs sont différentes, et la vitesse (constante) sinon.

Ensuite, on regarde si la tortue est dite *fatiguée*. En effet, la convention stipulant que les tortues fatiguées et cycliques sont considérées comme fatiguées, mais pas comme cycliques nous pousse à commencer par ce type de tortues.
Pour les détecter, on utilise la commande *Counter* qui permet de compter le nombre d'occurences dans une liste.  On récupère pour chaque tortue les 2 accélérations les plus fréquentes, et on regarde si elles sont opposées. Si c'est le cas, alors cela signifie que la tortue a changé régulièrement de rythme, avec la même accélération/décélération. On retourne dans le cas des tortues fatiguées leur *rythme de croissance* comme paramètre, correspondant à l'accélération/décélération la plus observée, ainsi que la vitesse maximale.

On peut ensuite passer aux tortues dites *cycliques*. Pour cela, on itère sur chaque top, et si l'on observe qu'une valeur de vitesse est identique à celle du premier top, alors on vérifie si le caractère cyclique est validé pour les tops suivants, jusqu'à atteindre un nombre de tops égal à la taille du premier cycle. De plus, on met une condition permettant de s'assurer que l'on observera bien 2 cycles consécutifs grâce au nombre de tops *nb_tops* attribué (par exemple, on ne peut pas conclure si une tortue est cyclique si on observe un cycle de taille 16, mais que l'on a *nb_tops* valant seulement 25). On retourne pour les tortues cycliques le cycle correspondant.

A noter que la taille maximale observée pour le cycle est de 99 tops. Or pour détecter un cycle de taille n il est nécessaire de récupérer au moins 2n+1 tops (car avec 2n+1 tops on calcule 2n vitesses sur lesquelles on veut observer 2 cycles). Donc **le nombre de tops retenu est 201** (on prend une marge de sécurité de 1 sur la taille du cycle).

Enfin les tortues *distraites* sont les tortues qui ne correspondent pas aux conditions précédentes. Dans ce cas on retourne les vitesses minimales et maximales observées.

On peut ainsi retourner un fichier donnant pour chaque tortue (définie par son *id*), sa catégorie et les paramètres correspondants.


## Vérification

A la fin, on vérifie que les proportions de chaque catégorie de tortues sont similaires. Puisqu'en théorie il y a équiprobabilité de tomber sur une des 4 catégories de tortue, d'où une répartition 1/4 pour chaque catégorie.

On a fait afficher ces statistiques à la fin du code *category.py*.


## Exécution 

Pour exécuter notre programme, il suffit de lancer **main.sh**, qui va catégoriser les tortues pour les 4 courses différentes.

En sortie, un fichier JSON est disponible par course, dans le dossier **results**. Ceux-ci comportent, pour chaque course, les attributs suivants :
* l'id de la tortue,
* la catégorie attribuée,
* les paramètres correspondants (*params*) : *cycle* et *fenetre* si la tortue est de type cyclique, *v_min* et *v_max* si la tortue est *distraite*, *v_initial* et *rythme_croissance* si elle est *fatiguée* et *v* pour les tortues *régulières*.
