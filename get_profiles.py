#---------------------------------------------------------------------------
# get_profiles.py
#
# Desc  :  Reads output of get_people.py and get_companies.py
#          and uses Google search to build a list of LinkedIn profile URLs
# Author:  Janet Prumachuk
# Date  :  Nov 2015
#---------------------------------------------------------------------------
import sys, requests, re, time
from google import search

def create_dict(companies):
    # create a dictionary for company name lookup
    cdict  = {}
    for c in companies:
        fields = c.split("|")
        if fields[0] != "id":
            key = fields[0]
            key = int(key)
            val = fields[1]
            cdict[key] = val
    return cdict

def fetch_profile_urls(people, companies):
    fn = "links_" + time.strftime("%y%m%d%I%M%S") + ".txt"
    ss = open(fn, 'wb')
    fields = []

    # form the search string and execute a google search
    for p in people:
        fields = p.split("|")
        if fields[0] != "company_id":
            company_id   = fields[0]
            company_id   = int(company_id)
            company_name = companies[company_id]
            company_name = company_name.replace(" ","+")
            company_name = re.sub(r"[^\x00-\x7f]+"," ", company_name)
            person_id    = fields[1]
            person_name  = fields[2]
            person_name  = person_name.replace(" ","+")
            search_str   = "linkedin+" + person_name + "+" + company_name + "\n"
            record       = person_id +  "|" + fields[2]

            # find the most relevant LinkedIn profile
            for url in search(search_str, lang='en', stop=1):
                 if "www.linkedin.com/pub/" in url:
                     record = record + "|" + url + "\n"
                     ss.write(record)
                     break
                 elif "www.linkedin.com/in/" in url:
                     record = record + "|" + url + "\n"
                     ss.write(record)
                     break
                 elif "linkedin.com" in url:
                     record = record + "|" + url + "\n"
                     ss.write(record)
                     break
                              
    ss.close()

def main():
    people_file  = open(sys.argv[1])
    company_file = open(sys.argv[2])
   
    cdict = create_dict(company_file)
    fetch_profile_urls(people_file, cdict)

    people_file.close()
    company_file.close()

if __name__ == '__main__':
    main()
