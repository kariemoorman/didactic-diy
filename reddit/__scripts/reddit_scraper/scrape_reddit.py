#!/usr/bin/python3

from reddit_scraper.subreddit_scraper import praw_subreddit_activity, pushshift_subreddit_activity 
from reddit_scraper.subreddit_search_scraper import praw_search_subreddit_activity, pushshift_search_subreddit_activity
from reddit_scraper.subreddit_user_activity_scraper import praw_find_commenters, pushshift_find_commenters
from reddit_scraper.reddit_user_activity_scraper import extract_user_activity

def scrape_reddit(api, scraper_type, input_list, search_query_list=['input'], category='results', before_days='0d', post_type='new', post_limit=1000, sep='tab'): 
    
    '''
    Function: 
    Using {api}, scrape Reddit for {scraper_type} data for {input_list} subreddits or usernames or subreddits and {search_query_list} items. 
    Write output as {sep} CSV to __data/__posts directory.
    
    Input Arguments: 
    scraper_type: input-type is (str), one of the following: 'subreddit', 'search', 'subreddit_user', or 'reddit_user'.
      - 'subreddit' calls subreddit_scraper.py.
      - 'search' calls subreddit_search_scraper.py.
      - 'subreddit_user' calls subbreddit_user_activity_scraper.py.
      - 'reddit_user' calls reddit_user_activity_scraper.py.
    api: input-type is (str), 'praw' or 'pushshift'.
    subreddit_list: input-type is (list) of (str) items.
    search_query_list: input-type is (list) of (str) items.
    category: input-type is (str), for use as an output directory name.
    before_days: input-type is (str) number of days, between 0 and 100 (e.g., '10d'), trailing {snapshotdate}. Default = '0d'.
    post_limit: input type is (int), between 1 - 1000 (1000 is max). Default = 1000.
    sep: input type is (str) item, 'tab' or 'comma'. Default = 'tab'.
    '''

    if scraper_type == 'subreddit':
        subreddit_list = input_list
        if api == 'pushshift': 
            pushshift_subreddit_activity(subreddit_list, category, before_days, post_limit, sep)
        elif api == 'praw': 
            praw_subreddit_activity(subreddit_list, category, post_type, post_limit, sep)
    
    elif scraper_type == 'search': 
        subreddit_list = input_list
        if api == 'pushshift': 
            pushshift_search_subreddit_activity(subreddit_list, search_query_list, category, before_days, post_limit, sep)
        elif api == 'praw': 
            praw_search_subreddit_activity(subreddit_list, search_query_list, category, post_type, post_limit, sep) 

    elif scraper_type == 'subreddit_user':
        subreddit_list = input_list
        if api == 'pushshift': 
            pushshift_find_commenters(subreddit_list, category, before_days, post_limit, sep)
        elif api == 'praw': 
            praw_find_commenters(subreddit_list, category, post_limit, sep)
    
    elif scraper_type == 'reddit_user':
        username_list = input_list
        extract_user_activity(username_list, post_type, post_limit, sep)


if __name__ == "__main__":
    scrape_reddit()
