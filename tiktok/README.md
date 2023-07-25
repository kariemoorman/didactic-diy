<h2 align='center'>didactic-diy: TikTok</h2>
<h4 align='center'>Data randomness, for practice and utility, using 
TikTok.</h4>

---

### Repository Contents
- <b>Web Scraping</b>
  - [tiktok_user_video_scraper.py](https://github.com/kariemoorman/didactic-diy/blob/main/tiktok/__scripts/tiktok_scraper/tiktok_user_video_scraper.py)  
    Choose either Selenium or Pyppeteer to dynamically scrape TikTok videos for one or more Tiktok usernames.  
      E.g., ```python3 tiktok_user_video_scraper.py blitzphd eczachly -b pyppeteer -o csv```

    
- <b>Sample Datasets</b>: [__data](https://github.com/kariemoorman/didactic-diy/tree/main/tiktok/__data)

- <b>TikTok Video Downloader</b>
  - [tiktok_downloader.py](https://github.com/kariemoorman/didactic-diy/blob/main/tiktok/__scripts/tiktok_downloader.py)  
    Choose either Selenium or Pyppeteer to dynamically download one or more Tiktok videos.  
      E.g., ```python3 tiktok_downloader.py <url> -b selenium -d firefox```
    
---

<p align='center'><b>License: <a href='https://choosealicense.com/licenses/gpl-3.0/'>GNU General 
Public License v3.0</a></b></p>
