#!/Users/jdetras/anaconda/bin/python
# ontology-mapper.py
# assign rice crop ontology IDs on trait names from a csv file
# Author: Jeffrey Detras
# Date: 07-21-2017

#import modules
import pandas as pd
import urllib2
import sys
from annotate_text import get_json
from annotate_text import print_annotations
from classes import csv_to_dataframe
from classes import get_unique_term
from classes import get_mapping

def main():

    #import query traits as pandas dataframe
    #query_file = 'table2.csv' #file
    query_file = 'SNPedia-2015-1122.unix.csv'
    query_df = csv_to_dataframe(query_file)
    
    #declare variable for query trait name column header
    tn_header = 'trait_name'

    #drop duplicates to get unique trait names only
    unique_trait_name = get_unique_term(query_df, tn_header)

    #web service URL
    REST_URL = "http://data.agroportal.lirmm.fr"
    api_key = "d56a0880-f2ae-4a1e-a80d-a538e9027558"
    #row count for query trait
    row = 1

    #do the API call for each trait
    #for text_to_annotate in query_df[tn_header]:
    for text_to_annotate in unique_trait_name:
        annotations = get_json(REST_URL + "/annotator?&ontologies=CO_320&whole_word_only=true&text=" + \
            urllib2.quote(text_to_annotate)) 
        id_pref = get_mapping(annotations)
        if id_pref is None:
            print "Term " + str(row) + "\t" + text_to_annotate + "\t" + "No match"
        else:
            print "Term " + str(row) + "\t" + text_to_annotate + "\t" + id_pref
        row = row + 1

if __name__ == '__main__':
    main()
