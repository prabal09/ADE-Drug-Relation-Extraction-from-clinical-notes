import glob
import re
import pandas as pd
import csv
from collections import defaultdict
import numpy as np
from text_extract import *
folders_txt_test = glob.glob('/home/user/NLP Methods in Biomedical Text Mining/gold-standard-test-data/test2/*.txt')
folders_ann_test = glob.glob('/home/user/NLP Methods in Biomedical Text Mining/gold-standard-test-data/test2/*.ann')
folders_txt_test = sorted(folders_txt_test)
folders_ann_test = sorted(folders_ann_test)
#print(len(folders_txt))
#print(len(folders_ann))
dfADE_test = pd.DataFrame(columns = ['corpus','ADE_Drug','ADE_Drug_label'])
dfREASON_test = pd.DataFrame(columns=['corpus','Reason_Drug','Reason_Drug_label'])
def test_df_ade_drug(df):
    #print(df)
    #print('ADE-Drug',df.ADE_Drug)
    df2 = pd.DataFrame(columns = ['corpus','ADE_Drug','ADE_Drug_label'])
    for d in range(len(df)):
        df_ = df.loc[d]
        if df_.ADE_Drug !='':
            #print(True)
            for ade,drug in df_.ADE_Drug:
                df2 = df2.append({'corpus':df_.corpus,'ADE_Drug':[ade,drug],'ADE_Drug_label':1},ignore_index=True)
    return df2

def test_df_reason_drug(df):
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
    return df3

for i in range(len(folders_ann_test)):
    filetxt_test = folders_txt_test[i]
    fileann_test = folders_ann_test[i]
    #df = extract_text(filetxt)
    df = combine_ds(filetxt_test, fileann_test)
    #print(df)
    #print(filetxt)
    '''df_ade_test = expand_df_ade_drug(df)
    dfADE_test = dfADE_test.append(df_ade_test,ignore_index=True)
    #print(df_ade)
    df_reason_test = expand_df_reason_drug(df)
    dfREASON_test = dfREASON_test.append(df_reason_test, ignore_index=True)
    #print(dfADE)
    #break
    #print(df_ade)
    #print(df_reason)
dfREASON_testpos = dfREASON_test.loc[dfREASON_test['Reason_Drug_label']==1]
dfREASON_testneg = dfREASON_test.loc[dfREASON_test['Reason_Drug_label']==0]
print(len(dfREASON_testneg))
print(len(dfREASON_testpos))
dfREASON_goldstd = pd.DataFrame(columns=['corpus','Reason_Drug','Reason_Drug_label'])
pos = int(len(dfREASON_testpos)/3)
print(pos)
neg = int(len(dfREASON_testneg)/1.5)
print(neg)
dfREASON_goldstd = dfREASON_goldstd.append(dfREASON_testpos.sample(pos))
dfREASON_goldstd = dfREASON_goldstd.append(dfREASON_testneg.sample(neg))
#len(dfREASON_goldstd)
print(dfREASON_goldstd['Reason_Drug_label'].sum(axis=0))

'''dfADE_testpos = dfADE_test.loc[dfADE_test['ADE_Drug_label']==1]
dfADE_testneg = dfADE_test.loc[dfADE_test['ADE_Drug_label']==0]
print(len(dfADE_test))
print(len(dfADE_test))
dfADE_goldstd = pd.DataFrame(columns=['corpus','ADE_Drug','ADE_Drug_label'])
pos = int(len(dfADE_testpos)/3)
print(pos)
neg = int(len(dfADE_testneg)/1.5)
print(neg)
dfADE_goldstd = dfADE_goldstd.append(dfREASON_testpos.sample(pos))
dfADE_goldstd = dfADE_goldstd.append(dfREASON_testneg.sample(neg))
#len(dfREASON_goldstd)
print(dfADE_goldstd['ADE_Drug_label'].sum(axis=0))'''
#print(dfADE_test)
#print(len(dfADE_test))
#print(sum(dfADE_test.ADE_Drug_label))
#print(dfREASON_test)
#print(len(dfREASON_test))
#print(sum(dfREASON_test.Reason_Drug_label))
'''print(dfADE_test.sample(5))
print('Total ADE-Drug Samples:%d'% (len(dfADE_test)))
print('ADE-Drug Pos Samples:%d'% (dfADE_test['ADE_Drug_label'].sum(axis=0)))'''
#print(dfREASON)
print('Total Reason-Drug Samples:%d'% (len(dfREASON_test)))
print(dfREASON_goldstd.sample(5))
print('Reason-Drug Pos Samples:%d'% (dfREASON_test['Reason_Drug_label'].sum(axis=0)))
#dfADE_test.to_csv(r'/home/user/PycharmProjects/BERT_RE/dfADE_goldstd.csv', index = False, header=True)
dfREASON_goldstd.to_csv(r'/home/user/PycharmProjects/BERT_RE/dfREASON_goldstdFPP.csv', index = False, header=True)
