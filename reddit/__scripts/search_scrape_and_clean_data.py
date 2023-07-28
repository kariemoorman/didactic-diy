#!/usr/bin/python3

import argparse
from reddit_scraper.subreddit_lists import *
from reddit_nlp.reddit_text_preprocessor import preprocess_data
from reddit_scraper.subreddit_search_scraper import SubredditSearchScraper


class SubredditSearchDataProcessor:
    def __init__(self, subreddits, search_query_items, category, sep='tab', api='praw', post_type='new', before_days='0d', post_limit=1000, amznsubdir_list=['Amazon', 'AmazonAlexa', 'AmazonPrimeAV', 'AmazonSmartHome'], method='token', singularize='yes', stopwords='yes', stopword_listtype='general'):
        self.subreddits = subreddits
        self.search_query_items = search_query_items
        self.category = category
        self.sep = sep
        self.api = api
        self.post_type = post_type
        self.before_days = before_days
        self.post_limit = post_limit
        self.amznsubdir_list = amznsubdir_list
        self.method = method
        self.singularize = singularize
        self.stopwords = stopwords
        self.stopword_listtype = stopword_listtype

    def process_data(self):
        ## Search and Scrape Subreddits
        scraper = SubredditSearchScraper(self.subreddits, self.category, self.sep, output_format='csv')
        scraper.extract_search_subreddit_data(self.search_query_items, api=self.api, post_type=self.post_type, before_days=self.before_days, post_limit=self.post_limit)
        ## Preprocess Text Data
        for subreddit in self.subreddits:
            data_filepath = f'../__data/__posts'
            category_list = [self.category]
            column_list = ['title', 'body', 'comments']
            preprocess_data(data_filepath, sep=self.sep, category_list=category_list, amznsubdir_list=self.amznsubdir_list,
                            column_list=column_list, method=self.method, singularize=self.singularize,
                            stopwords=self.stopwords, stopword_listtype=self.stopword_listtype)


def main():
    parser = argparse.ArgumentParser(description="Search, Scrape, and Clean Reddit Posts")
    parser.add_argument("subreddits", type=str, nargs="+", help="List of subreddits")
    parser.add_argument("--search_query_items", "-q", type=str, nargs="+", help="List of search queries")
    parser.add_argument("--category", "-c", type=str, help="Name of the output directory (e.g., DataScience)")
    parser.add_argument("--sep", type=str, choices=["tab", "comma"], default="tab", help="Separator for the CSV output")
    parser.add_argument("--api", type=str, choices=["praw", "pushshift", "pullpush"], default="praw", help="API selection (praw, pushshift, or pullpush)")
    parser.add_argument("--post_type", "-t", type=str, choices=["hot", "new", "top"], default="new", help="Type of posts to retrieve, for use with Praw API")
    parser.add_argument("--before_days", "-b", type=str, default="0d", help="Number of trailing days (e.g., 10d), for use with Pushshift/Pullpush API")
    parser.add_argument("--post_limit", "-l", type=int, default=1000, help="Number of posts to retrieve (1-1000)")
    parser.add_argument("--amznsubdirs", nargs="+", default=['Amazon', 'AmazonAlexa', 'AmazonPrimeAV', 'AmazonSmartHome'], help="List of Amazon-specific subdirectories")
    parser.add_argument("--method", type=str, choices=["token", "lemma"], default="token", help="Text preprocessing method")
    parser.add_argument("--singularize", type=str, choices=["yes", "no"], default="yes", help="Singularize words during preprocessing")
    parser.add_argument("--stopwords", type=str, choices=["yes", "no"], default="yes", help="Apply stopwords during preprocessing")
    parser.add_argument("--stopword_listtype", type=str, choices=["general", "prep", "full"], default="general", help="Stopword list type during preprocessing")

    args = parser.parse_args()

    processor = SubredditSearchDataProcessor(args.subreddits, args.search_query_items, args.category, args.sep, args.api,
                                    args.post_type, args.before_days, args.post_limit, args.amznsubdirs,
                                    args.method, args.singularize, args.stopwords, args.stopword_listtype)
    processor.process_data()


if __name__ == "__main__":
    main()
    
    
# python search_scrape_and_clean_data.py datascience MachineLearning -q GPT -c TEST -l 10