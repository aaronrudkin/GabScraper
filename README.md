# Gab Scraper

This code scrapes a range of post IDs from [Gab.ai](http://gab.ai/), given a user login. I wrote it as part of an upcoming investigation into elite message transmission and social network analysis of Gab.

## Example data

`cat REDACTED.json`

```javascript
{"id":REDACTED,"created_at":"2016-09-14T21:16:21+00:00","revised_at":null,"edited":false,
"body":"Just picked up my new copy of #Pepe's newest best seller!  Can't wait to read it!\n\nhttps:\/\/i.sli.mg\/QdG2yn.png\n\n#Trump\n#MAGA",
"only_emoji":false,"liked":false,"disliked":false,"bookmarked":false,"repost":false,"reported":false,
"score":15,"like_count":0,"dislike_count":0,"is_quote":false,"is_reply":false,"is_replies_disabled":false,
"embed":{"html":"<a href=\"https:\/\/i.sli.mg\/QdG2yn.png\" target=\"_blank\" class=\"post__embed__body post__embed__body--photo\"><div class=\"post__embed__body__image\" style=\"background-image: url('https:\/\/ipr2.gab.ai\/9ab9fc66af8e49914d18ef9fd406d3059f647cb0\/68747470733a2f2f692e736c692e6d672f51644732796e2e706e67\/')\"><\/div><\/a>",
	"iframe":false},
"category":null,"category_details":null,
"user":{
	"id":REDACTED,"name":REDACTED,"username":REDACTED,
	"picture_url":"https:\/\/gabfiles.blob.core.windows.net\/user\/5845aa24deb46.jpg",
	"verified":false,"is_donor":false,"is_pro":false,"is_private":false}
}
```

## Installation instructions

0. Install Python `mechanize` module and `html5lib` module: `pip install -r requirements.txt`
1. Rename `auth_blank.json` to `auth.json` and provide user credentials.
2. `python scrape_posts.py min_id max_id` to scrape posts
3. `python scrape_users.py` to scrape users
4. (NOT IMPLEMENTED) `python spider_post_users.py` to spider usernames for scraping from the posts you've scraped.
5. `python spider_users.py` to spider additional users for scraping.

Default ID range for posts is 1-10,000.

## Denial of service note

Although the code inserts pauses between each scrape and I haven't personally run into any resource limits, it's theoretically possible that something like this exhaust server resources and cause problems for the administrators of Gab.ai. Please use responsibly. The script will shut down if it receives a 429 status code from Gab.

## Code Style Guide

`pylint` settings are contained in `.pylintrc`.

`pep8` settings are as follows:
`pep8 --ignore W191,E101,E111,E501,E128`

## Contributions?

Please feel free to open a pull request.
