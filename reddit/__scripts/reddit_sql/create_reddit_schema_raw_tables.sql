/* --- Create DB Schema --- */ 

CREATE SCHEMA IF NOT EXISTS reddit; 

/* --- PRAW Tables --- */ 

CREATE TABLE IF NOT EXISTS reddit.praw_subreddit_activity_raw (
	row_id serial NOT NULL PRIMARY KEY,
	created_unix_utc timestamp, 
	created_datetime_pst datetime, 
	post_type varchar(20),
	title varchar(300),
	author varchar(20),
	score integer,
	id varchar(20), 
	subreddit varchar(100), 
	url varchar(200), 
	body text,
	num_comments integer, 
	comments longtext
);

CREATE TABLE IF NOT EXISTS reddit.praw_search_subreddit_activity_raw (
	row_id serial NOT NULL PRIMARY KEY,
	created_unix_utc timestamp, 
	created_datetime_pst datetime, 
	post_type varchar(20),
	search_item varchar(100),
	subreddit varchar(100), 
	id varchar(20), 
	title varchar(300),
	author varchar(20),
	score integer,
	url varchar(200), 
	body text,
	num_comments integer, 
	comments longtext
);

CREATE TABLE IF NOT EXISTS reddit.praw_subreddit_user_submission_frequency (
	row_id serial NOT NULL PRIMARY KEY,
	query_date date,
	subreddit varchar(100),
	comment_author varchar(20),
	comment_frequency integer
);

CREATE TABLE IF NOT EXISTS reddit.praw_subreddit_user_comment_frequency (
	row_id serial NOT NULL PRIMARY KEY,
	query_date date,
	subreddit varchar(100),
	submission_author varchar(20),
	submission_frequency integer
);

CREATE TABLE IF NOT EXISTS reddit.praw_reddit_user_submissions ( 
	row_id serial NOT NULL PRIMARY KEY,
	created_unix_utc timestamp, 
	created_pst datetime, 
	post_type varchar(20),
	username varchar(20),
	subreddit varchar(100),
	id varchar(20), 
	title varchar(300),
	body text,
	num_comments integer, 
	submission_comments longtext,
	reddit_permalink varchar(200)
);

CREATE TABLE IF NOT EXISTS reddit.praw_reddit_user_comments ( 
	row_id serial NOT NULL PRIMARY KEY,
	created_unix_utc timestamp, 
	created_pst datetime, 
	post_type varchar(20),
	commenter_name varchar(20),
	subreddit varchar(100),
	comment longtext,
	reddit_permalink varchar(200)
);


/* --- PushShift Tables --- */ 

CREATE TABLE IF NOT EXISTS reddit.pushshift_subreddit_submissions_raw ( 
	row_id serial NOT NULL PRIMARY KEY,
	subreddit varchar(100),
	selftext text,
	author_fullname varchar(30),
	gilded integer,
	title varchar(300),
	link_flair_richtext varchar(20), 
	subreddit_name_prefixed varchar(100), 
	hidden boolean NOT NULL, 
	pwls integer,
	link_flair_css_class varchar(20),
	thumbnail_height integer,
	top_awarded_type varchar(20),
	hide_score boolean NOT NULL,
	quarantine boolean NOT NULL,
	link_flair_text_color varchar(10),
	upvote_ratio decimal(3 ,2) NOT NULL,
	author_flair_background_color varchar(20),
	subreddit_type varchar(10) NOT NULL,
	total_awards_received integer,
	media_embed json,
	thumbnail_width integer, 
	author_flair_template_id varchar(20), 
	is_original_content boolean NOT NULL,
	secure_media json,
	is_reddit_media_domain boolean NOT NULL,
	is_meta boolean NOT NULL,
	category varchar(20),
	secure_media_embed json,
	link_flair_text varchar(20),
	score integer,
	is_created_from_ads_ui boolean NOT NULL,
	author_premium boolean NOT NULL,
	thumbnail varchar(20) NOT NULL,
	edited boolean,
	author_flair_css_class varchar(20),
	author_flair_richtext varchar(10),
	gildings varchar(20),
	post_hint varchar(30),
	content_categories varchar(20),
	is_self boolean NOT NULL,
	link_flair_type varchar(20),
	wls integer,
	removed_by_category varchar(20),
	author_flair_type varchar(20), 
	domain varchar(30),
	allow_live_comments boolean,
	suggested_sort varchar(20),
	url_overridden_by_dest varchar(200),
	view_count integer,
	archived boolean,
	no_follow boolean,
	is_crosspostable boolean,
	pinned boolean,
	over_18 boolean,
	preview json,
	all_awardings text,
	awarders text,
	media_only boolean,
	can_gild boolean,
	spoiler boolean,
	locked boolean NOT NULL,
	author_flair_text varchar(10),
	treatment_tags varchar(100),
	removed_by varchar(20),
	distinguished varchar(20),
	subreddit_id varchar(20) NOT NULL,
	link_flair_background_color varchar(10),
	id varchar(20),
	is_robot_indexable boolean NOT NULL,
	author varchar(20),
	discussion_type varchar(10),
	num_comments integer,
	send_replies boolean NOT NULL,
	whitelist_status varchar(20),
	contest_mode boolean NOT NULL,
	author_patreon_flair boolean NOT NULL,
	author_flair_text_color varchar(10),
	permalink varchar(200),
	parent_whitelist_status varchar(20), 
	stickied boolean NOT NULL,
	url varchar(200),
	subreddit_subscribers integer,
	created_utc timestamp,
	num_crossposts integer,
	media json,
	is_video boolean,
	retrieved_utc timestamp,
	updated_utc timestamp,
	utc_datetime_str datetime,
	crosspost_parent_list json,
	crosspost_parent json,
	poll_data json,
	author_cakeday boolean,
	media_metadata json,
	is_gallery boolean,
	gallery_data json,
	edited_on timestamp,
	created_pst datetime
);

