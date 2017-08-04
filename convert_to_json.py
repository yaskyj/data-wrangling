#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

#Regex for names with one colon
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
#Regex for names with characters that will be ignored
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
#Regex for the end of street names
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#Mapping based on review of audit_street_names script
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

#Mapping based on review of explor_tag_types script
city_mapping = { "Boulder, CO": "Boulder",
            "lafayette": "Lafayette",
            " Lafayette": "Lafayette",
            u"Boulder, CO \u200e": "Boulder",
            "boulder": "Boulder"
            }

#Mapping based on review of explor_tag_types script
post_mapping = { "80026-2872": "80026",
            "80303-1229": "80303",
            "80305-9998": "80305",
            "CO 80027": "80027",
            "CO 80305": "80305"
            }

#List for the created portion of the item's dictionary
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

#Checks for the street names ending with a key in the street_mapping, returns the proper name if found
def clean_street_name(street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type in street_mapping:
            return street_mapping[street_type]
        else:
            return street_name

#Checks if tag is the street
def is_street_name(elem):
    return elem.attrib['k'] == "addr:street"

#Checks for the city names in the key of city_mapping, returns the proper name if found
def clean_city_name(city_name):
    if city_name in city_mapping:
        return city_mapping[city_name]
    else:
        return city_name

#Check if the tag is the city
def is_city_name(elem):
    return elem.attrib['k'] == "addr:city"

#Checks for the city names in the key of city_mapping, returns the proper name if found
def clean_post(post):
    if post in post_mapping:
        return post_mapping[post]
    else:
        return post

#Check if the tag is the city
def is_post(elem):
    return elem.attrib['k'] == "addr:postcode"

def shape_element(element):

    node = {}

    #Only adding tags that are node or way
    if element.tag == "node" or element.tag == "way" :
        node["type"] = element.tag

        #Adds all node references to one list
        if element.tag == "way":
            node["node_refs"] = []
            for nd in element.iter("nd"):
                node["node_refs"].append(nd.attrib['ref'])

        #Create pos list to hold latitude and longitude
        pos = []

        #Iterate through the element attributes
        for attribute in element.attrib:

            #Check to see if the attribute is in the created list
            if attribute in CREATED:
                #Checks if created already exists in node, if not add it before adding
                #the attribute
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

            #Other attributes are just added with colons replaces with underscores
            else:
                node[attribute.replace(":", "_")] = element.get(attribute) 

        #If pos exists, then add to node
        if len(pos) > 0:
            node["pos"] = pos

        #Iterate through tag elements
        for tag in element.iter("tag"):

            #Check for problem characters and ignore if present
            if problemchars.match(tag.attrib['k']):
                pass

            #Check if the tag more than one colon and if so, ignores tag
            elif tag.attrib['k'].count(":") > 1:
                pass

            #Match against one colon
            elif lower_colon.match(tag.attrib['k'].lower()):

                #Checks for address attributes
                if tag.attrib['k'].find("addr:") == 0:
                    #Checks if address is already in node, if not, the else
                    #statement creates it before adding the attribute
                    if "address" in node:
                        #Checks for street name, cleans, and adds
                        if is_street_name(tag):
                            node["address"]["street"] = clean_street_name(tag.attrib['v'])
                        #Checks for city name, clean, and adds
                        elif is_city_name(tag):
                            node["address"]["city"] = clean_city_name(tag.attrib['v'])
                        elif is_post(tag):
                            node["address"]["postcode"] = clean_post(tag.attrib['v'])
                        #Takes the second part of the address and adds that and the
                        #value to the node
                        else:
                            node["address"][tag.attrib['k'].split(":")[1]] =  tag.attrib['v']
                    else:
                        if is_street_name(tag):
                            node["address"] = {}
                            node["address"]["street"] = clean_street_name(tag.attrib['v'])
                        elif is_city_name(tag):
                            node["address"] = {}
                            node["address"]["city"] = clean_city_name(tag.attrib['v'])
                        elif is_post(tag):
                            node["address"] = {}
                            node["address"]["postcode"] = clean_post(tag.attrib['v'])
                        else:
                            node["address"] = {}
                            node["address"][tag.attrib['k'].split(":")[1]] =  tag.attrib['v']

                #All other one colon tags have the colon replaced with an underscore
                else:
                    node[tag.attrib['k'].replace(":", "_")] = tag.attrib['v']
            #Adds normal node
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
    data = process_map('boulder.osm')
