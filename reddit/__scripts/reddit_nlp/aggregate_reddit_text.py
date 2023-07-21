#!/usr/bin/python3

import os 
import re
from datetime import datetime, date
import json
import glob
import pandas as pd

## Reddit Dataset Aggregation Function ## 
def aggregate_reddit_data(df_filepath, column_list, category, subreddit_name):
    '''
    Specify a {df_filepath} pointing to a set of {subreddit_name} dataFrames. 
    Aggregate datasets using glob. 
    Write aggregated dataset as CSV to __aggregated_posts/{subreddit_name} directory. 
    For each {column} in {column_list}, convert {column} values to list. 
    Write list as JSON to __aggregated_posts/{subreddit_name} directory.
    
    Input Arguments: 
    df_filepath: input type is (str) item, denoting filepath. 
    column_list: input-type is (list) of (str) items.
    subreddit_name: input type is (str) item.
    
    Example: 
    datascience_filepath = 'reddit/__data/__posts/DataScience/MachineLearning'
    column_list = ['title', 'body', 'comments']
    subreddit_name = 'MachineLearning'
    category = 'DataScience'
    aggregate_reddit_data(datascience_filepath, column_list, category, subreddit_name)
    
    '''
    snapshotdate = datetime.today().strftime('%d-%b-%Y') 
    snapshotdatetime = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')
    
    dfs = glob.glob(f'{df_filepath}/*.csv')
    agg_df = pd.concat([pd.read_csv(fp, header=0) for fp in dfs], ignore_index=True)
    os.makedirs(f"../__data/__aggregated_posts/{category}/{subreddit_name}/raw/{snapshotdate}/{subreddit_name}_data", exist_ok=True)
    print(f'Saving aggregated DataFrame to: __aggregated_posts/{subreddit_name} ...')
    agg_df.to_csv(f'../__data/__aggregated_posts/{category}/{subreddit_name}/raw/{snapshotdate}/{subreddit_name}_agg_data/{subreddit_name}_agg_df_{snapshotdatetime}.csv', index=False)
    for column in column_list: 
        os.makedirs(f"../__data/__aggregated_posts/{category}/{subreddit_name}/raw/{snapshotdate}/{subreddit_name}_{column}_data", exist_ok=True)
        column_ls = agg_df[column].to_list()
        with open(f'../__data/__aggregated_posts/{category}/{subreddit_name}/raw/{snapshotdate}/{subreddit_name}_{column}_data/{subreddit_name}_{column}_agg_{snapshotdatetime}.json', 'w') as f:
            json.dump(column_ls, f, indent=2) 



if __name__ == "__main__":
    aggregate_reddit_data()
