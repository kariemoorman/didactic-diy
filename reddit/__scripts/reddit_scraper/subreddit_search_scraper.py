#!/usr/bin/python3

import os
import sys
import argparse
import json
from datetime import datetime
import pandas as pd
import requests
import praw

## add credentials.py script to .gitignore list to keep personal keys safe. ##
from credentials import my_client_id, my_client_secret, my_user_agent, my_password, my_username

class RedditSubredditSearchScraper:
    def __init__(self, subreddits, category, sep='tab', output_format='csv'):
        self.subreddits = subreddits
        self.category = category
        self.sep = sep
        self.output_format = output_format

        ## Establish Reddit Connection ##
        self.reddit = praw.Reddit(client_id=my_client_id, client_secret=my_client_secret, user_agent=my_user_agent, username=my_username, password=my_password)

        ## Datetime Snapshot ##
        self.snapshotdate = datetime.today().strftime('%d-%b-%Y')
        self.snapshotdatetime = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')

    def _praw_search_subreddit_activity(self, query_items, post_type, post_limit):
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
            for search_item in query_items:
                ## Print task status message.
                print(f'Gathering "{post_type}" posts for search item: "{search_item}" in "{subreddit}" Subreddit...')
                ## Extract subreddit posts (submissions and comments).
                sub_posts = self.reddit.subreddit(subreddit).search(search_item, sort=post_type, limit=post_limit)
                for post in sub_posts:
                    ## Transform unix datetime to PST.
                    created_pst = datetime.fromtimestamp(post.created_utc).strftime('%d-%b-%Y %H:%M:%S')
                    comments = []
                    submission = self.reddit.submission(id=post.id)
                    submission.comments.replace_more(limit=None)
                    for comment in submission.comments.list():
                        comments.append(f'{comment.author}: {comment.body}')
                    ## Transform posts data to pandas DataFrame.
                    posts.append([post.created_utc, created_pst, post_type, search_item, post.subreddit, post.id, post.title, post.author, post.score, post.url, post.selftext, post.num_comments, comments])
                    post_df = pd.DataFrame(posts, columns=['created_unix_utc', 'created_datetime_pst', 'post_type', 'search_item', 'subreddit', 'id', 'title', 'author', 'score', 'url', 'body', 'num_comments', 'comments'])
                    ## Write DataFrame to output directory based on output format.
                    if self.output_format == 'parquet':
                        post_df.to_parquet(f'../__data/__posts/{self.category}/{subreddit}/{subreddit}_subreddit_search_{post_type}_posts_{self.snapshotdatetime}.parquet', index=False)
                    elif self.output_format == 'json':
                        post_df.to_json(f'../__data/__posts/{self.category}/{subreddit}/{subreddit}_subreddit_search_{post_type}_posts_{self.snapshotdatetime}.json', orient='records')
                    elif self.output_format == 'csv':
                        post_df.to_csv(f'../__data/__posts/{self.category}/{subreddit}/{subreddit}_subreddit_search_{post_type}_posts_{self.snapshotdatetime}.csv', index=False, sep=delimiter)
                    else: 
                        print('Unsupported file format specified.')

    def _pushshift_search_subreddit_activity(self, query_items, api, before_days, post_limit):
        if self.sep == 'tab':
            delimiter = '\t'
        elif self.sep == 'comma':
            delimiter = ','
        ##Iterate over items in subreddits list.
        for subreddit in self.subreddits:
            ## Print task initialization message.
            print(f'Gathering {post_limit} {before_days}-trailing posts for Subreddit: "{subreddit}"...')
            subreddit_search_submissions_df = pd.DataFrame()
            subreddit_search_comments_df = pd.DataFrame()
            for search_item in query_items: 
                ## Print task status message.
                print(f'Querying "{search_item}" in Subreddit: "{subreddit}"...')
                ## Load submissions and comments from {subreddit} using Pushshift API.
                submissions = json.loads(requests.get(f'https://api.{api}.io/reddit/search/submission?subreddit={subreddit}&before={before_days}&size={post_limit}&q={search_item}&sort=created_utc&metadata=false', timeout=20).text or '{}' or '' or '[]' or 'None' or None)
                comments = json.loads(requests.get(f'https://api.{api}.io/reddit/search/comment?subreddit={subreddit}&before={before_days}&size={post_limit}&q={search_item}&sort=created_utc&metadata=false', timeout=20).text or '{}' or '' or '[]' or 'None' or None)
                subreddit_submissions_df = pd.DataFrame(submissions['data'])
                subreddit_comments_df = pd.DataFrame(comments['data'])
                if not subreddit_submissions_df.empty:
                    ## Create output directory.
                    os.makedirs(f"../__data/__posts/subreddits/{self.category}/{subreddit}", exist_ok=True)
                    ## Add column denoting search item used in subreddit query and append to DataFrame.
                    subreddit_submissions_df['search_item'] = f'{search_item}'
                    ## Transform unix datetime to PST, and append to DataFrame.
                    if 'created_utc' in subreddit_submissions_df:
                        submission_created_pst = [datetime.fromtimestamp(item).strftime('%d-%b-%Y %H:%M:%S') for item in subreddit_submissions_df.created_utc]
                        subreddit_submissions_df['created_pst'] = submission_created_pst
                    ## Concatenate DataFrames in a single DataFrame.
                    subreddit_search_submissions_df = pd.concat([subreddit_search_submissions_df,subreddit_submissions_df], ignore_index=True)
                if not subreddit_comments_df.empty: 
                    ## Create output directory.
                    os.makedirs(f"../__data/__posts/subreddits/{self.category}/{subreddit}", exist_ok=True)
                    ## Add column denoting search item used in subreddit query and append to DataFrame.
                    subreddit_comments_df['search_item'] = f'{search_item}'
                    ## Transform unix datetime to PST, and append to DataFrame.
                    if 'created_utc' in subreddit_comments_df:
                        comment_created_pst = [datetime.fromtimestamp(item).strftime('%d-%b-%Y %H:%M:%S') for item in subreddit_comments_df.created_utc]
                        subreddit_comments_df['created_pst'] = comment_created_pst
                    ## Concatenate DataFrames in a single DataFrame.
                    subreddit_search_comments_df = pd.concat([subreddit_search_comments_df,subreddit_comments_df], ignore_index=True)
            ## Write DataFrames to output directory based on output format.
            if self.output_format == 'parquet':
                subreddit_search_comments_df.to_parquet(f'../__data/__posts/test/subreddits/{self.category}/{subreddit}/{subreddit}_subreddit_search_comments_{before_days}_{self.snapshotdatetime}.parquet', index=False)
                subreddit_search_submissions_df.to_parquet(f'../__data/__posts/test/subreddits/{self.category}/{subreddit}/{subreddit}_subreddit_search_submissions_{before_days}_{self.snapshotdatetime}.parquet', index=False)
            elif self.output_format == 'json':
                subreddit_search_comments_df.to_json(f'../__data/__posts/test/subreddits/{self.category}/{subreddit}/{subreddit}_subreddit_search_comments_{before_days}_{self.snapshotdatetime}.json', orient='records')
                subreddit_search_submissions_df.to_json(f'../__data/__posts/test/subreddits/{self.category}/{subreddit}/{subreddit}_subreddit_search_submissions_{before_days}_{self.snapshotdatetime}.json', orient='records')
            elif self.output_format == 'csv':
                subreddit_search_comments_df.to_csv(f'../__data/__posts/test/subreddits/{self.category}/{subreddit}/{subreddit}_subreddit_search_comments_{before_days}_{self.snapshotdatetime}.csv', index=False, sep=delimiter)
                subreddit_search_submissions_df.to_csv(f'../__data/__posts/test/subreddits/{self.category}/{subreddit}/{subreddit}_subreddit_search_submissions_{before_days}_{self.snapshotdatetime}.csv', index=False, sep=delimiter)
            else: 
                print('Unsupported file format specified.')


    def extract_search_subreddit_data(self, query_items, post_type='new', api='praw', before_days='0d', post_limit=1000):
        if api == 'praw':
            self._praw_search_subreddit_activity(query_items, post_type, post_limit)
        elif api in ['pushshift','pullpush']:
            self._pushshift_search_subreddit_activity(query_items, api, before_days, post_limit)
        else: 
            print("Unsupported API specified.")
        print("Task Complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reddit Scraper")
    parser.add_argument("--api", type=str, choices=["praw", "pushshift", "pullpush"], default="praw", help="API ('praw' or 'pushshift')")
    parser.add_argument("subreddits", nargs="+", help="List of subreddits")
    parser.add_argument("--query_items", '-q', nargs="+", help="List of search query items")
    parser.add_argument("--category", "-c", type=str, help="Category for the output directory")
    parser.add_argument("--post_type", "-t", type=str, choices=["hot", "new", "top"], default="new", help="Type of posts to retrieve")
    parser.add_argument("--before_days", "-b", type=str, default="0d", help="Type of posts to retrieve")
    parser.add_argument("--post_limit", "-l", type=int, default=1000, help="Limit of posts to retrieve (1-1000)")
    parser.add_argument("--sep", type=str, choices=["tab", "comma"], default="tab", help="Separator for the CSV output")
    parser.add_argument("--output_format", "-o", type=str, choices=["csv", "parquet", "json"], default="csv", help="Output format (csv, parquet, json)")

    args = parser.parse_args()

    scraper = RedditSubredditSearchScraper(args.subreddits, args.category, args.sep, args.output_format)
    scraper.extract_search_subreddit_data(args.query_items, args.post_type, args.api, args.before_days, args.post_limit)
