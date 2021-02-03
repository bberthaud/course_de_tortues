#!usr/bin/python3

import urllib.request
import json
import time
import argparse
from collections import defaultdict


def main(courses, nb_tops):
    dict_list = defaultdict(list)
    top_start = {}
    top_end = {}
    for i in range(nb_tops):
        start = time.time()
        for course in courses:
            urlpage = "http://tortues.ecoquery.os.univ-lyon1.fr:8080/" + course
            with urllib.request.urlopen(urlpage) as page:
                dict_page = json.loads(page.read().decode())
                if i == 0:
                    top_start[course] = dict_page['tortoises'][0]['top']
                elif i == nb_tops - 1:
                    top_end[course] = dict_page['tortoises'][0]['top']
            dict_list[course].append(dict_page)
        delay = time.time() - start
        time.sleep(3 - delay)

    for course in courses:
        filename = 'data/data_{}.json'.format(course)
        with open(filename, 'w') as json_file:
            json.dump(dict_list[course], json_file)
    
    return top_start, top_end

def verification_top(courses, nb_tops, top_start, top_end):
    """fonction qui verifie que le nombre de tops scrappes correspond bien a celui souhaite"""
    for course in courses:
        nb_scrap = top_end[course] - top_start[course] + 1
        if nb_scrap != nb_tops:
            return False
    return True


if __name__ == '__main__':
    """exemple de requete:
    python scrapper.py -n 199
    """
    parse = argparse.ArgumentParser()
    parse.add_argument('-n', '--nb_tops', type=int, default=199, help="nombre de tops")
    args = parse.parse_args()
    courses = ['tiny', 'small', 'medium', 'large']
    top_start, top_end = main(courses, args.nb_tops)
    while not verification_top(courses, args.nb_tops, top_start, top_end):
        print("Error scrapping : try again...")
        top_start, top_end = main(courses, args.nb_tops)