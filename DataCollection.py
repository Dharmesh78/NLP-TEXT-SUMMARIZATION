
import requests
from nltk import sent_tokenize
from lxml import html
import bs4 as bs
import urllib.request
import re

scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text

print(article_text)
'''url = 'https://en.wikipedia.org/wiki/Pollution' # url to scrape data from
urlpath='/html/body/div[3]/div[3]/div[4]/div'



response = requests.get(url)
source_code = html.fromstring(response.content)# get filtered source code

element=source_code.xpath(urlpath)
print(element)
text=str(element[0].text_content())
text=" ".join(text.split())'''


#l=sent_tokenize(article_text)

testfile = open(r"testFile.txt","w+")
testfile.write(article_text)


testfile.close()

