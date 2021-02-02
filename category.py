import parser
from collections import Counter


def est_reguliere(vitesses):
    vitesse_prec = vitesses[0]
    for vitesse in vitesses:
        if vitesse != vitesse_prec:
            return
        vitesse_prec = vitesse
    return {'v': vitesse}

def est_fatiguee(vitesses, acc):
    counter = Counter(acc)
    main_acc = counter.most_common(1)[0]
    freq = main_acc[1]/float(len(acc))
    if freq > 0.75:
        return {'v_initial': max(vitesses), 'rythme_croissance': main_acc[0]}

def est_cyclique(vitesses):
    cycle = [vitesses[0]]
    for i in range(1,len(vitesses)):
        if vitesses[i] != cycle[0]:
            cycle.append(vitesses[i])
        else:
            for j in range(1,len(cycle)):
                if i+j >= len(vitesses)-1 or vitesses[i+j] != cycle[j]:
                    return
            return {'cycle': cycle}

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

def main():
    course = 'small'
    tortues = parser.tortues_attr(course)
    categories = []
    for i in tortues:
        tortue = tortues[i]
        cat = categorie(tortue)

        # print(tortue['top'])
        # print(tortues['vitesse'])
        # print(tortues['acc'])
        categories.append(cat[0])
        # print(cat)
    print(Counter(categories))


main()
