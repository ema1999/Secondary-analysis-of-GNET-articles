import requests
from bs4 import BeautifulSoup
import pickle
import pandas as pd
import spacy
from spacy import displacy
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class Class:
    def __init__(self, articleDate, listOfOrgsMentioned, listOfPlatformsMentioned):
        self.articleDate = articleDate
        self.listOfOrgsMentioned = listOfOrgsMentioned
        self.listOfPlatformsMentioned = listOfPlatformsMentioned

    def __str__(self):
        orgsString = ", ".join(self.listOfOrgsMentioned)
        platString = ", ".join(self.listOfPlatformsMentioned)
        return "Article Date: "+ self.articleDate + "\nOrganisations Mentioned: "+ orgsString + \
        "\nPlatforms Mentions: " + platString + "\n------------------------------"

def readPickleFile(file):
    #pickle_data=pd.read_pickle(file)
    infile = open(file, 'rb')
    pickle_data = pickle.load(infile)
    infile.close()
    return pickle_data

data= readPickleFile('DatawithDateOrgPlatform')
newdata=[]
for page in data: # mentions of same organisations under different names get merged here
    for article in page:
        for org in article.listOfOrgsMentioned:
            index = article.listOfOrgsMentioned.index(org)
            if org == "Salafi-jihadist":
                article.listOfOrgsMentioned[index] = "Salafi-Jihadist"
            elif org == "Salafi-Jihadi":
                article.listOfOrgsMentioned[index] = "Salafi-Jihadist"
            elif org == "PA’s":
                article.listOfOrgsMentioned[index] = "Patriotic Alternative’s"
            elif org == "Al Qaeda":
                article.listOfOrgsMentioned[index] = "al-Qaeda"
            elif org == "Al-Qaeda":
                article.listOfOrgsMentioned[index] = "al-Qaeda"
            elif org == "The Islamic State":
                article.listOfOrgsMentioned[index] = "Islamic State"
            elif org == "the Islamic State":
                article.listOfOrgsMentioned[index] = "Islamic State"
            elif org == "Islamic State Central":
                article.listOfOrgsMentioned[index] = "Islamic State"
            elif org == "ISIS":
                article.listOfOrgsMentioned[index] = "Islamic State"
            elif org == "the Atomwaffen Division":
                article.listOfOrgsMentioned[index] ="Atomwaffen Division"
            elif org == "The Atomwaffen Division":
                article.listOfOrgsMentioned[index] ="Atomwaffen Division"
            elif org == "AfD":
                article.listOfOrgsMentioned[index] ="Atomwaffen Division"
            elif org == "the Boogaloo Bois":
                article.listOfOrgsMentioned[index] ="the Boogaloo Boys"
            elif org == "Dabiq":
                article.listOfOrgsMentioned[index] ="Dabiq and Rumiyah"
        for plat in article.listOfPlatformsMentioned:
            index = article.listOfPlatformsMentioned.index(plat)
            if plat == "Soundcloud":
                article.listOfPlatformsMentioned[index] ="SoundCloud"
            if plat == "Whatsapp":
                article.listOfPlatformsMentioned[index] ="WhatsApp"



allorgs=[]
for page in data:
    for article in page:
        if len(article.listOfOrgsMentioned) > 0:
            allorgs.append(article.listOfOrgsMentioned[0])
        elif len(article.listOfOrgsMentioned) > 1:
            allorgs.append(article.listOfOrgsMentioned[1])
        elif len(article.listOfOrgsMentioned) > 2:
            allorgs.append(article.listOfOrgsMentioned[2])

allplats=[]
for page in data:
    for article in page:
        if len(article.listOfPlatformsMentioned) > 0:
            allplats.append(article.listOfPlatformsMentioned[0])
        elif len(article.listOfPlatformsMentioned) > 1:
            allplats.append(article.listOfPlatformsMentioned[1])
        elif len(article.listOfPlatformsMentioned) > 2:
            allplats.append(article.listOfPlatformsMentioned[2])


