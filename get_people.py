#-----------------------------------------------------------------
# get_people.py
#
# Desc  :  Reads a file of company IDs and gets people and roles
# Author:  Janet Prumachuk
# Date  :  Nov 2015
#-----------------------------------------------------------------
import sys, requests, re, time, os

def fetchpeople(companies):
    fn = "people4_" + time.strftime("%y%m%d%I%M%S") + ".txt"
    pf = open(fn, 'w')
    header = 'company_id|person_id|name|role|confirmed|bio|follower_count\n'
    pf.write(header.encode('utf8'))
    token = "&access_token=" + os.environ["AL_TOKEN"]
    d = "|"
    for c in companies:
        results = []
        items = c.split("|")
        company_id = items[0]
        if company_id == "id":
            continue

        pageno = 1
        while 1:
            url = "https://api.angel.co/1/startup_roles?&startup_id=" + \
                  str(company_id) + "&page=" + str(pageno)
            r = requests.get(url + token)
            time.sleep(36)  # API has rate limit of 100 requests per hour
            rjson = r.json()
            results.append( rjson['startup_roles'] )
            if rjson['last_page'] == rjson['page']:
                break
            else:
                pageno += 1

        for page in results:                
            for segment in page:
                if 'role' in segment:
                    role = d + segment['role']
                    confirmed = d + unicode( str(segment['confirmed']) )
                    if 'name' in segment['user']: 
                        name = d + segment['user']['name']
                        id = d + unicode( str(segment['user']['id']),errors='ignore' ) 
                        
                        bio = d
                        if segment['user']['bio'] is not None:
                            bio = d + segment['user']['bio'].replace("\n",". ")
                            bio = bio.replace("/t"," ")

                        followers = d
                        if segment['user']['follower_count'] is not None:
                            followers = d + unicode(str(segment['user']['follower_count']),
                                                        errors='ignore')
   
                        record = company_id + id + name + role + confirmed + bio + \
                                 followers + '\n'
                        pf.write(record.encode('utf8', errors='ignore'))

    pf.close()

def main():
    company_file = open(sys.argv[1])
    fetchpeople(company_file)
    company_file.close()

if __name__ == '__main__':
    main()
