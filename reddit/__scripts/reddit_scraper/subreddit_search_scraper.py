#!/usr/bin/python

import os, sys, time
import requests
from datetime import datetime
import json
import pandas as pd
import praw 


## Add credentials.py script to .gitignore list to keep personal keys safe. ##
from reddit_scraper.credentials import *



## Datetime Snapshot ##
snapshotdate = datetime.today().strftime('%d-%b-%Y')
snapshotdatetime = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')


## Subreddit Search and Retrieve Post Scraper Function Using Reddit PRAW API ##
def praw_search_subreddit_activity(subreddit_list, search_query_list, category, post_type, post_limit=1000, sep='tab'):
    '''
    Function: 
    For each {subreddit} item in {subreddit_list},
    search for posts containing each {search_item} in {search_query_list}, and
    extract {post_limit} number of {post_type} posts (submissions + comments). 
    Write output as CSV to __posts/{category}/{subreddit} directory.
    
    Input Arguments: 
    subreddit_list: input type is (list) of (str) items.
    search_query_list: input type is (list) of (str) items.
    category: input type is (str) item.
    post_type: input type is (str) item, 'hot', 'new', 'top'.
    post_limit: input type is (int) between 1 - 1000 (1000 is max), or None.
    sep: input type is (str) item, 'tab' or 'comma'. Default = 'tab'.
    
    Output Dataset Headers: 
    ['created_unix_utc', 'created_datetime_pst', 'title', 'author', 'score', 'id', 'subreddit', 'url', 'body', 'num_comments', 'comments']
    
    Example: 
    praw_search_subreddit_activity(subreddit_list=['MachineLearning','datascience'], search_query_list=['language model', 'image model'], category='DataScience', sep='tab', post_type='hot', post_limit=1000)
    praw_search_subreddit_activity(subreddit_list=['alexa','amazonecho'], search_query_list=['notification', 'volume'], category='Amazon', sep='comma', post_type='new', post_limit=1000)
    
    '''
    
    try: 
        if type(subreddit_list) != list:
            raise TypeError 
        if all(isinstance(item, str) for item in subreddit_list) != True:
            raise TypeError
        if type(category) != str:
            raise TypeError 
        if post_type not in ['hot', 'new', 'top']:
            raise TypeError 
        if type(search_query_list) != list:
            raise TypeError 
        if all(isinstance(item, str) for item in search_query_list) != True:
            raise TypeError
        if post_limit > 1000:
            raise TypeError
        if sep not in ['comma','tab']:
            raise TypeError
    
        if sep=='tab': 
            sep='\t'
        if sep =='comma':
            sep=','
    
        ## Establish Reddit Connection ##
        reddit = praw.Reddit(client_id= my_client_id, client_secret= my_client_secret, user_agent= my_user_agent)
        
        ##Iterate over items in subreddit_list.
        for subreddit in subreddit_list:
            try:
                ## Print task initialization message.
                print(f'\nGathering "{post_type}" posts from Subreddit: "{subreddit}"...')
                ## Create output directory.
                os.makedirs(f"../__data/__posts/{category}/{subreddit}", exist_ok=True)
                ##Iterate over search items in search_query_list.
                posts = []
                for search_item in search_query_list:
                    try:
                        ## Print task status message.
                        print(f'Gathering "{post_type}" posts for search item: "{search_item}" in "{subreddit}" Subreddit...')
                        ## Extract subreddit posts (submissions and comments).
                        sub_posts = reddit.subreddit(subreddit).search(search_item, sort=post_type, limit=post_limit)
                        for post in sub_posts:
                            ## Transform unix datetime to PST, and append to DataFrame.
                            created_pst = datetime.fromtimestamp(post.created_utc).strftime('%d-%b-%Y %H:%M:%S')
                            comments = []
                            submission = reddit.submission(id=post.id)
                            submission.comments.replace_more(limit=None)
                            for comment in submission.comments.list():
                                comments.append(f'{comment.author}: {comment.body}')
                            ## Transform posts data to pandas DataFrame.
                            posts.append([post.created_utc, created_pst, post_type, search_item, post.subreddit, post.id, post.title, post.author, post.score, post.url, post.selftext, post.num_comments, comments])
                            post_df = pd.DataFrame(posts,columns=['created_unix_utc', 'created_datetime_pst', 'post_type', 'search_item', 'subreddit', 'id', 'title', 'author', 'score', 'url', 'body', 'num_comments', 'comments'])
                            ## Write DataFrame as CSV to output directory.
                            post_df.to_csv(f'../__data/__posts/{category}/{subreddit}/{subreddit}_subreddit_search_{post_type}_posts_{snapshotdatetime}.csv', index=False, sep=sep)
                    except ValueError: 
                        print(f"Error occured while querying '{search_item}' in Subreddit: {subreddit}. Skipping... ")
                        continue
            except ValueError: 
                print(f"Error occured while gathering posts from from Subreddit: {subreddit}. Skipping... ")
                continue
        ## Print task completion message.
        print('Task is Complete!')
        time.sleep(5)
    except TypeError:
        print(f'\nOh no! Seems there is an issue with the input values:\n\n   Subreddit List: {subreddit_list}\n   Search Query List: {search_query_list}\n   Category: {category}\n   Post Type: {post_type}\n   Post Limit: {post_limit}')
        print('\nPlease correct your input values, and try again.\n')
    finally: 
        sys.exit(1)


