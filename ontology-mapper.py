#!/Users/jdetras/anaconda/bin/python
# ontology-mapper.py
# assign rice crop ontology IDs on trait names from a csv file
# Author: Jeffrey Detras
# Date: 07-21-2017

#import modules
import pandas as pd
import urllib2
from annotate_text import get_json
from annotate_text import print_annotations

#import query traits as pandas dataframe
query_file = 'table2.csv' #file
query = pd.read_csv(query_file, sep=',', header=0)
query_df = pd.DataFrame(query)

#declare variable for query trait name column header
tn_header = 'trait_name'

#web service URL
REST_URL = "http://data.agroportal.lirmm.fr"

#row count for query trait
row = 1

#do the API call for each trait
for text_to_annotate in query_df[tn_header]:
    annotations = get_json(REST_URL + "/annotator?&ontologies=CO_320&text=" + urllib2.quote(text_to_annotate)) 
    #print query trait, row and annotation from web service call
    print 'Query trait: ' + str(row) + ' : ' + text_to_annotate
    print_annotations(annotations)
    row = row + 1
