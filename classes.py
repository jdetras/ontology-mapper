#!/usr/bin/python

import pandas as pd
import urllib2
import json

api_key = "d56a0880-f2ae-4a1e-a80d-a538e9027558"

#convert csv file into a dataframe
#takes first row as header
def csv_to_dataframe(query_file):
    query = pd.read_csv(query_file, sep=',', header =0)
    query_df = pd.DataFrame(query)
    return query_df;

#get unique terms or keywords from specified dataframe column
def get_unique_term(query_df, column_header):
    unique_term = query_df[column_header].copy().str.lower()
    unique_term.drop_duplicates(keep='first', inplace=True)
    return unique_term;

def get_json(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + api_key)]
    return json.loads(opener.open(url).read())

#print a tabular format search_term, ontology_id, ontology_term
def get_mapping(annotations, get_class=True):
    for result in annotations:
       class_details = get_json(result["annotatedClass"]["links"]["self"]) if get_class else result["annotatedClass"]
       class_id = class_details["@id"]
       class_pref = class_details["prefLabel"]
       return class_id + "\t" + class_pref
       #print search_term + "\t" + class_details["@id"] + "\t" + class_details["prefLabel"]
