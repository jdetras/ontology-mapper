#!/usr/bin/env python

import argparse
import pandas as pd

def csv_to_dataframe(filename):
    table = pd.read_csv(filename, sep=',', header=0)
    df = pd.DataFrame(table)
    return df;

def main():
    #load input query and mapping files
    print 'Loading query and mapping files...'
    parser = argparse.ArgumentParser(description='Provide Crop Ontology IDs to a table of traits')
    parser.add_argument('query_file', nargs='?')
    parser.add_argument('mapping_file', nargs='?')
    args = parser.parse_args()
    query_file = args.query_file
    mapping_file = args.mapping_file

    #create dataframes
    print 'Creating dataframes...'
    query_df = csv_to_dataframe(query_file)
    mapping_df = csv_to_dataframe(mapping_file)

    #drop empty columns
    query_df.dropna(axis=1, how='all', inplace=True)
    query_df.dropna(axis=0, how='all', inplace=True)
    
    mapping_df.dropna(axis=1, how='all', inplace=True)
    mapping_df.dropna(axis=0, how='all', inplace=True)
   
    #declare variable for trait name header
    query_trait_header = 'trait_name'
    mapping_trait_header = 'trait_name'

    query_df[query_trait_header] = query_df[query_trait_header].str.lower()
    #map terms
    print 'Mapping terms...'
    merged_df = query_df.merge(mapping_df, left_on=query_trait_header, right_on=mapping_trait_header, how='outer')
    
    #print output file
    print 'Writing output file...'
    output_file = 'mapping_' + query_file + '_' + mapping_file + '.csv'
    print_output = open(output_file, 'w')
    print_output.write(merged_df.to_csv(index=False))
    print 'Done.' + 'Output file is ' + output_file
 
if __name__ == '__main__':
    main()
