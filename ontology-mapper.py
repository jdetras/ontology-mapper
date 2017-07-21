#!/Users/jdetras/anaconda/bin/python
# ontology-mapper.py
# assign rice crop ontology IDs on trait names from a csv file
# Author: Jeffrey Detras
# Date: 07-21-2017

#import modules
import sys
import getopt
import pandas as pd

#import trait dictionary as a dataframe
td_file = 'TD_CO_320_Rice_EN_v5_v160323.csv'
td = pd.read_csv(td_file, sep=',', header=0)
td_df = pd.DataFrame(td)
#print td_df

#copy trait ID and trait name into a new dataframe
td_trait_header = 'Trait name'
td_trait_id = 'Trait ID'
trait_name = td_df[[td_trait_id, td_trait_header]].copy()

#drop duplicate entries for the traits
trait_name.drop_duplicates(keep=False, inplace=True)
#print trait_name

#import query traits for annotation
query_file = 'table.csv'
query = pd.read_csv(query_file, sep=',', header=0)
query_df = pd.DataFrame(query)
#print query_df

#assign variable for query trait name column header
tn_header = 'trait_name'

#search for exact match for trait_name in query_df
## currently working for exact match

for row in trait_name.itertuples():
    print query_df.loc[query_df[tn_header].isin(trait_name[td_trait_header])]