corgs = Counter(allorgs)
cplats = Counter(allplats)

print(corgs.most_common())
print(cplats.most_common())
print("----------------------------")

counter =0
for page in data:
    for article in page:
        if len(article.listOfOrgsMentioned) > 0 or len(article.listOfPlatformsMentioned) > 0:
            counter += 1


print("this analysis is done on " ,counter , " articles")

#------------------------------------------------------------------------------------------------------------------------------

#delete the duplicates
def removeRepeatedEntries(inList):
    return list(dict.fromkeys(inList))


alldates=[]

for page in data:
    for article in page:
            alldates.append(article.articleDate)


AllDates=[]
for i in alldates:
    AllDates.append(i[3:])


print('this one', len([('Telegram', 48), ('Twitter', 45), ('Facebook', 17), ('YouTube', 12), ('Instagram', 6), ('Stormfront', 5), ('Discord', 3), ('TikTok', 3), ('al-Furqan Media Foundation', 3), ('WhatsApp', 2), ('Netflix', 2), ('Parler', 2), ('Google', 2), ('Muslim News', 2), ('the Jewish Chronicle', 1), ('Love Frankie', 1), ('Reddit.com', 1), ('Neinchan’s', 1), ('Guardian', 1), ('Twitch', 1), ('OkCupid', 1), ('AFP', 1), ('NBC', 1), ('AIC', 1), ('AT&T', 1), ('al Furqan', 1), ('RTLM', 1), ('Istok', 1), ('archive.org', 1), ('BBC Monitoring', 1), ('Blackberry', 1), ('Voice of Hind', 1)]))
Plotmaking = False

print(Counter(AllDates).most_common())
DatesThroughTime = ['12/2019', 7,'01/2020', 4, '02/2020', 9,'03/2020', 9, '04/2020', 14, '05/2020', 11, '06/2020', 13,
                    '07/2020', 16, '08/2020', 16,'09/2020', 17,'10/2020', 16, '11/2020', 14, '12/2020', 12, '01/2021', 21,
                    '02/2021', 12, '03/2021', 21,'04/2021', 13,'05/2021', 12,  '06/2021', 16, '07/2021', 10,'08/2021', 14,
                    '09/2021', 14,'10/2021', 8, '11/2021', 9,'12/2021', 4, '01/2022', 10,'02/2022', 8, '03/2022', 7,  '04/2022', 6]

Dates=DatesThroughTime[::2]
DatesCount=DatesThroughTime[1::2]

print('dates', Dates)
print('count', DatesCount)


Telegram =['04/2022', '04/2022', '04/2022', '03/2022', '03/2022', '02/2022', '02/2022', '01/2022', '01/2022', '12/2021',
'11/2021', '11/2021', '11/2021', '10/2021', '10/2021', '09/2021', '09/2021', '08/2021', '08/2021', '08/2021', '07/2021',
'06/2021', '05/2021', '05/2021', '05/2021', '03/2021', '03/2021', '03/2021', '03/2021', '03/2021', '03/2021', '02/2021',
           '02/2021', '02/2021', '02/2021', '02/2021', '02/2021', '02/2021', '01/2021', '01/2021', '01/2021', '01/2021',
           '01/2021', '01/2021', '12/2020', '11/2020', '10/2020', '10/2020', '10/2020', '09/2020', '09/2020', '08/2020',
'08/2020', '08/2020', '07/2020', '06/2020', '06/2020', '06/2020', '06/2020', '05/2020', '05/2020', '05/2020', '05/2020',
'04/2020', '04/2020', '03/2020', '02/2020', '12/2019']

