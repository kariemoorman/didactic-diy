#!/usr/bin/python

import os, sys, time
from datetime import datetime, date
import re
import glob
import json
import pandas as pd 
import numpy as np

sys.path.append("/Users/karie/Github/didactic-diy/reddit/__scripts")

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

from reddit_nlp.clean_reddit_text import * 

## clean_reddit_text Function list: 
# open_json, 
# remove_usernames,
# remove_hyperlinks, 
# expand_contractions, 
# ner_reddit,
# remove_punctuation, 
# remove_stopwords, 
# remove_numbers,
# singularize_plural_noun,
# tokenize text,
# lemmatize_text,
# format_dataset




def remove_amazon_numbers(text): 
    '''
    Required python pkgs: 
    - re (import re)
    
    Function: Remove numbers from text data.
    
    Input Arguments: 
    text: input type is list of (str) items.
    
    '''
    text = [re.sub(r"((1st|1|first)( (G|g)eneration| (G|g)en))|(( G|g)eneration|( G|g)en) (1st|1|(O|o)ne)", "firstgen", sentence) for sentence in text] 
    text = [re.sub(r"((2nd|2|second)( (G|g)eneration| (G|g)en))|(( G|g)eneration|( G|g)en) (2nd|2|(T|t)wo)", "secondgen", sentence) for sentence in text] 
    text = [re.sub(r"((3rd|3|third)( (G|g)eneration| (G|g)en))|(( G|g)eneration|( G|g)en) (3rd|3|(T|t)hree)", "thirdgen", sentence) for sentence in text] 
    text = [re.sub(r"((4th|4|fourth)( (G|g)eneration| (G|g)en))|(( G|g)eneration|( G|g)en) (4th|4|(F|f)our)", "fourthgen", sentence) for sentence in text] 
    text = [re.sub(r"((5th|5|fifth)( (G|g)eneration| (G|g)en))|(( G|g)eneration|( G|g)en) (5th|5|(F|f)ive)", "fifthgen", sentence) for sentence in text] 
    text = [re.sub(r"((6th|6|sixth)( (G|g)eneration| (G|g)en))|(( G|g)eneration|( G|g)en) (6th|6|(S|s)ix)", "sixthgen", sentence) for sentence in text] 
    text = [re.sub(r"((7th|7)( (G|g)eneration| (G|g)en))", "seventhgen", sentence) for sentence in text] 
    text = [re.sub(r"((8th|8)( (G|g)eneration| (G|g)en))", "eightgen", sentence) for sentence in text] 
    text = [re.sub(r"((9th|9)( (G|g)eneration| (G|g)en))", "ninthgen", sentence) for sentence in text] 
    text = [re.sub(r"((10th|10)( (G|g)eneration| (G|g)en))", "tenthgen", sentence) for sentence in text] 
    text = [re.sub(r"\b1st(-(P|p)arty| (P|p)arty)\b", "firstparty", sentence) for sentence in text]
    text = [re.sub(r"\b3rd(-(P|p)arty| (P|p)arty)\b", "thirdparty", sentence) for sentence in text]
    text = [re.sub(r"(1x)('?s)?", "one_time", sentence) for sentence in text] 
    text = [re.sub(r"(2x)('?s)?", "two_times", sentence) for sentence in text] 
    text = [re.sub(r"(3x)('?s)?", "three_times", sentence) for sentence in text] 
    text = [re.sub(r"(4x)('?s)?", "four_times", sentence) for sentence in text] 
    text = [re.sub(r"(5x)('?s)?", "five_times", sentence) for sentence in text] 
    text = [re.sub(r"\b1st\b", "first", sentence) for sentence in text] 
    text = [re.sub(r"\b2nd\b", "second", sentence) for sentence in text] 
    text = [re.sub(r"\b3rd\b", "third", sentence) for sentence in text]
    text = [re.sub(r'\b([0-9](th|st|rd|nd))\b', '', sentence) for sentence in text]
    text = [re.sub(r'\b([0-9]\-)([0-9]x)\b', '', sentence) for sentence in text]
    text = [re.sub(r'\b([0-9]\.)([0-9]x[0-9]+\"?)?', '', sentence) for sentence in text]
    text = [re.sub(r'\s([0-9]+.?[0-9]+)([a-z]+)\b', '', sentence) for sentence in text]
    text = [re.sub(r'\b([A-Za-z]+?[0-9]+[A-Za-z]+[0-9]+[A-Za-z]+)\b', '', sentence) for sentence in text]
    text = [re.sub(r'\b([A-Za-z]+)?([0-9]+)([A-Za-z]+)?\b', '', sentence) for sentence in text] #n32w
    #text = [re.sub(r'\b([A-Za-z]+[0-9]+)([A-Za-z]+)? \b', '', sentence) for sentence in text] #new
    text = [re.sub(r'([A-Za-z]+[0-9]+)\b', '', sentence) for sentence in text]
    text = [re.sub(r'([A-Z]+[0-9])\w+', '', sentence) for sentence in text]
    text = [re.sub(r'([$]?[0-9]+[%a-z]+?\.? )\b', '', sentence) for sentence in text]
    text = [re.sub(r'\s([0-9]+[\.,:\-\_]?)([0-9]+)?([a-z]+)?', '', sentence) for sentence in text]
    text = [re.sub(r'(?<=[A-Za-z]|\_|\-)([0-9]+[\.,:\-\_]?)([0-9]+)?([a-z]+)?( )?\b', '', sentence) for sentence in text]
    #text = [re.sub(r'\s[a-z]\b', '', sentence) for sentence in text]
    return text


