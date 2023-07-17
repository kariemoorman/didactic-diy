/* --- PRAW Table --- */ 

CREATE TABLE IF NOT EXISTS reddit.praw_subbreddit_activity_text_clean (
	row_id serial NOT NULL PRIMARY KEY,
	created_unix_utc timestamp, 
	created_datetime_pst datetime,
	title varchar(300),
	author varchar(20),
	score integer,
	id varchar(20), 
	subreddit varchar(100), 
	url varchar(200), 
	body text,
	num_comments integer, 
	comments longtext,
	commenter_list json,
	commenter_count integer,
	comment_list json,
	cleaned_title varchar(300),
	cleaned_body text,
	cleaned_comments longtext
)

/* --- PushShift Tables --- */ 

CREATE TABLE IF NOT EXISTS reddit.pushshift_subreddit_submissions_text_clean ( 
	row_id serial NOT NULL PRIMARY KEY,
	created_utc timestamp,
	utc_datetime_str datetime,
	created_pst datetime,
	retrieved_utc timestamp,
	subreddit varchar(100), 
	submission_id varchar(20),
	permalink varchar(200),
	url varchar(200), 
	submission_author
	title varchar(300), 
	body text,
	removed_by_category varchar(20),
	is_created_from_ads_ui boolean
	cleaned_title varchar(300),
	cleaned_body text
)

CREATE TABLE IF NOT EXISTS reddit.pushshift_subreddit_comments_text_clean (
	row_id serial NOT NULL PRIMARY KEY,
	created_utc timestamp,
	utc_datetime_str datetime,
	created_pst datetime,
	retrieved_utc timestamp,
	subreddit varchar(100), 
	submission_id varchar(20),
	comment_id varchar(20),
	permalink varchar(200),
	comment_author varchar(20),
	is_submitter boolean,
	comments longtext,
	parent_id integer,
	nest_level integer,
	cleaned_comments longtext
)


/* --- GRANT permissions on Database & Tables to Users --- */ 

GRANT ALL ON reddit.* TO '<username>';


/* --- LOAD CSVs into Corresponding Tables --- */ 

/* --- MySQL --- */
LOAD DATA INFILE '<filepath>' INTO TABLE <table_name>;

/* --- PostgreSQL --- */
COPY <table_name> FROM '<filepath>' WITH (FORMAT csv);
