## Reddit-NLP Example Use-Cases

### Pre-Processing Reddit Text Data 
Text pre-processing is a fundamental step in data analysis, used to regularize or "clean" raw data. Symbols, punctuation, and other irregularities present in raw text data are removed, and variations in entity names and processes undergo regularization. Once "cleaned", the output dataset is ready for use in various ML-related analysis tasks (e.g., classification, clustering, topic modeling, sentiment analysis).

#### [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py)
The [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) script uses the <b>preprocess_data( )</b> function to locate and clean reddit text data. Required input variables include specification of a *data_filepath* and a *category_list* of subdirectory name(s) containing the Subreddit datasets you wish to clean.

The nested filepath structure expected by <b>preprocess_data( )</b> is provided below:

```
 
data_filepath = '/data_directory'
category_list = ['category_a_subdirectory_name', 'category_b_subdirectory_name']

> data_directory
    >> category_a_subdirectory_name
        >>> subreddit_1_subdirectory_name
            >>>> subreddit_1_dataset_1.csv
            >>>> subreddit_1_dataset_2.csv
            >>>> subreddit_1_dataset_3.csv
        >>> subreddit_2_subdirectory_name
            >>>> subreddit_2_dataset_1.csv
            >>>> subreddit_2_dataset_2.csv
            >>>> subreddit_2_dataset_3.csv
    >> category_b_subdirectory_name
        >>> subreddit_1_subdirectory_name
            >>>> subreddit_a_dataset_1.csv
            >>>> subreddit_a_dataset_2.csv
            >>>> subreddit_a_dataset_3.csv
        >>> subreddit_2_subdirectory_name
            >>>> subreddit_2_dataset_1.csv
            >>>> subreddit_2_dataset_2.csv
            >>>> subreddit_2_dataset_3.csv

```

For a given category subdirectory, <b>preprocess_data( )</b> identifies all nested Subreddit subdirectories as a default (i.e., when *subreddit_list*=['all']), and for each Subreddit will aggregate and clean all specified text columns of the dataset (defined via *column_list* input variable) using the *method* specified (either "lemma" or "token"). Additionally, users may specify the delimiter of the output cleaned dataset using the *sep* input variable, either "tab" or "comma" (see [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) for a defined list of input variables).

Amazon-specific categories of subreddits, identified via *amznsubdir_list*, undergo text pre-processing using [clean_amazon_reddit_text.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/clean_amazon_reddit_text.py), while non-Amazon Subreddits undergo text pre-processing using [clean_reddit_text.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/clean_reddit_text.py). The two scripts differ in terms of regularization of NER and numbers.

To better understand <b>preprocess_data( )</b>, consider the example below. The *data_filepath* denotes the directory containing the *category_list* subdirectories. The text columns are defined via *column_list* as ['title', 'body', 'comments'], the text pre-processing *method* is "token", and the output dataset will be 'tab' delimited. The text cleaning step will include filtering of *stopwords*, using the 'general' *stopword_listtype*, and the NER step will include singularization (specified via *singularize* input variable).

```
 
data_filepath = 'reddit/__data/__posts'
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
                >>>>>> alexa_dataset_2.csv
            >>>>> subreddit_2_subdirectory (e.g., amazon)
                >>>>>> amazon_dataset_1.csv
                >>>>>> amazon_dataset_2.csv
        >>>> AmazonPrimeAV
            >>>>> subreddit_1_subdirectory (e.g., amazonprime)
                >>>>>> amazonprime_dataset_1.csv
                >>>>>> amazonprime_dataset_2.csv
            >>>>> subreddit_2_subdirectory (e.g., AmazonPrimeVideo)
                >>>>>> amazonprimevideo_dataset_1.csv
                >>>>>> amazonprimevideo_dataset_2.csv

```

In this example, all Subreddit subdirectory names within a provided Category subdirectory are discovered at runtime, as *subreddit_list* is set to ['all']. In cases where the explicit specification of Subreddit subdirectories is desired, simply define the list of target Subreddit subdirectories using the *subreddit_list* input variable (e.g., subreddit_list=['amazon', 'alexa']).