CREATE TABLE IF NOT EXISTS reddit.pushshift_subreddit_comments_raw ( 
	row_id serial NOT NULL PRIMARY KEY,
	subreddit_id varchar(20) NOT NULL,
	author_is_blocked boolean,
	comment_type varchar(20),
	edited boolean,
	author_flair_type varchar(20),
	total_awards_received integer,
	subreddit varchar(100),
	author_flair_template_id varchar(20), 
	id varchar(20),
	gilded integer,
	archived boolean,
	collapsed_reason_code varchar(20),
	no_follow boolean,
	author varchar(20),
	send_replies boolean,
	parent_id integer,
	score integer,
	author_fullname varchar(30),
	all_awardings varchar(10),
	body longtext,
	top_awarded_type varchar(20),
	author_flair_css_class varchar(20),
	author_patreon_flair boolean,
	collapsed boolean,
	author_flair_richtext varchar(10),
	is_submitter boolean NOT NULL,
	gildings varchar(10),
	collapsed_reason varchar(10),
	associated_award varchar(10),
	stickied boolean NOT NULL,
	author_premium boolean,
	can_gild boolean NOT NULL,
	link_id varchar(20),
	unrepliable_reason varchar(10),
	author_flair_text_color varchar(10),
	score_hidden boolean NOT NULL,
	permalink varchar(200) NOT NULL,
	subreddit_type varchar(10) NOT NULL,
	locked boolean NOT NULL,
	author_flair_text varchar(10),
	treatment_tags varchar(10),
	created_utc	timestamp, 
	subreddit_name_prefixed varchar(100), 
	controversiality integer,
	author_flair_background_color varchar(10),
	collapsed_because_crowd_control varchar(10),
	distinguished varchar(10),
	retrieved_utc timestamp,
	updated_utc	timestamp, 
	body_sha1 varchar(40) NOT NULL,
	nest_level integer,
	utc_datetime_str datetime,
	author_cakeday boolean,
	created_pst datetime
);

-- CREATE TABLE IF NOT EXISTS reddit.pushshift_search_subreddit_activity_raw ( 
-- 	row_id serial NOT NULL PRIMARY KEY,
-- );

CREATE TABLE IF NOT EXISTS reddit.pushshift_subreddit_user_submission_frequency ( 
	row_id serial NOT NULL PRIMARY KEY,
	query_date date,
	before_date varchar(60),
	subreddit varchar(100),
	submission_author varchar(20),
	submission_frequency integer
);

CREATE TABLE IF NOT EXISTS reddit.pushshift_subreddit_user_comment_frequency ( 
	row_id serial NOT NULL PRIMARY KEY,
	query_date date,
	before_date varchar(60),
	subreddit varchar(100),
	comment_author varchar(20),
	comment_frequency integer
);


/* --- LOAD CSVs into Corresponding Tables --- */ 

/* --- MySQL --- */
LOAD DATA INFILE '<filepath>' 
INTO TABLE <table_name>
FIELDS TERMINATED BY '\t'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

/* --- PostgreSQL --- */
COPY <table_name> 
FROM '<filepath>' 
WITH (FORMAT csv)
DELIMITER '\t'
CSV HEADER;
