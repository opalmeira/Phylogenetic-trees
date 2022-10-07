#!/usr/bin/env python3.10
# # -*- coding: utf-8 -*-

""" Update phylogenetic tree of Monkeypox in json file
Part 1: Finds the name of the node with the most number of descendents
Part 2: Load the json file, index it, search the path of the target node, 
return the path in string format
Part 3: Adjust the name of the path so it can be used to add key clade 
and value lII.b to the dictionary labels within the key branch_attrs
of the children
Part 4: Write the new updated dictionary to a json file
"""

import json
import pandas as pd

from ete3 import Tree
from benedict import benedict


# Part 1

def read_tree():
    # Reading tree with ete3 eases searching for the node
    tree = Tree("/home/ondinap/work/gisaid/mpx/tree.nwk_09_21", format = 1)
    return tree

def create_dict(tree):
    # Creates a dictionary of nodes and correspondents number of descendents.
    # It makes a list of number of descendents and put in descending order
    dic = {}
    for node in tree.traverse("postorder"):
        dic[node.name] = len(node)
    ordered_dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse = True))
    ordered_list = sorted(list(dic.values()), reverse = True)
    return ordered_dic, ordered_list

def grab_target_node(dic,rank):
    num_d = dic[rank]
    return num_d

def get_name(dic,pos_value):
    for key,value in dic.items():
        if pos_value == value:
            node_name = key
            
    return node_name

# Part 2

def read_my_dict():
    """Load json file with benedict will preserve the 
    dictionary format, besides leaving flexibility 
    for keypath_separator. This is set to 'None' 
    upon loading so that it does not cause error 
    when there is a dot in any of the keys or values, 
    since the keypath_separator default is a dot.
    """
    my_dict_new = benedict.from_json("/home/ondinap/work/gisaid/mpx/MPxV_Global3.json",keypath_separator=None)
    my_dict_new.standardize()
    my_dict_new = benedict(my_dict_new, keypath_separator = ".")
    
    return my_dict_new

def index_dict(v):
    # Indexing all keys and values and putting them in a list
    g = []
    def print_dict(v,prefix=''):
        if isinstance(v, dict):
            for k, v2 in v.items():
                p2 = "{}.{}".format(prefix,k)
                print_dict(v2,p2)
        elif isinstance(v,list):
            for i, v2 in enumerate(v):
                # the brackets here will be useful later to access the list index
                p2 = "{}[{}]".format(prefix,i)
                print_dict(v2,p2)
        else:
            g.append(['{}'.format(prefix),v])
            
        return g

    return print_dict(v)

def target_path(g,node_name):
    # Grab the indexed keys of the target node yield from part 1 above
    for i in g:
        for j in i:
            if j == node_name:
                nome = i[0]
                
    return nome

# Part 3

def prep_name(nome):
    nome1 = nome.strip('name') + "branch_attrs.labels"
    nome1 = nome1.strip(".")
    
    return nome1

def update_dict(dic,path_name):
    return dic[path_name].update({"clade":"IIb B.1"})

def conv_bene_write(n1):
    """ Saving dictionary from benedict type does not take a second argument
    as pandas.DataFrame.to_json does such as the indentation of the json file.
    Since Auspice takes a very specific format with the indentation I'm
    forced to read the final dictionary back in pandas and save it setting
    the 'indent' argument
    """
    dic_to_save = n1.to_json() # This takes one argument only
    dic_to_save = pd.read_json(dic_to_save)
    dic_to_save.to_json("/home/ondinap/work/gisaid/mpx/MPxV_Global3-test.json", indent = 1)

def main():

    """Part 1. Node with the highest number of descendents
    Create an empty dictionary
    Iterate each node and count the leaves
    Add the name of the node as key and number of leaves to the dictionary
    Get the numbers from the dictionary and order it in a list
    Map the number with the name of the node
    """
    tree = read_tree()
    dic_result = create_dict(tree)
    num_desc = grab_target_node(dic_result[1],9)
    node_name = get_name(dic_result[0],num_desc)

    """Part 2. Read and index json file, then grabs the path of the target node
    """
    my_dic = read_my_dict()
    my_dic_idx = index_dict(my_dic)
    path = target_path(my_dic_idx,node_name)

    """Part 3. Prepare the name of the path and update the json file within the target path
    """
    path = prep_name(path)
    update_dict(my_dic,path)

    """ Part 4. Write the updated dic to json file
    """
    conv_bene_write(my_dic)

main()

