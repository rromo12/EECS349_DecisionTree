# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 nodes if numeric, and a dictionary (key=attribute value, value=node) if nominal.  
#            For numeric, the 0 index holds examples < the splitting_value, the 
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on
string = ""
clauselist = []
class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None

    def classify(self, instance):
        '''
        given a single observation, will return the output of the tree
        '''
        if self.label == None:
            if(self.is_nominal):
                value = instance[self.decision_attribute]
                if(value not in self.children.keys()):
                    value = self.children.keys()[0]
                    
                return self.children[value].classify(instance)
            else:
                if(instance[self.decision_attribute] < self.splitting_value):
                    return self.children[0].classify(instance)
                else:
                    return self.children[1].classify(instance)
        else:
            return self.label 

    def print_tree(self, indent = 0):
        '''
        returns a string of the entire tree in human readable form
        IMPLEMENTING THIS FUNCTION IS OPTIONAL
        '''
        # Your code here
        pass


    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        global string,clauselist
        temp_string = string
        if(self.label == 1):
            clause = string[:-4] + "\n OR"

            clauselist.append(clause)
            string = ""
        elif(self.label == 0):
            pass
        elif self.is_nominal:
            # add self to global string
            string += "("+self.name +"="  + str(self.value) +") AND"
            for value,node in self.children.iteritems():
                string = temp_string
                node.print_dnf_tree()
        else:
            string += "(" + self.name + "<"  + str(self.splitting_value) + ") AND "
            self.children[0].print_dnf_tree()
            string = temp_string + "(" + self.name + ">=" + str(self.splitting_value) + ") AND "
            self.children[1].print_dnf_tree()
        return "if " + "".join(clauselist)[:-5]