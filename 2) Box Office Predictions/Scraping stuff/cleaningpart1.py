# This deals with the fact that there were tables with and without a closing date

import pandas as pd
import csv

def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

# 'Close' starts in 2002

dfbig = pd.read_csv('movie_data_13527.csv')
titles = dfbig.columns.values.tolist()
values = dfbig.values.tolist()

valuesfixed = []
for value in values:
    val1 = value[:]
    if 'boxofficemojo' in str(value[9]):
        val1 = value[:8]
        val1.append(None)
        val1.extend(value[8:])
        val1.pop(-1)
    val1.pop(-1)
    valuesfixed.append(val1)
titles.pop(-1)    
#removes values from both cause "rated _" thing wasn't stable
outlist = [titles[:]]
outlist.extend(valuesfixed)    

csv_writer(outlist, 'movie_data_13527_fixed.csv')

c1, c2, c3 = 0, 0, 0
for entry in outlist:
    if entry[8] == 'Close':
        c1 = c1 + 1
    elif entry[8] == None:
        c2 = c2 + 1
    elif 'boxofficemojo' in entry[10]:
        c3 = c3 + 1
a = len(outlist) == (c1+c2+c3)
print(a)

dfbig_fixed = pd.read_csv('movie_data_13527_fixed.csv')

print(outlist[0])
print(outlist[1])
