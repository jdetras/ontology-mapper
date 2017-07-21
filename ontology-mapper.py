#!/Users/jdetras/anaconda/bin/python

import pandas as pd

#import trait dictionary 
td_file = '/Users/jdetras/scripts/ontology-mapper/TD_CO_320_Rice_EN_v5_v160323.csv'
td = pd.read_csv(td_file, sep=',', header=0)
td_df = pd.DataFrame(td)
#print td_df

#copy trait ID and trait name into a new dataframe
trait_name = td_df[['Trait ID', 'Trait name']].copy()

#drop duplicate entries for the traits
trait_name.drop_duplicates(keep=False, inplace=True)
#trait_name = trait_name[ 'Trait name'].str.lower()
print trait_name

#import query traits for annotation
query_file = '/Users/jdetras/scripts/ontology-mapper/table.csv'
query = pd.read_csv(query_file, sep=',', header=0)
query_df = pd.DataFrame(query)
#print query_df

#for row in trait_name.itertuples():
    #print (row)
 #   print query_df.loc[query_df['trait_name'].isin(trait_name['Trait name'])]

#for row in trait_name:
#    print (row)

#print query_df.loc[query_df['trait_name'] == trait_name.loc[trait_name['Trait name']

#for column in query_df:
#	print (column)

#for trait_name, query_trait_name in test.itertuples(index=False):
#    print a, b
