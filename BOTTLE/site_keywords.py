#-----------------------------------------------------------------
# site_keywords.py
#
# Desc  :  Functions to capture and clean keywords for a URL    
#
# Author:  Janet Prumachuk
# Date  :  Dec 2015
#-----------------------------------------------------------------
import re, nltk, urllib2, sys, mechanize
from html2text import html2text 
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from synonyms import get_custom_synonyms

def fetch_html(url_string):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]
    try:
        raw_html = br.open(url_string).read().decode('utf-8')
        return(raw_html) 
    except:
        return(-1)

def clean_html(html):
    # Remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?s)<(script|style).*?>.*?(</\1>)", "", html.strip())

    # Remove comments 
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)

    # Remove URLs
    cleaned = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', cleaned)

    # Remove remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)

    # Other special characters:
    cleaned = re.sub(r"&amp;", " ", cleaned)

    # Deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()

def compute_fdist(tokens):
    # Remove single character tokens and numbers
    new_text = [w for w in tokens if len(w) > 3]
    new_text = [w for w in new_text if not w.isnumeric()]

    # De-punctuate and convert to lowercase
    new_text = [w.lower() for w in new_text if w.isalpha()]
   
    # Keep only nouns and adverbs
    #tags = nltk.pos_tag(new_text)
    #new_text = [w for w,cd in tags if (cd[0] in ['N','R'])]

    # Lemmatize the word (gives us better results than stemming)
    lemma = WordNetLemmatizer()
    new_text = map(lemma.lemmatize, new_text)

    # Remove stopwords 
    stopwords = nltk.corpus.stopwords.words('english')
    custom_list = ['facebook', 'twitter', 'instagram', 'pinterest', 'youtube', 
                   'google', 'blog', 'help', 'give', 'donate', 'way', 'join', 
                   'make', 'month', 'week', 'day', 'year', 'time', 'name', 
                   'team', 'fundraise', 'key', 'search', 'way', 'today', 
                   'member', 'program', 'event', 'york', 'membership', 
                   'visit', 'support', 'day', 'night', 'show', 'fall', 
                   'winter', 'spring', 'summer', 'gift', 'benefit', 'state', 
                   'stay', 'height', 'video', 'email', 'money', 'news',
                   'opportunity', 'donate', 'press', 'faq', 'infographic',
                   'find', 'save', 'new', 'site', 'story', 'view', 'share',
                   'become', 'center', 'holiday', 'january', 'february',
                   'march', 'april', 'may', 'june', 'july', 'august', 
                   'september', 'october', 'november', 'december', 'sunday', 
                   'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                   'saturday', 'policy', 'every', 'please', 'change']

    custom_stopwords = [unicode(i) for i in custom_list]
    stopwords.extend( custom_stopwords )
    new_text = [w for w in new_text if w not in stopwords]
    new_text = [w for w in new_text if len(w) > 3]

    # Calculate frequency distribution
    fdist = nltk.FreqDist(new_text)
    return(fdist)