## Subreddit Search and Retrieve Post Scraper Function Using Pushshift API ##
def pushshift_search_subreddit_activity(subreddit_list, search_query_list, category, before_days='0d', post_limit=1000, sep='tab'):
    '''
    Function: 
    For each {subreddit} item in {subreddit_list}, 
    extract {post_limit} number of posts (submissions + comments). 
    Write output as CSV to __data/__posts/subreddits/{category}/{subreddit} directory.
    
    Input Arguments: 
    subreddit_list: input-type is (list) of (str) items.
    search_query_list: input-type is (list) of (str) items.
    category: input-type is (str), for use as an output directory name.
    before_days: input-type is (str) number of days, between 0 and 100 (e.g., '10d'), trailing {snapshotdate}. Default = '0d'.
    post_limit: input type is (int), between 1 - 1000 (1000 is max). Default = 1000.
    sep: input type is (str) item, 'tab' or 'comma'. Default = 'tab'.

    Example: 
    pushshift_search_subreddit_activity(subreddit_list=['MachineLearning','datascience'], search_query_list=['image model','language model'],category='DataScience', before_days='90d', post_limit=1000)
    pushshift_search_subreddit_activity(subreddit_list=['alexa','amazonecho'], search_query_list=['notification','volume'],category='Amazon', before_days='90d', post_limit=1000)
    
    '''

    subreddit_list = subreddit_list
    search_query_list = search_query_list
    category = category
    before_days = before_days
    output_size = post_limit
    sep = sep
    
    try: 
        if type(subreddit_list) != list:
            raise TypeError 
        if all(isinstance(item, str) for item in subreddit_list) != True:
            raise TypeError
        if type(category) != str:
            raise TypeError 
        if before_days.endswith('d') != True:
            raise TypeError 
        if type(search_query_list) != list:
            raise TypeError 
        if all(isinstance(item, str) for item in search_query_list) != True:
            raise TypeError
        if output_size > 1000:
            raise TypeError
        if sep not in ['comma','tab']:
            raise TypeError
    
        if sep=='tab': 
            sep='\t'
        if sep =='comma':
            sep=','

        ##Iterate over items in subreddit_list.
        for subreddit in subreddit_list: 
            try:
                ## Print task initialization message.
                print(f'Gathering {before_days}-trailing posts for Subreddit: "{subreddit}"...')
                subreddit_s_df = pd.DataFrame()
                #subreddit_c_df = pd.DataFrame()
                for search_item in search_query_list: 
                    try: 
                        ## Print task status message.
                        print(f'Querying "{search_item}" in Subreddit: "{subreddit}"...')
                        ## Load submissions from {subreddit} using Pushshift API.
                        submissions = json.loads(requests.get(f'https://api.pushshift.io/reddit/search/submission?subreddit={subreddit}&before={before_days}&size={output_size}&q={search_item}&sort=created_utc&metadata=false').text or '{}' or '' or '[]' or 'None' or None)
                        ## Transform data.json to pandas DataFrame.
                        subreddit_submissions_df = pd.DataFrame(submissions['data'])
                        ## Check if query returned results.
                        if not subreddit_submissions_df.empty: 
                            ## Create output directory.
                            os.makedirs(f"../__data/__posts/test/subreddits/{category}/{subreddit}", exist_ok=True)
                            ## Add column denoting search item used in subreddit query and append to DataFrame.
                            subreddit_submissions_df['search_item'] = f'{search_item}'
                            ## Transform unix datetime to PST, and append to DataFrame.
                            if 'created_utc' in subreddit_submissions_df:
                                submission_created_pst = [datetime.fromtimestamp(item).strftime('%d-%b-%Y %H:%M:%S') for item in subreddit_submissions_df.created_utc]
                                subreddit_submissions_df['created_pst'] = submission_created_pst
                            ## Concatenate DataFrames in a single DataFrame.
                            subreddit_s_df = pd.concat([subreddit_s_df,subreddit_submissions_df], ignore_index=True)
                            ## For each submission, gather comment thread. 
                            ### API is currently broken (23 February 2023) ###
                            #for submission_id in subreddit_submissions_df['id']:
                            #    comments = json.loads(requests.get(f'https://api.pushshift.io/reddit/search/comment?subreddit={subreddit}&link_id={submission_id}&metadata=false').text or '{}' or '' or '[]')
                            #    subreddit_comments_df = pd.DataFrame(comments['data'])
                            #    comments_created_pst = [datetime.fromtimestamp(item).strftime('%d-%b-%Y %H:%M:%S') for item in subreddit_comments_df.created_utc]
                            #    subreddit_comments_df['created_pst'] = comments_created_pst
                            #subreddit_c_df = pd.concat([subreddit_c_df,subreddit_comments_df], ignore_index=True)    
                        else: 
                            print(f'\t No results for "{search_item}" in {subreddit}...') 
                    except ValueError: 
                        print(f"Error occured while querying '{search_item}' in Subreddit: {subreddit}. Skipping... ")
                        continue
                ## Write DataFrame as CSV to output directory.
                subreddit_s_df.to_csv(f'../__data/__posts/test/subreddits/{category}/{subreddit}/{subreddit}_subreddit_search_submissions_{before_days}_{snapshotdatetime}.csv', index=False, sep=sep)
                #subreddit_c_df.to_csv(f'../__data/__posts/test/subreddits/{category}/{subreddit}/{subreddit}_subreddit_search_comments_{before_days}_{snapshotdatetime}.csv', index=False)
            except ValueError: 
                print(f"Error occured while gathering posts from from Subreddit: {subreddit}. Skipping... ")
                continue
        ## Print task completion message.
        print('Task is Complete!')
        time.sleep(5)
    except TypeError:
        print(f'\nOh no! Seems there is an issue with the input values:\n\n   Subreddit List: {subreddit_list}\n   Search Query List: {search_query_list}\n   Category: {category}\n   Before Days: {before_days}\n   Post Limit: {post_limit}')
        print('\nPlease correct your input values, and try again.\n')
    finally: 
        sys.exit(1)
        
