import os, requests
path = '/Users/derekupdegraff/Metis_Class/Fletcher_Scraping'
#path = '/home/ubuntu/Fletcher_Scraping'

def rawhtml(urlstring):
    try:
        response = requests.get(urlstring)
    except requests.exceptions.RequestException:    # This is the correct syntax
        response = ''
    if response:
        return response.text
    else:
        return ''

def get_direct_link(urlstring):
    html = rawhtml(urlstring)
    stop = html.find('.txt') + 4
    start = max([0,stop - 200])
    htmlshort = html[start:stop]
    start2 = htmlshort.rfind('href="') + len('href="')
    shorter = htmlshort[start2:]
    if shorter[:2] == '//':
        shorter = 'http://' + shorter[2:]
    return shorter
    
import time
t0 = time.time()
        
#years = list(range(1994, 1995))
status_string = ''
years = list(range(1993, 1994))
for year in years:
    pwfile = path + '/' + str(year) + '/urls_to_visit.txt'
    if os.path.isfile(pwfile):
        with open(pwfile, 'r') as myfile:
            urls = myfile.read().replace('\n', ' ')
        urls = urls.split()
    valid_urls = []
    direct_links = []
    book_counter = 0
    urls = urls[:30] # SUBSET
    for url in urls:
        # sometimes this accidentally grabs the raw url not going back
        if '/works/' in url: 
            html = rawhtml(url)
            if len(html) > 200:
                valid_urls.append(url)
            if '.txt' in html:
                direct_links.append(get_direct_link(url))
    if len(direct_links) > 0:
        pwf = path + '/' + str(year)
        with open(pwf + '/direct_links.txt', 'w') as textfile:
            textfile.write('\n'.join(direct_links))
        for i in range(len(direct_links)):
            html_good = rawhtml(direct_links[i])
            if len(html_good) > 200:
                with open(pwf + '/book_' + str(i+1) + '.txt', 'w') as textfile2:
                    textfile2.write(html_good)
                book_counter = book_counter + 1
    yr = 'Year: ' + str(year)
    tot = ',   Total URLs: ' + str(len(urls))
    val = ',   Valid URLs: ' + str(len(valid_urls))
    lnk = ',   Good Links: ' + str(len(direct_links))
    ret = ',   Retreived Books: ' + str(book_counter) + '\n'
    status_string =  status_string + yr + tot + val + lnk + ret
with open(path + '/scraping_status.txt', 'w') as textfile3:
    textfile3.write(status_string)
    
t1 = time.time()
dt1 = t1-t0
print(dt1)           
