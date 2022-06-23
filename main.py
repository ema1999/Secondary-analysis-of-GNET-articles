import requests
from bs4 import BeautifulSoup
import pickle
import pandas as pd
import spacy
from spacy import displacy

I_WANT_TO_WEBSCRAPE = False # set this to be true when you want to webscrape anew

if I_WANT_TO_WEBSCRAPE:
    def search(url, documentClass):
        # Returns a url
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        iList = soup.find_all(class_=documentClass)
        retObj = []
        for o in iList:
            retObj.append(o["href"])
        return retObj

    def search2(url, documentClass):
        # Returns a url
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    startUrl = 'https://gnet-research.org/resources/insights/'

# at the time of webscraping there were 10 pages of articles (if there are more at the time you are web scrapping, add a page and its url
    differentPages = ['https://gnet-research.org/resources/insights/', 'https://gnet-research.org/resources/insights/page/2/', 'https://gnet-research.org/resources/insights/page/3/', 'https://gnet-research.org/resources/insights/page/4/',
                  'https://gnet-research.org/resources/insights/page/5/', 'https://gnet-research.org/resources/insights/page/6/', 'https://gnet-research.org/resources/insights/page/7/',
                  'https://gnet-research.org/resources/insights/page/8/', 'https://gnet-research.org/resources/insights/page/9/', 'https://gnet-research.org/resources/insights/page/10/']

    urlsFromDifferentPages =[]  #function generates links to each article
    for i in differentPages:
        links = search(i,"link-to-post" )
        urlsFromDifferentPages.append(links)

    def removeRepeatedEntries(inList): # removal of any repeat entries
        return list(dict.fromkeys(inList))

    urlsFromDifferentPagesCorrected =[]

    for listo in urlsFromDifferentPages:
        undouble = removeRepeatedEntries(listo)
        urlsFromDifferentPagesCorrected.append(undouble)


    pageUrls = search(startUrl, "link-to-post")
    print ('this one', urlsFromDifferentPagesCorrected)
    print(pageUrls)
    pageUrls = removeRepeatedEntries(pageUrls)



    i = 0
    Faildump = 0
    for page in urlsFromDifferentPagesCorrected: #parsing the data to get article content (still with html tags, next section will clean it)
        i+=1
        articleContent = []
        textContent = []

        for link in page:
            oneContent = search2(link, "mailmunch-forms-before-post")
            articleContent.append(oneContent)

        for article in articleContent:
            try:
                content = article.findAll("p")
                s = str(content)
                textContent.append(s)
            except:
                print("A article has no p") # if there is no paragraphs in an entry
                Faildump+=1

        # Here we open a file to write the text content of the page to
        # we use pickle to save the data
        filename = 'textOfArticle'+str(i) #
        outfile = open(filename, 'wb')
        pickle.dump(textContent, outfile)
        outfile.close()
        print(filename+" written successfully")
        print("Number of bad articles: "+str(Faildump))


Cleaning_data = True # again set this to true if you want data to be cleaned (it's quite resource heavy)


def readPickleFile(file):
    #pickle_data=pd.read_pickle(file)
    infile = open(file, 'rb')
    pickle_data = pickle.load(infile)
    infile.close()
    return pickle_data


textContent1= readPickleFile('textOfArticle1')
textContent2= readPickleFile('textOfArticle2')
textContent3= readPickleFile('textOfArticle3')
textContent4= readPickleFile('textOfArticle4')
textContent5= readPickleFile('textOfArticle5')
textContent6= readPickleFile('textOfArticle6')
textContent7= readPickleFile('textOfArticle7')
textContent8= readPickleFile('textOfArticle8')
textContent9= readPickleFile('textOfArticle9')
textContent10= readPickleFile('textOfArticle10')




