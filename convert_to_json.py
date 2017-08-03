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


#Based on review of audit_street_names script
street_mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "st": "Street",
            "Dr": "Drive",
            "Ct": "Court",
            "Blvd": "Boulevard",
            "Baselin": "Baseline",
            "Ave.": "Avenue"
            }

#Based on review of explor_tag_types script
city_mapping = { "Boulder, CO": "Boulder",
            "lafayette": "Lafayette",
            " Lafayette": "Lafayette",
            u"Boulder, CO \u200e": "Boulder",
            "CO": "Boulder",
            "boulder": "Boulder"
            }

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def clean_street_name(street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type in street_mapping:
            return street_mapping[street_type]
        else:
            return street_name

def is_street_name(elem):
    return elem.attrib['k'] == "addr:street"

def clean_city_name(city_name):
    if city_name in city_mapping:
        return city_mapping[city_name]
    else:
        return city_name

def is_city_name(elem):
    return elem.attrib['k'] == "addr:city"

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
                node[attribute.replace(":", "_")] = element.get(attribute) 

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
            elif lower_colon.match(tag.attrib['k'].lower()):
                if tag.attrib['k'].find("addr:") == 0:
                    if "address" in node:
                        if is_street_name(tag):
                            node["address"]["street"] = clean_street_name(tag.attrib['v'])
                        elif is_city_name(tag):
                            node["address"]["city"] = clean_city_name(tag.attrib['v'])
                        else:
                            node["address"][tag.attrib['k'].split(":")[1]] =  tag.attrib['v']
                    else:
                        if is_street_name(tag):
                            node["address"] = {}
                            node["address"]["street"] = clean_street_name(tag.attrib['v'])
                        elif is_city_name(tag):
                            node["address"] = {}
                            node["address"]["city"] = clean_city_name(tag.attrib['v'])
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
    file_out = "boulderimport.json"#.format(file_in)
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
    data = process_map('sample.osm')
