from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords
import math


testfile = open(r"Preprocessed2.txt","r")
inputText=testfile.read()
sentences=sent_tokenize(inputText)

#print(len(sentences[0]))
#print(len(sentences))
'''STOPWORDS REMOVAL'''
stopwordsL = set(stopwords.words('english'))

def frequency_matrix(sentences):
    "Here, each sentence is the key and the value is a dictionary of word frequency."""
    freq_mat={}
    ps=PorterStemmer()
    for sent in sentences:
        freq_table = {}
        words = word_tokenize(sent)
        for word in words:
            word = ps.stem(word)

            if word.lower() in stopwordsL:
                continue
            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        freq_mat[sent[:20]] = freq_table

    return freq_mat

def tf_matrix(freq_matrix):
    "TF(t) = (Number of times term t appears in a paragraph) / (Total number of terms in the paragraph)"""
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sent = len(f_table)
        #print(count_words_in_para)
        for word, count in f_table.items():
            tf_table[word] = round(count / count_words_in_sent,11)

        tf_matrix[sent] = tf_table

    return tf_matrix




def word_per_document(freq_mat):
    word_per_doc_table = {}
    '''“how many paragraphs in the document contain the word” used as denominator in tf-idf'''
    for sent, f_table in freq_mat.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table


'''IDF(t) = log_e(Total number of paragraphs in the document / Number of paragraphs with term t in it)'''
def idf_matrix(freq_matrix, word_per_doc, total_paragraphs):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = round(math.log10(total_paragraphs / float(word_per_doc[word])),11)

        idf_matrix[sent] = idf_table

    return idf_matrix


freq_mat=frequency_matrix(sentences)
tf_mat=tf_matrix(freq_mat)

wpdtable=word_per_document(freq_mat)
idf_mat=idf_matrix(freq_mat,wpdtable,len(sentences))



def tfidf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):  # here, keys are the same in both the table
            tf_idf_table[word1] = round(float(value1 * value2),11)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix



def score_sentences(tf_idf_matrix):
    """
    score a sentence by its word's TF
    Basic algorithm: adding the TF frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """

    sentenceValue = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score

        sentenceValue[sent] = round(total_score_per_sentence / count_words_in_sentence,11)

    return sentenceValue



def find_threshold(sentenceValue):
    """
    Find the average score from the sentence value dictionary
    :rtype: int
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original summary_text
    average = (sumValues / len(sentenceValue))

    return average

tfidf_mat=tfidf_matrix(tf_mat,idf_mat)

sentenceValue=score_sentences(tfidf_mat)

th=find_threshold(sentenceValue)



print(freq_mat)
print(tf_mat)
print(wpdtable)
print(idf_mat)
print(tfidf_mat)
print(sentenceValue)


def generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:20] in sentenceValue and sentenceValue[sentence[:20]] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary

summary=generate_summary(sentences,sentenceValue,2*th)
FileObj = open(r"Summarized2.txt","w+")
l=summary.split('.')

for i in l:
    if(len(i)>0):
        #print(i[1])
        i1=i[1].upper()+i[2:]
        FileObj.write(i1+'.\n')

FileObj.close()



