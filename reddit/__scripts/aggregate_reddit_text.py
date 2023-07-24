#!/usr/bin/python3

import os
from datetime import datetime, date
import json
import glob
import argparse
import pandas as pd
import argparse


class RedditDataAggregator:
    def __init__(self, df_filepath, subreddit_name, category, text_column_list=['title', 'body', 'comments'], output_format='csv'):
        self.df_filepath = df_filepath
        self.text_column_list = text_column_list
        self.category = category
        self.subreddit_name = subreddit_name
        self.output_format = output_format.lower()

        self.snapshotdate = datetime.today().strftime('%d-%b-%Y') 
        self.snapshotdatetime = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')

    def aggregate_reddit_data(self):
        '''
        Specify a {df_filepath} pointing to a set of {subreddit_name} dataFrames. 
        Aggregate datasets using glob. 
        Write aggregated dataset as CSV/JSON/Parquet to __aggregated_posts/{subreddit_name} directory. Default = 'csv.'
        For each {column} in {text_column_list}, convert {column} values to list. 
        Write list as JSON to __aggregated_posts/{subreddit_name} directory.
        '''


        dfs = glob.glob(f'{self.df_filepath}/*.csv')
        agg_df = pd.concat([pd.read_csv(fp, header=0, encoding="utf-8", engine='python', sep=None) for fp in dfs], ignore_index=True)
        os.makedirs(f"../__data/__aggregated_posts/{self.category}/{self.subreddit_name}/raw/{self.snapshotdate}/{self.subreddit_name}_agg_data", exist_ok=True)
        print(f'Saving aggregated DataFrame to: __aggregated_posts/{self.subreddit_name} ...')

        output_file_path = f'../__data/__aggregated_posts/{self.category}/{self.subreddit_name}/raw/{self.snapshotdate}/{self.subreddit_name}_agg_data/{self.subreddit_name}_agg_df_{self.snapshotdatetime}'
        
        #Option to write aggregated dataset as JSON, PARQUET or CSV.
        if self.output_format == 'json':
            output_file_path += '.json'
            agg_df.to_json(output_file_path, index=False, orient='records', lines=True)
        elif self.output_format == 'parquet':
            output_file_path += '.parquet'
            agg_df.to_parquet(output_file_path, index=False)
        else:
            output_file_path += '.csv'
            agg_df.to_csv(output_file_path, index=False)

        for column in self.text_column_list: 
            os.makedirs(f"../__data/__aggregated_posts/{self.category}/{self.subreddit_name}/raw/{self.snapshotdate}/{self.subreddit_name}_{column}_data", exist_ok=True)
            column_ls = agg_df[column].to_list()
            with open(f'../__data/__aggregated_posts/{self.category}/{self.subreddit_name}/raw/{self.snapshotdate}/{self.subreddit_name}_{column}_data/{self.subreddit_name}_{column}_agg_{self.snapshotdatetime}.json', 'w', encoding='utf-8') as f:
                json.dump(column_ls, f, indent=2) 

def main():
    parser = argparse.ArgumentParser(description='Aggregate Reddit data from DataFrames.')
    parser.add_argument('df_filepath', type=str, help='Path to the input DataFrames.')
    parser.add_argument('--subreddit_name', '-s', type=str, help='Name of the subreddit.')
    parser.add_argument('--category', '-c', type=str, help='Category name.')
    parser.add_argument('--text_columns', '-t', type=str, nargs='+', default=['title', 'body', 'comments'], help='List of columns to aggregate. Default is ["title", "body", "comments"].')
    parser.add_argument('--output_format', '-o', choices=['json', 'parquet', 'csv'], default='csv', help='Output file format. Choices: json, parquet, csv. Default is csv.')
    args = parser.parse_args()

    aggregator = RedditDataAggregator(args.df_filepath, args.subreddit_name, args.category, args.text_columns, args.output_format)
    aggregator.aggregate_reddit_data()


if __name__ == "__main__":
  main()
