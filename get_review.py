import requests
import re

def get_review(gameID, cursor, reviews):
    base_url = "https://store.steampowered.com/appreviews/" + gameID +"?json=1&filter=recent&l=english&num_per_page=100&cursor=" + cursor
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'accept': "application/json"}
    
    try:
        res = requests.get(base_url, headers = headers)
        res_json = res.json()
        num_reviews = res_json['query_summary']['num_reviews']

        if cursor == '*':
            total_reviews = res_json['query_summary']['total_reviews']
            if total_reviews <= 100:
                for i in range(0, total_reviews):
                    s = res_json['reviewes'][i]['review'].replace('\n', '')
                    #pattern = r'[^a-zA-Z0-9]'
                    #s = re.sub(pattern=pattern, repl=' ', string=s)
                    reviews.append(s)
                    return

        if cursor == res_json['cursor']: #Repeat end
            for i in range(0, num_reviews):
                reviews.append(res_json['reviews'][i]['review'].replace('\n', ''))
                return
        else: #repeat
            cursor = res_json['cursor']
            for i in range(0, 100):
                reviews.append(res_json['reviews'][0]['review'].replace('\n', ''))
            get_review(gameID, cursor, reviews) 
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
get_review("1448440", '*', reviews)
print(reviews)
