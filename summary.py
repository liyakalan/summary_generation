import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """SRMS Titanic was a British passenger liner, operated by the White Star Line, that sank in the North Atlantic Ocean on 
15 April 1912 after striking an iceberg during her maiden voyage from Southampton, England to New York City, United States. 
Of the estimated 2,224 passengers and crew aboard, more than 1,500 died, making it the deadliest sinking of a single ship up to that time.
It remains the deadliest peacetime sinking of an ocean liner or cruise ship. The disaster drew public attention, 
provided foundational material for the disaster film genre, and has inspired many artistic works.
RMS Titanic was the largest ship afloat at the time she entered service and the second of three Olympic-class ocean liners operated by 
the White Star Line. She was built by the Harland and Wolff shipyard in Belfast. Thomas Andrews, the chief naval architect
of the shipyard, died in the disaster. Titanic was under the command of Captain Edward Smith, who went down with the ship. 
The ocean liner carried some of the wealthiest people in the world, as well as hundreds of emigrants from the British Isles, 
Scandinavia, and elsewhere throughout Europe, who were seeking a new life in the United States and Canada.
The first-class accommodation was designed to be the pinnacle of comfort and luxury, with a gymnasium, swimming pool, smoking rooms, 
high-class restaurants and cafes, a Turkish bath and hundreds of opulent cabins. A high-powered radiotelegraph transmitter was available 
for sending passenger "marconigrams" and for the ship's operational use. Titanic had advanced safety features, such as watertight 
compartments and remotely activated watertight doors, contributing to its reputation as "unsinkable".
Titanic was equipped with 16 lifeboat davits, each capable of lowering three lifeboats, for a total of 48 boats; 
she carried only 20 lifeboats, four of which were collapsible and proved hard to launch while she was sinking 
(Collapsible A nearly swamped and was filled with a foot of water until rescue; Collapsible B completely overturned while launching). 
Together, the 20 lifeboats could hold 1,178 people—about half the number of passengers on board, and one third of the number of passengers
the ship could have carried at full capacity (consistent with the maritime safety regulations of the era). 
When the ship sank, the lifeboats that had been lowered were only filled up to an average of 60%."""

def summary_generation(rawdata):
    stopwords = list(STOP_WORDS)
    #print(stopwords)

    nlp = spacy.load('en_core_web_sm')
    data = nlp(rawdata)
    #print(data)

    tokens = [token.text for token in data]
    #print(tokens)

    word_freq = {}
    for word in data:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1
    #print(word_freq)

    max_freq = max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
    #print(word_freq)

    sent_tokens = [sent for sent in data.sents]
    #print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]
    #print(sent_scores)

    select_len = int(len(sent_tokens) * 0.3)
    #print(select_len)

    summary = nlargest(select_len, sent_scores, key = sent_scores.get)
    #print(summary)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)


    #print(text)
    #print(summary)
    #print("Length of original text ", len(text.split(' ')))
    #print("Length of summary text ", len(summary.split(' ')))

    return summary, data, len(rawdata.split(' ')), len(summary.split(' '))