## Reddit-Scraper Example Use-Cases

### Identify & Extract Reddit User Activity

#### 
[subreddit-user-activity-scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit-user-activity-scraper.py)
The 
[subreddit-user-activity-scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit-user-activity-scraper.py) 
script uses Pushshift's API to generate a list of Reddit users who provide submissions and comments within a pre-defined set of Subreddits, ordered by frequency.

If you identify the most frequent users within a particular Subreddit, use this script.  

#### 
[reddit-user-activity-scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/reddit-user-activity-scraper.py)
The 
[reddit-user-activity-scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/reddit-user-activity-scraper.py) 
script uses Reddit's PRAW API to extract submission and comment activity for a pre-defined set of Reddit users.

If you want to find the submission and comment history for a particular Reddit user, use this script.

### Extract Subreddit Post Activity

#### [subreddit-scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit-scraper/subreddit-scraper.py) 
The [subreddit-scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit-scraper.py) script allows for use of both Reddit's PRAW API (via *praw_subreddit_activity( )*) and Pushshift's API (via *pushshift_subreddit_activity( )*) to extract submission and comment activity for a pre-defined list of Subreddits.

If you want to extract submissions and comments for a particular Subreddit, use this script.

#### 
[subreddit-search-scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit-search-scraper.py)
The 
[subreddit-search-scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit-search-scraper.py) 
script allows for use of both Reddit's PRAW API (via *praw_search_subreddit_activity( )*) and Pushshift's API (via *pushshift_search_subreddit_activity( )*) to extract submission and comment activity for a predefined list of Subreddits, based on a set of pre-defined search terms.

If you want to extract submissions and comments for a particular Subreddit, only when they include a particular search term, use this script.

#### 
[subreddit_lists.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_lists.py)
The 
[subreddit_lists.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_lists.py) 
script provides a list of subreddits for use in both the
[subreddit-scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit-scraper.py) 
function (as input argument *subreddit_list*) and 
[subreddit-search-scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit-search-scraper.py) 
function (as input arguments *subreddit_list* & *search_query_list*).
