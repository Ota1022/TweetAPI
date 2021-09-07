# How to collect tweets using Twitter API v2  

This code assumes that you are using the Twitter API v2 for academic research. After cloning this repository, create `.env` and enter the bearer token as described in `.envsample`.

## Referenced articles  
- An Extensive Guide to collecting tweets from Twitter API v2 for academic research using Python 3  
    https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a  

- Twitter API v2 Documentation Fields  
    https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all  

- Twitter API Reference GET /2/tweets/search/all  
    https://developer.twitter.com/en/docs/twitter-api/fields  


## How to use get_tweet.py  
- `keyword = "#~"`:  
    Type the hashtag you want to search for in ~.  
    If you want to exclude retweets, use `# keyword = "#~ -is:retweet"`  

- `start_date = "2021-00-00T00:00:00.000Z"` `end_date = "2021-00-00T00:00:00.000Z"`:  
    This is written in UTC of ISO 8601/RFC 3339. If you want to run in Japan Standard Time, subtract 9 hours.  
    For example, if you want to search from 19:00 to 21:00 JST on September 7, 2021, type  
    `start_date = "2021-09-07T10:00:00.000Z"` and `end_date = "2021-09-07T12:00:00.000Z"`.  

- `max_results = 200`:  
    The Documentation of the Twitter API describes, "The maximum number of search results to be returned by a request. A number between 10 and the system A number between 10 and the system limit (currently 500). By default, a request response will return 10 results. By default, a request response will return 10 results."  Make change the number as needed.  