For users who use [subreddit_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_scraper.py) and/or [subreddit_search_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_search_scraper.py) to generate subreddit_datasets, the [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) script provides a simple way to aggregate and pre-process Reddit text data.

For users who wish to perform a preliminary text pre-processing step and do not need to specify Subreddit subdirectories within a list of Category subdirectories, the [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) script is for you.

For users who wish to perform a preliminary text pre-processing step and wish to specify Subreddit subdirectories within a specific list of Category subdirectories, the [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) script is for you.


<br>


### Scrape and Pre-Process Reddit Text Data 

#### [scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main//reddit/__scripts/reddit_nlp/scrape_and_clean_reddit_data.py)

The [scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/scrape_and_clean_reddit_data.py) script allows users ability to dynamically scrape a particular subreddit and pre-process the associated text data within one command. It contains two options: 

<b>scrape_and_clean_reddit_posts( )</b>

<b>search_scrape_and_clean_reddit_posts( )</b>.

<br>
The <b>scrape_and_clean_reddit_posts( )</b> function requires users specify a *subreddit_list* of subreddit names, a *category* subdirectory name (where the set of Subreddit subdirectories and Subreddit datasets will be written), and a choice of *api* (either 'praw' or 'pushshift'). Depending on *api* choice, users can further define input specifications for webscraping task execution (e.g., api='praw': post_type, post_limit; api='pushshift': before_days, post_limit).

With a *subreddit_list*, a *category* subdirectory name, and a choice of *api* specified, <b>scrape_and_clean_reddit_posts( )</b> calls [subreddit_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_scraper.py) and [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) to perform a webscraping task and text cleaning task for each Subreddit.

Consider the following example:

```
 
subreddit_list = ['MachineLearning', 'datascience']
category='DataScience'

scrape_and_clean_reddit_posts(
    subreddit_list=subreddit_list, 
    category=category, 
    sep='tab', 
    api='praw', 
    post_type='new', 
    before_days='0d', 
    post_limit=1000, 
    amznsubdir_list=['Amazon','AmazonAlexa','AmazonPrimeAV','AmazonSmartHome'], 
    method='token', 
    singularize='yes', 
    stopwords='yes', 
    stopword_listtype='general'):

```

The Subreddits 'MachineLearning' and 'datascience' are scraped using 'praw' *api*, returning a maximum of 1000 'new' posts (submissions and associated comments). For each Subreddit, the resultant dataset undergoes a text pre-processing step using 'token' method, including filtering of *stopwords* using the 'general' *stopword_listtype* and singularization as part of the NER step (specified via *singularize* input variable).

<br>

The <b>search_scrape_and_clean_reddit_posts( )</b> function is used in instances where the user wishes to perform a search query on the set of input Subreddits (e.g., "search for posts containing 'language models' in 'MachineLearning' and 'datascience' Subreddits."). It calls [subreddit_search_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_search_scraper.py) and [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) to perform both a query search and webscraping task and text cleaning task for each Subreddit.

The <b>search_scrape_and_clean_reddit_posts( )</b> function requires a *search_query_list* of search query terms in addition to a *subreddit_list* of Subreddit names, a *category* subdirectory name (where the set of Subreddit subdirectories and Subreddit datasets will be stored), and a choice of *api* (either 'praw' or 'pushshift'). Depending on *api* choice, users can further define input specifications (e.g., api='praw': post_type, post_limit; api='pushshift': before_days, post_limit).

Consider the following example:

```
 
subreddit_list = ['MachineLearning', 'datascience']
search_query_list = ['language model', 'GPT']
category='DataScience'

search_scrape_and_clean_reddit_posts(
    subreddit_list=subreddit_list, 
    search_query_list=search_query_list, 
    category=category, 
    sep='tab', 
    api='praw', 
    post_type='new', 
    before_days='0d', 
    post_limit=1000, 
    amznsubdir_list=['Amazon','AmazonAlexa','AmazonPrimeAV','AmazonSmartHome'], 
    method='token', 
    singularize='yes', 
    stopwords='yes', 
    stopword_listtype='general')

```

