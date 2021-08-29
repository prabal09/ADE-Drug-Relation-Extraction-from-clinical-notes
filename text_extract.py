import glob
import re
import pandas as pd
import csv
from collections import defaultdict
import numpy as np
from sen_segmenter import *
#import json
folders_txt = glob.glob('/home/user/NLP Methods in Biomedical Text Mining/track2-training_data_2/*.txt')
folders_ann = glob.glob('/home/user/NLP Methods in Biomedical Text Mining/track2-training_data_2/*.ann')
folders_txt_test = glob.glob('/home/user/NLP Methods in Biomedical Text Mining/gold-standard-test-data/test2/*.txt')
folders_ann_test = glob.glob('/home/user/NLP Methods in Biomedical Text Mining/gold-standard-test-data/test2/*.ann')
folders_txt = sorted(folders_txt_test)
folders_ann = sorted(folders_ann_test)
#print(len(folders_txt))
def extract_hashtags(text):
    # initializing hashtag_list variable
    hashtag_list = []

    # splitting the text into words
    for word in text.split():

        # checking the first charcter of every word
        if word[0] == '#':
            # adding the word to the hashtag_list
            hashtag_list.append(word[1:])

            # printing the hashtag_list
    print("The hashtags in \"" + text + "\" are :")
    for hashtag in hashtag_list:
        print(hashtag)
def extract_text(filetxt):
    df = pd.DataFrame(columns = ['corpus','Drug','ADE','Reason','ADE_Drug','Reason_Drug'])
    #print(df)
    with open(filetxt,encoding="utf8") as f:
        text_ = f.read()
        #print(text_==None)
        listh = [m.start() for m in re.finditer('#', text_)]
        #numb_i = [1,2,3,4,5,6,7,8,9]
        #print(listh==[])
        if listh != []:
            for i in listh:
                j = text_[i+1:].find('#')
                #print('i,j=',i,j)
                j = i+j
                if text_[i+1:j] != '':
                    df = df.append({'corpus':[text_[i+1:j]]},ignore_index = True)
                    #print(df2)
                    #df.append(df2,ignore_index=True)
        regex = r'(?:\d\.){1}.(.+?)(?:\d\.){1}'
        p = re.compile(regex, flags=re.DOTALL)
        sections = p.findall(text_)
        #print(sections)
        #print(len(sections))
        for i in range(0, len(sections)):
            str2=''.join(sections[i])
            df = df.append({'corpus': [str2]}, ignore_index=True)
    df.fillna('',inplace = True)
    return df

def extract_ann(fileann):
    #list_of_sent_words = []
    ADE = [];Drug = [];Reason = []
    ADE_Drugdd = defaultdict(list);Reason_Drugdd = defaultdict(list)
    with open(fileann,"r", encoding="utf8") as csv_file:
        #text_ = csv_file.read()
        #listDrug = [m.start() for m in re.finditer('Drug', text_)]
        #listDrug
        csv_file = csv.reader(csv_file, delimiter=' ', quotechar = '"')
        list1 = []
        for row in csv_file:
            '''print(row)
            break
            #rowx = row.split()
            list_of_sent_words.append(row)'''
            t1 = " ".join(row)
            t1 = t1.replace('Arg1:','')
            t1 = t1.replace('Arg2:', '')
            t2 = t1.split()
            list1.append(t2)
            #print(" ".join(row))
            #print(list1)
        for t in range(len(list1)):
            if list1[t][1] == 'Reason':
                w = list1[t][4:]
                Reason.append((list1[t][0],' '.join(w)))

            if list1[t][1] == 'Drug':
                w = list1[t][4:]
                Drug.append((list1[t][0],' '.join(w)))

            if list1[t][1] == 'ADE':
                w = list1[t][4:]
                ADE.append((list1[t][0],' '.join(w)))
        Reasondd = defaultdict(list)
        for k,v in Reason:
            Reasondd[k].append(v)
        Drugdd = defaultdict(list)
        for k, v in Drug:
            Drugdd[k].append(v)
        ADEdd = defaultdict(list)
        for k,v in ADE:
            ADEdd[k].append(v)
        for t in range(len(list1)):
            if list1[t][1] == 'ADE-Drug':
                w = list1[t][2:]
                #print(w)
                #print(list1[t])
                ade = ADEdd[str(w[0])]
                drug = Drugdd[str(w[1])]
                #print(ade)
                #print(drug)
                #di = (ADE[str(w[0])],Drug(str(w[1])))
                #print(di)
                for a in ade:
                    for d in drug:
                        #print(a,d)
                        ADE_Drugdd[a].append(d)
        for t in range(len(list1)):
            if list1[t][1] == 'Reason-Drug':
                w = list1[t][2:]
                #print(w)
                #print(list1[t])
                reason = Reasondd[str(w[0])]
                drug = Drugdd[str(w[1])]
                #print(ade)
                #print(drug)
                #di = (ADE[str(w[0])],Drug(str(w[1])))
                #print(di)
                for a in reason:
                    for d in drug:
                        #print(a,d)
                        Reason_Drugdd[a].append(d)
    return Drugdd,ADEdd,Reasondd,ADE_Drugdd,Reason_Drugdd

