from bs4 import BeautifulSoup
import urllib.request
import json
import time

nb_tops = 50
course = 'small'

urlpage = "http://tortues.ecoquery.os.univ-lyon1.fr:8080/" + course
dict_list = []
for i in range(nb_tops):
    start = time.time()
    # query the website and return the html to the variable 'page'
    page = urllib.request.urlopen(urlpage)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')
    dict_soup = eval(soup.string)
    dict_list.append(dict_soup)
    end = time.time()
    t = 3 - (end-start)
    time.sleep(t)
    
filename = 'data_{}.json'.format(course)
with open(filename, 'w') as json_file:
    json.dump(dict_list, json_file)
        