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
from functions import csv_to_dataframe
from functions import get_unique_term
from functions import get_mapping

def main():

    #import query traits as pandas dataframe
    #query_file = 'table2.csv' #file
    #query_file = 'SNPedia-2015-1122.unix.csv'
    query_file = 'snpedia_sample.csv'
    query_df = csv_to_dataframe(query_file)
    query_df.drop(query_df.ix[:,'Unnamed: 14':'Unnamed: 25'].columns, axis=1, inplace=True)
    #declare variable for query trait name column header
    tn_header = 'trait_name'

    #drop duplicates to get unique trait names only
    unique_trait_name = get_unique_term(query_df, tn_header)

    #web service URL
    REST_URL = "http://data.agroportal.lirmm.fr"
    api_key = "d56a0880-f2ae-4a1e-a80d-a538e9027558"
    #row count for query trait
    row = 1
    match = 0
    no_match = 0
    #do the API call for each trait
    #for text_to_annotate in query_df[tn_header]:
    mapping_output = open('mapping2.csv', 'w')
    for row in query_df.itertuples():
        #print (row)
        text_to_annotate = row[12]
        #text_to_annotate
    #for text_to_annotate in query_df[tn_header]:
    #for text_to_annotate in unique_trait_name:
        annotations = get_json(REST_URL + "/annotator?&ontologies=CO_320&whole_word_only=true&text=" + \
            urllib2.quote(text_to_annotate)) 
        id_pref = get_mapping(annotations)
        #print id_pref
        if id_pref is None:
            query_df['CO_ID'] = ''
            query_df['CO_name'] = ''
        else:
            query_df['CO_ID'] = id_pref[32:46]
            query_df['CO_name'] = id_pref[47:]
    output = query_df.to_csv(index=False)
    mapping_output.write(output)
        #if id_pref is None:
            #mapping_output.write(+ "\t" + text_to_annotate + "\t\t\t" + "no match" + "\n")
            #mapping_output.write("Term " + str(row) + "\t" + text_to_annotate + "\t\t\t" + "no match" + "\n")
        #elif text_to_annotate in id_pref:
        #    mapping_output.write("Term " + str(row) + "\t" + text_to_annotate + "\t" + id_pref + "\t" + "exact match""\n") 
        #row = row + 1

if __name__ == '__main__':
    main()
