from random import shuffle
from ID3 import *
from operator import xor
from parse import parse
import matplotlib.pyplot as plt
import os.path
import random
from pruning import validation_accuracy
from numpy import linspace


# NOTE: these functions are just for your reference, you will NOT be graded on their output
# so you can feel free to implement them as you choose, or not implement them at all if you want
# to use an entirely different method for graphing

def get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, pct):
    '''
    get_graph_accuracy_partial - Given a training set, attribute metadata, validation set, numerical splits count, and percentage,
    this function will return the validation accuracy of a specified (percentage) portion of the trainging setself.
    '''
    depth = 20
    num_training_samples = int(math.floor(pct*len(train_set)))+1 #number of training samples to use 
    data_subset = random.sample(train_set,num_training_samples)
    tree = ID3(data_subset, attribute_metadata, numerical_splits_count, depth)
    return validation_accuracy(tree,validate_set)

def get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, pcts):
    '''
    Given a training set, attribute metadata, validation set, numerical splits count, iterations, and percentages,
    this function will return an array of the averaged graph accuracy partials based off the number of iterations.
    '''
    total = 0
    for i in range(iterations):
        total+=get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, pcts)
    return float(total)/iterations

# get_graph will plot the points of the results from get_graph_data and return a graph
def get_graph(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, lower, upper, increment):
    '''
    get_graph - Given a training set, attribute metadata, validation set, numerical splits count, depth, iterations, lower(range),
    upper(range), and increment, this function will graph the results from get_graph_data in reference to the drange
    percentages of the data.
    '''
    numb = int((upper-lower)/increment)
    x=linspace(lower,upper,numb)
    print x
    y=[]
    for i in x:
        print i
        y.append(get_graph_data(train_set,attribute_metadata,validate_set,numerical_splits_count,iterations,i))
    plt.figure(0) 
    print x, y
    print len(x),len(y)
    plt.plot(x,y)
    plt.show()
    return plt.plot(x, y)