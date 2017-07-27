#!/usr/bin/env python

import argparse
import pandas as pd
import urllib2
import sys
from annotate_text import get_json
from annotate_text import print_annotations
from functions import csv_to_dataframe
from functions import get_unique_term
from functions import get_mapping

REST_URL = "http://data.agroportal.lirmm.fr"
API_KEY = "d56a0880-f2ae-4a1e-a80d-a538e9027558"

def main():    

    parser = argparse.ArgumentParser(description='Provide Crop Ontology IDs for a list of traits.')
    parser.add_argument('infile', nargs='?')
    args = parser.parse_args()
    query_file = args.infile
    #TODO add error checking if file is missing  
  
    query_df = csv_to_dataframe(query_file)
    #TODO add function to read csv, tab or excel as input file
    query_df.dropna(axis=1, how='all', inplace=True)
    query_df.dropna(axis=0, how='all', inplace=True)
    #declare variable for query trait name column header
    tn_header = 'trait_name'

    #drop duplicates to get unique trait names only
    unique_trait_name = get_unique_term(query_df, tn_header)

    #get info from web service for each trait
    mapping_list = []
    
    for row in query_df.itertuples():
        text_to_annotate = row[12]
        #TODO automatically extract column number for trait name
        annotations = get_json(REST_URL + "/annotator?&ontologies=CO_320&whole_word_only=true&text=" + 
                               urllib2.quote(text_to_annotate)) 
        id_pref = get_mapping(annotations)
        #extract values and save into list 
        if id_pref is None:
            mapping_list.append('') 
        else:
            co_id = id_pref[0].replace('http://www.cropontology.org/rdf/','')
            co_name = id_pref[1]
            mapping_list.append([co_id, co_name])
    
    #merge query and mapping dataframes
    column_label = ['CO_ID', 'CO_name']
    mapping_df = pd.DataFrame.from_records(mapping_list, columns=column_label)
    merged_df = pd.concat([query_df, mapping_df], axis=1)
    
    #print merged df to file
    print_output = open('mapping3.csv', 'w')
    output = merged_df.to_csv(index=False)
    print_output.write(output)

if __name__ == '__main__':
    main()
