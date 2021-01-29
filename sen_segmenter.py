import spacy
import re
from text_extract import *
nlp = spacy.load('en')
boundary = re.compile('^[0-9]$')

def custom_seg(doc):
    prev = doc[0].text
    length = len(doc)
    for index, token in enumerate(doc):
        if (token.text == '.' and boundary.match(prev) and index!=(length - 1)):
            doc[index+1].sent_start = False
        prev = token.text
    return doc
def sentence_segmenter(text):
    current_position = 0
    cursor = 0
    sentences = []
    start = 0
    for c in range(len(text)):
        # print(text)
        if text[c] == "." or text[c] == "!":
            try:
                int(text[c-1])
            except ValueError:
                # print(text[start:start+10])
                # print(text[ind_c-5:ind_c+5])
                # int()
                sentences.append(text[current_position:cursor + 1])
                current_position = cursor + 2
        cursor += 1
    sentences = list(filter(('.').__ne__, sentences))
    sentences = list(filter(('').__ne__, sentences))
    return sentences
# For cleaning the text
import spacy
import nltk
from nltk.tokenize import word_tokenize
#from nltk.tokenize import MWETokenizer
from nltk.corpus import stopwords
import regex as re
import string
nlp = spacy.load("en")
sp = spacy.load('en_core_web_sm')

#nltk.download('stopwords')
#nltk.download('punkt')

# spacy (362 words)
spacy_st = nlp.Defaults.stop_words
# nltk(179 words)
nltk_st = stopwords.words('english')


def clean(text, http=True, punc=True, lem=True, stop_w=True):
    if http is True:
        text = re.sub("https?:\/\/t.co\/[A-Za-z0-9]*", '', text)

    # stop words
    # in here I changed the placement of lower for those of you who want to use
    # Cased BERT later on.
    if stop_w == 'nltk':
        text = [word for word in word_tokenize(text) if not word.lower() in nltk_st]
        text = ' '.join(text)

    elif stop_w == 'spacy':
        text = [word for word in word_tokenize(text) if not word.lower() in spacy_st]
        text = ' '.join(text)

    # lemmitizing
    if lem == True:
        lemmatized = [word.lemma_ for word in sp(text)]
        text = ' '.join(lemmatized)

    # punctuation removal
    if punc is True:
        strnew = string.punctuation.replace('<','')
        strnew = strnew.replace('>', '')
        strnew = strnew.replace('/', '')
        text = text.translate(str.maketrans('', '', strnew))

    # removing extra space
    text = re.sub("\s+", ' ', text)

    return text

if __name__ == "__main__":
    '''filetxt = folders_txt[23]
    fileann = folders_ann[23]
    #print(folders_txt[23])
    final_df = combine_ds(filetxt,fileann)
    #print(final_df)
    #print(final_df.columns)
    #print(final_df.loc[3:6])
    #df2 = expand_df_ade_drug(final_df)
    df3 = expand_df_reason_drug(final_df)
    text = df3.corpus[0][0]
    relation = df3.Reason_Drug[0]
    print(len(df3))
    print(df3.head(2))
    print(relation)
    nlp.add_pipe(custom_seg, before='parser')
    doc = nlp(text)
    #print(doc)
    current_position = 0
    cursor = 0
    sentences = []
    for c in text:
        if c == "." or c == "!":
            sentences.append(text[current_position:cursor + 1])
            current_position = cursor + 2
        cursor += 1

    sentences = list(filter(('.').__ne__, sentences))
    for sentence in sentences:
        if relation[0] in sentence:
            if relation[1] in sentence:
                print(sentences.index(sentence))
                print(True)
                print(sentence)
    #for sentence in doc.sents:
    #    print(sentence.text)'''
    text = 'Alcoholic Cirrhosis/Acute Alcoholic Hepatitis: Admitted to [**Hospital3 **] from outside hospital after recent variceal bleed s/p variceal banding. ' \
           'Here, repeat EGD was performed which showed previously banded esophageal varices and gastric variceswith stigmata of recent bleeding. ' \
           'No new bands placed. Subsequently underwent uncomplicated TIPS on [**2140-7-16**]. Completed 5 day course of octreotide and 7 day course of ' \
           'levofloxacin for SBP prophylaxis. Unfortunately, patient continued to decompensate, with rising bilirubin and INR. She was treated ' \
           'with lactulose and rifaximin for encephalopathy. Ultrasound [**7-18**] and [**7-20**] both showed patent TIPS. . Given rising bili/INR, ' \
           'she was given a trial of pentoxyfilline and ursodiol for suspected acute alcoholic hepatitis. Corticosteroids not given because of recent bleeding. ' \
           'However,her synthetic function did not improve, and her creatinine subsequently rose from 0.6 to 3.0. A diagnostic paracentesis ' \
           'was performed (on [**7-29**]), which demonstrated no evidence of SBP. Her pentoxyfilline and ursodiol were discontinued as there was no' \
           'clear improvement on treatment. She was started empirically on' \
           'octreotide/midodrine for possible hepatorenal syndrome.' \
           'Nephrotoxic medications were held and she was given volume' \
           'repletion both with normal saline and albumin. Creatinine' \
           'subsequently improved to 1.2-1.4 at the time of discharge.' \
           '.' \
           'For nutritional support a post-pyloric feeding tube was placed' \
           'and tube feeds were intiated per nutrition recommendations. She' \
           'will be discharged for continued nutritional support to meet' \
           'caloric goals.' \
           '.' \
           'She was seen by social work for substance abuse support. In' \
           'addition, she was provided with information on post-discharge' \
           'support services.' \
           '.' \
           'MELD at time of discharge was 33, driven by a bilirubin of 19.8,' \
           'creatinine of 1.4, and an INR of 2.9..' \
           'Diuretics held given renal failure and lack of ascites on ultrasound, s/p TIPS.'
    text2 = "She was treated with lactulose and rifaximin for <REASON> encephalopathy </REASON>. Ultrasound [**7-18**] \
            and [**7-20**] both showed patent TIPS. Given rising bili/INR, she was given a trial of pentoxyfilline \
            and ursodiol for suspected acute alcoholic hepatitis. <DRUG> Corticosteroids </DRUG> not given because of \
            recent bleeding. However, her synthetic function did not improve, and her creatinine subsequently rose \
            from 0.6 to 3.0. A diagnostic paracentesis was performed (on [**7-29**]), which demonstrated no evidence \
            of SBP. Her pentoxyfilline and ursodiol were discontinued as there was no clear improvement on treatment."
    print(text2)
    #sentences = sentence_segmenter(text)
    #print(sentences)
    cleantxt = clean(text2,punc=True,lem=False)
    print("CLEANTEXT:",end = '\n')
    print(cleantxt)

