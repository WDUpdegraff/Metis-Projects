import requests, re

base = 'https://openlibrary.org'
mid = '/search?q=a&sort=editions&has_fulltext=true&language=eng&page='
rest = '&first_publish_year='

startslug = 'http://openlibrary.org/api/volumes/brief/json/'
stopslug = '?listofworks='

url = 'https://openlibrary.org/search?q=a&sort=editions&has_fulltext=true&language=eng&page=1&first_publish_year=2007'

def rawhtml(urlstring):
    response = requests.get(urlstring)
    return response.text
            
def getgoods(url):
    firstbit = 'https://openlibrary.org/works/'
    matches = re.findall( '<a href="/works/(.*?)>', rawhtml(url))
    matches_good = []
    for match in matches:
        if '/' in match:
            if'/works' not in match:
                if '"' in match:
                    matches_good.append(firstbit + match[:match.find('"')])
    return matches_good

import os
path = '/Users/derekupdegraff/Metis_Class/Fletcher_Scraping'
#path = '/home/ubuntu/Fletcher_Scraping'

years = list(range(1994, 1995))
pagenums = list(range(1,20))
for year in years:
    to_visit = []
    for pagenum in pagenums:          
        url = base + mid + str(pagenum) + rest + str(year)
        goods = getgoods(url)
        if type(goods) == list:
            to_visit.extend(goods)
    to_visit = list(set(to_visit))
    pwf = path + '/' + str(year)
    if not os.path.exists(pwf):
        os.makedirs(pwf)
    with open(pwf + '/urls_to_visit.txt', 'w') as textfile:
        textfile.write('\n'.join(to_visit))