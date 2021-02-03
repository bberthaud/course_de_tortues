#!usr/bin/python3

import parser
from collections import Counter
import argparse
import json


def est_reguliere(vitesses):
    vitesse_prec = vitesses[0]
    for vitesse in vitesses:
        if vitesse != vitesse_prec:
            return
        vitesse_prec = vitesse
    return {'v': vitesse}

def est_fatiguee(vitesses, acc):
    counter = Counter(acc)
    if 2 <= len(counter) <= 4:
        main_acc = counter.most_common(2)
        if main_acc[0][0] == -main_acc[1][0]:
            return {'v_initial': max(vitesses), 'rythme_croissance': abs(main_acc[0][0])}

def est_cyclique(vitesses):
    cycle = [vitesses[0], vitesses[1]]
    for i in range(2,len(vitesses)):
        if vitesses[i] != cycle[0]:
            cycle.append(vitesses[i])
        else:
            for j in range(1,len(cycle)):
                if i+j >= len(vitesses) or vitesses[i+j] != cycle[j]:
                    return
            return {'cycle': cycle, 'fenetre': len(cycle)}

def distraite(vitesses):
    v_min = min(vitesses)
    v_max = max(vitesses)
    return {'v_min': v_min, 'v_max': v_max}
        

def categorie(tortue):
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
    tortues = parser.tortues_attr(course)
    categories = []
    for i in tortues:
        tortue = tortues[i]
        cat = categorie(tortue)
        dict_tortue = {'id': i, 'categorie': cat[0], 'param': cat[1]}
        categories.append(dict_tortue)

        # print(tortue['top'])
        # print(tortue['vitesse'])
        # print(tortue['acc'])
        # print(cat)

    filename = 'results/results_{}.json'.format(course)
    with open(filename, 'w') as json_file:
        json.dump(categories, json_file)

    fenetres = [cat['param']['fenetre'] for cat in categories if cat['categorie'] == 'cyclique']
    if fenetres:
        max_fenetre = max(fenetres)
        # print(max_fenetre)

    # stats repartition
    stats = Counter([cat['categorie'] for cat in categories])
    print(stats)


if __name__ == '__main__':
    """exemple de requete:
    python category.py -c tiny
    """
    parse = argparse.ArgumentParser()
    parse.add_argument('-c', '--course', type=str, help="taille de la course (tiny, small, medium, large)")
    args = parse.parse_args()
    main(args.course)
