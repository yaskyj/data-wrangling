#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

#Open  city file
osm_file = open("boulder.osm", "r")

#Regex to find word at the end of the street name
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
#Create dictionary to hold street names
street_types = defaultdict(set)

#Correct street names
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

#Check street names against expected and add to dictionary
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 

#Looks for the addr:street attrib
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

#Iterate through elements in file in order to review street names
def audit():
    for event, elem in ET.iterparse(osm_file):
        if elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    pprint.pprint(dict(street_types))
    # print_sorted_dict(street_types)


if __name__ == '__main__':
    audit()