#-----------------------------------------------------------------
# find_site_keywords.py
#
# Desc  :  Finds important keywords for a URL.  Takes two args: 
#
# 1) a fully formed URL, e.g. http://habitat.org
# 2) an integer specifying the number of keywords to return, e.g. 20
#
# Author:  Janet Prumachuk
# Date  :  Dec 2015
#-----------------------------------------------------------------
import re, nltk, urllib2, sys, mechanize
from html2text import html2text 
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def fetch_html(url_string):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]
    try:
        raw_html = br.open(url_string).read().decode('utf-8')
        return(raw_html) 
    except:
        print "Sorry, this site could not be accessed.\n"
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
    # Applies text mining techniques from the NLTK package and 
    # calculates the frequency distribution of words, excluding stopwords

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
    #print( new_text )

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
                   'become', 'center', 'holiday']

    custom_stopwords = [unicode(i) for i in custom_list]
    stopwords.extend( custom_stopwords )
    new_text = [w for w in new_text if w not in stopwords]
    new_text = [w for w in new_text if len(w) > 3]

    #print(new_text)

    # Calculate frequency distribution
    fdist = nltk.FreqDist(new_text)
   
    return(fdist)


def main():
    url = str( sys.argv[1] )
    N = int( sys.argv[2] )
    
    print( "Fetching " + url + "...")
 
    html_text  = fetch_html(url)
    if html_text == -1:
        return()

    html_text  = clean_html(html_text)
    plain_text = html2text(html_text)
    tokens     = nltk.word_tokenize(plain_text)
    keywords   = compute_fdist(tokens)
    #print keywords

    # Show the top n words
    print( "Top " + str(N) + " words found for " + url + ":")
    for word, freq in keywords.most_common(N):
        print ('%s, %d' % (word, freq)).encode('utf-8')


if __name__ == '__main__':
    main()
