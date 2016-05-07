import math
from node import Node
from collections import defaultdict
import sys
import operator

def fix_missing_attributes(data_set,attribute_metadata):
    '''
    Fix Missing attributes with mode for nominal attributes and average for numerical attributes
    ===========================================================================================================
    Input:data_set and attribute_metadata
    ===========================================================================================================
    Output: the fixed data set without missing attributes
    '''
    defaults = []
    for attribute in range(len(attribute_metadata)):
        if(attribute_metadata[attribute]['is_nominal']):
            defaults.append(attribute_mode(data_set,attribute))
        else:
            defaults.append(attribute_average(data_set,attribute))

    for data in range(len(data_set)):
        for attribute in range(len(attribute_metadata)):
            if(data_set[data][attribute] == '?'):
                data_set[data][attribute] = defaults[attribute]
    return data_set

def attribute_mode(data_set,attribute):
    '''
    Calculate Mode of a Nominal attribute
    ===========================================================================================================
    Input:data_set and nominal attribute index
    ===========================================================================================================
    Output: Mode of this attribute
    '''
    dictionary = {}
    for data in data_set:
        if data[attribute] != None:
            if data[attribute] in dictionary.keys():
                dictionary[data[attribute]] += 1
            else:
                dictionary[data[attribute]] = 1
    return max(dictionary.iteritems(), key=operator.itemgetter(1))[0]

def attribute_average(data_set,attribute):
    '''
    Calculate average value for a numerical attribute
    ===========================================================================================================
    Input:data_set and attribute index
    ===========================================================================================================
    Output: Average value for this attribute
    '''
    total = 0
    for data in data_set:
        if(data[attribute] != None):
            total +=data[attribute]
    average = float(total)/len(data_set)
    return average    

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    Actually calls the ID3 Helper function to generate ID3 tree
    had to make it this way to avoid the recursive calls trying to fix missing attributes
    '''
    data_set= fix_missing_attributes(data_set,attribute_metadata)
    return ID3_helper(data_set, attribute_metadata, numerical_splits_count, depth)

def ID3_helper(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
	maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================
    # '''

    leaf = Node()
    threshold =0.1
    if(len(data_set) == 0 or depth == 0 or check_homogenous(data_set) != None or entropy(data_set)<threshold or len(attribute_metadata) == 0):
        #if examples empty return default default(mode)
        #or if all examples have same classification return that classification (mode of the dataset is the same as the homogenous classification)
        #or if depth has reached its limit
        # attributes is empty return mode
        leaf.label = mode(data_set)
        leaf.decision_attribute = None
        leaf.is_nominal = None
        leaf.value = None
        leaf.splitting_value = None
        leaf.name = None
        return leaf
    else:
        best_attribute,splitting_value = pick_best_attribute(data_set,attribute_metadata,numerical_splits_count)
        #tree<- a new decision tree with root best
        leaf.label = None
        leaf.decision_attribute = best_attribute
        leaf.name = attribute_metadata[best_attribute]['name']
        # attribute_metadata.pop(best_attribute)      #remove best attribute from list of attributes
        numerical_splits_count[best_attribute] -= 1 #lower numerical splits of this attribute by 1 

        #case of zero information gain on all possible splitting attributes
        if(best_attribute == False):
            leaf.label = mode(data_set)
            leaf.decision_attribute= None
            leaf.name = None
            leaf.splitting_value = None
            leaf.value = None
            return leaf
        elif(splitting_value == False): #case of nominal attribute
            leaf.is_nominal = True
            examples = split_on_nominal(data_set,best_attribute)
            leaf.splitting_value = splitting_value
            # dictionary (key=attribute value, value=node)
            dictionary = {}
            for value, data in examples.iteritems():
                dictionary[value]= ID3_helper(data,attribute_metadata,numerical_splits_count,depth-1)
            leaf.children = dictionary
            return leaf
            # recursive call to ID3
        else: #case of numeric
            examples = split_on_numerical(data_set,best_attribute,splitting_value)
            leaf.is_nominal = False
            leaf.splitting_value=splitting_value
            #list of 2 nodes
            leaf.children = [
            ID3_helper(examples[0],attribute_metadata,numerical_splits_count,depth-1),
            ID3_helper(examples[1],attribute_metadata,numerical_splits_count,depth-1)
            ]
            return leaf
    return leaf
            # recursive call to ID3
