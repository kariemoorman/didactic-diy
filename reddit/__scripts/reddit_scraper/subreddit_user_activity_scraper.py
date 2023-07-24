#!/usr/bin/python3

import os
import time
import argparse
import json
from datetime import datetime
from collections import Counter
import pandas as pd
import requests
import praw

## add credentials.py script to .gitignore list to keep personal keys safe. ##
from credentials import my_client_id, my_client_secret, my_user_agent, my_password, my_username

class SubredditUserActivityScraper:
    def __init__(self, subreddits, category):
        self.subreddits = subreddits
        self.category = category

        ## Establish Reddit Connection ##
        self.reddit = praw.Reddit(client_id=my_client_id, client_secret=my_client_secret, user_agent=my_user_agent, username=my_username, password=my_password)

        ## Datetime Snapshot ##
        self.snapshotdate = datetime.today().strftime('%d-%b-%Y')
        self.snapshotdatetime = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')

    def _praw_find_commenters(self, post_limit=1000):
        ##Iterate over subreddit items in subreddits list.
        for subreddit in self.subreddits:
            ## Print task initialization message.
            print(f'Gathering users from Subreddit: "{subreddit}"...')
            users = []
            sub_posts = self.reddit.subreddit(subreddit).new(limit=post_limit)
            for post in sub_posts:
                created_pst = datetime.fromtimestamp(post.created_utc).strftime('%d-%b-%Y %H:%M:%S')
                commenters = []
                submission = self.reddit.submission(id=post.id)
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():
                    commenters.append(f'{comment.author}')
                users.append([post.created_utc, created_pst, post.id, post.subreddit, post.url, post.author, commenters])
                #Write Results to CSV
                os.makedirs(f"../__users/subreddit_users/{self.category}/{subreddit}/{self.snapshotdate}/praw", exist_ok=True)
            post_df = pd.DataFrame(users,columns=['created_unix_utc', 'created_datetime_pst','id', 'subreddit', 'url', 'author', 'commenters'])
            post_df.to_csv(f'../__users/subreddit_users/{self.category}/{subreddit}/{self.snapshotdate}/praw/{subreddit}_subreddit_newposts_{self.snapshotdatetime}.csv', index=False, sep='\t', encoding='utf-8')  
            #Isolate Post Submitters and Commenters for Frequency Count
            submitter_list = Counter(list(post_df.author)).most_common()
            commenters_flattened = [item for sublist in list(post_df.commenters) for item in sublist]
            commenters_flattened_no_na = [i for i in commenters_flattened if i == i and i !='' and i !='None']
            commenter_list = Counter(commenters_flattened_no_na).most_common()
            #Restructure Username Frequency Results as Dictionary
            s=dict(submitter_list)
            c=dict(commenter_list)
            #Create DataFrame with Metadata
            commenters_output_df = pd.DataFrame({"query_date": self.snapshotdate, "subreddit": subreddit, "comment_author": c.keys(), "comment_frequency": c.values()})
            submitters_output_df = pd.DataFrame({"query_date": self.snapshotdate, "subreddit": subreddit, "submission_author": s.keys(), "submission_frequency": s.values()})
            #Write Frequency Results as CSV
            commenters_output_df.to_csv(f'../__data/__users/subreddit_users/{self.category}/{subreddit}/{self.snapshotdate}/praw/{subreddit}_username_commenters_{self.snapshotdatetime}.csv', index=False, sep='\t', encoding='utf-8')
            submitters_output_df.to_csv(f'../__data/__users/subreddit_users/{self.category}/{subreddit}/{self.snapshotdate}/praw/{subreddit}_username_submitters_{self.snapshotdatetime}.csv', index=False, sep='\t', encoding='utf-8')
            time.sleep(5)

    def _pushshift_find_commenters(self, api, before_days, post_limit):
        ##Iterate over subreddit items in subreddits list.
        for subreddit in self.subreddits: 
            print(f'Gathering users from Subreddit: "{subreddit}"...')
            os.makedirs(f"../__data/__users/subreddit_users/{self.category}/{subreddit}/{self.snapshotdate}/ps", exist_ok=True)
            submissions = json.loads(requests.get(f'https://api.{api}.io/reddit/search/submission?subreddit={subreddit}&before={before_days}&size={post_limit}&sort=created_utc&metadata=false', timeout=20).text)
            comments = json.loads(requests.get(f'https://api.{api}.io/reddit/search/comment?subreddit={subreddit}&before={before_days}&size={post_limit}&sort=created_utc&metadata=false', timeout=20).text)

            submissions_df = pd.DataFrame(submissions['data'])
            comments_df = pd.DataFrame(comments['data'])
            #Isolate Post Submitters and Commenters for Frequency Count
            output_submissions_list = Counter(list(submissions_df.author)).most_common()
            output_comments_list = Counter(list(comments_df.author)).most_common()
            #Restructure Username Frequency Results as Dictionary
            s=dict(output_submissions_list)
            c=dict(output_comments_list)
            #Create DataFrame with Metadata
            comment_output_df = pd.DataFrame({"query_date": self.snapshotdate, "before_date": before_days,"subreddit": subreddit, "comment_author": c.keys(), "comment_frequency": c.values()})
            submission_output_df = pd.DataFrame({"query_date": self.snapshotdate, "before_date": before_days,"subreddit": subreddit, "submission_author": s.keys(), "submission_frequency": s.values()})
            #Write Frequency Results as CSV
            comment_output_df.to_csv(f'../__data/__users/subreddit_users/{self.category}/{subreddit}/{self.snapshotdate}/ps/{subreddit}_subreddit_commenters_{before_days}_{self.snapshotdatetime}.csv', index=False, sep='\t', encoding='utf-8')
            submission_output_df.to_csv(f'../__data/__users/subreddit_users/{self.category}/{subreddit}/{self.snapshotdate}/ps/{subreddit}_subreddit_submitters_{before_days}_{self.snapshotdatetime}.csv', index=False, sep='\t', encoding='utf-8')
            time.sleep(5)

    def extract_subreddit_user_activity(self, api='praw', before_days='0d', post_limit=1000):
        if api == 'praw':
            self._praw_find_commenters(post_limit)
        elif api in ['pushshift', 'pullpush']:
            self._pushshift_find_commenters(api, before_days, post_limit)
        else: 
            print("Unsupported API specified.")
        print("Task Complete!")


def main():
    parser = argparse.ArgumentParser(description="Subreddit User Activity Scraper")
    parser.add_argument("subreddits", nargs="+", help="Subreddit names (e.g., datascience)")
    parser.add_argument("--api", type=str, choices=["praw", "pushshift", "pullpush"], default="praw", help="API selection (praw, pushshift, or pullpush)")
    parser.add_argument("--category", "-c", type=str, help="Name of the output directory (e.g., DataScience)", required=True)
    parser.add_argument("--before_days", "-b", type=str, default="0d", help="Number of trailing days (e.g., 10d), for use with Pushshift/Pullpush API")
    parser.add_argument("--post_limit", "-l", type=int, default=1000, help="Number of posts to retrieve (1-1000)")

    args = parser.parse_args()

    scraper = SubredditUserActivityScraper(args.subreddits, args.category)
    scraper.extract_subreddit_user_activity(args.api, args.before_days, args.post_limit)

if __name__ == "__main__":
    main()