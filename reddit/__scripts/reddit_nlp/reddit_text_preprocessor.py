#!/usr/bin/python

import os,sys
from reddit_nlp.clean_amazon_reddit_text import preprocess_amazon_text_data
from reddit_nlp.clean_reddit_text import preprocess_text_data



def find_paths(data_filepath):
    dict = {}
    dir_list = next(os.walk(data_filepath))[1]
    for i in dir_list: 
        subreddit_list = [i for i in next(os.walk(f'{data_filepath}/{i}'))[1]]
        dict[i] = subreddit_list 
    return dict 


def preprocess_data(data_filepath, category_list=['all'], subreddit_list=['all'], sep='tab', amznsubdir_list=['Amazon','AmazonAlexa','AmazonPrime','AmazonPrimeAV','AmazonSmartHome'], column_list=['title', 'body', 'comments'], method='token', singularize='yes', stopwords='yes', stopword_listtype='general'):
    '''
    Function: Locate and preprocess text data.
    - Find all the data in the specified {data_filepath}.
    - Preprocess text entries, specified by {column_list}.
    - Remove hyperlinks, 
    - Expand contractions, 
    - Remove numbers,
    - Perform NER regularization,
    - Remove punctuation, 
    - Optional: Filter stop words, Singularize words.
    - Tokenize/Lemmatize text.
    
    Input Arguments: 
    data_filepath: input type is (str), denoting path to text datasets. 
    category_list: input type is list of (str) items, denoting output subdirectory name(s). Default = ['all'].
    subreddit_list: 
    sep: input type is (str) item, 'tab' or 'comma'. Default = 'tab'.
    amznsubdir_list: input type is list of (str) items, denoting output subdirectory name(s) with Amazon-specific datasets. Default = ['Amazon','AmazonAlexa','AmazonPrimeAV','AmazonSmartHome'].
    column_list: input type is list of (str) items, denoting columns containing text to undergo pre-processing. Default = ['title', 'body', 'comments'].
    method: input type is (str) item, 'token' or 'lemma'. Default = 'token'.
    singularize: input type is (str) item, 'yes' or 'no'. Default = 'yes'.
    stopwords: input type is (str) item, 'yes' or 'no'. Default = 'yes'.
    stoplist_type: input type is (str) item, 'simple' (no prepositions), 'prep' (prepositions only), 'full' (both). Default = 'general'.
    
    Example: 
    data_filepath = '/didactic-diy/reddit/__data/__posts'
    preprocess_data(data_filepath, category_list=['Amazon'], subreddit_list=['all'], column_list=['title', 'body', 'comments'], method='lemma')
    
    '''
    
    dict = find_paths(data_filepath)

    if category_list[0] == 'all': 
        print(category_list)
        category_list = dict.keys()

    try: 
        if len([k for k in dict if k in category_list]) == 0:
            raise TypeError
        if len([k for k in category_list if k in dict]) < len(category_list): 
            print(f'\n\nError: {[k for k in category_list if k not in dict]} not found!')
            raise TypeError 

        print(f"\nPre-processing text data for the following categories and subreddits:\n ")
        for k in category_list: 
            if subreddit_list[0] == 'all': 
                print(f' {k}:\n {dict[k]}\n') 
            else: 
                print(f' {k}:\n {subreddit_list}\n') 

        for k in category_list:
            if subreddit_list[0] == 'all': 
                subreddit_list = dict[k]
            else: 
                subreddit_list = subreddit_list
            if k in amznsubdir_list: 
                amazon_filepath = f'{data_filepath}/{k}'
                for subreddit in subreddit_list:
                    amazon_subreddit_filepath = f'{amazon_filepath}/{subreddit}'
                    preprocess_amazon_text_data(amazon_subreddit_filepath, column_list=column_list,sep=sep, category=k, subreddit_name=subreddit, method=method, singularize=singularize, stopwords=stopwords, stopword_listtype=stopword_listtype)
            elif k not in amznsubdir_list: 
                filepath = f'{data_filepath}/{k}'
                for subreddit in subreddit_list:
                    subreddit_filepath = f'{filepath}/{subreddit}'
                    preprocess_text_data(subreddit_filepath, column_list=column_list, sep=sep, category=k, subreddit_name=subreddit, method=method, singularize=singularize, stopwords=stopwords, stopword_listtype=stopword_listtype)

    except TypeError:
        print(f'\nOh no! Seems there is an issue with the input values:\n\n Input Directory ({data_filepath})\n does not contain one or more of the subdirectories provided in category_list:\n {category_list}.')
        print('\nPlease check your input values, and try again.\n')
    finally: 
        sys.exit(1)


if __name__ == "__main__":
    preprocess_data()