def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the output value (index 0) is the same for all examples in the the data_set, if so return that output value, otherwise return None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
     '''
    test = data_set[0][0]
    for data in data_set:
        if(data[0] != test):
            return None
    return test
# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    max_gain = 0
    max_index = 0
    splitting_value = 0
    #check all attributes
    for index in range(1,len(attribute_metadata)):
        #if attribute is nominal use nominal gain calculation
        if attribute_metadata[index]['is_nominal']:
            #if higher than max gain then this is our best attribute and should be our new max gain,index and splitting value is false
            if(max_gain< gain_ratio_nominal(data_set,index)):
                max_gain = gain_ratio_nominal(data_set,index)
                max_index = index
                splitting_value = False

        else: #if nominal and numerical splits > 0, use nominal gain calculation
            if(numerical_splits_count[index]>0): 
                if(max_gain< gain_ratio_numeric(data_set,index,steps)[0]):
                    #if higher than max gain then this is our best attribute and should be our new max gain,index and splitting value
                    max_gain,splitting_value = gain_ratio_numeric(data_set,index,steps)
                    max_index = index

    
    if(max_gain==0): #if max gain is 0 then all attributes gain was 0, return false, false 
         max_index = False
         splitting_value = False

    return (max_index,splitting_value)
# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)


# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    # Your code here

    dictionary = {}

    for data in data_set:
        if data[0] in dictionary.keys():
            dictionary[data[0]] += 1
        else:
            dictionary[data[0]] = 1
    return max(dictionary.iteritems(), key=operator.itemgetter(1))[0]
        
           
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. See Textbook for formula
    ========================================================================================================
    '''
    positive = 0
    ttl = len(data_set)
    
    def log2(x):
        if x == 0.0:
            return 0.0
        else:
            return math.log(x,2)
    for data in data_set:
        if(data[0] == 1):
            positive +=1
    positive = float(positive)
    negative = ttl - positive
    pospro = positive/ttl
    negpro = negative/ttl
    entropy = -((pospro * (log2(pospro))) + ((negpro) * (log2(negpro))))
    return abs(entropy)


# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    intrinsic = 0
    gain = float(entropy(data_set))
    attribute_values = []
    subsets = split_on_nominal(data_set,attribute)
    for value in subsets.keys():
        sub = subsets[value]
        gain -= float(len(sub))/len(data_set) * float(entropy(sub))
        temp = float(abs(len(sub)))/abs(len(data_set))
        intrinsic += temp * math.log(temp,2)
    if intrinsic == 0:
        intrinsic = 0.0000001
    return abs(float(gain)/intrinsic)

# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    # Your code here
    thresholds = {}
    intrinsic = 0
    attribute_values = []
    gain_ratio = 0
    threshold = 0
    max_splitting_val = 0

    for index in range(len(data_set)):
        if(index%steps == 0):
            #split using this value
            sublists = split_on_numerical(data_set,attribute,data_set[index][attribute])

            #make sure that lists are of size greater than 0 to avoid entropy function crashing
            if(len(sublists[0]) > 0 and len(sublists[1])>0):    
                intrinsic = 0
                gain = float(entropy(data_set))
                #calculate gain ratio using sublists from splitting on this value
                for sublist in sublists:
                    gain -= float(len(sublist))/len(data_set) * float(entropy(sublist))
                    temp = float(abs(len(sublist)))/abs(len(data_set))
                    intrinsic += temp * math.log(temp,2)
                #store this possible threshold value and its gain ratio
                if intrinsic == 0:
                    intrinsic = 0.0000001
                thresholds[data_set[index][attribute]]=abs(float(gain)/intrinsic)
              

    # #get the max gain ratio and return it and its associated threshold
    #     for threshold, gain_ratio in thresholds.iteritems():
    #         if(gain_ratio > max_gain_ratio):
    #             max_gain_ratio = gain_ratio
    #             max_splitting_val = threshold
    if(thresholds != {}):
        threshold,gain_ratio = max(thresholds.iteritems(), key=operator.itemgetter(1))
    return gain_ratio,threshold
# ======== Test case =============================
# data_set,attr,step = [[0,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    dictionary = defaultdict(list)
    for data in data_set:
        dictionary[data[attribute]].append(data)
    return dictionary
# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
	attribute has value less than the splitting value, the second list contains the other examples
    ========================================================================================================
    Output: Tuple of two lists as described above
    ========================================================================================================
    '''
    less = []
    other = []
    for data in data_set:
        if(data[attribute] <splitting_value):
            less.append(data)
        else:
            other.append(data)
    return (less,other)
# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])


