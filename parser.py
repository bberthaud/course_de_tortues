import json
from collections import defaultdict


def top_positions(course):
    filename = 'data_{}.json'.format(course)
    with open(filename, 'r') as json_data:
        dict_list = json.load(json_data)
        tortues = defaultdict(lambda: defaultdict(list))
        for data_dict in dict_list:
            tortoises = data_dict['tortoises']
            for i in range(len(tortoises)):
                tortue = tortoises[i]
                tortues[i]['top'].append(tortue['top'])
                tortues[i]['position'].append(tortue['position'])
    return tortues

def vitesses(tortue):
    tops = tortue['top']
    positions = tortue['position']
    for j in range(len(tops)-1):
        vitesse = (positions[j+1] - positions[j]) / (tops[j+1] - tops[j])
        tortue['vitesse'].append(vitesse)

def accelerations(tortue):
    tops = tortue['top']
    vitesses = tortue['vitesse']
    for j in range(len(vitesses)-1):
        acc = abs(vitesses[j+1] - vitesses[j]) / (tops[j+2] - tops[j+1])
        tortue['acc'].append(acc)


def tortues_attr(course):
    tortues = top_positions(course)
    for i in tortues:
        tortue = tortues[i]
        vitesses(tortue)
        accelerations(tortue)
    return tortues


    