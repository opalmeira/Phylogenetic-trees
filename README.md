# Phylogenetic-trees
Updating a phylogenetic tree within a json file

This is a sample script to update a phylogenetic tree within a json file to be visualized on Auspice Nextstrain.\
The mission here is to add a key-value pair in a specific branch of the tree where the node has the tenth highest number of descendants.

**Input files:** tree.nwk and file.json\
**Output file:** updated_file.json

## Requirements:
* python-benedict (https://github.com/fabiocaccamo/python-benedict)

* ete3 (https://github.com/etetoolkit/ete)

Script was written in Python 3.10

A more generalized version is under construction
