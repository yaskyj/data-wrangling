#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road"
            }

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node["type"] = element.tag

        if element.tag == "way":
            node["node_refs"] = []
            for nd in element.iter("nd"):
                node["node_refs"].append(nd.attrib['ref'])
        #Create pos list to hold latitude and longitude
        pos = []

        #Iterate through the element attributes
        for attribute in element.attrib:
            #Check to see if the attribute in in the created list
            if attribute in CREATED:
                if "created" in node:
                    node["created"][attribute] = element.get(attribute)
                else:
                    node["created"] = {}
                    node["created"][attribute] = element.get(attribute)
            #If latitude or longitude then insert into the pos list
            elif attribute == "lat":
                pos.insert(0, float(element.get(attribute)))
            elif attribute == "lon":
                pos.insert(-1, float(element.get(attribute)))
            #Other attributes are just added
            else:
                node[attribute] = element.get(attribute) 

        #If pos exists, then add
        if len(pos) > 0:
            node["pos"] = pos

        #Iterate through tag elements
        for tag in element.iter("tag"):
            #Check for problem characters and ignore if present
            if problemchars.match(tag.attrib['k']):
                pass
            #Check if the tag more than one colon and if so, ignore
            elif tag.attrib['k'].count(":") > 1:
                pass
            #Match against one colon matches
            elif lower_colon.match(tag.attrib['k']):
                if tag.attrib['k'].find("addr:") == 0:
                    if "address" in node:
                        node["address"][tag.attrib['k'].split(":")[1]] =  tag.attrib['v']
                    else:
                        node["address"] = {}
                        node["address"][tag.attrib['k'].split(":")[1]] =  tag.attrib['v']
                else:
                    node[tag.attrib['k'].replace(":", "_")] = tag.attrib['v']
            else:
                node[tag.attrib['k']] = tag.attrib['v']

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

if __name__ == "__main__":
    data = process_map('example.osm')
