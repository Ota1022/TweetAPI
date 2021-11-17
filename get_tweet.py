import os

import csv
import datetime
import dateutil.parser
import requests
import time


def auth():
    return "YOUR_KEY"


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_url(keyword, start_date, end_date, max_results=10):
    search_url = "https://api.twitter.com/2/tweets/search/all"
    query_params = {
        "query": keyword,
        "start_time": start_date,
        "end_time": end_date,
        "max_results": max_results,
        "expansions": "author_id",
        "tweet.fields": "id,text,author_id,created_at",
        "user.fields": "id,name,username",
        "next_token": {},
    }
    return (search_url, query_params)


def connect_to_endpoint(url, headers, params, next_token=None):
    params["next_token"] = next_token
    response = requests.request("GET", url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


bearer_token = auth()
headers = create_headers(bearer_token)
# keyword = "#~ -is:retweet"
keyword = "#~"
# 日本時間から-9h
start_date = "2021-00-00T11:00:00.000Z"
end_date = "2021-00-00T11:00:00.000Z"
max_results = 200
total_tweets = 0
JST = datetime.timezone(datetime.timedelta(hours=+9), "JST")

url = create_url(keyword, start_date, end_date, max_results)
json_response = connect_to_endpoint(url[0], headers, url[1])

dt_now = datetime.datetime.now()
csvFile = open(
    "tweet" + str(dt_now.strftime("%y%m%d_%H%M%S")) + ".csv",
    "a",
    newline="",
    encoding="utf-8",
)
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["created_at", "text"])
csvFile.close()


def append_to_csv(json_response, fileName):
    csvFile = open(fileName, "a", newline="", encoding="utf-8")
    csvWriter = csv.writer(csvFile)

    for i in range(len(json_response["data"])):
        ca = json_response["data"][i]["created_at"]
        created_at = dateutil.parser.parse(ca).astimezone(JST).replace(tzinfo=None)
        text = json_response["data"][i]["text"].replace("\n", "")
        res = [created_at, text]
        csvWriter.writerow(res)
    csvFile.close()


count = 0
flag = True
next_token = None

while flag:
    print("Token: ", next_token)
    url = create_url(keyword, start_date, end_date, max_results)
    json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
    result_count = json_response["meta"]["result_count"]

    if "next_token" in json_response["meta"]:
        # Save the token to use for next call
        next_token = json_response["meta"]["next_token"]
        print("Next Token: ", next_token)
        if result_count is not None and result_count > 0 and next_token is not None:
            append_to_csv(
                json_response, "tweet" + str(dt_now.strftime("%y%m%d_%H%M%S")) + ".csv"
            )
            count += result_count
            total_tweets += result_count
            print("Total # of Tweets added: ", total_tweets)
            print("-------------------")
            time.sleep(5)

    else:
        if result_count is not None and result_count > 0:
            print("-------------------")
            append_to_csv(
                json_response, "tweet" + str(dt_now.strftime("%y%m%d_%H%M%S")) + ".csv"
            )
            count += result_count
            total_tweets += result_count
            print("Total # of Tweets added: ", total_tweets)
            print("-------------------")
            break

        flag = False
        next_token = None
    time.sleep(10)

print("Total number of results: ", total_tweets)
