import glob
import re
import pandas as pd
import csv
from collections import defaultdict
import numpy as np
from text_extract import *
folders_txt = glob.glob('/home/user/NLP Methods in Biomedical Text Mining/track2-training_data_2/*.txt')
folders_ann = glob.glob('/home/user/NLP Methods in Biomedical Text Mining/track2-training_data_2/*.ann')
folders_txt = sorted(folders_txt)
folders_ann = sorted(folders_ann)
#print(len(folders_txt))
#print(len(folders_ann))
dfADE = pd.DataFrame(columns = ['corpus','ADE_Drug','ADE_Drug_label'])
dfREASON = pd.DataFrame(columns=['corpus','Reason_Drug','Reason_Drug_label'])
for i in range(len(folders_ann)):
    filetxt = folders_txt[i]
    fileann = folders_ann[i]
    #df = extract_text(filetxt)
    df = combine_ds(filetxt, fileann)
    #print(df)
    #print(filetxt)
    '''df_ade = expand_df_ade_drug(df)
    dfADE = dfADE.append(df_ade,ignore_index=True)
    df_adeneg = df_ade.loc[df_ade['ADE_Drug_label'] == 0]
    #print(len(df_adeneg))
    if len(df_adeneg) < 0.65 * (len(df_ade) - len(df_adeneg)):
        dfADE = dfADE.append(df_adeneg, ignore_index=True)'''
    #print(df_ade)
    df_reason = expand_df_reason_drug(df)
    dfREASON = dfREASON.append(df_reason, ignore_index=True)
    df_reasonneg = df_reason.loc[df_reason['Reason_Drug_label'] == 0]
    if len(df_reasonneg)<0.65*(len(df_reason)-len(df_reasonneg)):
        dfREASON = dfREASON.append(df_reasonneg, ignore_index=True)
    #print(dfADE)
    #break
    #print(df_ade)
    #print(df_reason)
#print(dfADE)
'''print(dfADE.sample(5))
print('Total ADE-Drug Samples:%d'% (len(dfADE)))
print('ADE-Drug Pos Samples:%d'% (dfADE['ADE_Drug_label'].sum(axis=0)))'''
#print(dfREASON)
print(dfREASON.sample(5))
print('Total Reason-Drug Samples:%d'% (len(dfREASON)))
print('Reason-Drug Pos Samples:%d'% (dfREASON['Reason_Drug_label'].sum(axis=0)))
#dfADE.to_csv(r'/home/user/PycharmProjects/BERT_RE/dfADEn2c2.csv', index = False, header=True)
dfREASON.to_csv(r'/home/user/PycharmProjects/BERT_RE/dfREASONn2c2FPP.csv', index = False, header=True)
