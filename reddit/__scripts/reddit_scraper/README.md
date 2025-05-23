<h3 align='center'>Reddit-Scraper Example Use-Cases </h3>

---
### Identify & Extract Reddit User Activity
---
- #### [subreddit_user_activity_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_user_activity_scraper.py)  

The [subreddit_user_activity_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_user_activity_scraper.py) script generates a list of Reddit users who provide submissions and comments within a user-defined set of Subreddits, ordered by frequency, and writes results to a user-defined directory (e.g., --category) using one of the following APIs: "praw", "pushshift", "pushpull" (default = "praw").

```
python3 subreddit_user_activity_scraper.py datascience MachineLearning -c DataScience 

python3 subreddit_user_activity_scraper.py alexa amazonecho -c Amazon 
```

If you wish to identify the most frequent users within a particular Subreddit, use this script.  

- #### [reddit_user_activity_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/reddit_user_activity_scraper.py)
The [reddit_user_activity_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/reddit_user_activity_scraper.py) script uses Reddit's PRAW API to extract submission and comment activity for a user-defined set of Reddit usernames.

```
python3 reddit_user_activity_scraper.py <username> <username> 
```

If you wish to find the submission and comment history for a particular Reddit user, use this script.

 
---
### Extract Subreddit Post Activity
--- 
- #### [subreddit_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_scraper.py) 
The [subreddit_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_scraper.py) script extracts submission and comment activity for a user-defined list of Subreddits, and writes results to a user-defined directory (e.g., --category) using one of the following APIs: "praw", "pushshift", "pushpull" (default = "praw").

```
python3 subreddit_scraper.py datascience MachineLearning -c DataScience

python3 subreddit_scraper.py alexa amazonecho -c Amazon
```

If you wish to extract submissions and comments for a particular Subreddit, use this script.

- #### [subreddit_search_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_scraper.py)
The [subreddit_search_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_scraper.py) script extracts submission and comment activity for a user-defined list of Subreddits, filtered on a set of user-defined search query terms, and writes results to a user-defined directory (e.g., --category) using one of the following APIs: "praw", "pushshift", "pushpull" (default = "praw").

```
python3 subreddit_search_scraper.py datascience MachineLearning -q GPT LLM -c DataScience

python3 subreddit_search_scraper.py alexa amazonecho -q notification alarm playback drop-in -c Amazon
```

If you wish to extract submissions and comments for a particular Subreddit, only when they include a particular search term, use this script.

- #### [subreddit_lists.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_lists.py)
The [subreddit_lists.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit_lists.py) script provides a list of subreddits for use in both the [subreddit-scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit-scraper.py) function (as input argument *subreddit_list*) and [subreddit-search-scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__scripts/reddit_scraper/subreddit-search-scraper.py) function (as input arguments *subreddit_list* & *search_query_list*).

---

#### Important Note: 
To use Reddit-Scraper scripts in their current form, please 

(1) Create a credentials.py file that contains your Reddit development application and user credentials, e.g., 
```
filepath: didactic-diy/reddit/__scripts/reddit_scraper/credentials.py
```
```
#!/usr/bin/python3

## Credentials ##
my_client_id = '<your_client_id>'
my_client_secret = '<your_client_secret>'
my_user_agent = '<your_user_agent>'
my_password = "<your_password>"
my_username = "<your_username>"

```

(2) Add credentials.py to .gitignore 
```
filepath: didactic-diy/.gitignore
```
```
# Credentials files
credentials.py
```
