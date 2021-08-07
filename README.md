# Relation Extraction: ADE-Drug and Reason-Drug using SciBERT with Positional Tagging

Developing an NLU pipeline to determine relations such as Adverse Drug Event (ADE) due to a Drug or Reason for using a Drug, from Clinical Notes. SciBERT model is used for this purpose which is pretrained on Computer Science and Biomedical research papers

![image](https://user-images.githubusercontent.com/32479901/128592592-3de00137-aa9d-4451-bbd2-103ba367544d.png)


Task Overview: Obtain the established relation between a Drug with its Reason/ADE

▪ Approach: SciBERT tokenizer and model, with positional tagging in the input text, is taken as the base model, which is then concatenated it with a fully connected    neural network with dropout of 30%, and fine-tuned on n2c2 dataset to develop a relation-extraction model

▪ Positional Tagging used in SciBERT helps learn the values of the newly added tokens to extract relations.

▪ Attained an accuracy (F1-score) of 78% for ADE-Drug


