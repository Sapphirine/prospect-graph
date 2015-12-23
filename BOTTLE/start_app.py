import nltk
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from html2text import html2text
import os, sys, re
from bottle import get, post, route, run, debug, request, response, static_file, template
from py2neo import Graph
from site_keywords import fetch_html, clean_html, compute_fdist

reload(sys)
sys.setdefaultencoding('utf8')

# Globals
snowball_stemmer   = SnowballStemmer("english")
wordnet_lemmatizer = WordNetLemmatizer()

# set connection information (defaults to http://localhost:7474/db/data/)
graph_db = Graph()

@route('/js/<filename>')
def js_static(filename):
    return static_file(filename, root='./js')

@route('/img/<filename>')
def img_static(filename):
    return static_file(filename, root='./img')

@route('/css/<filename>')
def img_static(filename):
    return static_file(filename, root='./css')

@route('/')
def index():
    return template("index.tpl", data='', keywords='', orgname='')

@route('/', method='POST')
def submit(data='', keywords=''):
    orgname = request.forms.get('orgname').strip().lower()
    keywords = []
    results = []
    if not orgname:
        keywords.append("Error: please enter an organization name.")
    else:
        N = 10
        url = "http://www." + orgname + ".org"
        html_text = fetch_html(url)
        if html_text == -1:
            keywords.append("Sorry, this site could not be accessed.")
        else:
            html_text  = clean_html(html_text)
            plain_text = html2text(html_text)
            tokens     = nltk.word_tokenize(plain_text)
            wordfreqs  = compute_fdist(tokens)
            for word, freq in wordfreqs.most_common(N):
                word = word.strip()
                if freq > 1:
                    # Keep the word, the lemma, and the stem
                    keywords.append(word)
                    lemma = wordnet_lemmatizer.lemmatize(word)
                    if lemma and (lemma != word):
                        keywords.append(lemma)
                    stem = snowball_stemmer.stem(word)
                    if stem and (stem not in [word, lemma]):
                        keywords.append(stem)

            if len(keywords) > 0:
                results = graph_db.cypher.execute( \
                    "MATCH (p:Person)-[:LIKES]->(i:Interest), " \
                    "      (p)-[r:HAS_ROLE]->(c:Company) " \
                    "WHERE i.interestType in {keywords} " \
                    "RETURN DISTINCT p.Name as person_name, " \
                    "                p.Bio as bio, " \
                    "                r.roleType as role, " \
                    "                c.Name as company_name, " \
                    "                c.raisedAmount as funds, " \
                    "                c.companySize as size, " \
                    "                c.companyURL as website, " \
                    "                c.primaryLocation as location, " \
                    "                p.profileURL as profile " \
                    "ORDER BY c.raisedAmount DESC", {"keywords": keywords})
            else:
                results = "Sorry, no keywords found on this site."

    return template("index.tpl", data=results, keywords=keywords, orgname=orgname)
                          
run(host='10.0.0.8', port=8080, debug=False)
#run(host='localhost', port=8080, debug=False)