def amazon_ner_reddit(text): 
    '''        
    Required python pkgs: 
    - re (import re)
    
    Function: Regularize select items from text data (Amazon-specific).

    Input Arguments: 
    text: input type is list of (str) items.
       
    '''
    ## General (Abbreviations, Disfluencies)
    text = [re.sub(r"\b(R|r) and (D|d)\b", "research and development", sentence) for sentence in text]
    text = [re.sub(r"e v e r y t i m e", "everytime", sentence) for sentence in text]
    text = [re.sub(r"\b(USA|usa|U\.S\.|US)\b", " united_states ", sentence) for sentence in text]
    text = [re.sub(r"\b(U\.K\.|UK)\b", " uk ", sentence) for sentence in text]
    text = [re.sub(r" (r\/|\/r\/)", " subreddit ", sentence) for sentence in text]
    text = [re.sub(r"\b(O|o)(K|k)\b", "okay", sentence) for sentence in text]
    text = [re.sub(r"\bhelp u\b", "help you", sentence) for sentence in text]
    text = [re.sub(r"\byr\b", "year", sentence) for sentence in text]
    text = [re.sub(r"\be-mail\b", "email", sentence) for sentence in text]
    text = [re.sub(r"\b(pre-made)\b", "premade", sentence) for sentence in text]
    text = [re.sub(r"\b(re-used)\b", "reused", sentence) for sentence in text]
    text = [re.sub(r"\bsoooo\b", "so", sentence) for sentence in text]
    text = [re.sub(r"\bslooowwww\b", "slow", sentence) for sentence in text]
    text = [re.sub(r"\b(thx|thnx|tysm|ty|thank you|thank u|thank)\b", "thanks", sentence) for sentence in text]
    text = [re.sub(r"\bgooood\b", "good", sentence) for sentence in text]
    text = [re.sub(r"\bbyyyyye\b", "bye", sentence) for sentence in text]
    text = [re.sub(r"\b(A|a)$(A|a)(P|p) (R|r)ocky\b", "asap rocky", sentence) for sentence in text]
    text = [re.sub(r"\bshut the f up\b", "shut the fuck up", sentence) for sentence in text]
    text = [re.sub(r"\bspammed\b", "spam", sentence) for sentence in text]
    text = [re.sub(r"\b(B|b)ricked\b", "brick", sentence) for sentence in text]
    ## Sounds 
    text = [re.sub(r"\bwhite noise\b", "whitenoise", sentence) for sentence in text]
    text = [re.sub(r"\bbrown noise\b", "brownnoise", sentence) for sentence in text]
    text = [re.sub(r"\bpink noise\b", "pinknoise", sentence) for sentence in text]
    text = [re.sub(r"\bsleep sounds?\b", "sleepsounds", sentence) for sentence in text]
    text = [re.sub(r"\bthunderstorm sounds?\b", "thunderstormsounds", sentence) for sentence in text]
    text = [re.sub(r"\brain sounds?\b", "rainsounds", sentence) for sentence in text]
    text = [re.sub(r"\b(ambient (noise|sounds?))\b", "ambientsounds", sentence) for sentence in text]
    text = [re.sub(r"\b(S|s)leep (J|j)ar(s|(\'|\’)s)?\b", "sleepjar", sentence) for sentence in text]
    ## Settings/Prompts
    text = [re.sub(r"\b(pre-recorded)\b", "prerecorded", sentence) for sentence in text]
    text = [re.sub(r"\b(home-screen|home screen)s?\b", "homescreen", sentence) for sentence in text]
    text = [re.sub(r"\b(home-screen|home screen)s?\b", "homescreen", sentence) for sentence in text]
    text = [re.sub(r"\btemp\b", "temperature", sentence) for sentence in text]
    text = [re.sub(r"\bre\-added\b", "readded", sentence) for sentence in text]
    text = [re.sub(r"\b(re\-pair)", "repair", sentence) for sentence in text]
    text = [re.sub(r"\b(re(\-| )purposing)\b", "repurpose", sentence) for sentence in text]
    text = [re.sub(r"\b(re\-enabl)", "reenabl", sentence) for sentence in text]
    text = [re.sub(r"\b(re\-creat)", "recreat", sentence) for sentence in text]
    text = [re.sub(r"\b(re\-register)", "reregister", sentence) for sentence in text]
    text = [re.sub(r"\b(re\-sync)", "resync", sentence) for sentence in text]
    text = [re.sub(r"\b(re\-link)", "relink", sentence) for sentence in text]
    text = [re.sub(r"\b(re\-setting)", "resetting", sentence) for sentence in text]
    text = [re.sub(r"\b(re\-install)", "reinstall", sentence) for sentence in text]
    text = [re.sub(r"\b(re\-ask)", "reask", sentence) for sentence in text]
    text = [re.sub(r"\bvol\b", "volume", sentence) for sentence in text]
    text = [re.sub(r"\binstalling\b", "install", sentence) for sentence in text]
    ## Locations 
    text = [re.sub(r"\bdining room\b", "diningroom", sentence) for sentence in text]
    text = [re.sub(r"\b(multi-room|multi room)\b", "multiroom", sentence) for sentence in text]
    text = [re.sub(r"\bliving room\b", "livingroom", sentence) for sentence in text]
    text = [re.sub(r"\bbed room\b", "bedroom", sentence) for sentence in text]
    ## Radio Stations  
    text = [re.sub(r"\b(SXM|sxm)\b", "siriusxm", sentence) for sentence in text]
    text = [re.sub(r"\b(R|r)adio 1\b", "radioone", sentence) for sentence in text]
    text = [re.sub(r"\b(R|r)adio 2\b", "radiotwo", sentence) for sentence in text]
    text = [re.sub(r"\b(R|r)adio 3\b", "radiothree", sentence) for sentence in text]
    text = [re.sub(r"\b(R|r)adio 4\b", "radiofour", sentence) for sentence in text]
    text = [re.sub(r"\b(H|h)eart (FM|fm)\b", "heartfm", sentence) for sentence in text]
    text = [re.sub(r"\bi(H|h)eart( (R|r)adio)?\b", "iheartradio ", sentence) for sentence in text]
    text = [re.sub(r"\b(i |i\-|i)?(H|h)eart( FM| fm|FM|fm)\b", "iheartradio", sentence) for sentence in text]
    text = [re.sub(r"\b(BBC|Bbc|bbc) ((N|n)ews)\b", "bbcnews", sentence) for sentence in text]
    text = [re.sub(r"\b(C|c)(\-| )(S|s)pan\b", "cspan", sentence) for sentence in text]
    ## Apps
    text = [re.sub(r"\b(P|p)aramount(\+| \+)\b", "paramountplus", sentence) for sentence in text]
    text = [re.sub(r"\b(H|h)(B|b)(O|o) (M|m)ax\b", "hbomax", sentence) for sentence in text]
    text = [re.sub(r"\b(D|d)isney(\+| \+| (P|p)lus)\b", "disneyplus", sentence) for sentence in text]
    text = [re.sub(r"\b(F|f)lash (B|b)riefing(s)?\b", "flashbrief", sentence) for sentence in text]
    text = [re.sub(r"\b(F|f)lash (N|n)ews (B|b)riefing(s)?\b", "flashbrief", sentence) for sentence in text]
    ## Smart Devices 
    #### General
    text = [re.sub(r"\b((W|w)i-(F|f)i|(W|w)i (F|f)i)\b", "wifi", sentence) for sentence in text]
    text = [re.sub(r"\bsound bar\b", "soundbar", sentence) for sentence in text]
    text = [re.sub(r"\bvac\b", "vacuum", sentence) for sentence in text]
    text = [re.sub(r"\bdimmer switch\b", "dimmerswitch", sentence) for sentence in text]
    text = [re.sub(r"\b((S|s)mart )(((L|l)ights?)|((B|b)ulbs?))\b", "smartlight", sentence) for sentence in text] 
    text = [re.sub(r"\b((S|s)mart )(P|p)lugs?\b", "smartplug", sentence) for sentence in text] 
    text = [re.sub(r"\b((M|m)otion )(S|s)ensors?\b", "motionsensor", sentence) for sentence in text] 
    text = [re.sub(r"\b((S|s)mart )(T\|t)(V|v)\b", "smarttv", sentence) for sentence in text] 
    text = [re.sub(r"\b(S|s)mart (H|h)ome\b", "smarthome", sentence) for sentence in text] 
    text = [re.sub(r"\bhome assistant\b", "homeassistant", sentence) for sentence in text]
    text = [re.sub(r"\b((M|m)icro)( )?(SDs?)( cards?)?\b", "microsdcard", sentence) for sentence in text]
    text = [re.sub(r"\b(S|s)(D|d) cards?\b", "sdcard", sentence) for sentence in text]
    text = [re.sub(r"\b(I|i)(R|r) (?=(lightbulb|filter|light|option|microwave|dim|reflection|camera|LED|led|(night vision))(s?)\b)", "infrared", sentence) for sentence in text]
    text = [re.sub(r"\b(I|i)(R|r)\b", "infrared", sentence) for sentence in text]
    text = [re.sub(r"\b(C|c) (wire)\b", "cwire", sentence) for sentence in text]
    #### Amazon-owned 
    text = [re.sub(r"\b((T|t)(P|p) (L|l)ink (K|k)asa)\b", "tplinkkassa", sentence) for sentence in text]
    text = [re.sub(r"\b(K|k)asa\b", "tplinkkassa", sentence) for sentence in text]
    text = [re.sub(r"\b(((F|f)ire( TV| tv|TV|tv) (C|c)ubes?)|((F|f)ire (C|c)ubes?)|((F|f)ire(C|c)ubes?))\b", "firecube", sentence) for sentence in text]
    text = [re.sub(r"\b((F|f)ire )(TV|tv)( OS| os)?\b", "firetv", sentence) for sentence in text] 
    text = [re.sub(r"\b(((F|f)ire )(TV|tv) (S|s)tick|((F|f)ire )(S|s)tick)\b", "firetvstick", sentence) for sentence in text] 
    text = [re.sub(r"\b(E|e)ero mesh\b", "eero", sentence) for sentence in text] 
    text = [re.sub(r"\b(B|b)link( doorbell)? cam(era)?s?\b", "blinksecurity", sentence) for sentence in text] 
    text = [re.sub(r"\b(E|e)ufy(( (S|s)olo)?cam(era)?s?( E20)?)?\b", "eufysecurity", sentence) for sentence in text] 
    #### Specific Brands
    text = [re.sub(r"\b((P|p)hill?ips )?(H|h)ue\b", "philipshue", sentence) for sentence in text]
    text = [re.sub(r"\bphilipshue (((L|l)ight(bulb| bulb)?s?)|smartlight)\b", "huesmartlight", sentence) for sentence in text]
    text = [re.sub(r"\b(J|j)(B|b)(L|l) speakers?\b", "jblspeaker", sentence) for sentence in text]
    text = [re.sub(r"\b(L|l)(G|g) ((S|s)mart)?(T|t)(V|v)\b", "lgsmarttv ", sentence) for sentence in text] 
    text = [re.sub(r"\b(R|r)oku (TV|tv|smarttv)\b", "rokutv ", sentence) for sentence in text] 
    text = [re.sub(r"\b(S|s)amsung (TV|tv|smarttv)\b", "samsungtv ", sentence) for sentence in text] 
    text = [re.sub(r"\b(I|i)nsignia (TV|tv|smarttv)\b", "insigniatv ", sentence) for sentence in text] 
    text = [re.sub(r"\b(((L|l)ight(B|b| B| b)ulbs?)|(B|b)ulbs?)\b", "lightbulb", sentence) for sentence in text]
    text = [re.sub(r"\b(D|d)link (S|s)ensors?\b", "dlinksensor", sentence) for sentence in text]
    text = [re.sub(r"\b(W|w)emo (P|p)lugs?\b", "wemoplug", sentence) for sentence in text]
    text = [re.sub(r"\b(NETGEAR|(N|N)etgear) (N|n)ighthawk\b", "netgearnighthawk", sentence) for sentence in text]
    text = [re.sub(r"\b((L|l)(G|g) (T|t)hin(Q|q|k)|(T|t)hin(Q|q|k) (skill|app))\b", "lgthinqskill", sentence) for sentence in text]
    text = [re.sub(r"\b(X|x)(B|b)ox (S|s)eries (S|s|x|X)\b", "xbox", sentence) for sentence in text]
    text = [re.sub(r"\b(S|s)onos ((O|o)ne|(B|b)eam)\b", "sonos", sentence) for sentence in text]
    text = [re.sub(r"\b(M|m)ac (I|i)?(O|o)(S|s)\b", "macos", sentence) for sentence in text]
    text = [re.sub(r"\b(I|i)phone (I|i)?(O|o)(S|s)\b", "iphoneos", sentence) for sentence in text]
    text = [re.sub(r"\bpi\-hole\b", "pihole", sentence) for sentence in text]
    ## Prime Video Music
    text = [re.sub(r"\b(((AMAZON|Amazon|amazon) (PRIME|Prime|prime) (M|m)usic (U|u)nlimited)|((AMAZON|Amazon|amazon) (PRIME|Prime|prime) (M|m)usic)|((PRIME|Prime|prime) (M|m)usic (U|u)nlimited)|((PRIME|Prime|prime) (M|m)usic))\b", "primemusic", sentence) for sentence in text]
    text = [re.sub(r"\b(AMAZON|Amazon|amazon) (M|m)usic (U|u)nlimited\b", "primemusic", sentence) for sentence in text]
    text = [re.sub(r"\b(M|m)usic (U|u)nlimited\b", "primemusic", sentence) for sentence in text]
    text = [re.sub(r"\b((AMAZON|Amazon|amazon) (PRIME|Prime|prime) (V|v)ideo|(PRIME|Prime|prime) (V|v)ideo)\b", "primevideo", sentence) for sentence in text]
    text = [re.sub(r"\b(AMAZON|Amazon|amazon) (PRIME|Prime|prime)\b|\b(PRIME|Prime|prime)\b", "amazonprime", sentence) for sentence in text]
    ## Amazon
    text = [re.sub(r"\b(A|a)mazon (B|b)asics?\b", "amazonbasics", sentence) for sentence in text] 
    text = [re.sub(r"\b(A|a)mazon (S|s)idewalk\b", "amazonsidewalk", sentence) for sentence in text]
    text = [re.sub(r"\b(A|a)mazon (S|s)hopping app?\b", "shoppingapp", sentence) for sentence in text]
    ## Alexa App
    text = [re.sub(r"\b(A|a)mazon (K|k)ids\+?\b", "amazonkids", sentence) for sentence in text]
    text = [re.sub(r"\b(A|a)lexa(s|\'s)\b", "alexa", sentence) for sentence in text] 
    text = [re.sub(r"\b(A|a)lexa ios? app\b", "alexaapp", sentence) for sentence in text]
    text = [re.sub(r"\b(R|r)outines?\b", "routine", sentence) for sentence in text] 
    text = [re.sub(r"\b(A|a)lexa (phone app|app)\b", "alexaapp", sentence) for sentence in text]
    ## Echo Dot
    text = [re.sub(r"\b((A|a)mazon (E|e)cho (D|d)ots?|(E|e)cho (D|d)ots?)\b", "echodot", sentence) for sentence in text] 
    text = [re.sub(r"\bDots?\b", "echodot", sentence) for sentence in text] 
    ## Echo Show
    text = [re.sub(r"\b(A|a)lexa (S|s)hows?\b", "echoshow", sentence) for sentence in text] 
    text = [re.sub(r"\b((E|e)cho )(S|s)how(s| 5| 8| 10| 15)?\b", "echoshow", sentence) for sentence in text] 
    text = [re.sub(r"\bShow(s|((\'|\’)s)| 5| 8| 10| 15)\b", "echoshow", sentence) for sentence in text] 
    ## Echo Flex 
    text = [re.sub(r"\b(E|e)cho flex\b", "echoflex", sentence) for sentence in text] 
    ## Echo Soundbar 
    text = [re.sub(r"\b(E|e)cho (subwoofer|sub)\b", "echosoundbar", sentence) for sentence in text] 
    ## Echo
    text = [re.sub(r"\b(A|a)mazon (E|e)cho devices?\b", "amazonecho", sentence) for sentence in text] 
    text = [re.sub(r"\b((A|a)mazon (E|e)cho (A|a)uto|(E|e)cho (A|a)uto)\b", "echoauto", sentence) for sentence in text]
    text = [re.sub(r"\b((A|a)mazon (A|a)lexa) (E|e)cho(s|\'s)?\b", "amazonecho", sentence) for sentence in text] 
    text = [re.sub(r"\b((A|a)lexa)\/(E|e)cho(s|\'s)?\b", "amazonecho", sentence) for sentence in text] 
    text = [re.sub(r"\b(E|e)cho devices?\b", "amazonecho", sentence) for sentence in text] 
    text = [re.sub(r"\b(E|e)chos?\b", "amazonecho", sentence) for sentence in text] 
    ## Alexa Features 
    text = [re.sub(r"\b(W|w)hisper mode\b", "whispermode", sentence) for sentence in text] 
    text = [re.sub(r"\b(W|w)ake words?\b", "wakeword", sentence) for sentence in text]
    text = [re.sub(r"\b(K|k)ids(\+| \+)\b", "kidsplus", sentence) for sentence in text]
    text = [re.sub(r"\b(D|d)rop (in|into)\b", "dropin", sentence) for sentence in text]
    text = [re.sub(r"\bon\/off\b", "onoff", sentence) for sentence in text]
    text = [re.sub(r"\b(B|b)\.?t\.?w\b", "bytheway", sentence) for sentence in text]
    text = [re.sub(r"\b((B|b)y the way)\b", "bytheway", sentence) for sentence in text]
    ## Filter 
    text = [re.sub(r"\b(etc)(\.?\,?)", "", sentence) for sentence in text]
    text = [re.sub(r" \& ", " and ", sentence) for sentence in text]
    text = [re.sub(r"\&", " and ", sentence) for sentence in text]
    #text = [re.sub(r"\b(radio station|station|radio)\b", "radiostation", sentence) for sentence in text]
    return text


