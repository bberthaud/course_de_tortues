#!usr/bin/python3

"""Ce module sert a recuperer les donnees du serveur web"""

import urllib.request
import json
import time
import argparse
from collections import defaultdict


def main(courses, nb_tops):
    """fonction principale pour scrapper"""
    dict_list = defaultdict(list)
    top_start = {}
    top_end = {}
    for i in range(nb_tops):
        start = time.time()
        for course in courses:
            # on recupere le dictionnaire json
            urlpage = "http://tortues.ecoquery.os.univ-lyon1.fr:8080/" + course
            with urllib.request.urlopen(urlpage) as page:
                dict_page = json.loads(page.read().decode())
                # top_start et top_end servent a la fonction verification_top
                if i == 0:
                    top_start[course] = dict_page['tortoises'][0]['top']
                elif i == nb_tops - 1:
                    top_end[course] = dict_page['tortoises'][0]['top']
            # pour chaque course on stocke les dict dans une liste
            dict_list[course].append(dict_page)
        delay = time.time() - start
        # le temps entre deux scrapping doit etre egale a 3s, d'ou le delay qui prend en compte le temps de calcul
        time.sleep(3 - delay)

    # on sauvegarde les donnees dans des fichiers json du dossier data
    for course in courses:
        filename = 'data/data_{}.json'.format(course)
        with open(filename, 'w') as json_file:
            json.dump(dict_list[course], json_file)
    
    return top_start, top_end

def verification_top(courses, nb_tops, top_start, top_end):
    """fonction qui verifie que le nombre de tops scrappes correspond bien a celui souhaite
    renvoie True si c'est bon, False sinon"""
    for course in courses:
        # on compare le premier et le dernier top scrappes
        nb_scrap = top_end[course] - top_start[course] + 1
        # lors du scrapping s'il y a un saut ou une redondance de top on le verra ici
        if nb_scrap != nb_tops:
            return False
    return True


if __name__ == '__main__':
    """exemple de requete:
    python scrapper.py -n 199
    """
    # l'utilisateur choisit le nombre de tops à scrapper
    parse = argparse.ArgumentParser()
    parse.add_argument('-n', '--nb_tops', type=int, default=199, help="nombre de tops")
    args = parse.parse_args()
    courses = ['tiny', 'small', 'medium', 'large']
    
    top_start, top_end = main(courses, args.nb_tops)
    # tant que le nombre de tops scrappes n'est pas bon, on recommence le processus en entier
    while not verification_top(courses, args.nb_tops, top_start, top_end):
        print("Error scrapping : try again...")
        top_start, top_end = main(courses, args.nb_tops)