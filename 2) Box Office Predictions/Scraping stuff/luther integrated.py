import requests
from bs4 import BeautifulSoup
import time
import random
import csv
#time1, time2 = 4,2


def grabstuff(url):
    response = requests.get(url)
    page = response.text
    soup =  BeautifulSoup(page, 'lxml')
    grosses, words, foreign = [], [], None
    bigtable = soup.find('table', {'border' : '0', 'cellspacing' : '0', 'width' : '878px'})
    if bigtable:
        subtable = bigtable.find('div', {'class' : 'mp_box_content'})
        if subtable:
            columnbit = subtable.findAll('td')#, {'width' : '35%'}
            if columnbit:
                for row in columnbit:
                    if '$' in row.text:
                        gross = int(row.text.replace('$','').replace(',',''))
                        grosses.append(gross)
                    if ':' in row.text:
                        word = str(row.text)
                        if '\xa0' in word:
                            word = word[2:]
                        words.append(word)
                if len(grosses) == 3:
                    foreign = grosses[1]
    
    def aftercolon(mystring):
        return mystring[mystring.find(':') + 2:]
    
    def timetranslate(timestring):
        timelist = timestring.split()
        t = 0
        for i in range(len(timelist)):
            if 'h' and 'r' in timelist[i]:
                t = t + int(timelist[i-1])*60
            if 'm' and 'n' in timelist[i]:
                t = t + int(timelist[i-1])
        return t
    
    def tonum(numstr):
        numstr2 = numstr.replace(',','')
        try:
            return int(numstr2)
        except ValueError:
            return float(numstr2)
    
    def budgettranslate(mystring):
        multiplier = 1
        cleanstring = mystring.replace('$','').replace(',','').replace(' ','')
        cleanstring = cleanstring.lower()
        if 'n/a' in cleanstring:
            return None
        elif 'million' in cleanstring:
            multiplier = multiplier*1000000
            cleanstring = cleanstring.replace('million','')
        elif 'm' in cleanstring:
            multiplier = multiplier*1000000
            cleanstring = cleanstring.replace('m','')        
        if 'thousand' in cleanstring:
            multiplier = multiplier*1000
            cleanstring = cleanstring.replace('thousand','')
        return int(tonum(cleanstring)*multiplier)
    
    
    othertable = soup.find('table', {'border' : '0', 'cellspacing' : '1',
                                     'cellpadding' : '4', 'width' : '95%', 'bgcolor' : '#dcdcdc'})
    genre, runtime, rating, budget = None, None, None, None
    if othertable:
        stuff = othertable.findAll('td')
        if stuff:
            for line in stuff:
                if "Genre" in line.text:
                    genre = aftercolon(str(line.text))
                elif 'Runtime' in line.text:
                    runtime = timetranslate(aftercolon(str(line.text)))
                elif 'Rating' in line.text:
                    rating = aftercolon(str(line.text))
                elif 'Budget' in line.text:
                    budget = budgettranslate(aftercolon(str(line.text)))
        
    
    thirdtables = soup.findAll('table', {'border' : '0', 'cellspacing' : '1', 'cellpadding' : '5',
                                     'style': 'border-collapse: collapse' , 'width' : '100%'})

    w_alltime, d_alltime, w_yearly = None, None, None
    w_yearly_rating, d_yearly_rating =  None, None
    
    for table in thirdtables:
        if 'All Time Domestic' in table.text:
            goodtable = table
    
            cols = goodtable.findAll('tr')
            
        
            for col in cols:
                if 'All Time Worldwide' in col.text:
                    w_alltime = tonum(str(col.find('td', {'align' : 'center', }).text))
                elif 'All Time Domestic' in col.text:
                    d_alltime = tonum(str(col.find('td', {'align' : 'center', }).text))
                elif 'Worldwide Yearly' in col.text:
                    w_yearly = tonum(str(col.find('td', {'align' : 'center', }).text))
                elif rating != None: 
                    if 'Yearly ' + rating + ' Rated' in col.text:
                        w_yearly_rating = tonum(str(col.find('td', {'align' : 'center', }).text))
                    elif 'Rated ' + rating in col.text:
                        d_yearly_rating = tonum(str(col.find('td', {'align' : 'center', }).text))
    
    return [foreign, budget, genre, runtime, rating, w_alltime,
           d_alltime, w_yearly, w_yearly_rating, d_yearly_rating]
    #return w_alltime, d_alltime, w_yearly, w_yearly_rating, d_yearly_rating
def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

t0 = time.time()

allrows = []
check1, check2 = ' DOMESTIC GROSSES', 'Movie Title (click to view)'
for year in range(1980, 2017):
    yearrows = []
    for i in range(1,9):
        baseurl = 'http://www.boxofficemojo.com/yearly/chart/'
        midchunk = '&view=releasedate&view2=domestic&yr='
        suffix = '?page=' + str(i) + midchunk + str (year) + '&p=.htm'
       # time.sleep(1+1*random.random())
        response = requests.get(baseurl + suffix)
        page = response.text
        soup =  BeautifulSoup(page, 'lxml')
        if str(year) + check1 not in soup.text or check2 not in soup.text:
            break
        # this breaks two layers of loops instead of one, making this faster
        else:
            bigtable = soup.find('table', {'border' : '0', 'cellspacing' : '1', 'cellpadding' : '5'})
#            if bigtable is not None:
            headerrow = bigtable.find('tr', {'bgcolor' : '#dcdcdc'})
            headerthings = headerrow.findAll('a')
            columntitles = []
            for thing in headerthings:
                if len(thing.text) > 0:
                    columntitles.append(thing.text)
            closecheck = True
            if 'Close' not in columntitles:
                columntitles.extend(['Close'])
                closecheck = False
            columntitles.extend(['Year','Link','Foreign Gross', 'Budget',
                                 'Genre', 'Runtime', 'Rating',
                                 'All Time Worldwide', 'All Time Domestic',
                                 'Worldwide Yearly', 'Worldide Yearly in Rating',
                                 'Domestic Yearly in Rating'])
            if len(allrows) == 0:
                allrows.append(columntitles)
            #adding year later
            otherrows = bigtable.findAll('tr', {'bgcolor': ['#ffffff','#f4f4ff']})
            rows, movielinks = [], []
            for row in otherrows:
                if '<a href="/movies/?id=' in str(row):
                    cols = row.findAll('td')
                    coltext = []
                    for col in cols:
                        coltext.append(col.text)         
                        if '<a href="/movies/?id=' in str(col):
                            for link in col.find_all('a'):
                                movielink = 'http://www.boxofficemojo.com/' + link.get('href')
                    if closecheck == False:
                        coltext.extend([None])
                    coltext.extend([year, movielink])
#                    time.sleep(1+1*random.random())
                    coltext.extend(grabstuff(movielink))
                    rows.append(coltext)
            yearrows.extend(rows)
    allrows.extend(yearrows)
    csv_writer(allrows, 'movie_data_13527a.csv')
t1 = time.time()
dt1 = t1 - t0


#dt1 is 96 seconds for the lot

#this double counts but who cares
#its the sum of how many entries are not unique
def countdupes(mylistoflists):
    d = 0
    for i in range(len(mylistoflists)):
        others = [x for j,x in enumerate(mylistoflists) if j!=i]
        d = d + (mylistoflists[i] in others)
    return d
