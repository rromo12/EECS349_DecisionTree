import os.path
import csv
from operator import xor
from parse import *
import csv

# DOCUMENTATION
# ========================================
# this function outputs predictions for a given data set.
# NOTE this function is provided only for reference.
# You will not be graded on the details of this function, so you can change the interface if 
# you choose, or not complete this function at all if you want to use a different method for
# generating predictions.

def create_predictions(tree, predict):
    '''
    Given a tree and a url to a data_set. Create a csv with a prediction for each result
    using the classify method in node class.
    '''
    with open(predict, 'rb') as f:
        reader = csv.reader(f,csv.QUOTE_NONE)
        labels = reader.next()
        predict = list(reader)
    results = []
    with open('results.csv', 'wb') as resultsfile:
        wr = csv.writer(resultsfile, quoting=csv.QUOTE_ALL)
        for instance in predict:
            instance.insert(0, instance.pop())

            for i in range(len(instance)):
                try:
                    instance[i]=float(instance[i])
                except ValueError:
                    pass   
            wr.writerow([tree.classify(instance)])