def clean_amazon_text(text, method, singularize='yes', stopwords='yes', stopword_listtype='general'):
    '''
    Required python pkgs:
    - re (import re) 
    - nltk (from nltk.tokenize import word_tokenize, sent_tokenize)
    - nltk (from nltk.stem.wordnet import WordNetLemmatizer) 
    
    Function: Preprocess text entries.
    - Remove hyperlinks, 
    - Expand contractions, 
    - Remove numbers,
    - Perform NER regularization,
    - Remove punctuation, 
    - Option: Filter stop words,
    - Tokenize/Lemmatize text.
    
    Input Arguments: 
    text: input type is list of (str) items.
    method: input type is (str) item, 'token' or 'lemma'.
    singularize: input type is (str) item, 'yes' or 'no' (default = 'yes').
    stopwords: input type is (str) item, 'yes' or 'no' (default = 'yes').
    stoplist_type: input type is (str) item, 'simple' (no prepositions), 'prep' (prepositions only), 'full' (both) (default = 'general').
    
    Examples: 
    clean_text(utterance_list, 'lemma')
    clean_text(utterance_list, 'token')
    
    '''
    method = method 
    singularize = singularize
    stopword_listtype=stopword_listtype
    
    text = remove_hyperlinks(text)
    text = expand_contractions(text)
    text = amazon_ner_reddit(text)
    text = remove_amazon_numbers(text)
    text = remove_punctuation(text)
    
    if method == 'token': 
        text_output = tokenize_text(text)
        text_output = amazon_ner_reddit(text_output)
    elif method == 'lemma': 
        text_output = lemmatize_text(text) 
        text_output = amazon_ner_reddit(text_output)
    if singularize == 'yes': 
        text_output = singularize_plural_noun(text_output)
    if stopwords == 'yes': 
        text_output = remove_stopwords(text_output, stopword_listtype)
    return text_output


