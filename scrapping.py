import urllib.request as rq
import ssl
from bs4 import BeautifulSoup
import csv


word = input('enter a word: ')
ssl._create_default_https_context = ssl._create_unverified_context
request = rq.Request('http://dictionary.cambridge.org/dictionary/english-chinese-traditional/'+word)
response = rq.urlopen(request)
html_doc =  response.read()
soup = BeautifulSoup(html_doc, 'html.parser')

hw = []
pos = []
dataSrc = []
ipas = []

trans = []
egs = []

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    phrases = soup.find_all('div', class_ = 'phrase-block pad-indent')
    for phrase in phrases:
        hw = phrase.find('span', class_ = 'phrase')
        hw = hw.get_text()
        pos = 'phrase'
        for df in phrase.find_all('div', class_ = 'def-block pad-indent'):
            for peg in df.find_all('span', class_ = 'eg'):
                egs.extend([peg.get_text()])

            for ex in df.find_all('div', class_ = 'examp emphasized'):
                ex.clear()

            for tran in df.find_all('span', class_ = 'trans'):
                trans.extend([tran.get_text()])

#           print(hw)
#           print(pos)
#           print(trans)
#           print(egs)
#           print('----------------------------')

            trans = '<br>'.join(trans)
            egs = '<br>'.join(egs)

            writer.writerow([hw, pos, None, trans, egs])

            egs = []
            trans = []
            phrase.clear()

    entries = soup.find_all('div', class_ = 'entry-body__el clrd js-share-holder')
    for entry in entries:
        hw = entry.find('span', class_ = 'hw').string
        pos = entry.find('span', class_ = 'pos').string
        for df in entry.find_all('div', class_ = 'def-block pad-indent'):
            for ipa in entry.find_all('span', class_ = 'ipa'):
                ipas.extend(['/'+ipa.get_text()+'/'])

            for eg in df.find_all('span', class_ = 'eg'):
                egs.extend([eg.get_text()])

            for ex in df.find_all('div', class_ = 'examp emphasized'):
                ex.clear()

            for tran in df.find_all('span', class_ = 'trans'):
                trans.extend([tran.get_text()])
                
            ipas = '<br>'.join(ipas)
            trans = '<br>'.join(trans)
            egs = '<br>'.join(egs)

            if trans == []:
                break
            else:
#               print(hw)
#               print(pos)
#               print(ipas)
#               print(trans)
#               print(egs)
#               print('----------------------------')

                writer.writerow([hw, pos, ipas, trans, egs])
            
                ipas = []
                trans = []
                egs = [] 
