#!/usr/bin/python

import os, sys
import re
import pandas as pd




def reformat_praw_comments(praw_df): 
    comments = []
    tmp = []
    comment_col = praw_df.comments
    
    for i in comment_col: 
        comments.append(i)
    for j in comments: 
        commentors = re.findall(r"((?<=\'|\")[A-Za-z0-9_-]+(?=\:))",j)
        starts_with = re.findall(r"(\'|\")(?=[A-Za-z0-9_-]+\:)",j)
        tmp.append([commentors,len(commentors), starts_with,j])
    tmp_df = pd.DataFrame(tmp, columns=['commenters', 'commenter_count', 'starts_w', 'comment_text'])

    comment_list = []
    rgx_1 = r'(?<=\')\, (?=\'[A-Za-z0-9_-]+\:)'
    rgx_2 = r'(?<=\")\, (?=\"[A-Za-z0-9_-]+\:)'

    for i in range(len(tmp_df.comment_text)): 
        input = "".join(list(set(tmp_df.starts_w[i])))
        txt = tmp_df.comment_text[i]
        if input == "'": 
            txt = re.sub(r"(\\\'|\'|\\\’|\’)","\'", txt)
            txt = re.sub(r'\[|\]', "", txt)
            output = re.split(rgx_1, txt)
            comment_list.append(output)
        elif input == "\"": 
            txt = re.sub(r'\[|\]', "",txt)
            output = re.split(rgx_2, txt)
            comment_list.append(output)
        elif input == "\'\"": 
            txt = re.sub(r'\[|\]', "",txt)
            tmp_txt = re.sub(r"(\')(?=([A-Za-z0-9_-]+: )(.*?)\')", '\"', txt)
            tmp_txt = re.sub(r"(\')(?=$|\, (\"|\\\"))",'\"',tmp_txt)
            output = re.split(rgx_2, tmp_txt)
            comment_list.append(output)
        else: 
            comment_list.append(['NaN'])
    tmp_df['comment_list'] = comment_list
    praw_df["commenter_list"] = tmp_df.commenters
    praw_df["commenter_count"] = tmp_df.commenter_count
    praw_df['comment_list'] = comment_list
    return praw_df


if __name__ == "__main__":
    reformat_praw_comments()