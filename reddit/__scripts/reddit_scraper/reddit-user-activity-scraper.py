#!/usr/bin/python

import os, sys, time
from datetime import datetime
import praw 
import pandas as pd

## Add credentials.py script to .gitignore list to keep personal keys safe. ##
from reddit_scraper.credentials import *


## Date and Datetime Snapshot ##
snapshotdate = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')


## Reddit User Activity Scraper Function ## 
def extract_user_activity(username_list, post_type='new', post_limit=1000, sep='tab'):
    '''
    Function:
    For {username} in {username_list}, 
    extract {username} {post_type} post activity (new/hot submissions and comments) across Reddit.
    Write output as CSV to __data/__users/users/{username} directory.
    
    Input Arguments: 
    username_list: input type is (list) of (str) items.
    post_limit: input type is (int) between 1 - 1000 (1000 is max), or None.
    post_type: input type is (str), either 'new' or 'hot'.
    sep: input type is (str) item, 'tab' or 'comma'. Default = 'tab'.

    Output Dataset Headers:
    Comments: ['created_unix_utc', 'created_pst', 'post_type', 'commenter_name', 'subreddit', 'comment', 'reddit_permalink']
    Submissions: ['created_unix_utc', 'created_pst', 'post_type', 'username', 'subreddit', 'id', 'title', 'body', 'num_comments', 'submission_comments', 'reddit_permalink']
    
    Example: 
    extract_user_activity(username_list=['dojoteef','kunjaan'], post_limit=10, post_type='new')
    
    '''
    
    if sep=='tab': 
        sep='\t'
    if sep =='comma':
        sep=','
        
    ## Establish Reddit Connection ##
    reddit = praw.Reddit(client_id= my_client_id, client_secret= my_client_secret, user_agent= my_user_agent)

    ## Extract User Submissions and Comments.
    for username in username_list: 
        comments = []
        print(f'Gathering "{post_type}" posts for Reddit user: "{username}"...')
        os.makedirs(f"../__data/__users/usernames/{username}", exist_ok=True)
        if post_type == 'new': 
            cm = reddit.redditor(username).comments.new(limit=None)
        if post_type == 'hot': 
            cm = reddit.redditor(username).comments.hot(limit=None)        
        for comment in cm:
            created_pst = datetime.fromtimestamp(comment.created_utc).strftime('%d-%b-%Y %H:%M:%S')
            comments.append([comment.created_utc, created_pst, post_type, username, comment.subreddit, comment.body, comment.permalink])
        comments_df = pd.DataFrame(comments, columns=['created_unix_utc', 'created_pst', 'post_type', 'commenter_name', 'subreddit', 'comment', 'reddit_permalink'])
        comments_df.to_csv(f'../__data/__users/usernames/{username}/{username}_subreddit_comments_{post_type}_{snapshotdate}.csv', index=False, sep=sep)
        submissions = []
        if post_type == 'new': 
            sm = reddit.redditor(username).submissions.new(limit=post_limit)
        if post_type == 'hot': 
            sm = reddit.redditor(username).submissions.hot(limit=post_limit) 
        for submission in sm: 
            created_pst = datetime.fromtimestamp(submission.created_utc).strftime('%d-%b-%Y %H:%M:%S')
            submission_comments_agg = []
            submission_comments = reddit.submission(id=submission.id)
            submission_comments.comments.replace_more(limit=None)
            for submission_comment in submission_comments.comments.list():
                submission_comments_agg.append(f'{submission_comment.author}: {submission_comment.body}')  
            submissions.append([submission.created_utc, created_pst, post_type, username, submission.subreddit, submission.id, submission.title, submission.selftext, submission.num_comments, submission_comments_agg, submission.url])
        submissions_df = pd.DataFrame(submissions, columns=['created_unix_utc', 'created_pst', 'post_type', 'username', 'subreddit', 'id', 'title', 'body', 'num_comments', 'submission_comments', 'reddit_permalink'])
        submissions_df.to_csv(f'../__data/__users/usernames/{username}/{username}_subreddit_submissions_{post_type}_{snapshotdate}.csv', index=False, sep=sep)
        time.sleep(60)
    print("Task is Complete!")
    
    

if __name__ == "__main__":
    extract_user_activity()