def combine_ds(filetxt,fileann):
    df = extract_text(filetxt)
    #print(df)
    Drugdd,ADEdd,Reasondd,ADE_Drugdd,Reason_Drugdd = extract_ann(fileann)
    for (t,n) in Drugdd.items():
        #print(t,n)
        for d in range(len(df)):
            for nn in n:
                if nn in df.corpus[d][0]:
                    #print(df.Drug[d])
                    if df.Drug[d] == '':
                        df.Drug[d] = [nn]
                    else:
                        if nn not in df.Drug[d]:
                            df.Drug[d].append(nn)

    for (t,n) in ADEdd.items():
        #print(t,n)
        for d in range(len(df)):
            for nn in n:
                if nn in df.corpus[d][0]:
                    #print(df.Drug[d])
                    if df.ADE[d] == '':
                        df.ADE[d] = [nn]
                    else:
                        if nn not in df.ADE[d]:
                            df.ADE[d].append(nn)

    for (t,n) in Reasondd.items():
        #print(t,n)
        for d in range(len(df)):
            for nn in n:
                if nn in df.corpus[d][0]:
                    #print(df.Drug[d])
                    if df.Reason[d] == '':
                        df.Reason[d] = [nn]
                    else:
                        if nn not in df.Reason[d]:
                            df.Reason[d].append(nn)
    for (t,n) in ADE_Drugdd.items():
        for nn in n:
            for d in range(len(df)):
                if all(tnn in df.corpus[d][0] for tnn in [t,nn]):
                    #print([t, nn])
                    #print(df.corpus[d][0])
                    #print(True)
                    if df.ADE_Drug[d] == '':
                        df.ADE_Drug[d] = [(t,nn)]
                    else:
                        df.ADE_Drug[d].append((t,nn))
    for (t,n) in Reason_Drugdd.items():
        for nn in n:
            for d in range(len(df)):
                if all(tnn in df.corpus[d][0] for tnn in [t,nn]):
                    #print([t, nn])
                    #print(df.corpus[d][0])
                    #print(True)
                    if df.Reason_Drug[d] == '':
                        df.Reason_Drug[d] = [(t,nn)]
                    else:
                        df.Reason_Drug[d].append((t,nn))
    #for i in range(len(df)):
    return df

