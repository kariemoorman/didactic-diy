#!/usr/bin/python

######################################################################
'''
Useful aggregations for use with 
{subreddit-scraper.py} & {subreddit-search-scraper.py} functions, 
for repective input variables {subreddit_list} & {search_query_list}.
'''
#######################################################################
#######################################################################
#######################################################################
###################### Subreddit Lists ################################
#######################################################################
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#######################################################################
################### General Subreddit Lists ###########################
#######################################################################
datascience_subreddit_list = ['MachineLearning', 'datascience']
tech_subreddit_list = [ 'technology', 'technews', 'privacy', 'cybersecurity', 'Futurology', 'Economics', 'SecurityAnalysis', 'InfoSecNews', 'CyberNews']
news_subreddit_list = ['news', 'worldnews', 'technews', 'business', 'economy', 'ecommerce']
music_subreddit_list = ['spotify', 'AppleMusic', 'Pandora', 'siriusxm', 'TIdaL', 'YoutubeMusic', 'AmazonMusic']
tv_subreddit_list = ['peacock', 'appletv', 'Hulu', 'youtubetv', 'ParamountPlus', 'PleX', 'netflix', 'PlutoTV', 'Roku', 'Freevee', 'AmazonPrimeVideo'] 
auto_subreddit_list = ['Rivian', 'Toyota', 'BMW', 'Tesla', 'Ford', 'Audi', 'Lexus', 'Chevy']
smarthome_subreddit_list = ['smarthome', 'homesecurity', 'homeassistant', 'homeautomation', 'TPLinkKasa', 'sonos', 'Aqara', 'RobotVacuums', 'Govee', 'blinkcameras', 'Ring','amazoneero', 'EufyCam', 'smartlife', 'wyzecam', 'TPLinkKasa', 'sonos', 'Aqara', 'RobotVacuums', 'Govee', 'roomba']
#######################################################################
############### Amazon-specific Subreddit Lists #######################
#######################################################################
amazon_subreddit_short_list = ['amazon', 'fuckamazon', 'amazonprime', 'alexa']
amazon_subreddit_long_list = ['amazon', 'fuckamazon', 'amazonprime', 'alexa', 'amazonecho','AmazonAstro', 'fireTV', 'AmazonPrimeVideo', 'AmazonMusic', 'audible', 'amazonprime','firetvstick','Freevee']
alexa_subreddit_list = ['alexa', 'amazonecho', 'AmazonAstro']
amazonprime_subreddit_list = ['amazonprime','fireTV', 'AmazonPrimeVideo', 'AmazonMusic', 'audible', 'amazonprime', 'firetvstick','Freevee']
primemusic_subreddit_list = ['AmazonMusic', 'audible'] # 'alexa', 'amazonprime'
primevideo_subreddit_list = ['AmazonPrimeVideo', 'fireTV', 'firetvstick', 'Freevee'] # 'alexa', 'amazonprime'
alexa_smarthome_subreddit_list = ['blinkcameras', 'Ring','amazoneero', 'roomba', 'sonos', 'Aqara', 'Govee', 'EufyCam', 'smartlife', 'wyzecam', 'TPLinkKasa'] # 'smarthome', 'homeautomation'
#######################################################################
#######################################################################
#######################################################################

#######################################################################
#######################################################################
#######################################################################
#################### Search Query Lists ###############################
#######################################################################
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#######################################################################
################# General Search Query Lists ##########################
#######################################################################
datascience_search_items = ['topic model', 'language model', 'image model', 'diffusion model', 'face recognition', 'facial recognition', 'voice recognition', 'image recognition']
llm_search_items = ['ChatGPT', 'HuggingFace', 'AllenNLP', 'OpenAI']
tech_topic_search_items = ['data privacy', 'user privacy', 'data security', 'user security', 'data breach', 'security breach']
tech_people_search_items = ['Tim Cook', 'Bezos', 'Bill Gates', 'Zuckerberg', 'Elon Musk']
tech_company_search_items = ['Apple', 'Palantir', 'OpenAI', 'Google', 'Accenture', 'Microsoft', 'Azure', 'Amazon', 'AWS', 'Facebook', 'Meta', 'Tiktok', 'Mastodon', 'Instagram', 'Metaverse', 'Tesla', 'Twitter', 'Spotify', 'Samsung', 'Oracle']
tech_browser_search_items = ['Bing', 'Chrome', 'Brave', 'Firefox', 'Microsoft Edge', 'Tor', 'DuckDuckGo']
smartphone_search_items = ['iphone', 'google pixel', 'android', 'smartphone', 'smart phone']
tv_provider_search_terms = ['hbo max', 'hbomax', 'hbo', 'showtime', 'starz', 'disney+', 'disney plus', 'paramount plus', 'paramount+', 'prime video']
music_provider_search_items = ['siriusxm', 'sxm', 'apple music', 'spotify', 'prime music', 'amazon music', 'youtube music', 'pandora', 'iheart radio']
music_search_items = ['podcast', 'playlist', 'playback', 'volume', 'songlist', 'music']
device_search_items = ['light', 'plug', 'tv', 'thermometer', 'garage door', 'router', 'speaker', 'phone', 'soundbar', 'camera', 'doorbell', 'doorcam', 'security system', 'computer', 'laptop', 'macbook', 'bluetooth', 'wifi', 'wi-fi', 'wi fi']
device_brand_items = ['jbl', 'sonos', 'xbox', 'lg', 'roku', 'toshiba', 'samsung', 'nest', 'tplink', 'kasa', 'eufy', 'roomba', 'eero', 'sony', 'tcl', 'vizio', 'hisense']
voice_ai_search_items = ['Alexa', 'Google Assistant', 'Siri', 'voice-assistant', 'voice assistant']
#######################################################################
############## Amazon-specific Search Query Lists #####################
#######################################################################
amazon_search_items = ['amazon prime', 'Amazon Alexa', 'Amazon', 'Alexa', 'Alexa ads', 'music unlimited', 'prime music', 'firestick', 'fire stick', 'amazon music', 'echo show', 'prime video', 'Amazon Ring', 'prime app', 'alexa app', 'echo auto', 'amazon fresh', 'Whole Foods', 'amazon basics', 'amazon sidewalk']
alexa_device_search_items = ['echo show', 'echo flex', 'echo dot', 'echo auto', 'firetv', 'fire tv', 'firestick', 'firetvstick', 'fire tv stick', 'fire tv cube', 'fire cube', 'firecube']
alexa_search_items =  ['notification', 'reminder', 'subscription', 'premium', 'sound', 'noise', 'alarm', 'ad', 'ads', 'advertising', 'connection', 'wifi', 'issue', 'volume', 'device', 'kids+', 'kid', 'child', 'explicit', 'sleep jar', 'trivia', 'radio', 'station', 'call', 'drop in', 'drop-in', 'routine', 'weather', 'news', 'location', 'light', 'flash briefing', 'whisper', 'podcast', 'playlist', 'color', 'voice history', 'shopping', 'wake word', 'wakeword', 'by the way', 'audio', 'camera', 'tune-in', 'skill']
alexa_function_terms = ['subscribe', 'turn off', 'turn on', 'stop', 'play', 'pause', 'resume', 'help', 'whisper', 'link', 'connect', 'call', 'drop in', 'drop-in', 'hear', 'listen', 'spy', 'understand', 'playback', 'repeat', 'switch', 'sync', 'shop']
#######################################################################
#######################################################################
#######################################################################