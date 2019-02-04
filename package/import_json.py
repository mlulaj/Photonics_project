import json
import package.definitions as clt

# This module provides a method to read the json file and return a list of network elements to the main() of the program
# In Python, methods whose name begins with _ are intended to be 'internal' methods. They should be never
# called outside of the class or module where they are defined.


def import_netelems_from_json(file_pointer):
    with open(file_pointer) as fp:
        json_struct = json.load(fp)

    return _builder(json_struct['network_nodes'])

# json.load() reads the json file and maps it into a list of dictionaries. Run the program in debug mode to take a
#  look at the json_struct object and compare its structure to the one of.json file

# The _builder method then creates the network_elements list to return to the main. Basically it maps the elements
#  of the json_struct object to the corresponding classes LineSystem, Fiber and Amplifier, which are defined in the
#  definitions.py module


def _builder(json_struct):
    network_elements_list = []
    for elem in json_struct:
        net_elem = getattr(clt, elem['type'])(**elem)
        network_elements_list.append(net_elem)

    return network_elements_list

# For each dict in the json_struct list, it looks at the 'type' entry and builds a corresponding class. ...
#  (EX: if 'type' is LineSystem, build an object of the LineSystem class with the attributes listed in the dict).
#  Classes definitions and their __init__() methods are in the 'definitions.py' module.
# Uses getattr() to get the correct name of the class to be initialized corresponding to 'type'
# Uses the 'keyword arguments' of python (**elem) (search the web for more info) to pass the dict to the ...
#  class builder. dict's keys and values will be mapped to the object attributes.
