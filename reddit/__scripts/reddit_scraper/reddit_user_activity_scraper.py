#!/usr/bin/python3

import os
import time
import argparse
from datetime import datetime
import pandas as pd
import praw

## Add credentials.py script to .gitignore list to keep personal keys safe. ##
from credentials import my_client_id, my_client_secret, my_user_agent, my_password, my_username


## Date and Datetime Snapshot ##
snapshotdate = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')


class RedditUserActivity: 
    def __init__(self, post_type='new', post_limit=1000, output_format='csv'): 
        self.post_type = post_type
        self.post_limit = post_limit
        self.output_format = output_format

        ## Establish Reddit Connection ##
        self.reddit = praw.Reddit(client_id=my_client_id, client_secret=my_client_secret, user_agent=my_user_agent, username=my_username, password=my_password)

        ## Datetime Snapshot ##
        self.snapshotdate = datetime.today().strftime('%d-%b-%Y')
        self.snapshotdatetime = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')


    ## Reddit User Activity Scraper Function ## 
    def extract_user_activity(self, usernames):
        ## Extract User Submissions and Comments.
        for username in usernames: 
            comments_ls = []
            submissions_ls = []
            print(f'Gathering "{self.post_type}" posts for Reddit user: "{username}"...')
            os.makedirs(f"../__data/__users/usernames/{username}", exist_ok=True)

            if self.post_type == 'new': 
                submissions = self.reddit.redditor(username).submissions.new(limit=self.post_limit)
                comments = self.reddit.redditor(username).comments.new(limit=None)
            if self.post_type == 'top': 
                submissions = self.reddit.redditor(username).submissions.top(limit=self.post_limit)
                comments = self.reddit.redditor(username).comments.top(limit=None)
            if self.post_type == 'hot': 
                submissions = self.reddit.redditor(username).submissions.hot(limit=self.post_limit)
                comments = self.reddit.redditor(username).comments.hot(limit=None) 

            for comment in comments:
                c_created_pst = datetime.fromtimestamp(comment.created_utc).strftime('%d-%b-%Y %H:%M:%S')
                comments_ls.append([comment.created_utc, c_created_pst, self.post_type, username, comment.subreddit, comment.body, comment.permalink])
            comment_df = pd.DataFrame(comments_ls, columns=['created_unix_utc', 'created_pst', 'post_type', 'commenter_name', 'subreddit', 'comment', 'reddit_permalink'])
            comment_df.to_csv(f'../__data/__users/usernames/{username}/{username}_subreddit_comments_{self.post_type}_{self.snapshotdate}.csv', index=False, sep='\t')
            for submission in submissions: 
                s_created_pst = datetime.fromtimestamp(submission.created_utc).strftime('%d-%b-%Y %H:%M:%S')
                submission_comments_agg = []
                submission_comments = self.reddit.submission(id=submission.id)
                submission_comments.comments.replace_more(limit=None)
                for submission_comment in submission_comments.comments.list():
                    submission_comments_agg.append(f'{submission_comment.author}: {submission_comment.body}')  
                submissions_ls.append([submission.created_utc, s_created_pst, self.post_type, username, submission.subreddit, submission.id, submission.title, submission.selftext, submission.num_comments, submission_comments_agg, submission.url])
            submission_df = pd.DataFrame(submissions_ls, columns=['created_unix_utc', 'created_pst', 'post_type', 'username', 'subreddit', 'id', 'title', 'body', 'num_comments', 'submission_comments', 'reddit_permalink'])
            submission_df.to_csv(f'../__data/__users/usernames/{username}/{username}_subreddit_submissions_{self.post_type}_{self.snapshotdate}.csv', index=False, sep='\t')
            time.sleep(40)
        print("Task is Complete!")
 

def main(): 
    parser = argparse.ArgumentParser(description="Reddit User Activity Scraper")
    parser.add_argument("usernames", nargs="+", help="List of usernames")
    parser.add_argument("--post_type", "-t", type=str, choices=["hot", "new", "top"], default="new", help="Type of posts to retrieve")
    parser.add_argument("--post_limit", "-l", type=int, default=1000, help="Limit of posts to retrieve (1-1000)")
    
    args = parser.parse_args()

    scraper = RedditUserActivity(args.post_type, args.post_limit)
    scraper.extract_user_activity(args.usernames)

if __name__ == "__main__":
    main()