<h3 align='center'>Reddit-NLP Example Use-Cases</h3>

---
### Pre-Processing Reddit Text Data 
---

Text pre-processing is a fundamental step in data analysis, used to regularize or "clean" raw data. Symbols, punctuation, and other irregularities present in raw text data are removed, and variations in entity names and processes undergo regularization. Once "cleaned", the output dataset is ready for use in various ML-related analysis tasks (e.g., classification, clustering, topic modeling, sentiment analysis).

- #### [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py)
The [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) script uses the <b>preprocess_data( )</b> function to locate and clean reddit text data. Required input variables include specification of a *data_filepath* and a *category_list* of subdirectory name(s) containing the Subreddit datasets you wish to clean, e.g., 
```
   data_filepath = '~/didactic-diy/reddit/__data/__posts'  
   reddit_text_preprocessor(data_filepath, category_list=['Amazon'])
```
For a each category subdirectory provided in the *category_list*, (e.g., [Amazon](https://github.com/kariemoorman/didactic-diy/tree/main/reddit/__data/__posts/Amazon)), [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) identifies all nested Subreddit subdirectories, and for each Subreddit will aggregate and clean all specified text columns of the dataset (defined via *column_list* input variable) using the *method* specified (either "lemma" or "token"). Additionally, users may specify the delimiter of the output cleaned dataset using the *sep* input variable, either "tab" or "comma" (see [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py#L18) for a defined list of input variables).

- #### [clean_reddit_text.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/clean_reddit_text.py) &  [clean_amazon_reddit_text.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/clean_amazon_reddit_text.py) 
Non-Amazon Subreddits undergo text pre-processing using [clean_reddit_text.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/clean_reddit_text.py). Amazon-specific categories of subreddits, explicitly defined via *amznsubdir_list*, undergo text pre-processing using [clean_amazon_reddit_text.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/clean_amazon_reddit_text.py). The two scripts differ in terms of regularization of NER and numbers.

For users who wish to perform a preliminary text pre-processing step and do not need to specify Subreddit subdirectories within a list of Category subdirectories, the [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) script is for you.

For users who wish to perform a preliminary text pre-processing step and wish to specify Subreddit subdirectories within a specific list of Category subdirectories, the [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) script is for you.

--- 
### File Structure Requirements for [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py)

The nested filepath structure expected by the underlying function of [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py), <b>preprocess_data( )</b> is provided below:

```
 
data_filepath = '/data_directory'
category_list = ['category_a_subdirectory_name', 'category_b_subdirectory_name']

> data_directory
    >> category_a_subdirectory_name
        >>> subreddit_1_subdirectory_name
            >>>> subreddit_1_dataset_1.csv
            >>>> ...
        >>> subreddit_2_subdirectory_name
            >>>> subreddit_2_dataset_1.csv
            >>>> ...
    >> category_b_subdirectory_name
        >>> subreddit_1_subdirectory_name
            >>>> subreddit_a_dataset_1.csv
            >>>> ...
        >>> subreddit_2_subdirectory_name
            >>>> subreddit_2_dataset_1.csv
            >>>> ...

```

To better understand <b>preprocess_data( )</b>, consider the example below. The *data_filepath* denotes the directory containing the *category_list* subdirectories. The text columns are defined via *column_list* as ['title', 'body', 'comments'], the text pre-processing *method* is "token", and the output dataset will be 'tab' delimited. The text cleaning step will include filtering of *stopwords*, using the 'general' *stopword_listtype*, and the NER step will include singularization (specified via *singularize* input variable).

```
 
data_filepath = '/reddit/__data/__posts'
category_list = ['AmazonAlexa','AmazonPrimeAV']

preprocess_data(data_filepath,  
                category_list=category_list, 
                subreddit_list=['all'],
                sep='tab',
                amznsubdir_list=['Amazon','AmazonAlexa','AmazonPrime','AmazonPrimeAV','AmazonSmartHome'],
                column_list=['title', 'body', 'comments'], 
                method='token',
                singularize='yes', 
                stopwords='yes', 
                stopword_listtype='general')

```

Amazon-specific sudirectory category names, defined via *amznsubdir_list*, do include those category names specified in the *category_list*: ['AmazonAlexa','AmazonPrimeAV']. This means the associated Subreddit datasets will call [clean_amazon_reddit_text.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/clean_amazon_reddit_text.py) during text pre-processing.

The nested filepath structure associated with *data_filepath* and *category_list* input variables is provided below:

```
 
data_filepath = 'reddit/__data/__posts'
category_list = ['AmazonAlexa','AmazonPrimeAV']

> reddit 
  >> __data 
    >>> __posts
        >>>> AmazonAlexa
            >>>>> subreddit_1_subdirectory (e.g., alexa)
                >>>>>> alexa_dataset_1.csv
                >>>>>> ...
            >>>>> subreddit_2_subdirectory (e.g., amazon)
                >>>>>> amazon_dataset_1.csv
                >>>>>> ...
        >>>> AmazonPrimeAV
            >>>>> subreddit_1_subdirectory (e.g., amazonprime)
                >>>>>> amazonprime_dataset_1.csv
                >>>>>> ...
            >>>>> subreddit_2_subdirectory (e.g., AmazonPrimeVideo)
                >>>>>> amazonprimevideo_dataset_1.csv
                >>>>>> ...

```

In this example, all Subreddit subdirectory names within a provided Category subdirectory are discovered at runtime, as *subreddit_list* is set to ['all']. In cases where the explicit specification of Subreddit subdirectories is desired, simply define the list of target Subreddit subdirectories using the *subreddit_list* input variable (e.g., subreddit_list=['amazon', 'alexa']).

For users who use [subreddit_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_scraper.py) and/or [subreddit_search_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_search_scraper.py) to generate subreddit_datasets, the [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) script provides a simple way to quickly aggregate and pre-process Reddit text data.

---
