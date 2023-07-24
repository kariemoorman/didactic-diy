#!/usr/bin/python3

import os
import argparse
import json
from datetime import datetime
import pandas as pd
import requests
import praw

## add credentials.py script to .gitignore list to keep personal keys safe. ##
from reddit_scraper.credentials import *

class SubredditScraper:
    def __init__(self, subreddits, category, sep='tab', output_format='csv'):
        self.subreddits = subreddits
        self.category = category
        self.sep = sep
        self.output_format = output_format

        ## Establish Reddit Connection ##
        self.reddit = praw.Reddit(client_id=my_client_id, client_secret=my_client_secret, user_agent=my_user_agent)

        ## Datetime Snapshot ##
        self.snapshotdate = datetime.today().strftime('%d-%b-%Y')
        self.snapshotdatetime = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')

    def _praw_subreddit_activity(self, post_type, post_limit):

        if self.sep == 'tab':
            delimiter = '\t'
        elif self.sep == 'comma':
            delimiter = ','

        ##Iterate over subreddit items in subreddits list.
        for subreddit in self.subreddits:
            ## Print task initialization message.
            print(f'Gathering {post_type} posts from Subreddit: "{subreddit}"...')
            ## Make output directories.
            os.makedirs(f"../__data/__posts/{self.category}/{subreddit}", exist_ok=True)
            ## Extract subreddit posts (submissions and comments).
            posts = []
            if post_type == 'new':
                sub_posts = self.reddit.subreddit(subreddit).new(limit=post_limit)
            elif post_type == 'hot':
                sub_posts = self.reddit.subreddit(subreddit).hot(limit=post_limit)
            elif post_type == 'top':
                sub_posts = self.reddit.subreddit(subreddit).top(limit=post_limit)
            for post in sub_posts:
                ## Transform unix datetime to PST.
                created_pst = datetime.fromtimestamp(post.created_utc).strftime('%d-%b-%Y %H:%M:%S')
                comments = []
                submission = self.reddit.submission(id=post.id)
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():
                    comments.append(f'{comment.author}: {comment.body}')
                ## Transform posts data to pandas DataFrame.
                posts.append([post.created_utc, created_pst, post_type, post.title, post.author, post.score, post.id, post.subreddit, post.url, post.selftext, post.num_comments, comments])
                post_df = pd.DataFrame(posts, columns=['created_unix_utc', 'created_datetime_pst', 'post_type', 'title', 'author', 'score', 'id', 'subreddit', 'url', 'body', 'num_comments', 'comments'])
                ## Write DataFrame to output directory based on output format.
                if self.output_format == 'parquet':
                    post_df.to_parquet(f'../__data/__posts/{self.category}/{subreddit}/{subreddit}_subreddit_{post_type}_posts_{self.snapshotdatetime}.parquet', index=False)
                elif self.output_format == 'json':
                    post_df.to_json(f'../__data/__posts/{self.category}/{subreddit}/{subreddit}_subreddit_{post_type}_posts_{self.snapshotdatetime}.json', orient='records')
                elif self.output_format == 'csv':
                    post_df.to_csv(f'../__data/__posts/{self.category}/{subreddit}/{subreddit}_subreddit_{post_type}_posts_{self.snapshotdatetime}.csv', index=False, sep=delimiter)
                else: 
                    print('Unsupported file format specified.')

    def _pushshift_subreddit_activity(self, api, before_days, post_limit):
        if self.sep == 'tab':
            delimiter = '\t'
        elif self.sep == 'comma':
            delimiter = ','
        ##Iterate over items in subreddits list.
        for subreddit in self.subreddits:
            ## Print task initialization message.
            print(f'Gathering {post_limit} {before_days}-trailing posts for Subreddit: "{subreddit}"...')
            ## Load submissions and comments from {subreddit} using Pushshift API.
            submissions = json.loads(requests.get(f'https://api.{api}.io/reddit/search/submission?subreddit={subreddit}&before={before_days}&size={post_limit}&sort=created_utc&metadata=false', timeout=20).text or '{}' or '' or '[]' or 'None' or None)
            comments = json.loads(requests.get(f'https://api.{api}.io/reddit/search/comment?subreddit={subreddit}&before={before_days}&size={post_limit}&sort=created_utc&metadata=false', timeout=20).text or '{}' or '' or '[]' or 'None' or None)
            ## Create output directory.
            os.makedirs(f"../__data/__posts/subreddits/{self.category}/{subreddit}", exist_ok=True)
            ## Transform data.json to pandas DataFrame.
            subreddit_submissions_df = pd.DataFrame(submissions['data'])
            subreddit_comments_df = pd.DataFrame(comments['data'])
            ## Transform unix datetime to PST, and append to DataFrame.
            comments_created_pst = [datetime.fromtimestamp(item).strftime('%d-%b-%Y %H:%M:%S') for item in subreddit_comments_df.created_utc]
            subreddit_comments_df['created_pst'] = comments_created_pst
            submission_created_pst = [datetime.fromtimestamp(item).strftime('%d-%b-%Y %H:%M:%S') for item in subreddit_submissions_df.created_utc]
            subreddit_submissions_df['created_pst'] = submission_created_pst
            ## Write DataFrames to output directory based on output format.
            if self.output_format == 'parquet':
                subreddit_comments_df.to_parquet(f'../__data/__posts/subreddits/{self.category}/{subreddit}/{subreddit}_subreddit_comments_{before_days}_{self.snapshotdatetime}.parquet', index=False)
                subreddit_submissions_df.to_parquet(f'../__data/__posts/subreddits/{self.category}/{subreddit}/{subreddit}_subreddit_submissions_{before_days}_{self.snapshotdatetime}.parquet', index=False)
            elif self.output_format == 'json':
                subreddit_comments_df.to_json(f'../__data/__posts/subreddits/{self.category}/{subreddit}/{subreddit}_subreddit_comments_{before_days}_{self.snapshotdatetime}.json', orient='records')
                subreddit_submissions_df.to_json(f'../__data/__posts/subreddits/{self.category}/{subreddit}/{subreddit}_subreddit_submissions_{before_days}_{self.snapshotdatetime}.json', orient='records')
            elif self.output_format == 'csv':
                subreddit_comments_df.to_csv(f'../__data/__posts/subreddits/{self.category}/{subreddit}/{subreddit}_subreddit_comments_{before_days}_{self.snapshotdatetime}.csv', index=False, sep=delimiter)
                subreddit_submissions_df.to_csv(f'../__data/__posts/subreddits/{self.category}/{subreddit}/{subreddit}_subreddit_submissions_{before_days}_{self.snapshotdatetime}.csv', index=False, sep=delimiter)
            else: 
                print('Unsupported file format specified.')


    def extract_subreddit_data(self, post_type='new', api='praw', before_days='0d', post_limit=1000):
        if api == 'praw':
            self._praw_subreddit_activity(post_type, post_limit)
        elif api in ['pushshift', 'pullpush']:
            self._pushshift_subreddit_activity(api, before_days, post_limit)
        else: 
            print("Unsupported API specified.")
        print("Task Complete!")


