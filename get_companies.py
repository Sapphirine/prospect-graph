#--------------------------------------------------------
# get_companies.py 
#
# Desc  :  Extracts a subset of startups from Angel List
# Author:  Janet Prumachuk
# Date  :  Nov 2015
#--------------------------------------------------------
import requests, re, time, os

def fetchdata():
    results = []
    token = "&access_token=" + os.environ["AL_TOKEN"]
    page = 1
    while 1:
        url = "https://api.angel.co/1/startups?page=" + str(page) + "&filter=raising"
        r = requests.get(url + token)
        time.sleep(36)    # API has rate limit of 100 requests per hour
        rjson = r.json()
        results.append( rjson['startups'] )
        if rjson['last_page'] == rjson['page']:
            return results
        else:
            page += 1

def flatten(json):
    fn = "companies_" + time.strftime("%y%m%d%I%M%S") + ".txt"
    f = open(fn, 'w') 
    header = 'id|name|logo_url|thumb_url|launch_date|quality|' \
           'high_concept|company_url|crunchbase_url|twitter_url|' \
           'linkedin_url|location|company_size|raising_amount|'\
           'pre_money_valuation|raised_amount\n'
    f.write(header.encode('utf8'))

    d = "|"
    for page in json:                
        for segment in page:
            if 'name' in segment:
                id = unicode( str(segment['id']), errors='ignore' ) 
                name = d + segment['name']

                logo_url = d
                if segment['logo_url'] is not None:
                    logo_url = d + segment['logo_url']

                thumb_url = d
                if segment['thumb_url'] is not None:
                    thumb_url = d + segment['thumb_url']

                launch_date = d
                if 'launch_date' in segment: 
                    if segment['launch_date'] != False:
                        if segment['launch_date'] is not None:
                            launch_date = d + segment['launch_date']

                quality = d + unicode( str(segment['quality']), errors='ignore' )

                high_concept = d
                if segment['high_concept'] is not None:
                    high_concept = d + segment['high_concept']

                company_url = d
                if segment['company_url'] is not None:
                    company_url = d + segment['company_url']

                crunchbase_url = d
                if segment['crunchbase_url'] is not None:
                    crunchbase_url = d + segment['crunchbase_url']

                twitter_url = d
                if segment['twitter_url'] is not None:
                    twitter_url = d + segment['twitter_url']

                linkedin_url = d
                if segment['linkedin_url'] is not None:
                    linkedin_url = d + segment['linkedin_url']

                location = d 
                if 'locations' in segment:
                    if segment['locations'] != False:
                        for l in segment['locations']:
                            if 'display_name' in l:
                                location = d + l['display_name']

                company_size = d
                if segment['company_size'] is not None:
                    company_size = d + segment['company_size']

                raising_amount = "|0"
                valuation      = "|0"
                raised_amount  = "|0"
                if 'fundraising' in segment:
                    if segment['fundraising'] != False:
                        if 'raising_amount' in segment['fundraising']:
                            raising_amount = d + unicode(str(segment['fundraising']['raising_amount']),errors='ignore')
                        if 'pre_money_valuation' in segment['fundraising']:
                            valuation = d + unicode(str(segment['fundraising']['pre_money_valuation']),errors='ignore')
                        if 'raised_amount' in segment['fundraising']:
                            raised_amount = d + unicode(str(segment['fundraising']['raised_amount']),errors='ignore')

                record = id + name + logo_url + thumb_url + quality \
                         + high_concept + company_url + crunchbase_url + twitter_url \
                         + linkedin_url + location + company_size + raising_amount + valuation \
                         + raised_amount + '\n'

                f.write(record.encode('utf8', errors='ignore'))

    f.close()

if __name__ == '__main__':
    jsondata = fetchdata()
    flatten(jsondata)

