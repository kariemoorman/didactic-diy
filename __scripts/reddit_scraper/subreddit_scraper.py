#!/usr/bin/python

import os, sys
import requests
from datetime import datetime
import pandas as pd
import json
import praw 


## add credentials.py script to .gitignore list to keep personal keys safe. ##
from reddit_scraper.credentials import *

## Establish Reddit Connection ##
reddit = praw.Reddit(client_id= my_client_id, client_secret= my_client_secret, user_agent= my_user_agent)

## Datetime Snapshot ##
snapshotdate = datetime.today().strftime('%d-%b-%Y')
snapshotdatetime = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')


## Subreddit Post-Scraper Function Using PRAW ##
def praw_subreddit_activity(subreddit_list, category, post_type, post_limit, sep='tab'):
    '''
    Function:
    For each {subreddit} item in {subreddit_list}, 
    extract {post_limit} number of {post_type} posts (submissions + comments). 
    Write output as CSV to __posts/{category}/{subreddit} directory.
    
    Input Arguments: 
    subreddit_list: input type is (list) of (str) items.
    category: input type is (str) item, for use as an output directory name.
    post_type: input type is (str) item, 'hot', 'new', or 'top'.
    post_limit: input type is (int) between 1 - 1000 (1000 is max), or None.
    sep: input type is (str) item, 'tab' or 'comma'. Default = 'tab'.

    Output Dataset Headers: 
    ['created_unix_utc', 'created_datetime_pst', 'title', 'author', 'score', 'id', 'subreddit', 'url', 'body', 'num_comments', 'comments']
    
    Example: 
    praw_subreddit_activity(subreddit_list=['MachineLearning','datascience'], category='DataScience', post_type='hot', post_limit=1000)
    praw_subreddit_activity(subreddit_list=['alexa','amazonecho'], category='Amazon', post_type='new', post_limit=1000)
    
    '''
    ## To-Do: Add input validation checks. 
    post_limit = post_limit
    post_type = post_type 
    subreddit_items = subreddit_list
    category = category
    
    if sep=='tab': 
        sep='\t'
    if sep =='comma':
        sep=','

    ##Iterate over subreddit items in subreddit_list.
    for subreddit in subreddit_items: 
        ## Print task initialization message.
        print(f'Gathering {post_type} posts from Subreddit: "{subreddit}"...')
        ## Make output directories.
        os.makedirs(f"../__data/__posts/{category}/{subreddit}", exist_ok=True)
        ## Extract subreddit posts (submissions and comments).
        posts = []
        if post_type == 'new':
            sub_posts = reddit.subreddit(subreddit).new(limit=post_limit)
        elif post_type == 'hot':
            sub_posts = reddit.subreddit(subreddit).hot(limit=post_limit)
        elif post_type == 'top':
            sub_posts = reddit.subreddit(subreddit).top( limit=post_limit)
        for post in sub_posts:
            ## Transform unix datetime to PST.
            created_pst = datetime.fromtimestamp(post.created_utc).strftime('%d-%b-%Y %H:%M:%S')
            comments = []
            submission = reddit.submission(id=post.id)
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                    comments.append(f'{comment.author}: {comment.body}')
            ## Transform posts data to pandas DataFrame.
            posts.append([post.created_utc, created_pst, post_type, post.title, post.author, post.score, post.id, post.subreddit, post.url, post.selftext, post.num_comments, comments])
            post_df = pd.DataFrame(posts,columns=['created_unix_utc', 'created_datetime_pst', 'post_type', 'title', 'author', 'score', 'id', 'subreddit', 'url', 'body', 'num_comments', 'comments'])
            ## Write DataFrame as CSV to output directory.
            post_df.to_csv(f'../__data/__posts/{category}/{subreddit}/{subreddit}_subreddit_{post_type}_posts_{snapshotdatetime}.csv', index=False, sep=sep)
    ## Print task completion message.
    print('Task is Complete!')           



## Subreddit Post-Scraper Function Using Pushshift API ##
def pushshift_subreddit_activity(subreddit_list, category, before_days, post_limit, sep='tab'):
    '''
    Function:
    For each {subreddit} item in {subreddit_list}, 
    extract {post_limit} number of posts (submissions + comments). 
    Write output as CSV to __data/__posts/subreddits/{category}/{subreddit} directory.
    
    Input Arguments: 
    subreddit_list: input-type is (list) of (str).
    category: input-type is (str).
    before_days: input-type is (str) number of days, between 0 and 100 (e.g., '10d'), trailing {snapshotdate}.
    post_limit: input type is (int), between 1 - 1000 (1000 is max).
    sep: input type is (str) item, 'tab' or 'comma'. Default = 'tab'.
    
    Example: 
    pushshift_subreddit_activity(subreddit_list=['MachineLearning','datascience'], category='DataScience', before_days='90d', post_limit=1000)
    pushshift_subreddit_activity(subreddit_list=['alexa','amazonecho'], category='Amazon', before_days='90d', post_limit=1000)
    
    '''

    subreddit_list = subreddit_list
    category = category
    before_days = before_days
    output_size = post_limit
    
    if sep=='tab': 
        sep='\t'
    if sep =='comma':
        sep=','
    
    ##Iterate over items in subreddit_list.
    for subreddit in subreddit_list: 
        ## Print task initialization message.
        print(f'Gathering {before_days}-trailing posts for Subreddit: "{subreddit}"...')
        ## Load submissions and comments from {subreddit} using Pushshift API.
        submissions = json.loads(requests.get(f'https://api.pushshift.io/reddit/search/submission?subreddit={subreddit}&before={before_days}&size={output_size}&sort=created_utc&metadata=false').text or '{}' or '' or '[]' or 'None' or None)
        comments = json.loads(requests.get(f'https://api.pushshift.io/reddit/search/comment?subreddit={subreddit}&before={before_days}&size={output_size}&sort=created_utc&metadata=false').text or '{}' or '' or '[]' or 'None' or None)
        ## Create output directory.
        os.makedirs(f"../__data/__posts/test/subreddits/{category}/{subreddit}", exist_ok=True)
        ## Transform data.json to pandas DataFrame.
        subreddit_submissions_df = pd.DataFrame(submissions['data'])
        subreddit_comments_df = pd.DataFrame(comments['data'])
        ## Transform unix datetime to PST, and append to DataFrame.
        comments_created_pst = [datetime.fromtimestamp(item).strftime('%d-%b-%Y %H:%M:%S') for item in subreddit_comments_df.created_utc]
        subreddit_comments_df['created_pst'] = comments_created_pst
        submission_created_pst = [datetime.fromtimestamp(item).strftime('%d-%b-%Y %H:%M:%S') for item in subreddit_submissions_df.created_utc]
        subreddit_submissions_df['created_pst'] = submission_created_pst
        ## Write DataFrames as CSV to output directory.
        subreddit_comments_df.to_csv(f'../__data/__posts/test/subreddits/{category}/{subreddit}/{subreddit}_subreddit_comments_{before_days}_{snapshotdatetime}.csv', index=False, sep=sep) #sep='\t', encoding='utf-8'
        subreddit_submissions_df.to_csv(f'../__data/__posts/test/subreddits/{category}/{subreddit}/{subreddit}_subreddit_submissions_{before_days}_{snapshotdatetime}.csv', index=False, sep=sep) #sep='\t', encoding='utf-8'
    ## Print task completion message.
    print('Task is Complete!')
