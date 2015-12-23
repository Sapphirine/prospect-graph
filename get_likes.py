#---------------------------------------------------------------------
# get_likes.py
#
# Desc  :  Takes a file containing IDs and LinkedIn URLs.  Captures
#          the interests and writes IDs and interests to a file.
#
# Author:  Janet Prumachuk
# Date  :  Dec 2015
#---------------------------------------------------------------------
import re, nltk, urllib2, sys, mechanize
from nltk import SnowballStemmer
import cookielib
from html2text import html2text 
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from synonyms import get_custom_synonyms

reload(sys)
sys.setdefaultencoding('utf8')

def fetch_html(url_string):
    cj = cookielib.LWPCookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    br.set_handle_referer(False)
    br.set_handle_redirect(True)
    br.set_handle_redirect(mechanize.HTTPRedirectHandler)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) ' \
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')]
    try:
        br.open(url_string)
    except:
        return(-1)

    url = br.geturl()
    #print url
    raw_html = br.open(url).read().decode('utf-8')
    #print raw_html
    return raw_html

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

def standardize(tokens):
    # Remove single character tokens and numbers
    new_text = [w for w in tokens if len(w) > 3]
    new_text = [w for w in new_text if not w.isnumeric()]

    # De-punctuate and convert to lowercase
    new_text = [w.lower() for w in new_text if w.isalpha()]
   
    # Keep words with more than 3 letters
    new_text = [w for w in new_text if len(w) > 3]
    return(new_text) 

def avoid_truncated_words(i, some_text):
    # Starting from index i, back up until we reach a blank space
    try:
        int(i)
    except:
        return i

    i = int(i)
    while 1:
        if some_text[i] != " ":
            i -= 1 
        else:
            break
    return i

def main():
    urlfile = open(sys.argv[1])
    outfile = open(sys.argv[2], 'w')
    snowball_stemmer = SnowballStemmer("english")

    header = "personID|Interest\n"
    outfile.write(header)

    valid_words = ['animal', 'arts', 'culture', 'children', 'civil', 'rights', 'social', 
                   'disaster', 'humanitarian', 'economic', 'empowerment',
                   'education', 'environment', 'health', 'human', 'politics', 'poverty',
                   'science', 'technology', 'social', 'services']

    for row in urlfile:
        items = row.split("|")
        personID = items[0]
        url = items[2]
        html_text = fetch_html(url) 
        if html_text == -1:
            continue

        html_text  = clean_html(html_text)
        plain_text = html2text(html_text)
        #print plain_text

        start_text = "cares about:"
        start_idx = plain_text.find(start_text) 
        if start_idx == -1:
            start_text = "matters to you."
            start_idx = plain_text.find(start_text) 

        if start_idx != -1:
            start_idx += len(start_text)
            end_idx    = plain_text.find(":", start_idx + 1, start_idx + 180)
            if end_idx != -1:
                end_idx = plain_text.find(":") - 1
            else:
                end_idx = start_idx + 180

            end_idx = avoid_truncated_words(end_idx, plain_text)

            #print start_idx, end_idx
            all_interests = plain_text[start_idx : end_idx]
            tokens   = nltk.word_tokenize(all_interests)
            keywords = standardize(tokens)

            for k in keywords:
                if k in valid_words:
                    record = personID + "|" + k + "\n"
                    outfile.write(record.encode('utf8', errors='ignore'))
                    stem = snowball_stemmer.stem(k)
                    if stem != k:
                        record = personID + "|" + stem + "\n"
                        outfile.write(record.encode('utf8', errors='ignore'))

                    more_words = get_custom_synonyms(k)
                    if more_words:
                        for w in more_words:
                            record = personID + "|" + w + "\n"
                            outfile.write(record.encode('utf8', errors='ignore'))
                            stem = snowball_stemmer.stem(w)
                            if stem not in [k,w]:
                                record = personID + "|" + stem + "\n"
                                outfile.write(record.encode('utf8', errors='ignore'))

    urlfile.close()
    outfile.close()

if __name__ == '__main__':
    main()