def preprocess_amazon_text_data(df_filepath, category, subreddit_name, sep='tab', method='token', column_list=['title','body','comments'], singularize='yes', stopwords='yes', stopword_listtype='general'):
    '''
    Function: Aggregate & regularize input text data. 
    - Aggregate Amazon-specific datasets in {df_filepath} using glob.
    - Reformat aggregated dataset using format_dataset().
    - For each {column} in {column_list}, convert aggregated dataset {column} values to list.
    - Write aggregated text list as JSON to __data/__aggregated_posts/{category}/{subreddit_name} directory.
    - Clean text data using clean_text().
    - Write cleaned text list as JSON to __data/__aggregated_posts/{category}/{subreddit_name} directory.
    
    Input Arguments: 
    df_filepath: input type is (str) item, denoting filepath. 
    category: input type is (str) item, denoting output subdirectory name.
    subreddit_name: input type is (str) item, denoting output subdirectory name.
    method: input type is (str) item, 'token' or 'lemma'. Default = 'token'.
    sep: input type is (str) item, 'tab' or 'comma'. Default = 'tab'.
    column_list: input type is (list) of (str) items, denoting columns containing text to undergo pre-processing (e.g., 'title', 'body', 'comments').
    singularize: input type is (str) item, 'yes' or 'no'. Default = 'yes'.
    stopwords: input type is (str) item, 'yes' or 'no'. Default = 'yes'.
    stoplist_type: input type is (str) item, 'general' (no prepositions), 'prep' (prepositions only), 'full' (both). Default = 'general'.
    
    
    Example: 
    amazon_filepath = 'reddit/__data/__posts/Amazon/alexa'
    column_list = ['title', 'body', 'comments']
    
    process_amazon_text_data(df_filepath=amazon_filepath, column_list, category='Amazon', subreddit_name='alexa', method='lemma')
    process_amazon_text_data(df_filepath=amazon_filepath, column_list, category='Amazon', subreddit_name='alexa', method='token')
    
    '''
    
    try: 
        if len(glob.glob(f"{df_filepath}/*.csv")) == 0:
            #CSV names: {list(filter(lambda f: f.endswith(".csv"), os.listdir(df_filepath)))}
            raise TypeError 
        if type(subreddit_name) != str:
            raise TypeError 
        if type(category) != str:
            raise TypeError 
        if singularize not in ['yes','no']:
            raise TypeError 
        if stopwords not in ['yes','no']:
            raise TypeError 
        if method not in ['token','lemma']:
            raise TypeError
        if stopword_listtype not in ['general','prep','full']:
            raise TypeError
        if sep not in ['comma','tab']:
            raise TypeError

        if sep=='tab': 
            sep='\t'
        if sep =='comma':
            sep=','

        snapshotdate = datetime.today().strftime('%d-%b-%Y') 
        snapshotdatetime = datetime.today().strftime('%d-%b-%Y_%H-%M-%S')
        print(f'\nInitializing Text Cleaning Task... \n Category: {category}\n Subreddit: "{subreddit_name}"\n')
        ## Extract and concatenate datasets.
        dfs = glob.glob(f'{df_filepath}/*.csv')
        agg_df = pd.concat([pd.read_csv(fp, header=0, encoding="utf-8", engine='python', sep=None) for fp in dfs], ignore_index=True)
        ## Format datasets.
        agg_format_df = format_dataset(agg_df)
        ## Save aggregated dataset.
        os.makedirs(f"../__data/__aggregated_posts/{category}/{subreddit_name}/raw/{snapshotdate}/{subreddit_name}_agg_data", exist_ok=True)
        print(f' ...Saving aggregated "{subreddit_name}" dataset.\n')
        agg_format_df.to_csv(f'../__data/__aggregated_posts/{category}/{subreddit_name}/raw/{snapshotdate}/{subreddit_name}_agg_data/{subreddit_name}_agg_df_{snapshotdatetime}.csv', index=False, encoding='utf-8', sep=sep)
        ## Reset index.
        clean_df = agg_format_df.reset_index()
        for column in column_list:
            #Convert text column from series to list form.
            column_ls = clean_df[column].to_list()
            os.makedirs(f"../__data/__aggregated_posts/{category}/{subreddit_name}/raw/{snapshotdate}/{subreddit_name}_{column}_data", exist_ok=True)
            print(f' ...Saving aggregated "{subreddit_name}_{column}" text.')
            json_raw_object = f'../__data/__aggregated_posts/{category}/{subreddit_name}/raw/{snapshotdate}/{subreddit_name}_{column}_data/{subreddit_name}_{column}_agg_{snapshotdatetime}.json'
            print(f" ...Initializing text cleaning for '{subreddit_name}_{column}' dataset\n(method='{method}', singularize='{singularize}', stopwords='{stopwords}', stopword_listtype='{stopword_listtype}').")
            with open(json_raw_object, 'w') as f:
                json.dump(column_ls, f, indent=2)
            if column != 'title': 
                output_text = remove_usernames(column_ls)
                output_text = clean_amazon_text(output_text, method, singularize, stopwords, stopword_listtype)
            else: 
                output_text = clean_amazon_text(column_ls, method, singularize, stopwords, stopword_listtype)
            clean_df[f'cleaned_{column}'] = output_text
            os.makedirs(f"../__data/__aggregated_posts/{category}/{subreddit_name}/clean/{snapshotdate}/{subreddit_name}_{column}_data", exist_ok=True)
            print(f' ...Saving cleaned "{subreddit_name}_{column}" text.')
            json_clean_object = f'../__data/__aggregated_posts/{category}/{subreddit_name}/clean/{snapshotdate}/{subreddit_name}_{column}_data/{subreddit_name}_{column}_agg_clean_{method}_{snapshotdatetime}.json'
            with open(json_clean_object, 'w', encoding='utf-8') as f:
                json.dump(output_text, f, indent=2)
            print(f" Text Cleaning Task for '{subreddit_name}_{column}' Complete!\n")
        os.makedirs(f"../__data/__aggregated_posts/{category}/{subreddit_name}/clean/{snapshotdate}/{subreddit_name}_agg_data", exist_ok=True)
        clean_df.to_csv(f'../__data/__aggregated_posts/{category}/{subreddit_name}/clean/{snapshotdate}/{subreddit_name}_agg_data/{subreddit_name}_agg_clean_{method}_df_{snapshotdatetime}.csv', index=False, sep=sep)
        print(f"Text Cleaning Task for Subreddit: '{subreddit_name}' Complete!\n")

    except TypeError:
        print(f'\nOh no! Seems there is an issue with the input values:\n\n   Input Directory: {df_filepath}\n   Number CSVs: {len(glob.glob(f"{df_filepath}/*.csv"))}\n   Subreddit: {subreddit_name}\n   Category: {category}\n   Method: {method}\n   Dataset separator: {sep}\n   Stopword (y/n): {stopwords}\n   Stopword List: {stopword_listtype}\n   Singularize (y/n): {singularize}')
        print('\nPlease check your input values, and try again.\n')
    #finally: 
    #    sys.exit(1)
   
    
if __name__ == "__main__":
   preprocess_amazon_text_data()