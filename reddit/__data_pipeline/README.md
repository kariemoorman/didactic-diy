## Reddit Data Pipeline

<b>Author: [@kariemoorman](https://github.com/kariemoorman)</b>

--- 
### Overview Statement

Parameters considered when constructing a data pipeline include the following: 
- <b>GDPR Compliance</b>: <i>Is any of the data I wish to extract classified as PII/PHI? </i>
- <b>Cost</b>: <i>How much am I willing to spend to maintain each step of the data pipeline? </i>
- <b>SLA</b>: <i>How fast do I need the data to be transformed and loaded for visualization? </i>
- <b>Data Storage Location</b>: <i>Where do I want my data to be stored: local/on-premises, cloud, or hybrid? </i>
- <b>Data Throughput</b>: <i>How much data needs to be transmitted in each READ/WRITE request (i.e., do I need distributed/batch compute capabilities)? </i>
- <b>Data Visualization</b>: <i>What types of analysis are meaningful for this dataset, what tools are best for visualizing those analyses, who do I want to have view access? </i>
- <b>ETL vs. ELT</b>: <i>Which option is best for my use case? </i>
- <b>Automation</b>: <i>How can I automate all tasks within the workflow? </i>

---
### Project Summary

For this project, the goal is to select and extract data for a subset of subreddits and/or Reddit users, day-over-day, 
transform and execute a series of NLP and ML tasks on the extracted data, and load that transformed data into a dashboard for visualization, for little to no monetary cost. This means I am prioritizing monetary cost over time cost, and I assume the risk of encountering time delays in order to maintain low cost strategy. The workflow should permit both on-demand and automated/scheduled executions.

I want to construct an automated data pipeline that adheres to the following constraints:
- Extracted data is not classified as PHI/PII. While usernames are extracted, no additional uniquely identifying information is included (e.g., profile metadata such as About description, social media links).
- Low to No Cost.
- SLA on data extraction and transformation tasks is end-of-day (EOD).
- Data, both extracted and tranformed, is stored locally and is available to end users. 
- Data extraction, transformation, and load steps READ/WRITE is small (between 2-10 MB of data per request).
- Data visualization incorporates analyses of NER, topic modeling, sentiment, and user behaviors, and can be surfaced using a python-friendly dashboard application for view by anyone.
- ELT, as it allows for fast turnaround of transformation step and for external validation of processes within data transformation step.



---
### Data Pipeline Design
<img src="https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__data_pipeline/images/data_pipelines-reddit_local_pipeline.drawio.png" height="500"/>


---
### Extract & Load 

<img src="https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__data_pipeline/images/reddit_local_datapipline-extract.png" height="180" />

After [registering a Reddit developer application](https://www.reddit.com/prefs/apps/) and [receiving an access token](https://praw.readthedocs.io/en/stable/getting_started/authentication.html), use [PRAW API](https://praw.readthedocs.io/en/stable/index.html) to extract data for a particular subreddit or Reddit user.
Write that data, in whatever format (e.g., JSON, Parquet, CSV), to local storage. Load that data to a local repository (e.g., SQL database; local subdirectory). Make that data accessible to end users. 


---
### Transform & Load 

<img src="https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__data_pipeline/images/reddit_local_datapipline-transform.png" height="200" />
</p>
Using raw datasets, execute a series of NLP and ML tasks. Write output as new dataset, in whatever format (e.g., JSON, Parquet, CSV), to local storage. Append the new dataset to the existing datasets in local repository (e.g., SQL database; local subdirectory). Make that data accessible to end users. 

---
### Visualization 
  
<img src="https://github.com/kariemoorman/didactic-diy/blob/main/reddit/__data_pipeline/images/reddit_local_datapipline-visualize.png" height="180" src="image"/>

Using the compiled dataset from the transformation step, surface the analyses in the form of interactive dashboards via Dash. 


---
### Automation 

Workflow automation is accomplished using [crontab](https://www.geekbitzone.com/posts/macos/crontab/macos-schedule-tasks-with-crontab/) on MacOS.

--- 
<b>License: [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)</b>
