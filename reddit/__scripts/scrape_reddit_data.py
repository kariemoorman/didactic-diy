#!/usr/bin/python

from reddit_scraper.subreddit_lists import * 
from reddit_scraper.scrape_reddit import scrape_reddit

api = 'praw'
scraper_type = 'subreddit'
subreddit_list = ['alexa', 'datascience']
output_dir = 'TEST'
post_type = 'new'
post_limit = 1000
sep = 'tab'

scrape_reddit(api=api, scraper_type=scraper_type, input_list=subreddit_list, category=output_dir, post_type=post_type, post_limit=post_limit, sep=sep) 