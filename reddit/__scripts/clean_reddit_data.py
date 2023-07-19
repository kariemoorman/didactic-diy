#!/usr/bin/python

from reddit_nlp.reddit_text_preprocessor import preprocess_data
from reddit_nlp.clean_amazon_reddit_text import preprocess_amazon_text_data
from reddit_nlp.clean_reddit_text import preprocess_text_data



method='token'
test_output_dir = 'TEST'

amazon_alexa_filepath = '../__data/__posts/TEST/alexa'
amazon_subreddit='alexa'

#preprocess_amazon_text_data(df_filepath=amazon_alexa_filepath, category=test_output_dir, subreddit_name=amazon_subreddit, method=method)

datasci_filepath = '../__data/__posts/DataScience/MachineLearning'
datasci_subreddit='datascience'

preprocess_text_data(df_filepath=datasci_filepath, category=test_output_dir, subreddit_name=datasci_subreddit, method=method)

general_filepath = '../__data/__posts'
amazon_category_list = ['Amazon']
datasci_category_list = ['DataScience']

preprocess_data(data_filepath=general_filepath, category_list=amazon_category_list, subreddit_list=['sonos', 'wyzecam'], method=method)
preprocess_data(data_filepath=general_filepath, category_list=datasci_category_list, subreddit_list=['all'], method=method)