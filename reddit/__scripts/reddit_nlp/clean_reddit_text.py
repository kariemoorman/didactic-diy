#!/usr/bin/python

import os, sys, time
from datetime import datetime, date
import re
import glob
import json
import pandas as pd 
import csv 
csv.field_size_limit(sys.maxsize)

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import spacy 

from reddit_nlp.reformat_praw_comments import reformat_praw_comments


def open_json(json_object): 
    with open(json_object, 'r') as f:
        return json.load(f)


def remove_usernames(text): 
    '''
    Required python pkgs: 
    - re (import re)
    
    Function: Remove usernames from aggregated df.comments column.
    Intended to be used on {subreddit-scraper.py} and {subreddit-search-scraper.py} generated dataframes.
    
    Input Arguments: 
    text: input type is list of (str) items.
    
    '''
    text = [re.sub(r'\b([A-Za-z0-9\_\-]+: )', '', str(sentence)) for sentence in text]
    return text 


def remove_hyperlinks(text):
    '''
    Required python pkgs: 
    - re (import re)
    
    Function: Remove hyperlinks from text.
    
    Input Arguments: 
    text: input type is list of (str) items.
        
    '''
    #remove hyperlinks.
    text = [re.sub(r'(\(?http\S+\)?)', ' ', sentence) for sentence in text]
    text = [re.sub(r'(!\[.*\]\(.*\))', ' ', sentence) for sentence in text]
    text = [re.sub(r'(\(\/.*\))', '', sentence) for sentence in text]
    return text


def expand_contractions(text):
    '''
    Required python pkgs: 
    - re (import re)
    
    Function: Expand contractions in text.
    
    Input Arguments: 
    text: input type is list of (str) items.
        
    '''
    # specific patterns
    text = [re.sub(r"\b(i\.e\.\,?)\s?", "", sentence) for sentence in text]
    text = [re.sub(r"\btheyre\b", "they are", sentence) for sentence in text]
    text = [re.sub(r"\b(e\.g\.\,?)\s?", "", sentence) for sentence in text]
    text = [re.sub(r" \'em ", " them ", sentence) for sentence in text]
    text = [re.sub(r"(won('|\’)t|wont)", "will not", sentence) for sentence in text]
    text = [re.sub(r"((C|c)an('|\’)t|(C|c)ant)\b", "cannot", sentence) for sentence in text]
    text = [re.sub(r"\bdidnt\b", "did not", sentence) for sentence in text]
    text = [re.sub(r"\bhavnt\b", "have not", sentence) for sentence in text]
    text = [re.sub(r"\bhasnt\b", "has not", sentence) for sentence in text]
    text = [re.sub(r"\bdoesnt\b", "does not", sentence) for sentence in text]
    text = [re.sub(r"\bisnt\b", "is not", sentence) for sentence in text]
    text = [re.sub(r"\bive\b", "i have", sentence) for sentence in text]
    text = [re.sub(r"\bdont\b", "do not", sentence) for sentence in text]
    text = [re.sub(r"\bu\b", "you", sentence) for sentence in text]
    text = [re.sub(r"\bhavign\b", "having", sentence) for sentence in text]
    text = [re.sub(r"\bhavethe\b", "have the", sentence) for sentence in text]
    text = [re.sub(r"\bwiuld\b", "would", sentence) for sentence in text]
    text = [re.sub(r"\blet\'s", "let us", sentence) for sentence in text]
    # general patterns
    text = [re.sub(r"(?<=[a-z])n(\\\'|\'|\\\’|\’)t", " not", sentence) for sentence in text]
    text = [re.sub(r"(\\\'|\'|\’)re\b", " are", sentence) for sentence in text]
    #text = [re.sub(r"(\\'|\'|\’)s\b", "", sentence) for sentence in text]
    text = [re.sub(r"(?<=[a-z]|I)(\\\'|\'|\’)d\b", " would", sentence) for sentence in text]
    text = [re.sub(r"(?<=[a-z]|I)(\\\'|\'|\’)ll", " will", sentence) for sentence in text]
    text = [re.sub(r"(?<=[a-z]|I)(\'|\’)ve\b", " have", sentence) for sentence in text]
    text = [re.sub(r"\b(I|i)(\\\'m|\'m|\’m|m)\b", "i am", sentence) for sentence in text]
    text = [re.sub(r"\b((I|i)(\'|\’)ll|(I|i)ll)\b", "i will", sentence) for sentence in text]
    #text = [re.sub(r"\+", "plus", sentence) for sentence in text]
    return text


