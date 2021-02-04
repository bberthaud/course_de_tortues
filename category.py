#!usr/bin/python3

"""Ce module sert a trouver les categories pour chaque tortue ainsi que ses parametres
pour ce faire on se base sur les vitesses et accelerations calculees avec parser.py"""

import parser
from collections import Counter
import argparse
import json


# Les 3 fonctions suivantes renvoient les parametres de la tortue si le test reussit, None sinon

def est_reguliere(vitesses):
    """teste si la tortue est reguliere ie si ses vitesses sont identiques"""
    vitesse_prec = vitesses[0]
    for vitesse in vitesses:
        if vitesse != vitesse_prec:
            return
        vitesse_prec = vitesse
    return {'v': vitesse}

def est_fatiguee(vitesses, acc):
    """teste si la tortue est fatiguee ie si elle accelere et deccelere au meme rythme"""
    counter = Counter(acc)
    # une tortue fatiguee n'admet pas plus de 6 accelerations differentes (3 en valeur absolue), et au moins 2
    if 2 <= len(counter) <= 6:
        main_acc = counter.most_common(2)
        # les 2 accelerations les plus presentes doivent etre de signes opposes (egales en valeur absolue)
        if main_acc[0][0] == -main_acc[1][0]:
            return {'v_initial': max(vitesses), 'rythme_croissance': abs(main_acc[0][0])}

def est_cyclique(vitesses):
    """teste si la tortue est cyclique ie ses vitesses se repetent selon le meme schema"""
    # un cycle est de taille 2 minimum
    cycle = [vitesses[0], vitesses[1]]
    for i in range(2,len(vitesses)):
        if vitesses[i] != cycle[0]:
            cycle.append(vitesses[i])
        else:
        # si une vitesse correspond a la 1ere du cycle on teste toutes les suivantes
        # pour verifier si on detecte la repetition du cycle
            for j in range(1,len(cycle)):
                if i+j >= len(vitesses) or vitesses[i+j] != cycle[j]:
                    return
            return {'cycle': cycle, 'fenetre': len(cycle)}

def distraite(vitesses):
    """renvoie la vitesse minimale et la vitesse maximale"""
    v_min = min(vitesses)
    v_max = max(vitesses)
    return {'v_min': v_min, 'v_max': v_max}
        

def categorie(tortue):
    """teste dans l'ordre si la tortue est reguliere, fatiguee, cyclique, sinon distraite
    renvoie un tuple (categorie, parametres)"""
    vitesses = tortue['vitesse']
    acc = tortue['acc']
    if est_reguliere(vitesses):
        return 'reguliere', est_reguliere(vitesses)
    elif est_fatiguee(vitesses, acc):
        return 'fatiguee', est_fatiguee(vitesses, acc)
    elif est_cyclique(vitesses):
        return 'cyclique', est_cyclique(vitesses)
    # par elimination la derniere categorie est distraite
    else:
        return 'distraite', distraite(vitesses)

def main(course):
    """fonction globale qui sauvegarde les resultats"""
    tortues = parser.tortues_attr(course)
    categories = []
    for i in tortues:
        tortue = tortues[i]
        cat = categorie(tortue)
        dict_tortue = {'id': i, 'categorie': cat[0], 'param': cat[1]}
        categories.append(dict_tortue)

        # debugging
        # print(tortue['top'])
        # print(tortue['vitesse'])
        # print(tortue['acc'])
        # print(cat)

    # on sauvegarde les resultats dans le dossier results sous un format json
    filename = 'results/results_{}.json'.format(course)
    with open(filename, 'w') as json_file:
        json.dump(categories, json_file)

    # calcul du maximum de la taille des fenetres pour les tortues cycliques
    fenetres = [cat['param']['fenetre'] for cat in categories if cat['categorie'] == 'cyclique']
    if fenetres:
        max_fenetre = max(fenetres)
        # print(max_fenetre)

    # stats repartition categories
    stats = Counter([cat['categorie'] for cat in categories])
    print(stats)


if __name__ == '__main__':
    """exemple de requete:
    python category.py -c tiny
    """
    # l'utilisateur choisit le type de la course
    parse = argparse.ArgumentParser()
    parse.add_argument('-c', '--course', type=str, help="taille de la course (tiny, small, medium, large)")
    args = parse.parse_args()

    main(args.course)
