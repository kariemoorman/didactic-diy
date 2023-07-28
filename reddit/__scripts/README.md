<h3 align='center'>Reddit Data Extraction Example Use-Cases</h3>

---
### Scrape and Pre-Process Reddit Text Data 
---

- #### [scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main//reddit/__scripts/scrape_and_clean_reddit_data.py)

The [scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/scrape_and_clean_reddit_data.py) scrapes a particular subreddit and pre-processes the associated text data within one command. With *subreddits*, *category* output subdirectory name, and a choice of *api* specified (default is PRAW), [scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/scrape_and_clean_reddit_data.py) calls [subreddit_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_scraper.py) and [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) to perform a webscraping task and text cleaning task for each Subreddit. E.g.,

```
python3 scrape_and_clean_reddit_data.py datascience MachineLearning -c DataScience -l 100

python3 scrape_and_clean_reddit_data.py datascience MachineLearning -c DataScience --api praw --post_type new --post_limit 100 --method token --singularize yes --stop_words yes --stopword_listtype general
``````

In the above example, subreddits 'MachineLearning' and 'datascience' are scraped using 'praw' *api*, returning a maximum of 100 'new' posts (submissions and associated comments). For each Subreddit, the resultant dataset undergoes a text pre-processing step using 'token' method, including filtering of *stopwords* using the 'general' *stopword_listtype* as well as singularization as part of the NER step (specified via *singularize* input variable).

For users who want to specify a limited amount of information (e.g., a list of subreddit names, a category subdirectory name) and have the script handle the rest (webscraping and text pre-processing), [scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/scrape_and_clean_reddit_data.py) is for you.

For users who want to specify exact webscraping information (e.g., api, post_limit, post_type) and/or the type of text pre-processing to be conducted (e.g., 'token' or 'lemma', stopword filtering as 'general' or 'prep' or 'full', NER singularization), and have the script handle the rest (webscraping and text pre-processing), [scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/scrape_and_clean_reddit_data.py) is for you.

---
### Search, Scrape and Pre-Process Reddit Text Data 
---

- #### [search_scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/search_scrape_and_clean_reddit_data.py)

The [search_scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/search_scrape_and_clean_reddit_data.py) function is used in cases where the user wishes to perform a search query on a set of Subreddits. Users specify a list of *search_query_items*, a list of  *subreddits*, an output *category* subdirectory name (where the set of Subreddit subdirectories and Subreddit datasets will be stored), and the [search_scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/search_scrape_and_clean_reddit_data.py) function calls [subreddit_search_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_search_scraper.py) and [reddit_text_preprocessor.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_nlp/reddit_text_preprocessor.py) to perform both a query search and webscraping task and text cleaning task for each Subreddit. E.g.,

```
python3 search_scrape_and_clean_data.py datascience MachineLearning -q GPT LLM -c DataScience -l 100

python3 search_scrape_and_clean_data.py datascience MachineLearning -q GPT LLM -c DataScience --api praw --post_type new --post_limit 100 --method token --singularize yes --stop_words yes --stopword_listtype general
```


In the above example, subreddits 'MachineLearning' and 'datascience' are scraped using 'praw' *api*, returning a maximum of 100 'new' posts (submissions and associated comments) that contain either 'LLM' or 'GPT' search query terms. For each subreddit, the resultant dataset undergoes a text pre-processing step using 'token' method, and includes filtering of *stopwords* using the 'general' *stopword_listtype* and singularization as part of the NER step (specified via *singularize* input variable).

For users who want to add a list of search query terms to their extract and transform process, [search_scrape_and_clean_reddit_posts.py](https://github.com/kariemoorman/didactic-diy/blob/main//reddit/__scripts/reddit_nlp/scrape_and_clean_reddit_data.py) script is for you.

---
### Resultant File Structure 

Both [search_scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/search_scrape_and_clean_reddit_data.py) and [search_scrape_and_clean_reddit_data.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/search_scrape_and_clean_reddit_data.py) generate a nested subdirectory filepath structure described below:

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


---

<p align='center'><b>License: <a href='https://choosealicense.com/licenses/gpl-3.0/'>GNU General Public License v3.0</a></b></p>