def remove_punctuation(text):
    '''
    Required python pkgs: 
    - re (import re)
    
    Function: Remove punctuation and transform text to lowercase.

    Input Arguments: 
    text: input type is list of (str) items.

    '''
    #remove possessive marker.
    text = [re.sub(r"(\\'|\'|\’)s\b", "", sentence) for sentence in text]
    #remove quotation marks. 
    text = [re.sub(r'(\“|\"|\'|\’)','', sentence) for sentence in text]
    #replace \n with single space.
    text = [re.sub(r'(\s+)?(\\n\\n\\n|\\n\\n|\\n)', ' ', sentence) for sentence in text]
    text = [re.sub(r'(\s+)?(\n\n\n|\n\n|\n)', ' ', sentence) for sentence in text]
    #remove end punctuation.
    text = [re.sub(r'([\*\~])|([\.\.\.|\.\$\%\?\!\:\*\(\)\_\-\^\>\<\;\=\+\~\[\]\,\|]\B)', ' ', sentence) for sentence in text]
    #replace inline punctuation with single space.
    text = [re.sub(r'(\b[\:\*\_\-\^\>\<\=\+\|\/]\b)', ' ', sentence) for sentence in text]
    text = [re.sub(r'([\:\*\_\-\^\>\<\=\+\|\/])', ' ', sentence) for sentence in text]
    #remove all duplicate whitespace characters.
    text = [re.sub(r'(?<=[^\b\s])( )+', ' ', sentence) for sentence in text]
    #remove all non-word or whitespace characters, e.g., emojis.
    text = [re.sub(r'[^\w\s]', '', sentence) for sentence in text]
    #remove all duplicate whitespace characters.
    text = [re.sub(r'(?<=[^\b\s])( )+', ' ', sentence) for sentence in text]
    #return text in lowercase, and remove all leading and trailing white spaces.
    text = [sentence.lower().strip() for sentence in text]
    return text


def remove_stopwords(text, stoplist_type='general'):
    '''
    Required python pkgs: 
    - re (import re)
    
    Function: Filter stop words from input text, using specified {stoplist_type} {stop_words} list.
    
    Input Arguments: 
    text: input type is list of (str) items.
    stoplist_type: input type is (str) item, 'general' (no prepositions), 'prep' (prepositions only), 'full' (both).
    
    '''
    if stoplist_type == 'general': 
        stop_words_simple = ['is', 'am', 'are', 'was', 'were', 'be', 'been', 'being', 'will', 
                        'have', 'has', 'had', 'having',
                        'do', 'does', 'did',
                        'can', 'may', 'might', 'would', 'could',
                        'i', 'me', 'my', 'myself',
                        'we', 'our', 'ours', 
                        'you', 'your', 'yours',
                        'she', 'her', 'hers', 
                        'his', 'he', 'him', 
                        'they', 'them', 'theirs',
                        'there', 'their', 
                        'this', 'that', 'these', 'those', 
                        'then', 'so', 'a', 'an', 'the', 'as', 'it', 'too', 'when','and', 
                        'but', 'if', 'or', 'because']
        stop_words = stop_words_simple
    if stoplist_type == 'prep':  
        stop_words_prep = [ 'in', 'at', 'on', 'any', 'of', 'from', 'for', 'with']
        stop_words = stop_words_prep
    if stoplist_type == 'full': 
        stop_words_full = stop_words_simple + stop_words_prep
        stop_words = stop_words_full
    text_output = []
    for sentence in text: 
        text = ' '.join([word for word in sentence.lower().split() if word not in stop_words])
        text_output.append(text)
    return text_output