def expand_df_ade_drug(df):
    #print(df)
    #print('ADE-Drug',df.ADE_Drug)
    df2 = pd.DataFrame(columns = ['corpus','ADE_Drug','ADE_Drug_label'])
    for d in range(len(df)):
        df_ = df.loc[d]
        if df_.ADE_Drug !='':
            #print(True)
            for ade,drug in df_.ADE_Drug:
                df2 = df2.append({'corpus':df_.corpus,'ADE_Drug':[ade,drug],'ADE_Drug_label':1},ignore_index=True)
                #print('ADE-Drug', df.ADE_Drug[d])
                #print(df2)
        #print('Drug',df_.Drug)
        #print('ADE',df_.ADE)
        #print('ADE-Drug', df.ADE_Drug[d])
        if df_.Drug != '' and df_.ADE !='' and df.ADE_Drug[d] !='':
            for d1 in df_.Drug:
                for a1 in df_.ADE:
                    #print('a1,d1',a1,d1)
                    if (a1,d1) not in df.ADE_Drug[d]:
                        df2 = df2.append({'corpus': df_.corpus,'ADE_Drug': [a1, d1],'ADE_Drug_label': 0},ignore_index=True)
    pos = sum(df2.ADE_Drug_label)
    #print(pos)
    #print('df2',df2)
    #print(df2['ADE_Drug_label'].sum(axis=0))
    if 0.5*len(df2) > pos:
        #print(True)
        df2_1 = df2.loc[df2['ADE_Drug_label'] == 1]
        #print('df2_1',df2_1)
        df2_0 = df2.loc[df2['ADE_Drug_label'] == 0]
        #print('df2_0', df2_0)
        df2_0 = df2_0.sample(n = pos)
        #print('df2_0', df2_0)
        df2_f = df2_1.append(df2_0)
    else:
        df2_f = df2
    #print(df2_f.columns)
    #print('df2_f',df2_f)
    #print(df2_f['ADE_Drug_label'].sum(axis=0))
    df2_f = df2_f.sort_index()
    df_data = pd.DataFrame(columns=df2_f.columns)
    #print('df_data',df_data.columns)
    #print(len(df2_f))
    #print(df2_f['ADE_Drug'].to_list())
    ADE_Drug_li = df2_f['ADE_Drug'].to_list()
    drug_li = []
    for i in range(len(ADE_Drug_li)):
        drug_li.append(ADE_Drug_li[i][1])
    #print(drug_li)
    #-------------paste here-------#
    for index, row in df2_f.iterrows():
        text = row['corpus'][0]
        #print(text)
        #print(len(text))
        #print(row)
        #print(row['corpus'], row['ADE_Drug'],row['ADE_Drug_label'])
        sentences = sentence_segmenter(text)
        #print(sentences)
        #break
        #print(len(sentences))
        #relation = row['Reason_Drug']
        #print(relation)

        for i_sentence in range(len(sentences)-2):
            sen5 = ' '.join(sentences[i_sentence:i_sentence +2])
            #print(sen5)
            #print(len(sen5.split()))
            #break
            relation = row['ADE_Drug']
            #print(relation)
            if relation[1] in sen5:
                et=False
                if relation[0] in sen5:
                    et = True
                    #print(True,end = '\n')
                    #print(relation[0],end='\n')
                    #print(relation[1], end='\n')
                    #print('<REASON>'+relation[0]+'</REASON>', end='\n')
                    #print('<DRUG>' + relation[1] + '</DRUG>', end='\n')
                    relation0 = '<ADE>'+' '+relation[0]+' '+'</ADE>'
                    relation1 = '<DRUG>' +' '+ relation[1]+' '+'</DRUG>'
                    #print(relation0,relation1)
                    #print(type(sen5))
                    sen5 = sen5.replace(relation[0],relation0,1)
                    sen5 = sen5.replace(relation[1],relation1,1)
                    sen5 = clean(sen5,punc=True,lem = False)
                    #print('sen5 sample %d:'%(i_sentence),sen5,end = '\n')
                    df_data = df_data.append({'corpus': sen5, 'ADE_Drug': relation,
                                              'ADE_Drug_label': row['ADE_Drug_label']}, ignore_index=True)

                for drug in drug_li:
                    pos2 = df_data['ADE_Drug_label'].sum(axis=0)
                    l = len(df_data)
                    #print(pos2>0.55*l)
                    if pos2 > 0.75 * l:
                        if drug != relation[1]:
                            if drug in sen5:
                                if et !=True:
                                    relation0 = '<ADE>' + ' ' + relation[0] + ' ' + '</ADE>'
                                    drug1 = '<DRUG>' + ' ' + drug + ' ' + '</DRUG>'
                                    # print(relation0,relation1)
                                    # print(type(sen5))
                                    sen5 = sen5.replace(relation[0], relation0, 1)
                                    sen5 = sen5.replace(drug, drug1, 1)
                                sen5 = clean(sen5, punc=True, lem=False)
                                #print(drug,relation[1])
                                df_data = df_data.append({'corpus': sen5, 'ADE_Drug': [relation[0],drug],
                                                        'ADE_Drug_label': 0}, ignore_index=True)
    #print(df_data.sample(5))
    #print(len(df_data))
        # print(df_data.corpus[0])
    #print(df_data['Reason_Drug_label'].sum(axis=0))
    return df_data

