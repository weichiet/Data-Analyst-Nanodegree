#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""
#%%

import xml.etree.cElementTree as ET
import re
import codecs
import json
from collections import defaultdict

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
POSITION = ["lat", "lon"]

# The list of possible street type keywords in Singapore map
expected_street= ["Street", "Avenue", "Boulevard", "Central", "Circle", "Close", "Crescent", 
            "Court", "Drive", "Grove", "Heights", "Jalan", "Park", "Place", 
            "Square", "Loop", "Lane", "Link", "Lorong", 
            "Road",  "Taman", "Terrace",  "Trail", "View", "Walk", "Way" ]

# The list of mapping the abbreviated street name to the whole word
street_mapping = { "Ave": "Avenue", "Ave.": "Avenue",
            "Apt": "Apartment", "Apt.": "Apartment",             
            "Blvd": "Boulevard", "Blvd.": "Boulevard",            
            "Cres": "Crescent", "Cres.": "Crescent",
            "Dr": "Drive", "Dr.": "Drive", 
            "Jln": "Jalan", "Jln.": "Jalan", "jln": "Jalan",
            "Lor": "Lorong", "Lor.": "Lorong", 
            "Rd": "Road", "Rd.": "Road", "road": "Road",
            "St": "Street", "St.": "Street",
            "Tmn": "Taman", "Tmn.": "Taman",
            "Ter": "Terrace", "Ter.": "Terrace"            
            }


def update_street_name(street_name, street_mapping):
    '''
    This function update the abbreviated street name
    '''
    new_name = street_name
    
    #First checks if the street name contains any of the defined possible keywords.
    if not list(set(street_name.split()).intersection(set(expected_street))):
        # If the street name doesn't contain any possible keywords, check 
        # if it contains any abbreviated street type in the 'street_mapping'
        replaced_word = list(set(street_name.split()).intersection(set(street_mapping.keys())))
        # If yes, update the abbreviated street type
        if replaced_word:
            new_name = street_name.replace(replaced_word[0], street_mapping[replaced_word[0]])        
            
            # For debugging prupose
            #print (street_name, "=>", new_name)
            
    return new_name

def update_postcode(postcode, user):
    '''
    This function update the incorrect postal codes 
    created by user 'JaLooNz' by appending a '0'
    at the front of the postal code.
    '''
    new_postcode = postcode
    
    if len(postcode)!=6 and user =="JaLooNz":
        new_postcode = '0' + postcode
        
        # For debugging prupose
        #print (postcode, "=>", new_postcode)
        
    return new_postcode

#%%
def shape_element(element):
    '''
    This function transforms the shape of the data into a list of dictionaries.
    '''    
    
    # Empty dictionaries for each tags
    node =  {}
    created = {}
    position = {}
    address = {}
    node_refs = []
    additional_tag = defaultdict(dict)
    
    if element.tag == "node" or element.tag == "way" :
        # Set the type as 'node' or 'way'
        node["type"] = element.tag        
        
        # Iterate all the top level tags
        for key, values in element.attrib.items():  
            # Check if it is CREATED type
            if key in CREATED:
                created[key] = values
            # Check if it is POSITION type
            elif key in POSITION:
                position[key] = float(values)
            # Store the key value pair directly if it is not CREATED or POSITION
            else:
                node[key] = values
        
        # Iterate the second level 'tag'     
        for tag in element.iter("tag"):
            # Check if the attribute 'k' value contains problematic characters
            if not problemchars.search(tag.attrib['k']):
                # Check if the attribute 'k' value starts with 'addr:'
                if tag.attrib['k'].startswith("addr:"):
                    # Split the string starts with 'addr:'
                    splitted_addr = tag.attrib['k'].split(":")
                    # Store the key/value of address attributes 
                    # (Ignoring second ":" if exists)
                    if len(splitted_addr)==2:
                        address[splitted_addr[1]] = tag.attrib['v']
                        
                # Check if the 'k' value contains ':'
                elif tag.attrib['k'].find(":")>-1:
                    # Split the string and store the key/value pairs
                    # (Ignoring second ":" if exists)
                    splitted_tag = tag.attrib['k'].split(":")
                    additional_tag[splitted_tag[0]][splitted_tag[1]] = \
                                                                tag.attrib['v']
                                                    
                else:
                    # Store any others second level 'tags' which is not 
                    # 'addr' or contain ':'
                    if tag.attrib['k'] not in node.keys():
                        node[tag.attrib['k']] = tag.attrib['v']
        
        # Iterate the second level 'nd'                                       
        for tag in element.iter("nd"):
            node_refs.append(tag.attrib['ref'])
            
        # The following code add all the dictionaries which are not empty
        if created:    
            node["created"] = created
            
        if position:
            node["pos"] = [position["lat"], position["lon"]]
            
        # For 'address' dictionary, update the street names and postal codes
        # first before adding
        if address:
            if 'street' in address.keys():
                address["street"] = \
                    update_street_name(address["street"], street_mapping)   
                
            if 'postcode' in address.keys():
                address["postcode"] = \
                    update_postcode(address["postcode"],created['user'] ) 
                
            node["address"] = address
    
        if additional_tag:
            for key in additional_tag.keys():
                node[key] = additional_tag[key]
    
        if node_refs:
            node["node_refs"] = node_refs
        
        return node

    else:
        return None

#%%

def process_map(file_in, pretty = False):
    '''
    This function converts the list of dictionaries to an output JSON file
    '''
    # You do not need to change this file
    file_out = "{0}.json".format(file_in.split('.')[0])
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

#%%
if __name__ == "__main__":
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    
    OSMFILE = "sample.osm"
    
    data = process_map(OSMFILE, True)
    print("\nJSON file created")
    #pprint.pprint(data)
    
    
    
    
    
    
    
    
    
    
    
    
    