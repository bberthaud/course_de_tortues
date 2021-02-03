#!/bin/bash

course='tiny'
nb_tops=10

python scrapper.py -c $course -n $nb_tops
python category.py -c $course -n $nb_tops