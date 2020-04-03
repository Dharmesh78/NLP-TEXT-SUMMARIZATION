import re

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import pandas as pd


'''DEFINING REEGULAR EXPRESSION FOR IDENTIFYING VARIOUS IRRELAVANT PATTERN IN THE SCRAPPED TEXT'''



date=r"([0-2][0-9][\/\.][0-1][0-9][\/\.]\d{4}|3[01][\/\.][0-1][0-9][\/\.]\d{4})|(\d{4}-[0-1][0-9]-[0-2][0-9]|\d{4}-[" \
     r"0-1][0-9]-3[01])|([a-zA-z]{3,9}\s?[0-2][0-9]\,\s?\d{4}|[a-zA-z]{3,9}\s?3[01]\,\s?\d{4}|[0-2][0-9]\s[a-zA-z]{3," \
     r"9}\,?\s?\d{4}|3[01]\s[a-zA-z]{3,9}\,?\s?\d{4}) "

date2=r"(January|February|March|April|May|June|July|August|September|October|November|December)(\s?)([0-2]?[0-9]|[3][0-1])(\,)?(\s?)(\d{4})"
date3=r"([0-2]?[0-9]|[3][0-1])(\,)?(\s?)(January|February|March|April|May|June|July|August|September|October|November|December)(\s?)(\d{4})"

email=r"[a-z0-9\.]+\@[a-z]+\.[a-z]+\.[a-z]+|[a-z0-9\.]+\@[a-z]+\.[a-z]+"

url=r"www\.\w+\.\D+|https:\/\/www\.\w+\.\w{3}^\w"

hashtag=r"\#\w+"


#referencelin=r'(\[)\d+(\])'
regex = r'[^a-zA-Z0-9\s]'

'''READING THE CSV FILE AND TRANFORMING IT TO DICTIONARY'''

df=pd.read_csv("abbreviationData.csv")

mydict=dict(zip(df.Column1,df.Column2))
mydict['U.S.A.']="United States of America"




def preprocess(para):
    text = re.sub(date, '', para)

    text = re.sub(date2, '', text)
    text = re.sub(date3, '', text)
    text = re.sub(email, '', text)
    text = re.sub(url, '', text)
    text = re.sub(hashtag, '', text)
    text = re.sub(r'\^', '', text)

    sentences = sent_tokenize(text)
    text2 = ""
    #print(sentences)
    for sentence in sentences:
        sent = []
        words = word_tokenize(sentence)
        #print(words)
        for word in words:
            '''ABBREVIATION EXPANSION'''
            if word in mydict:
                word=mydict[word+'.']

            sent.append(word.lower())

        sent=' '.join(sent)
        sent = re.sub(regex, ' ', sent)
        sent=sent.strip()+". "
        text2+= sent
    text2=re.sub(r'\s{2,3}',' ',text2)

    return text2





with open("GlobalWarming", "r") as input:
    '''REMOVAL OF REFERENCE LINKS like [24]'''
    Inptext = re.sub(r"(\[)\d+(\])", '', input.read())
    para_list= Inptext.split("\n")

preprocessed_text=""



for para in para_list:
    preprocessed_para=preprocess(para)
    preprocessed_text+=preprocessed_para
    preprocessed_text+='\n'

'''WRITING THE PREPROCESSED TEXT INTO A FILE FOR CALCULATION OF TF IDF SCORE'''
FileObj2 = open(r"GWPreprocessed.txt","w+")
FileObj2.write(preprocessed_text)

FileObj2.close()