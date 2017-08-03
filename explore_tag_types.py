#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Exploring other tags
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

osm_file = open("boulder.osm", "r")

tag_counts = defaultdict(int)
tag_values = defaultdict(set)

def explore_tags(tag_type, tag_value):
    tag_counts[tag_type] += 1
    tag_values[tag_type].add(tag_value)

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 

def print_sorted_amounts(d):
    values = sorted(d.items(), key=lambda x:x[1], reverse=True)
    for k,v in values:
        print "%s: %d" % (k, v) 

def print_top_tags(d):
    count = 0
    top_tags = {}
    values = sorted(d.items(), key=lambda x:x[1], reverse=True)
    for k,v in values:
        if count < 10:
            if k != "addr:street" and k != "name":
                top_tags[k] = tag_values[k]
                count += 1
        else:
            break
    pprint.pprint(dict(top_tags))

def audit():
    for event, elem in ET.iterparse(osm_file):
        for tag in elem.iter("tag"):
            explore_tags(tag.attrib['k'], tag.attrib['v'])
    # pprint.pprint(dict(tag_counts))
    # print len(tag_counts)
    # print_sorted_dict(tag_counts)
    # print_sorted_amounts(tag_counts)
    print_top_tags(tag_counts)

if __name__ == '__main__':
    audit()