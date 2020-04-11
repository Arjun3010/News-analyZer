import requests 
from bs4 import BeautifulSoup
from newspaper import Article
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA
import matplotlib.pyplot as plt
import numpy as np

def getNews(val):
    
    url = 'https://news.google.com/search?for=' + val +'+news&hl=en-IN&gl=IN&ceid=IN:en'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    
    i = 0
    
    fig = plt.figure()

    for link in soup.findAll('div',class_='NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc'):
        if i == 3:
            break
        i = i + 1
        a = str(link.find('a')['href'])
        a = a.replace('.','https://news.google.com')
        getFromGoogle(a,i,fig)
    
    plt.tight_layout()
    plt.show()

def getFromGoogle(a,m,fig):
    
    try:

        k = Article(a)
        k.download()
        k.parse()
        
        u = 'https://www.google.com/search?client=firefox-b-d&q=' + k.title
        r = requests.get(u)
        soup = BeautifulSoup(r.content, 'html5lib') 
        
        i = 0
        z = []
        p = []
        
        for link in soup.findAll('div',class_='ZINbbc xpd O9g5cc uUPGi'):
            if i == 5:
                break
            i = i + 1
            b = str(link.find('a')['href'])
            b = b.replace('/url?q=','https://www.google.com/url?q=')
            v,s = searchHeadlines(b)
            
            if v not in z and v != '':
                z.append(v)
                p.append(s)
        
        
        x = np.asarray(z)
        y = np.asarray(p)
        
        print(x,y)
        
        mask1 = y < -0.5
        mask2 = y > 0.5        
        mask3 = (y >= -0.5) & (y <= 0.5)
        
        plt.subplot(3,1,m)
        plt.barh(x[mask1],y[mask1],color = 'red')
        plt.barh(x[mask3],y[mask3],color = 'grey')
        plt.barh(x[mask2],y[mask2],color = 'green')
        
        plt.xlim(-1,1)
        plt.title(k.title,fontfamily = 'Cooper Black',fontsize = 'x-large',wrap = True)
        
    except:
        print('error')

def searchHeadlines(a1):
    
    t = Article(a1)
    
    try:

        t.download()
        t.parse()
        t.nlp()
        
        s1 = SIA()        
        ps = s1.polarity_scores(t.summary)
        
        a1 = a1.replace('https://www.google.com/url?q=https://','')

        while(a1.find('https://') != -1):
            a1 = a1.replace('https://','')
        while(a1.find('www') != -1):
            a1 = a1.replace('www','')

        d = a1.split('.')
        
        if(d[0] == 'www' or d[0] == ''):
            n = 1
        else:
            n = 0
        
        string = ''
        
        if(len(d[n]) > 1):
            string = d[n]
        
        n = n + 1
        
        while('co' not in d[n] and 'com' not in d[n] and 'in' not in d[n]):
            if len(d[n]) > 2 and '%' not in d[n]:
                string = string + ' ' + d[n]
            n = n + 1
        return string,ps['compound']

    except:
        
        return '',0