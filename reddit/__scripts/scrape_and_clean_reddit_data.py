#!/usr/bin/python3

#import os, sys
#sys.path.insert(0, 'reddit/__scripts')

from reddit_scraper.subreddit_lists import * 
from reddit_nlp.reddit_text_preprocessor import preprocess_data
from reddit_scraper.subreddit_scraper import SubredditScraper


def scrape_and_clean_reddit_posts(subreddit_list, category, sep='tab', api='praw', post_type='new', before_days='0d', post_limit=1000, amznsubdir_list=['Amazon','AmazonAlexa','AmazonPrimeAV','AmazonSmartHome'], method='token', singularize='yes', stopwords='yes', stopword_listtype='general'):
    
    '''
    Function: Gather, isolate, and pre-process text data.
    - Scrape Reddit Subreddit(s) in {subreddit_list}, using either Praw (praw_subreddit_activity()) or Pushshift API (pushshift_subreddit_activity()).
    - Write output to '__data/__posts/{category}/{subreddit}'.
    - Pre-process text data using process_data().
    - Write aggregated data to '__data/__aggregated_posts/{category}/{subreddit}'.
    
    Input Arguments: 
    subreddit_list: input type is (list) of (str).
    category: input type is (str), denoting output subdirectory name.
    sep: input type is (str), 'tab' or 'comma'. Default='tab'.
    api: input type is (str), either 'praw' or 'pushshift'. Default = 'praw'.
    post_type: input type is (str) item, 'hot', 'new', or 'top'. Default = 'new'. (For use with Praw API)
    before_days: input type is (str) number of days, between 0 and 100 (e.g., '10d'), trailing {snapshotdate}. Default = '0d'. (For use with Pushshift API)
    post_limit: input type is (int), between 1 - 1000 (1000 is max). Default = 1000.
    amznsubdir_list: input type is list of (str) items, denoting output subdirectory name(s) with Amazon-specific datasets. Default = ['Amazon','AmazonAlexa','AmazonPrimeAV','AmazonSmartHome'].
    method: input type is (str) item, 'token' or 'lemma'. Default = 'token'.
    singularize: input type is (str) item, 'yes' or 'no'. Default = 'yes'.
    stopwords: input type is (str) item, 'yes' or 'no'. Default = 'yes'.
    stoplist_type: input type is (str) item, 'simple' (no prepositions), 'prep' (prepositions only), 'full' (both). Default = 'general'.
    
    Example: 
    subreddit_amazon_items = ['amazon', 'fuckamazon']
    subreddit_gen_items = ['technology', 'privacy', 'cybersecurity', 'MachineLearning', 'Economics', 'Futurology', 'news']

    scrape_and_clean_reddit_posts(subreddit_amazon_items, category='Amazon',api='pushshift')
    scrape_and_clean_reddit_posts(subreddit_gen_items, category='Technology',api='praw')
    
    '''
    scraper = SubredditScraper(subreddit_list, category, sep, output_format='csv')

    if api in ['pushshift', 'pullpush']: 
        scraper.extract_subreddit_data(api=api, before_days=before_days, post_limit=post_limit)
    elif api == 'praw': 
        scraper.extract_subreddit_data(api='praw', post_type=post_type, post_limit=post_limit)
    else: 
        print("Unsupported API specified.")
    
    for subreddit in subreddit_list: 
        data_filepath = f'../__data/__posts/{category}/{subreddit}'
        category_list = [category]
        column_list=['title', 'body', 'comments']
        preprocess_data(data_filepath, category_list=category_list, sep=sep, amznsubdir_list=amznsubdir_list, column_list=column_list,  method=method, singularize=singularize, stopwords=stopwords, stopword_listtype=stopword_listtype)               


if __name__ == "__main__":
    scrape_and_clean_reddit_posts()
