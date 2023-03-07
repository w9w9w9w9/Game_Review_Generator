import requests
import re
import urllib.parse
import pickle
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize, sent_tokenize

def sentence_preprocessing(s):
    pre = []
    sent_s = sent_tokenize(s)
    for i in sent_s:
        tmp_s = re.sub(r"[^a-z0-9]+", " ", i.lower())
        tmp_w = word_tokenize(tmp_s)
        if len(tmp_w) > 3:
            pre.append(tmp_w)
    return pre


def get_review(gameID, cursor, reviews):
    base_url = "https://store.steampowered.com/appreviews/" + gameID +"?json=1&filter=recent&l=english&num_per_page=100&cursor=" + cursor
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'accept': "application/json"}
    
    try:
        res = requests.get(base_url, headers = headers)
        res_json = res.json()
        num_reviews = res_json['query_summary']['num_reviews']
        new_cursor =  urllib.parse.quote(res_json['cursor'])
        if cursor == '*':
            total_reviews = res_json['query_summary']['total_reviews']
            print("totla reviews is: ", total_reviews)
            if total_reviews <= 100:
                for i in range(0, total_reviews):
                    s = res_json['reviews'][i]['review'].replace('\n', '')
                    s = sentence_preprocessing(s)
                    if len(s) > 3:
                        reviews.append(s)
                return
        
        if cursor == new_cursor: #Repeat end
            for i in range(0, num_reviews):
                s = res_json['reviews'][i]['review'].replace('\n', '')
                s = sentence_preprocessing(s)
                if len(s) > 3:
                    reviews.append(s)
            return
        else: #repeat
            for i in range(0, num_reviews):
                s = res_json['reviews'][i]['review'].replace('\n', '')
                s = sentence_preprocessing(s)
                if len(s) > 3:
                    reviews.append(s)
            get_review(gameID, new_cursor, reviews) 

    except Exception as e:
        print("error")
        print(e)

#GameID=['1','2','3','4']
#reviews = []
#tmp = []
#for i in GameID:
#    get_review(i, '*', tmp)
#    reviews.append(tmp)
reviews = []
get_review("1721470", '*', reviews)
print(reviews[:10])
with open('test.pkl', 'wb') as file:
    pickle.dump(reviews, file)

