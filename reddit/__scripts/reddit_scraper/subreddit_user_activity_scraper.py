#!/usr/bin/python3

import os, sys, time
import requests
from datetime import datetime
from collections import Counter

import json
import pandas as pd

import praw

from reddit_scraper.credentials import *

## Datetime Snapshot ##
snapshotdate = datetime.today().strftime('%d-%b-%Y')
snapshotdatetime = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')


## Subreddit User Activity Scraper Function via Reddit PRAW API ##
def praw_find_commenters(subreddit_list, category, post_limit=1000,sep='comma'):
    '''
    Caution: Reddit's Praw script takes a very long time to run.
             Please consider using pushshift_find_commenters() instead.
    '''
    
    try: 
        if type(subreddit_list) != list:
            raise TypeError 
        if all(isinstance(item, str) for item in subreddit_list) != True:
            raise TypeError
        if type(category) != str:
            raise TypeError 
        if post_limit > 1000:
            raise TypeError
        if sep not in ['comma','tab']:
            raise TypeError
    
        if sep=='tab': 
            sep='\t'
        if sep =='comma':
            sep=','
        
        ## Reddit Connection ##
        reddit = praw.Reddit(client_id= my_client_id, client_secret= my_client_secret, user_agent= my_user_agent)
        
        for subreddit in subreddit_list: 
            print(f'Gathering users from Subreddit: "{subreddit}"...')
            users = []
            sub_posts = reddit.subreddit(subreddit).new(limit=post_limit)
            for post in sub_posts:
                created_pst = datetime.fromtimestamp(post.created_utc).strftime('%d-%b-%Y %H:%M:%S')
                commenters = []
                submission = reddit.submission(id=post.id)
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():
                        #print(comment.body, comment.author.name) 
                    commenters.append(f'{comment.author}')
                users.append([post.created_utc, created_pst, post.id, post.subreddit, post.url, post.author, commenters])
            #Write Results to CSV
            os.makedirs(f"../__users/subreddit_users/{category}/{subreddit}/{snapshotdate}/praw", exist_ok=True)
            post_df = pd.DataFrame(users,columns=['created_unix_utc', 'created_datetime_pst','id', 'subreddit', 'url', 'author', 'commenters'])
            post_df.to_csv(f'../__users/subreddit_users/{category}/{subreddit}/{snapshotdate}/praw/{subreddit}_subreddit_newposts_{snapshotdatetime}.csv', index=False, sep=sep, encoding='utf-8')  
            #Isolate Post Submitters and Commenters for Frequency Count
            submitter_list = Counter(list(post_df.author)).most_common()
            commenters_flattened = [item for sublist in list(post_df.commenters) for item in sublist]
            commenters_flattened_no_na = [i for i in commenters_flattened if i == i and i !='' and i !='None']
            commenter_list = Counter(commenters_flattened_no_na).most_common()
            #Restructure Username Frequency Results as Dictionary
            s=dict(submitter_list)
            c=dict(commenter_list)
            #Create DataFrame with Metadata
            commenters_output_df = pd.DataFrame({"query_date": snapshotdate, "subreddit": subreddit, "comment_author": c.keys(), "comment_frequency": c.values()})
            submitters_output_df = pd.DataFrame({"query_date": snapshotdate, "subreddit": subreddit, "submission_author": s.keys(), "submission_frequency": s.values()})
            #Write Frequency Results as CSV
            commenters_output_df.to_csv(f'../__data/__users/subreddit_users/{category}/{subreddit}/{snapshotdate}/praw/{subreddit}_username_commenters_{snapshotdatetime}.csv', index=False, sep=sep)
            submitters_output_df.to_csv(f'../__data/__users/subreddit_users/{category}/{subreddit}/{snapshotdate}/praw/{subreddit}_username_submitters_{snapshotdatetime}.csv', index=False, sep=sep)
        print("Task is Complete!")
        time.sleep(5)
    except TypeError:
        print(f'\nOh no! Seems there is an issue with the input values:\n\n   Subreddit List: {subreddit_list}\n   Category: {category}\n   Post Limit: {post_limit}')
        print('\nPlease check your input values, and try again.\n')
    finally: 
        sys.exit(1)