The Subreddits 'MachineLearning' and 'datascience' are scraped using 'praw' *api*, returning a maximum of 1000 'new' posts (submissions and associated comments) that contain either 'language model' or 'GPT' search query terms. For each Subreddit, the resultant dataset undergoes a text pre-processing step using 'token' method, and includes filtering of *stopwords* using the 'general' *stopword_listtype* and singularization as part of the NER step (specified via *singularize* input variable).
<br>

Both <b>scrape_and_clean_reddit_posts( )</b> and <b>search_scrape_and_clean_reddit_posts( )</b> generate a nested subdirectory filepath structure described below:

```
 
> __data
    >> __posts
        >>> category (e.g., DataScience)
            >>>> subreddit_subdirectory_1 (e.g., MachineLearning)
                >>>>> machinelearning_dataset_1.csv
            >>>> subreddit_subdirectory_2 (e.g., datascience)
                >>>>> datascience_dataset_1.csv
    >> __aggregated_posts
        >>> category (e.g., DataScience)
            >>>> subreddit_1_subdirectory (e.g., MachineLearning)
                >>>>> clean
                    >>>>>> date
                        >>>>>>> subreddit_1_agg_data
                            >>>>>>>> subreddit_1_agg_clean_dataset.csv
                        >>>>>>> subreddit_1_body_data
                            >>>>>>>> subreddit_1_body_agg_clean_dataset.csv
                        >>>>>>> subreddit_1_comments_data
                            >>>>>>>> subreddit_1_comments_agg_clean_dataset.csv
                        >>>>>>> subreddit_1_title_data
                            >>>>>>>> subreddit_1_title_agg_clean_dataset.csv
                >>>>> raw
                    >>>>>> date
                        >>>>>>> subreddit_1_agg_data
                            >>>>>>>> subreddit_1_agg_dataset.csv
                        >>>>>>> subreddit_1_body_data
                            >>>>>>>> subreddit_1_body_agg_dataset.csv
                        >>>>>>> subreddit_1_comments_data
                            >>>>>>>> subreddit_1_comments_agg_dataset.csv
                        >>>>>>> subreddit_1_title_data
                            >>>>>>>> subreddit_1_title_agg_dataset.csv
            >>>> subreddit_2_subdirectory (e.g., datascience)
                >>>>> clean
                    >>>>>> date
                        >>>>>>> subreddit_2_agg_data
                            >>>>>>>> subreddit_2_agg_clean_dataset.csv
                        >>>>>>> subreddit_2_body_data
                            >>>>>>>> subreddit_2_body_agg_clean_dataset.csv
                        >>>>>>> subreddit_2_comments_data
                            >>>>>>>> subreddit_2_comments_agg_clean_dataset.csv
                        >>>>>>> subreddit_2_title_data
                            >>>>>>>> subreddit_2_title_agg_clean_dataset.csv
                >>>>> raw
                    >>>>>> date
                        >>>>>>> subreddit_2_agg_data
                            >>>>>>>> subreddit_2_agg_dataset.csv
                        >>>>>>> subreddit_2_body_data
                            >>>>>>>> subreddit_2_body_agg_dataset.csv
                        >>>>>>> subreddit_2_comments_data
                            >>>>>>>> subreddit_2_comments_agg_dataset.csv
                        >>>>>>> subreddit_2_title_data
                            >>>>>>>> subreddit_2_title_agg_dataset.csv

```

The '__posts' subdirectory is a product of the webscraping task, while the '__aggregated_posts' sudirectory is a product of the text cleaning task.


For users who want to specify a limited amount of information (i.e., a list of subreddit names, a category subdirectory name, a list of search query terms) and have the script handle the rest (webscraping and text pre-processing), the [scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main//reddit/__scripts/reddit_nlp/scrape_and_clean_reddit_data.py) script is for you.


For users who want to specify exact information regarding the type of api calls to be made (e.g., api as 'praw' or 'pushshift', post_limit, post_type, before_days) and/or the type of text pre-processing to be conducted (e.g., 'token' or 'lemma', stopword filtering as 'general' or 'prep' or 'full', NER singularization), and have the script handle the rest (webscraping and text pre-processing), the [scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main//reddit/__scripts/reddit_nlp/scrape_and_clean_reddit_data.py) script is for you.