Twitter =['04/2022', '04/2022', '01/2022', '01/2022', '12/2021', '11/2021', '11/2021', '10/2021', '10/2021', '08/2021',
'08/2021', '08/2021', '07/2021', '07/2021', '06/2021', '06/2021', '06/2021', '06/2021', '05/2021', '05/2021', '04/2021',
'04/2021', '04/2021', '03/2021', '03/2021', '03/2021', '02/2021', '02/2021', '02/2021', '02/2021', '01/2021', '01/2021',
          '01/2021', '01/2021', '01/2021', '12/2020', '12/2020', '12/2020', '12/2020', '11/2020', '11/2020', '11/2020',
'10/2020', '10/2020', '10/2020', '10/2020', '10/2020', '09/2020', '09/2020', '08/2020', '08/2020', '07/2020', '07/2020',
'07/2020', '07/2020', '06/2020', '06/2020', '05/2020', '04/2020', '04/2020', '04/2020', '03/2020', '03/2020', '02/2020', '12/2019']

Facebook =['03/2022', '02/2022', '01/2022', '11/2021', '11/2021', '10/2021', '10/2021', '08/2021', '07/2021', '06/2021',
'06/2021', '06/2021', '04/2021', '03/2021', '03/2021', '03/2021', '03/2021', '02/2021', '02/2021', '01/2021', '12/2020',
'12/2020', '11/2020', '10/2020', '09/2020', '08/2020', '07/2020', '07/2020', '07/2020', '06/2020', '05/2020', '05/2020', '05/2020',
           '04/2020', '02/2020', '02/2020', '12/2019']


Facebook.reverse()
Twitter.reverse()
Telegram.reverse()


telegram = ['12/2019', 1,  '01/2020', 0,  '02/2020', 1, '03/2020', 1,  '04/2020', 2,'05/2020', 4, '06/2020', 4, '07/2020', 1, '08/2020', 3, '09/2020', 2, '10/2020', 3, '11/2020', 1, '12/2020', 1, '01/2021', 6, '02/2021', 7, '03/2021', 6, '05/2021', 3, '06/2021', 1, '07/2021', 1,
'08/2021', 3, '09/2021', 2, '10/2021', 2, '11/2021', 3, '12/2021', 1, '01/2022', 2, '02/2022', 2, '03/2022', 2, '04/2022', 3]


twitter = ['12/2019', 1, '01/2020', 0, '02/2020', 1, '03/2020', 2, '04/2020', 3, '05/2020', 1, '06/2020', 2,  '07/2020', 4, '08/2020', 2, '09/2020', 2, '10/2020', 5, '11/2020', 3,  '12/2020', 4,
'01/2021', 5, '02/2021', 4, '03/2021', 3, '04/2021', 3, '05/2021', 2, '06/2021', 4, '07/2021', 2, '08/2021', 3, '09/2021', 0, '10/2021', 2, '11/2021', 2, '12/2021', 1, '01/2022', 2, '02/2022', 0, '03/2022', 0, '04/2022', 2]

facebook = ['12/2019', 1, '01/2020', 0, '02/2020', 2,  '03/2020', 0, '04/2020', 1, '05/2020', 3, '06/2020', 1, '07/2020', 3, '08/2020', 1, '09/2020', 1, '10/2020', 1, '11/2020', 1, '12/2020', 2, '01/2021', 1, '02/2021', 2, '03/2021', 4, '04/2021', 1, '05/2021', 0, '06/2021', 3, '07/2021', 1, '08/2021', 1, '09/2021', 0, '10/2021', 2, '11/2021', 2, '12/2021', 0, '01/2022', 1, '02/2022', 1, '03/2022', 1, '04/2022', 0]

Dates=telegram[::2]
telegramcount=telegram[1::2]
twittercount = twitter[1::2]
facebookcount=facebook[1::2]



QAnonThroughTime = []
for page in data:
    for article in page:
        for org in article.listOfOrgsMentioned:
            if org == 'al-Qaeda':
                QAnonThroughTime.append(article.articleDate)

