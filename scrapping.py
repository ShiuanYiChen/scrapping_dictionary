import urllib.request as rq
import ssl
from bs4 import BeautifulSoup
import csv

word = 'back'
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

phrases = soup.find_all('div', class_ = 'phrase-block pad-indent')
for phrase in phrases:
    hw = phrase.find('span', class_ = 'phrase')
    hw = hw.get_text()
    pos = 'phrase'
    pegs = phrase.find_all('span', class_ = 'eg')
    for peg in pegs:
        egs.extend([peg.get_text()])

    for ex in phrase.find_all('div', class_ = 'examp emphasized'):
        ex.clear()

    for tran in phrase.find_all('span', class_ = 'trans'):
        trans.extend([tran.get_text()])

    print(hw)
    print(pos)
    print(trans)
    print(egs)
    print('----------------------------')

    egs.clear()
    trans.clear()
    phrase.clear()

entries = soup.find_all('div', class_ = 'entry-body__el clrd js-share-holder')
for entry in entries:
    hw = entry.find('span', class_ = 'hw').string
    pos = entry.find('span', class_ = 'pos').string
    pron = entry.find_all('span', class_ = 'ipa')
    for ipa in pron:
        ipas.extend([ipa.get_text()])

    ee = entry.find_all('span', class_ = 'eg')
    for eg in ee:
        egs.extend([eg.get_text()])

    for ex in entry.find_all('div', class_ = 'examp emphasized'):
        ex.clear()

    for tran in entry.find_all('span', class_ = 'trans'):
        trans.extend([tran.get_text()])
        
    if trans == []:
        break
    else:
        print(hw)
        print(pos)
        print(ipas)
        print(trans)
        print(egs)
        print('----------------------------')

        ipas.clear()
        trans.clear()
        egs.clear()    


"""
entry-body
    entry-body__el clrd js-share-holder ＝*多詞性
        pos-header
            h3 di-title cdo-section-title-hw
                headword
                    hw ＝英文
                posgram ico-bg
                    pos ＝詞性
            pron-info
                us
                    data-src ＝音檔
                us
                    pron
                        ipa ＝/音標/
        pos-body
            sense-block ＝*多義
                sense-body
                    def-block pad-indent
                        def-body
                            trans ＝字義
                            examp emphasized
                                eg ＝例句
                    phrase-block pad-indent ＝*如果有片語
                        phrase-head
                            phrase-title
                                phrase ＝片語
                                    obj
                        phrase-body pad-indent
                            def-block pad-indent
                                def-body
                                    trans ＝字義
                                    examp emphasized
                                        eg ＝例句
                                        import requests
----------------------
英文 詞性

音標
字義
例句
"""