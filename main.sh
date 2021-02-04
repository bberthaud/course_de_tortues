#!/bin/bash

python3 scrapper.py -n 199

for course in 'tiny' 'small' 'medium' 'large'
do
    echo $course
    python3 category.py -c $course
    echo
done