import glob, time, csv
t0 = time.time()

#path = '/Users/derekupdegraff/Metis_Class/Fletcher_Scraping/'
path = '/home/ubuntu/Fletcher_Scraping/'

length_thresh = 100000
margin_len = 10000
step_size = 7000
good_size = 5000

def sentencecrop(mytext):
    start = mytext.find('.') + 1
    end = mytext.rfind('.') + 1
    return mytext[start:end].strip()

def isgood(mytext):
    # comment first line her out if troublesome
    badlist = ['\x80', '\x94', '»', '«', '*', 'Â', '¢', '$', '^']
   # badlist = ['»', '«', '*', 'Â', '¢', '$', '^']
    ctr = 1
    for entry in badlist:
        ctr = ctr * (entry not in mytext)
    return bool(ctr)
    
def getparas(mytext, threshold = 200):
    good = ''
    mylist = mytext.split('\n\n')
    for entry in mylist:
        if len(entry) > threshold:
            if isgood(entry):
                good = good + entry + '\n\n'
    good = good.replace('\n',' ')
    good = good.replace('-  ', '')
    good = good.replace('- ', '')
    return good

def generategood(mytext):
    good_text = ''
    bounds = []
    num_steps = int((len(mytext) - 2 * margin_len)/step_size) - 1
    for i in range(num_steps):
        start = margin_len + step_size * i
        end = start + step_size
        good_text = good_text + getparas(sentencecrop(mytext[start:end]))
        bounds.append([start,end])
        if len(good_text) > good_size:
            break
    if len(good_text) > good_size:
        return good_text

bigtable = []
message = ''
total_counter = 0
years = list(range(1910, 1911))
for year in years:
    century = str(int(year/100) + 1)
    year_counter = 0
    filenames_year = glob.glob(path + str(year) + '/document_*.txt')
    for filename in filenames_year:
        with open(filename) as myfile:
            text = myfile.read()
            if len(text) > length_thresh:
                goodtext = generategood(text)
                if goodtext:
                    bigtable.append([century, goodtext])
                    year_counter = year_counter + 1
                    total_counter = total_counter + 1
    message = message + str(year) + ': ' + str(year_counter) + ' documents grabbed.\n'

t1 = time.time()
dt1 = t1 - t0

message = message + '\nGrabbed ' + str(total_counter) + ' documents from ' + str(min(years)) + ' to ' + str(max(years))
message = message + '\n\nProgram took ' + str(dt1) + ' seconds'

with open (path + '/collection_report.txt', 'w') as reportfile:
    reportfile.write(message)
    
#with open(path + '/collected_text.csv', "wb") as f:
#    writer = csv.writer(f)
#    writer.writerows(bigtable)
with open(path + '/collected_text.csv', "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(bigtable)

    
            