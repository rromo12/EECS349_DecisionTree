from node import Node
from ID3 import *
from operator import xor

# Note, these functions are provided for your reference.  You will not be graded on their behavior,
# so you can implement them as you choose or not implement them at all if you want to use a different
# architecture for pruning.

def reduced_error_pruning(root,training_set,validation_set):
    '''
    take the a node, training set, and validation set and returns the improved node.
    You can implement this as you choose, but the goal is to remove some nodes such that doing so improves validation accuracy.
    NOTE you will probably not need to use the training set for your pruning strategy, but it's passed as an argument in the starter code just in case.
    '''

#     original_validation = validation_accuracy(root,validation_set))

#     if(root.label != None): #leaf, can't be pruned 
#         return root
#     else:
#         if root.is_nominal: #nominal splitting node  
#                 subsets = split_on_nominal(validation_set, root.decision_attribute)


#                 new_node = self.label = mode
#                 if(new_validation > original_validation):
#                     return new_node
#         else: #root is numeric
#                 new_validation =validation_accuracy(new_node,validation_set))
#                 if(new_validation > original_validation):
#                     return new_node

#         return root
# #
    pass
def validation_accuracy(tree,validation_set):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
    '''
    correct = 0
    for instance in range(len(validation_set)):
        if(tree.classify(validation_set[instance]) == validation_set[instance][0]):
            correct +=1
    return float(correct)/len(validation_set)