import pandas as pd
import string
import csv

def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

unique_ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17', 'Unrated', 'X']
others = []
    

df = pd.read_csv('movie_data_13527_fixed.csv')
data = df.copy()

for entry in data.Rating:
    if entry not in unique_ratings: 
        others.append(entry)
others = list(set(others))
for i in range(len(unique_ratings)):
    data.Rating = data.Rating.replace(unique_ratings[i],i)
for other in others:
    data.Rating = data.Rating.replace(other,len(unique_ratings))


translator = str.maketrans({key: None for key in string.punctuation})
genres = data.Genre.values.tolist()
allgenres, genreslist = set([]), []
for genre in genres:
    if type(genre) == str:
        subgenres = genre.lower().translate(translator).split()
        allgenres.update(set(subgenres))
        genreslist.append(subgenres)
    else:
        genreslist.append([None])
allgenres.remove('unknown')
genreuniques = list(allgenres)

genrebinaries = []
for subgenres in genreslist:
    genrebinary = []
    for genre in genreuniques:
        genrebinary.append((genre in subgenres) + 0)
    genrebinaries.append(genrebinary)
    
datalist = data.values.tolist()
bigvals = []
for i in range(len(datalist)):
    a = datalist[i]
    a.extend(genrebinaries[i])
    bigvals.append(a)
    
cpi = {1980 : 77.8, 1981 : 87.0, 1982 : 94.3, 1983 : 97.8, 1984 : 101.9, 1985 : 105.5, 1986 : 109.6, 1987 : 111.2, 1988 : 115.7, 1989 : 121.1, 1990 : 127.4, 1991 : 134.6, 1992 : 138.1, 1993 : 142.6, 1994 : 146.2, 1995 : 150.3, 1996 : 154.4, 1997 : 159.1, 1998 : 161.6, 1999 : 164.3, 2000 : 168.8, 2001 : 175.1, 2002 : 177.1, 2003 : 181.7, 2004 : 185.2, 2005 : 190.7, 2006 : 198.3, 2007 : 202.4, 2008 : 211.1, 2009 : 211.143, 2010 : 216.687, 2011 : 220.223, 2012 : 226.655, 2013 : 230.280, 2014 : 233.916, 2015 : 233.707, 2016 : 236.916}

bigvals2 = []
for row in bigvals:
    row1 = row[:]
    inf = cpi[2016]/cpi[row1[9]]
    if type(row1[3]) == str:
        row1[3] = round(int(row1[3].replace('$','').replace(',',''))*inf,2)
    if type(row1[5]) == str:
        row1[5] = round(int(row1[5].replace('$','').replace(',',''))*inf,2)
    row1[11] = round(row1[11]*inf,2)
    row1[12] = round(row1[12]*inf,2)
    bigvals2.append(row1)
    
    

titles = data.columns.values.tolist()
titles[2] = 'Movie Title'
titles[3] = 'Domestic Gross (2016 dollars)'
titles[11] = 'International Gross (2016 dollars)'
titles[12] = 'Budget (2016 dollars)'
titles.extend(genreuniques)

wholething = [titles]
wholething.extend(bigvals2)

csv_writer(wholething, 'movie_data_13527_fixed_binaries_inflation_adjusted.csv')



goodframe = pd.read_csv('movie_data_13527_fixed_binaries_inflation_adjusted.csv')