def remove_numbers(text): 
    '''
    Required python pkgs: 
    - re (import re)
    
    Function: Remove numbers from text data.
    
    Input Arguments: 
    text: input type is list of (str) items.
    
    '''
    text = [re.sub(r"(1x)('?s)?", "one time", sentence) for sentence in text] 
    text = [re.sub(r"(2x)('?s)?", "two times", sentence) for sentence in text] 
    text = [re.sub(r"(3x)('?s)?", "three times", sentence) for sentence in text] 
    text = [re.sub(r"(4x)('?s)?", "four times", sentence) for sentence in text] 
    text = [re.sub(r"(5x)('?s)?", "five times", sentence) for sentence in text]
    text = [re.sub(r'\b([0-9](th|st|rd|nd))\b', '', sentence) for sentence in text]
    text = [re.sub(r'\b([0-9]\-)([0-9]x)\b', '', sentence) for sentence in text]
    text = [re.sub(r'\b([0-9]\.)([0-9]x[0-9]+\"?)?', '', sentence) for sentence in text]
    text = [re.sub(r'\b([0-9]+.?[0-9]+)([a-z]+)\b', '', sentence) for sentence in text]
    text = [re.sub(r'\b([A-Za-z]+?[0-9]+[A-Za-z]+[0-9]+[A-Za-z]+)\b', '', sentence) for sentence in text]
    text = [re.sub(r'\b([A-Za-z]+)?([0-9]+)([A-Za-z]+)?\b', '', sentence) for sentence in text]
    text = [re.sub(r'([A-Z]+[0-9])\w+', '', sentence) for sentence in text]
    text = [re.sub(r'([$]?[0-9]+[%a-z]+?\.? )\b', '', sentence) for sentence in text]
    text = [re.sub(r'([0-9]+[\.,:\-\_]?)([0-9]+)?([a-z]+)?( )?\b', '', sentence) for sentence in text]
    return text


def ner_reddit(text): 
    '''        
    Required python pkgs: 
    - re (import re)
    
    Function: Regularize select items from text data.

    Input Arguments: 
    text: input type is list of (str) items.
       
    '''
    text = [re.sub(r"\b(O|o)(K|k)\b", "okay", sentence) for sentence in text]
    text = [re.sub(r"\byr\b", "year", sentence) for sentence in text]
    text = [re.sub(r"\bvac\b", "vacuum", sentence) for sentence in text]
    text = [re.sub(r"\bsoooo\b", "so", sentence) for sentence in text]
    text = [re.sub(r"\bslooowwww\b", "slow", sentence) for sentence in text]
    text = [re.sub(r"\b(multi-room|multi room)\b", "multiroom", sentence) for sentence in text]
    text = [re.sub(r"\b(thx|tysm|ty|thank you|thank)\b", "thanks", sentence) for sentence in text]
    text = [re.sub(r"\bgooood\b", "good", sentence) for sentence in text]
    text = [re.sub(r"byyyyye", "bye", sentence) for sentence in text]
    text = [re.sub(r"living room", "livingroom", sentence) for sentence in text]
    text = [re.sub(r"(pre-recorded)", "prerecorded", sentence) for sentence in text]
    text = [re.sub(r"dining room", "diningroom", sentence) for sentence in text]
    text = [re.sub(r"e-mail", "email", sentence) for sentence in text]
    text = [re.sub(r"((W|w)i-(F|f)i|(W|w)i (F|f)i)\b", "wifi", sentence) for sentence in text]
    text = [re.sub(r"(re-use)", "reuse", sentence) for sentence in text]
    text = [re.sub(r"(re-link)", "relink", sentence) for sentence in text]
    text = [re.sub(r"(re-set)", "reset", sentence) for sentence in text]
    text = [re.sub(r"(re-install)", "reinstall", sentence) for sentence in text]
    text = [re.sub(r"(M|m)ac (O|o)(S|s)", "macos", sentence) for sentence in text]
    text = [re.sub(r" \& ", " and ", sentence) for sentence in text]
    text = [re.sub(r"\&", " and ", sentence) for sentence in text]
    return text


nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

def singularize_plural_noun(text):
    '''
    Required python pkgs: 
    (https://spacy.io/usage/)
    - spacy (import spacy)
    - 'en_core_web_sm' language model (python -m spacy download en_core_web_sm)
    
    Function: Transform plural nouns to singular form. 

    Input Arguments: 
    text: input type is list of (str) items.
        
    '''
    result = []
    for sent in text: 
        sentence = nlp(sent)
        output = (" ".join([token.lemma_ for token in sentence]))
        result.append(output)
    return result


def tokenize_text(text): 
    '''
    Required python pkgs: 
     - nltk (from nltk.tokenize import word_tokenize, sent_tokenize)
     
    Function: Transform text into token form.
    
    Input Arguments: 
    text: input type is list of (str) items.
    
    '''
    token_ls = []
    for sentence in text:
        token_text = ' '.join(word_tokenize(sentence))
        token_ls.append(token_text)
    return token_ls


def lemmatize_text(text): 
    '''
    Required python pkgs: 
     - nltk (from nltk.stem.wordnet import WordNetLemmatizer)
    
    Function: Transform text into lemmatize form.
    
    Input Arguments: 
    text: input type is list of (str) items.
    
    '''
    lemmatizer = WordNetLemmatizer()
    lemma_ls = []
    for sentence in text: 
        lemma_text = ''.join([lemmatizer.lemmatize(word) for word in sentence.lower()]) #.split()
        lemma_ls.append(lemma_text.strip())
    return lemma_ls


def clean_text(text, method, singularize='yes', stopwords='yes', stopword_listtype='general'):
    '''
    Required python pkgs:
    - re (import re) 
    - nltk (from nltk.tokenize import word_tokenize, sent_tokenize)
    - nltk (from nltk.stem.wordnet import WordNetLemmatizer) 
    
    Function: Preprocess text entries.
    - Remove hyperlinks, 
    - Expand contractions, 
    - Remove numbers,
    - Perform NER regularization,
    - Remove punctuation, 
    - Option: Filter stop words,
    - Tokenize/Lemmatize text.
    
    Input Arguments: 
    text: input type is list of (str) items.
    method: input type is (str) item, 'token' or 'lemma'.
    singularize: input type is (str) item, 'yes' or 'no' (default = 'yes').
    stopwords: input type is (str) item, 'yes' or 'no' (default = 'yes').
    stoplist_type: input type is (str) item, 'simple' (no prepositions), 'prep' (prepositions only), 'full' (both) (default = 'general').
    
    Examples: 
    clean_text(utterance_list, 'lemma')
    clean_text(utterance_list, 'token')
    
    '''
    
    text = remove_hyperlinks(text)
    text = expand_contractions(text)
    text = remove_numbers(text)
    text = ner_reddit(text)
    text = remove_punctuation(text)
 
    # text = list(filter(None, text))
    if method == 'token': 
        text_output = tokenize_text(text)
    elif method == 'lemma': 
        text_output = lemmatize_text(text) 
    if singularize == 'yes': 
        text_output = singularize_plural_noun(text_output)
    if stopwords == 'yes': 
        text_output = remove_stopwords(text_output, stopword_listtype)  
    return text_output


