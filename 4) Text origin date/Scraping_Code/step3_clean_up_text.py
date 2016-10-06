import glob, time, datetime
from bs4 import BeautifulSoup

t0 = time.time()

def cleanup(mytext):
    soup = BeautifulSoup(mytext,'lxml')
    return str(soup.text)

path = '/Users/derekupdegraff/Metis_Class/Fletcher_Scraping/'
#path = '/home/ubuntu/Fletcher_Scraping'

grand_total, grand_diff = 0, 0
mess = ''
years = list(range(1994, 1995))
for year in years:
    diff = 0
    filenames_year = glob.glob(path + str(year) + '/document_*.txt')
    good_ones = []
    for filename in filenames_year:
        with open(filename) as myfile:
            text = myfile.read()
            prettytext = cleanup(text)
            diff = diff + (text != prettytext)
#            outname = filename[:-4] + 'BS.txt'
#            outname = outname.replace('document_', 'document')
            outname = filename
            with open(outname, 'w') as textfile:
                textfile.write(prettytext)
    grand_diff, grand_total = grand_diff + diff, grand_total + len(filenames_year)
    chngd = str(diff) + ' out of ' + str(len(filenames_year)) + ' changed.\n'
    mess = mess + str(year) + ':   ' + chngd

t1 = time.time()
dt1 = t1-t0

timestr = datetime.datetime.now().strftime("%m-%d__%I-%M%p")
outpath = path + 'prettification_report' + timestr + '.txt'
total = '\n\n' + str(grand_diff) + ' out of ' + str(grand_total) + ' changed overall.'
mess = mess + total + '\n\nOperation took ' + str(round(dt1)) + ' seconds.'

with open (outpath, 'w') as reportfile:
    reportfile.write(mess)