def expand_df_reason_drug(df):
    # print(df)
    # print('ADE-Drug',df.ADE_Drug)
    df3 = pd.DataFrame(columns=['corpus','Reason_Drug','Reason_Drug_label'])
    for d in range(len(df)):
        df_ = df.loc[d]
        if df_.Reason_Drug != '':
            # print(True)
            for ade, drug in df_.Reason_Drug:
                df3 = df3.append({'corpus': df_.corpus, 'Reason_Drug': [ade, drug], 'Reason_Drug_label': 1},
                                 ignore_index=True)
                # print('ADE-Drug', df.ADE_Drug[d])
                # print(df2)
        #print('Drug',df_.Drug)
        #print('Reason',df_.Reason)
        #print('Reason-Drug', df.Reason_Drug[d])
        if df_.Drug != '' and df_.Reason != '' and df.Reason_Drug[d] != '':
            for d1 in df_.Drug:
                for a1 in df_.Reason:
                    #print('(a1,d1)',(a1,d1))
                    if (a1, d1) not in df.Reason_Drug[d]:
                        df3 = df3.append({'corpus': df_.corpus, 'Reason_Drug': [a1, d1], 'Reason_Drug_label': 0},
                                         ignore_index=True)
    pos = sum(df3.Reason_Drug_label)
    if 0.5*len(df3) > pos:
        df3_1 = df3.loc[df3['Reason_Drug_label'] == 1]
        df3_0 = df3.loc[df3['Reason_Drug_label'] == 0]
        df3_0 = df3_0.sample(n = pos)
        df3_f = df3_1.append(df3_0)
    else:
        df3_f = df3
    df3_f = df3_f.sort_index()
    #print(df3_f.columns)
    #print(df3_f.head())
    df_data = pd.DataFrame(columns=df3_f.columns)
    #print('df_data',df_data.columns)
    #print(len(df3_f))
    #print(df2_f['ADE_Drug'].to_list())
    Reason_Drug_li = df3_f['Reason_Drug'].to_list()
    drug_li = []
    for i in range(len(Reason_Drug_li)):
        drug_li.append(Reason_Drug_li[i][1])
    #print(drug_li)
    #-------------paste here-------#
    for index, row in df3_f.iterrows():
        text = row['corpus'][0]
        #print(text)
        #print(row['corpus'], row['Reason_Drug'],row['Reason_Drug_label'])
        sentences = sentence_segmenter(text)
        #print(sentences)
        #break
        # print(len(sentences))
        #relation = row['Reason_Drug']
        #print(relation)
        for i_sentence in range(len(sentences) - 3):
            sen5 = ' '.join(sentences[i_sentence:i_sentence + 3])
            #print(sen5)
            #print(len(sen5.split()))
            #break
            relation = row['Reason_Drug']
            #print(relation)
            if relation[1] in sen5:
                et = False
                if relation[0] in sen5:
                    et = True
                    #print(True,end = '\n')
                    #print(relation[0],end='\n')
                    #print(relation[1], end='\n')
                    #print('<REASON>'+relation[0]+'</REASON>', end='\n')
                    #print('<DRUG>' + relation[1] + '</DRUG>', end='\n')
                    relation0 = '<REASON>'+' '+relation[0]+' '+'</REASON>'
                    relation1 = '<DRUG>' +' '+ relation[1]+' '+'</DRUG>'
                    #print(relation0,relation1)
                    #print(type(sen5))
                    sen5 = sen5.replace(relation[0],relation0,1)
                    sen5 = sen5.replace(relation[1],relation1,1)
                    sen5 = clean(sen5,punc=True,lem = False)
                    #print('sen5 sample %d:'%(i_sentence),sen5,end = '\n')
                    df_data = df_data.append({'corpus': sen5, 'Reason_Drug': relation,
                                              'Reason_Drug_label': row['Reason_Drug_label']}, ignore_index=True)

    #print(df_data.sample(5))
    #print(len(df_data))
        # print(df_data.corpus[0])
    #print(df_data['Reason_Drug_label'].sum(axis=0))
    return df_data

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


'''    for (t,n) in ADE.items():
        for d in range(len(df)):
            if n in df.corpus[d][0]:
                if df.ADE[d] == '':
                    df.ADE[d] = n
    for (t,n) in Reason.items():
        for d in range(len(df)):
            if n in df.corpus[d][0]:
                if df.Reason[d] == '':
                    df.Reason[d] = n'''




if __name__ == "__main__":
    filetxt = folders_txt[20]
    df1 = extract_text(filetxt)
    final_df = combine_ds(filetxt,fileann)
    df3 = expand_df_reason_drug(final_df)