if Cleaning_data:

    def remove_tags(html): #removing html tags to get only text
        # parse html content
        soup = BeautifulSoup(html, "html.parser")

        for data in soup(['style', 'script']):
            # Remove tags
            data.decompose()

        # return data by retrieving the tag content
        return ' '.join(soup.stripped_strings)



    def filterhtmltags(content):
        newlist=[]
        for htmlcontent in content:
            newlist.append(remove_tags(htmlcontent))
        return newlist


    textContent1filtered = filterhtmltags(textContent1)
    textContent2filtered = filterhtmltags(textContent2)
    textContent3filtered = filterhtmltags(textContent3)
    textContent4filtered = filterhtmltags(textContent4)
    textContent5filtered = filterhtmltags(textContent5)
    textContent6filtered = filterhtmltags(textContent6)
    textContent7filtered = filterhtmltags(textContent7)
    textContent8filtered = filterhtmltags(textContent8)
    textContent9filtered = filterhtmltags(textContent9)
    textContent10filtered = filterhtmltags(textContent10)


nlp = spacy.load("en_core_web_sm") # SpaCy comes into play
organisationsList = []
productList = []
class wordStatistics:
    def __init__(self, word, label, count):
        self.word = word
        self.label = label
        self.count = count

    def __str__(self):
        return "Word: "+self.word + ", Label: "+ self.label

    def printFull(self):
        print("Word: "+self.word + ", Label: "+ self.label + ", Count: "+ str(self.count))

def getCategory(listToExtractFrom, categoryList, categoryString):
    for item in listToExtractFrom:
        itemFound = False
        if item.label == categoryString:
            for categoryItem in categoryList:
                if categoryItem.word == item.word:
                    itemFound = True
                    break
            if not itemFound:
                categoryList.append(item)

def getArticleWordStats(filteredArticleContent):
    listOfStructs = []
    listOfPopularWords = []  # Multiple occurrences
    for word in filteredArticleContent.ents:
        wordFound = False
        for x in listOfStructs:
            if x.word == word.text:
                wordFound = True
                x.count += 1
        if not wordFound:
            listOfStructs.append(wordStatistics(word.text, word.label_, 1))

    for y in listOfStructs:
        if y.count > 1:
            listOfPopularWords.append(y)
    # Here you can run getCategory(listOfPopularWord, <<<listForCategoryType>>>, <<<CategoryString>>>)
    # to get statistics about an additional category of data. Make sure you create the list
    # above where the organisationsList and productList are defined too
    getCategory(listOfPopularWords, organisationsList, "ORG") # here we select organisations (for identification of extremist organisations)
    getCategory(listOfPopularWords, productList, "PRODUCT")  # and product for tech platforms

    return listOfPopularWords

def getPageData(content):
    pageStats = []
    for article in content:
        processedArticle = nlp(article)
        statsFromArticle = getArticleWordStats(processedArticle)
        pageStats.append(statsFromArticle)
    return pageStats

page1Stats = getPageData(textContent1filtered)
page2Stats = getPageData(textContent2filtered)
page3Stats = getPageData(textContent3filtered)
page4Stats = getPageData(textContent4filtered)
page5Stats = getPageData(textContent5filtered)
page6Stats = getPageData(textContent6filtered)
page7Stats = getPageData(textContent7filtered)
page8Stats = getPageData(textContent8filtered)
page9Stats = getPageData(textContent9filtered)
page10Stats = getPageData(textContent10filtered)

# Page has articles. Articles has words with labels


#print("/---------------------------/")
#for item in organisationsList:
#    print(item)
#print("/---------------------------/")
#for item in productList:
#    print(item)

