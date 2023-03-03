import requests
import json

def get_review(gameID, cursor, total_reviews):
    base_url = "https://store.steampowered.com/appreviews/" + gameID +"?json=1&filter=recent&l=english&num_per_page=100&cursor=" + cursor
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'accept': "application/json"}
    
    try:
        res = requests.get(base_url, headers = headers)
        res_json = res.json()
        num_reviews = res_json['query_summary']['num_reviews']

        if cursor == '*':
            total_reviews = res_json['query_summary']['total_reviews']
            print(total_reviews)

        if num_reviews < 100:
            #NO REPEAT
            print(num_reviews)
            print(res_json['reviews'][0]['review'])
        else:
             #REPEAT
            cursor = res_json['cursor']
            print(cursor)
            get_review(gameID, cursor, total_reviews)
    except Exception as e:
        print("error")
        print(e)

#GameID=[1,2,3,4]
#for i in GameID:
#    get_review(str(i), '*')
get_review("1448440", '*', 0)