## Subreddit User Activity Scraper Function via Pushshift API ##
def pushshift_find_commenters(subreddit_list, category, before_days='0d', post_limit=1000, sep='comma'):
    '''
    For each {subreddit} item in {subreddit_list}, 
    extract user activity across {post_limit} number of posts (submissions + comments). 
    Write output as CSV to __users/subreddit_users/{category}/{subreddit} directory.
    
    Input Arguments: 
    subreddit_list: input type is (list) of (str).
    category: input type is (str), for use as an output directory name.
    before_days: input type is (str) number of days, between 0 and 100 (e.g., '10d'), trailing {snapshotdate}. Default = '0d'.
    post_limit: input type is (int), between 1 - 1000 (1000 is max). Default = 1000.
    sep: input type is (str) item, 'tab' or 'comma'. Default = 'comma'.

    
    Output Dataset Headers:
    Submissions: ["query_date", "before_date", "submission_author", "submission_frequency"]
    Comments: ["query_date", "before_date", "comment_author", "comment_frequency"]
    
    Example: 
    pushshift_find_commenters(subreddit_list=['MachineLearning','datascience'], category='DataScience', before_days='90d', post_limit=1000)
    pushshift_find_commenters(subreddit_list=['alexa','amazonecho'], category='Amazon', before_days='90d', post_limit=500)
    
    '''
    
    try: 
        if type(subreddit_list) != list:
            raise TypeError 
        if all(isinstance(item, str) for item in subreddit_list) != True:
            raise TypeError
        if type(category) != str:
            raise TypeError 
        if before_days.endswith('d') != True:
            raise TypeError 
        if post_limit > 1000:
            raise TypeError
        if sep not in ['comma','tab']:
            raise TypeError

        if sep=='tab': 
            sep='\t'
        if sep =='comma':
            sep=','

        print(f'Finding subreddit users from Subreddit List:\n "{subreddit_list}"...')
        for subreddit in subreddit_list: 
            print(f"Gathering {output_size} '{before_days}-trailing' posts from Subreddit: '{subreddit}'...")
            os.makedirs(f"../__data/__users/subreddit_users/{category}/{subreddit}/{snapshotdate}/ps", exist_ok=True)
            try:
                submissions = json.loads(requests.get(f'https://api.pushshift.io/reddit/search/submission?subreddit={subreddit}&before={before_days}&size={output_size}&sort=created_utc&metadata=false').text)
                comments = json.loads(requests.get(f'https://api.pushshift.io/reddit/search/comment?subreddit={subreddit}&before={before_days}&size={output_size}&sort=created_utc&metadata=false').text)

                submissions_df = pd.DataFrame(submissions['data'])
                comments_df = pd.DataFrame(comments['data'])

                output_submissions_list = Counter(list(submissions_df.author)).most_common()
                output_comments_list = Counter(list(comments_df.author)).most_common()

                s=dict(output_submissions_list)
                c=dict(output_comments_list)

                comment_output_df = pd.DataFrame({"query_date": snapshotdate, "before_date": before_days,"subreddit": subreddit, "comment_author": c.keys(), "comment_frequency": c.values()})
                submission_output_df = pd.DataFrame({"query_date": snapshotdate, "before_date": before_days,"subreddit": subreddit, "submission_author": s.keys(), "submission_frequency": s.values()})

                comment_output_df.to_csv(f'../__data/__users/subreddit_users/{category}/{subreddit}/{snapshotdate}/ps/{subreddit}_subreddit_commenters_{before_days}_{snapshotdatetime}.csv', index=False, sep=sep)
                submission_output_df.to_csv(f'../__data/__users/subreddit_users/{category}/{subreddit}/{snapshotdate}/ps/{subreddit}_subreddit_submitters_{before_days}_{snapshotdatetime}.csv', index=False, sep=sep)
            except ValueError: 
                print(f"Error occured while gathering '{before_days}-trailing' posts from Subreddit: {subreddit}. Skipping... ")
                continue
        time.sleep(5)
        print("Task is Complete!")
    except TypeError:
        print(f'\nOh no! Seems there is an issue with the input values:\n\n   Subreddit List: {subreddit_list}\n   Category: {category}\n   Post Limit: {output_size}\n   Before Days: {before_days}')
        print('\nPlease check your input values, and try again.\n')
    finally: 
        sys.exit(1)
            



def extract_subreddit_user_activity(subreddit_list, category, api='pushshift', before_days='0d', post_limit=1000, sep='comma'): 
    
    try: 
        if api not in ['pushshift','praw']:
            raise TypeError
    
        if api == 'pushshift':
            try:
                pushshift_find_commenters(subreddit_list, category, before_days, post_limit, sep)
            except Exception: 
                print(f"Error occured while gathering Reddit users...")
        
        if api == 'praw':
            print('\nCaution... Reddit Praw API is slow. This could take a while...\n')
            try:
                praw_find_commenters(subreddit_list, category, post_limit, sep)
            except Exception: 
                print(f"Error occured while gathering Reddit users...")    
    
    except TypeError:
        print(f'\nOh no! Seems there is an issue with the input values.\n\n API: {api}.')
        print('\nPlease check your input values, and try again.\n')
    
    finally: 
        sys.exit(1)
    
    

if __name__ == "__main__":
    extract_subreddit_user_activity()
