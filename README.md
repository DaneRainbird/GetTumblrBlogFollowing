# Tumblr API - Get Blog Following List
This is a simple Python script that utilises [Pytumblr](https://github.com/tumblr/pytumblr) in order to return all of the blogs a given blog is following on Tumblr.  

## Requirements  
- Python 2.7 or greater.
- Consumer and OAuth 1.0 keys / secrets from Tumblr's [API  Console](https://api.tumblr.com/console/).

## Installation
Firstly, install Pytumblr via pip:  

```python 
pip install pytumblr  
```

Create a `credential` file (no extension), and place your aforementioned keys in the following order:  
```
consumer_key,
consumer_secret,
oauth_token,
oauth_secret,
```
Place the credential file in the same directory as  `blog_followers.py` and run:
```python
python3 blog_followers.py
```

## Disclaimer
This script is significantly over-engineered for what it does. This is intentional, as I used this mini-project as a chance to better my understanding of Python and it's coding practices.  