def format_dataset(df): 
    if df.columns[1] == 'created_datetime_pst': 
        datatype = 'praw'
    if df.columns[1]=='selftext':
        datatype = 'ps_submissions'
    if df.columns[1]=='author_is_blocked':
        datatype = 'ps_comments'
    #Praw: Reformat Comments
    if datatype =='praw':
        output_df = reformat_praw_comments(df)
    #Pushshift Submissions
    if datatype =='ps_submissions': 
        metadata_df = df[['created_utc', 'utc_datetime_str', 'created_pst', 'retrieved_utc', 'subreddit', 'id', 'permalink', 'url', 'author', 'title', 'selftext', 'removed_by_category', 'is_created_from_ads_ui']].copy()
        output_df = metadata_df.rename(columns={ "id": "submission_id", "author": "submission_author", "selftext": "body"})
    #Pushshift Comments
    if datatype =='ps_comments': 
        metadata_df = df[['created_utc', 'utc_datetime_str', 'created_pst', 'retrieved_utc', 'subreddit', 'link_id', 'id', 'permalink', 'author', 'is_submitter', 'body', 'parent_id', 'nest_level']].copy()
        output_df = metadata_df.rename(columns={"link_id": "submission_id", "id": "comment_id", "author": "comment_author", "body": "comments"})
    return output_df
    