Organisations = ["QAnon", "The Oath Keepers", "the ‘Freedom Convoy’", "Islamic State", "the Anti-Technology Movement", "al-Qaeda",
"Patriot Front", "Bastión Frontal", "JI", "JAD", "GamerGate", "Zionist Occupied Government", "Vinland", "English Defence League",
"Operation Werewolf", "Liminal Order", "German Indianthusiasm", "the Azov Battalion", "New World Order", "Taliban", "Salafist",
"The Islamic State", "Deterrence Dispensed", "Salafi-jihadist", "Salafi-Jihadi", "the Boogaloo Boys", "TINPS", "ASWJ",
"the Atomwaffen Division", "Hezbollah", "Al Qaeda", "Siege Culture", "Satanic", "Naxal", "Moro", "WKKK", "Atomwaffen Division",
"the Turkestan Islamic Party", "National Front", "Al-Battar", "Patriotic Alternative’s", "AfD", "EDL", "pro-Islamic State",
"NiemalsaufKnien", "Hamas", "ISIS", "Nobody’s Listening", "The Green Brigade", "White Power", "the Boogaloo Bois", "National Action",
"AWD", "the Islamic State", "Querdenken", "Islamic State Central", "RSS", "Salafi-Jihadist", "the Information Bank", "PKK", "FARC",
"TRF", "AQAP", "Proud Boys", "Fatah", "MS-13", "Anonymous", "IB", "CFI", "TAK", "ISGS", "IQB", "ISI", "Pastel", "NAR", "AST", "Order",
"ZHC", "RIM", "PA’s", "ULF", "CHP", "the Haqqani Network", "Dabiq", "Incel","Ebaa News Agency","Nashir News Agency","Dabiq and Rumiyah"]

Platforms= ["Stormfront", "Twitter", "Facebook", "Geo News", "Instagram", "Telegram", "WhatsApp", "Reddit.com",
"TikTok", "YouTube",  "Love Frankie",  "Guardian", "Soundcloud", "Discord", "Netflix", "Neinchan’s",
"TOR", "Parler", "Twitch", "SoundCloud", "DLive", "Entropy", "Muslim News", "BitChute", "OkCupid", "Incels.co", "AFP", "NBC", "Gab’s",
"Minecraft",  "Yola", "archive.org", "The Epoch Times", "CrowdTangle", "LBC", "MeWe", "AT&T",
"the Rojava Information Center", "al-Furqan", "al-Furqan Media Foundation", "Google", "TamTam", "BBC Monitoring", "Voice of Hind",
"al Furqan", "RTLM", "AIC", "Blackberry", "BCM", "Istok", "Ritam", "the Jewish Chronicle", "Android", "Apple"]


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


#page1Dates= readPickleFile('dateOfArticle1')

def getArticleDate(articleIndex, pageNumber):
    p = readPickleFile("dateOfArticle"+str(pageNumber))
    return p[articleIndex]

def wordIsInList(word, list):
    inList = False
    for listWord in list:
        if word.lower() == listWord.lower():
            inList = True
    return inList

#Globally accessible list, do not move pls
groupingData = []   #Pages, 10 elements. Each element, is a list with one Class per article outlining the organisations and plaforms mentioned in that article as well as the date of that article

def getGroupingsToList(pageXStats, indexNumber):
    articleIndex = 0
    pageGroupings = []
    for articleStats in pageXStats:
        articleDate = getArticleDate(articleIndex, indexNumber)
        #First search the list of organisations then platforms
        orgsList = []
        platList = []

        for struct in articleStats:
            word = struct.word
            if wordIsInList(word, Organisations):
                orgsList.append(word)
            if wordIsInList(word, Platforms):
                platList.append(word)

        myClass = Class(articleDate, orgsList, platList)
        pageGroupings.append(myClass)
        articleIndex += 1

    groupingData.append(pageGroupings)

getGroupingsToList(page1Stats, 1)
getGroupingsToList(page2Stats, 2)
getGroupingsToList(page3Stats, 3)
getGroupingsToList(page4Stats, 4)
getGroupingsToList(page5Stats, 5)
getGroupingsToList(page6Stats, 6)
getGroupingsToList(page7Stats, 7)
getGroupingsToList(page8Stats, 8)
getGroupingsToList(page9Stats, 9)
getGroupingsToList(page10Stats, 10)

for page in groupingData:
    for article in page:
        print(article)

#For later analysis, pickle groupingData into a file

filename = 'DatawithDateOrgPlatform'
outfile = open(filename, 'wb')
pickle.dump(groupingData, outfile)
outfile.close()
print(filename + " written successfully")