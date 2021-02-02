from bs4 import BeautifulSoup
import urllib.request
import json
import time
import argparse

"""exemple de requete:
python scrapper.py -c tiny -n 201
"""
parse = argparse.ArgumentParser()
parse.add_argument('-c', '--course', type=str, help="taille de la course (tiny, small, medium, large)")
parse.add_argument('-n', '--nb_tops', type=int, default=201, help="nombre de tops")
args = parse.parse_args()

urlpage = "http://tortues.ecoquery.os.univ-lyon1.fr:8080/" + args.course
dict_list = []
for i in range(args.nb_tops):
    start = time.time()
    # query the website and return the html to the variable 'page'
    page = urllib.request.urlopen(urlpage)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')
    dict_soup = eval(soup.string)
    dict_list.append(dict_soup)
    time.sleep(3 - (time.time()-start))
    
filename = 'data_{}.json'.format(args.course)
with open(filename, 'w') as json_file:
    json.dump(dict_list, json_file)
        