def main():
    parser = argparse.ArgumentParser(description="Subreddit Scraper")
    parser.add_argument("subreddits", nargs="+", help="List of subreddits")
    parser.add_argument("--api", type=str, choices=["praw", "pushshift", "pullpush"], default="praw", help="API selection (praw, pushshift, or pullpush)")
    parser.add_argument("--category", "-c", type=str, help="Name of the output directory (e.g., DataScience)")
    parser.add_argument("--post_type", "-t", type=str, choices=["hot", "new", "top"], default="new", help="Type of posts to retrieve, for use with Praw API")
    parser.add_argument("--before_days", "-b", type=str, default="0d", help="Number of trailing days (e.g., 10d), for use with Pushshift/Pullpush API")
    parser.add_argument("--post_limit", "-l", type=int, default=1000, help="Number of posts to retrieve (1-1000)")
    parser.add_argument("--sep", type=str, choices=["tab", "comma"], default="tab", help="Separator for the CSV output")
    parser.add_argument("--output_format", "-o", type=str, choices=["csv", "parquet", "json"], default="csv", help="Output format (csv, parquet, json)")

    args = parser.parse_args()

    scraper = SubredditScraper(args.subreddits, args.category, args.sep, args.output_format)
    scraper.extract_subreddit_data(args.post_type, args.api, args.before_days, args.post_limit)

if __name__ == "__main__":
    main()