def preprocess_text_data(df_filepath, category, subreddit_name, method='token', sep='tab', column_list = ['title', 'body', 'comments'], singularize='yes', stopwords='yes', stopword_listtype='general'):
    '''
    Function: Aggregate & regularize input text data. 
    - Aggregate datasets in {df_filepath} using glob.
    - Reformat aggregated dataset using format_dataset().
    - For each {column} in {column_list}, convert aggregated dataset {column} values to list.
    - Write aggregated text list as JSON to __aggregated_posts/{category}/{subreddit_name} directory.
    - Clean text data using clean_text().
    - Write cleaned text list as JSON to __aggregated_posts/{category}/{subreddit_name} directory.
    
    Input Arguments: 
    df_filepath: input type is (str) item, denoting filepath. 
    column_list: input type is (list) of (str) items.
    category: input type is (str) item, denoting output subdirectory name.
    subreddit_name: input type is (str) item, denoting output subdirectory name.
    method: input type is (str) item, 'token' or 'lemma'.
    singularize: input type is (str) item, 'yes' or 'no'. Default = 'yes'.
    sep: input type is (str) item, 'tab' or 'comma'. Default = 'tab'.
    stopwords: input type is (str) item, 'yes' or 'no'. Default = 'yes'.
    stoplist_type: input type is (str) item, 'simple' (no prepositions), 'prep' (prepositions only), 'full' (both). Default = 'general'.
    
    Example: 
    datascience_filepath = '../__data/__posts/DataScience/MachineLearning'
    column_list = ['title', 'body', 'comments']
    
    process_text_data(df_filepath=datascience_filepath, column_list=column_list, category='DataScience', subreddit_name='MachineLearning', method='lemma')
    process_text_data(df_filepath=datascience_filepath, column_list=column_list, category='DataScience', subreddit_name='MachineLearning', method='token')  
    
    '''
    
    try: 
        if len(glob.glob(f'{df_filepath}/*.csv')) == 0:
            raise TypeError 
        if type(subreddit_name) != str:
            print(f'Error: Specified subreddit ({subreddit_name}) not found!')
            raise TypeError 
        if type(category) != str:
            print(f'Error: Specified sudirectory category ({category}) not found!')
            raise TypeError 
        if singularize not in ['yes','no']:
            raise TypeError 
        if stopwords not in ['yes','no']:
            raise TypeError 
        if method not in ['token','lemma']:
            print(f'\nError: specified method ({method}) is unsupported!')
            raise TypeError
        if stopword_listtype not in ['general','prep','full']:
            print(f'\nError: specified stopword_listtype ({stopword_listtype}) is unsupported!')
            raise TypeError
        if sep not in ['comma','tab']:
            print(f'\nError: specified separator ({sep}) is unsupported!')
            raise TypeError
        
        if sep=='tab': 
            sep='\t'
        if sep =='comma':
            sep=','
    
        snapshotdate = datetime.today().strftime('%d-%b-%Y') 
        snapshotdatetime = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')
        print(f'\nInitializing Text Cleaning Task... \n Category: {category}\n Subreddit: "{subreddit_name}"\n')
        dfs = glob.glob(f'{df_filepath}/*.csv')
        agg_df = pd.concat([pd.read_csv(fp, header=0, encoding="utf-8", engine='python', sep=None) for fp in dfs], ignore_index=True) #, engine='python', sep=None
        agg_format_df = format_dataset(agg_df)
        os.makedirs(f"../__data/__aggregated_posts/{category}/{subreddit_name}/raw/{snapshotdate}/{subreddit_name}_agg_data", exist_ok=True)
        print(f'...Saving aggregated "{subreddit_name}" dataset.\n')
        agg_format_df.to_csv(f'../__data/__aggregated_posts/{category}/{subreddit_name}/raw/{snapshotdate}/{subreddit_name}_agg_data/{subreddit_name}_agg_df_{snapshotdatetime}.csv', index=False, sep=sep)
        clean_df = agg_format_df.reset_index()
        for column in column_list:
            column_ls = clean_df[column].to_list()
            os.makedirs(f"../__data/__aggregated_posts/{category}/{subreddit_name}/raw/{snapshotdate}/{subreddit_name}_{column}_data", exist_ok=True)
            print(f'...Saving aggregated "{subreddit_name}_{column}" text.')
            json_object = f'../__data/__aggregated_posts/{category}/{subreddit_name}/raw/{snapshotdate}/{subreddit_name}_{column}_data/{subreddit_name}_{column}_agg_{snapshotdatetime}.json'
            print(f"...Initializing text preprocessing for '{subreddit_name}_{column}' dataset\n(method='{method}', singularize='{singularize}', stopwords='{stopwords}', stopword_listtype='{stopword_listtype}').")
            with open(json_object, 'w') as f:
                json.dump(column_ls, f, indent=2)
            if column != 'title': 
                output_text = remove_usernames(column_ls)
                output_text = clean_text(output_text, method=method, singularize=singularize, stopwords=stopwords, stopword_listtype=stopword_listtype)
            else: 
                output_text = clean_text(column_ls, method=method, singularize=singularize, stopwords=stopwords, stopword_listtype=stopword_listtype)
            
            clean_df[f'cleaned_{column}'] = output_text
            os.makedirs(f"../__data/__aggregated_posts/{category}/{subreddit_name}/clean/{snapshotdate}/{subreddit_name}_{column}_data", exist_ok=True)
            print(f'...Saving cleaned "{subreddit_name}_{column}" text.')
            json_clean_object = f'../__data/__aggregated_posts/{category}/{subreddit_name}/clean/{snapshotdate}/{subreddit_name}_{column}_data/{subreddit_name}_{column}_agg_clean_{snapshotdatetime}.json'
            with open(json_clean_object, 'w') as f:
                json.dump(output_text, f, indent=2)
            print(f"Text Cleaning Task for '{subreddit_name}_{column}' Complete!\n")
        os.makedirs(f"../__data/__aggregated_posts/{category}/{subreddit_name}/clean/{snapshotdate}/{subreddit_name}_agg_data", exist_ok=True)
        clean_df.to_csv(f'../__data/__aggregated_posts/{category}/{subreddit_name}/clean/{snapshotdate}/{subreddit_name}_agg_data/{subreddit_name}_agg_clean_{method}_df_{snapshotdatetime}.csv', index=False, sep=sep)
        print(f"Text Cleaning Task for Subreddit: '{subreddit_name}' Complete!\n")      
    except TypeError:
        print(f'\nOh no! Seems there is an issue with the input values:\n\n   Input Directory: {df_filepath}\n   Number CSVs: {len(glob.glob(f"{df_filepath}/*.csv"))}\n   Subreddit: {subreddit_name}\n   Category: {category}\n   Method: {method}\n   Dataset separator: {sep}\n   Stopword (y/n): {stopwords}\n   Stopword List: {stopword_listtype}\n   Singularize (y/n): {singularize}')
        print('\nPlease check your input values, and try again.\n')
    
     
     
            
if __name__ == "__main__":
    preprocess_text_data()