print(len(QAnonThroughTime))
print(QAnonThroughTime)
alqaeda=[]
for i in QAnonThroughTime:
    alqaeda.append(i[3:])

print(Counter(alqaeda).most_common())

Alqaeda= ['12/2019', 0, '01/2020', 0, '02/2020', 0, '03/2020', 0, '04/2020', 2, '05/2020', 0, '06/2020', 3, '07/2020', 1, '08/2020', 3, '09/2020', 0, '10/2020', 3, '11/2020', 1, '12/2020', 0, '01/2021', 1, '02/2021', 0, '03/2021', 0, '04/2021', 0, '05/2021', 3, '06/2021', 1, '07/2021', 0, '08/2021', 1, '09/2021', 0, '10/2021', 0, '11/2021', 0, '12/2021', 0, '01/2022', 0, '02/2022', 0, '03/2022', 0, '04/2022', 0]

alqaedacount=Alqaeda[1::2]
print(alqaedacount)

if Plotmaking:

    QAnonThroughTime = []
    for page in data:
        for article in page:
            for org in article.listOfOrgsMentioned:
                if org == "QAnon":
                    QAnonThroughTime.append(article.listOfPlatformsMentioned)
                    QAnonThroughTime.append(article.articleDate)

    print(len(QAnonThroughTime))
    print(QAnonThroughTime)

    QAnonDates = []
    for i in QAnonThroughTime:
        QAnonDates.append(i[3:])

    print(Counter(QAnonDates).most_common())
    qanondates=['12/2019', 0,'01/2020', 0,'02/2020', 0,'03/2020', 0,'04/2020', 0,'05/2020', 0,'06/2020', 1,
                '07/2020', 2,'08/2020', 0,'09/2020', 1, '10/2020', 1,  '11/2020', 1,'12/2020', 1, '01/2021', 5,
                '02/2021', 2,'03/2021', 4,'04/2021', 2, '05/2021', 0, '06/2021', 4, '07/2021', 1, '08/2021', 1,
                '09/2021', 0,'10/2021', 2,'11/2021', 0, '12/2021', 0,'01/2022', 1,'02/2022', 1,'03/2022', 1,'04/2022', 1]

    DatesThroughTime = ['12/2019', 7, '01/2020', 4, '02/2020', 9, '03/2020', 9, '04/2020', 14, '05/2020', 11, '06/2020',
                        13, '07/2020', 16, '08/2020', 16, '09/2020', 17, '10/2020', 16, '11/2020', 14, '12/2020', 12,
                        '01/2021', 21,
                        '02/2021', 12, '03/2021', 21, '04/2021', 13, '05/2021', 12, '06/2021', 16, '07/2021', 10,
                        '08/2021', 14,
                        '09/2021', 14, '10/2021', 8, '11/2021', 9, '12/2021', 4, '01/2022', 10, '02/2022', 8, '03/2022',
                        7, '04/2022', 6]
    islamicdate=['12/2019', 1, '01/2020', 1, '02/2020', 2, '03/2020', 5, '04/2020', 1, '05/2020', 1, '06/2020', 1,
    '07/2020', 1,'08/2020', 7, '09/2020', 3, '10/2020', 5, '11/2020', 1, '12/2020', 0, '01/2021', 1,
    '02/2021', 1, '03/2021', 1, '04/2021', 1, '05/2021', 1, '06/2021', 1, '07/2021', 0, '08/2021', 2,
    '09/2021', 1, '10/2021', 1, '11/2021', 1, '12/2021', 0, '01/2022', 0, '02/2022', 1, '03/2022', 1,'04/2022', 0]

    print(qanondates)
    QAnonDates=qanondates[::2]
    QAnonDatesCount=qanondates[1::2]
    IslamicDates = islamicdate[::2]
    IslamicDatesCount = islamicdate[1::2]

    print('dates', QAnonDates)
    print('count', QAnonDatesCount)
    print('dates', IslamicDates)
    print('count', IslamicDatesCount)


   