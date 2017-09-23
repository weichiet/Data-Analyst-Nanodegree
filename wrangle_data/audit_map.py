import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint

# The list of possible street keywords in Singapore map
expected_street= ["Street", "Avenue", "Boulevard", "Central", "Circle", "Close", "Crescent", 
            "Court", "Drive", "Grove", "Heights", "Jalan", "Park", "Place", 
            "Square", "Loop", "Lane", "Link", "Lorong", 
            "Road",  "Taman", "Terrace",  "Trail", "View", "Walk", "Way" ]

def is_street_name(elem):
    '''
    Check if current tag attribute is an address street.
    '''
    return (elem.attrib['k'] == "addr:street")

def compare_street_name(street_types, street_name):
    '''
    This function checks if the street name contains any of the defined possible keywords.
    If no, the street name is stored in a dictionary with the last word
    of the street name as the key.    
    '''
    if not list(set(street_name.split()).intersection(set(expected_street))):
        street_types[street_name.split()[-1]].add(street_name)
       
def audit_street_name(osmfile):
    '''
    This function audits the street name in the address tags of the map to find 
    possible problematic street name.
    '''
    osm_file = open(osmfile, "r", encoding='utf-8')
    street_types = defaultdict(set)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    compare_street_name(street_types, tag.attrib['v'])
                    
    osm_file.close()
    return street_types

#%%

def is_postcode(elem):
    '''
    Check if current tag attribute is a postal code.
    '''
    return (elem.attrib['k'] == "addr:postcode")

def compare_postcode(user_postcodes, postcode, user, street_name):
    '''
    This function checks whether the postal code is 6 digits.  
    If the postal code is not 6 digits, the postal code is stored in 
    a dictionary with the user name as the key.
    '''
    if len(postcode)!=6:
        user_postcodes[user].add(postcode)    
        
        # Print the streetname along with the postal code
        print(street_name + ": " + postcode)

def audit_postcode(osmfile):
    '''
    This function audits the postal code in the address tags of the map to find 
    incorrect postal code.
    '''
    osm_file = open(OSMFILE, "r", encoding='utf-8')
    user_postcodes = defaultdict(set)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    street_name = tag.attrib['v']
                if is_postcode(tag):
                    compare_postcode(user_postcodes, tag.attrib['v'],
                                     elem.attrib['user'], street_name)    

    return user_postcodes

#%%
if __name__ == "__main__":
    OSMFILE = "sample.osm"
    
    # Audit the street name
    st_types = audit_street_name(OSMFILE)
    pprint.pprint(dict(st_types))
    
    print("\n")
    
    # Audit the postal code
    user_postcodes = audit_postcode(OSMFILE)
    pprint.pprint(dict(user_postcodes))









