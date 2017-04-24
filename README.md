# Gab Scraper

This code scrapes a range of post IDs from [Gab.ai](http://gab.ai/), given a user login. I wrote it as part of an upcoming investigation into elite message transmission and social network analysis of Gab.

## Installation instructions

0. Install Python `mechanize` module.
1. Rename `auth_blank.json` to `auth.json` and provide user credentials.
2. `python scrape_posts.py min_id max_id`

Default ID range is 1-10,000.

## Denial of service note

Although the code inserts pauses between each scrape and I haven't personally run into any resource limits, it's theoretically possible that something like this exhaust server resources and cause problems for the administrators of Gab.ai. Please use responsibly,


## Code Style Guide

`pylint` settings are contained in `.pylintrc`.

`pep8` settings are as follows:
`pep8 --ignore W191,E101,E111,E501,E128`

## Contributions?

Please feel free to open a pull request.
