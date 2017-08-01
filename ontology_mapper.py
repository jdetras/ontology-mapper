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
    tn_header_index = query_df.columns.get_loc(tn_header) + 1
    
    #get mapping from unique trait names only
    unique_trait_name = get_unique_term(query_df, tn_header)
    unique_mapping_list = []

    for text_to_annotate in unique_trait_name:
        annotations = get_json(REST_URL + "/annotator?&ontologies=CO_320&whole_word_only=true&text=" +
                               urllib2.quote(text_to_annotate))
        print 'Running query on ' + text_to_annotate
        id_pref = get_mapping(annotations)
        if id_pref is None:
            unique_mapping_list.append('')
        else:
            co_id = id_pref[0].replace('http://www.cropontology.org/rdf/','')   
            co_name = id_pref[1]
            unique_mapping_list.append([co_id, co_name])
    #merge query and mapping dataframes
    print 'Merging query and mapping...'
    column_label = ['CO_ID', 'CO_name']
    unique_mapping_df = pd.DataFrame.from_records(unique_mapping_list, columns=column_label)
    unique_merged_df = pd.concat([unique_trait_name, unique_mapping_df], axis=1)
    
    #print merged df to file
    print 'Printing output file...'
    unique_output_file = 'unique_mapping_' + query_file 
    print_unique_output = open(unique_output_file, 'w')
    unique_output = unique_merged_df.to_csv(index=False)
    print_unique_output.write(unique_output)
    print 'Done.'
'''
    #get info from web service for each trait
    mapping_list = []
    
    for row in query_df.itertuples():
        text_to_annotate = row[tn_header_index]
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
    mapping_output_file = 'mapping_' + query_file
    print_output = open(mapping_output_file, 'w')
    output = merged_df.to_csv(index=False)
    print_output.write(output)
'''
if __name__ == '__main__':
    main()
