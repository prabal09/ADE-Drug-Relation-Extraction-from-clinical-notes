# Relation Extraction: ADE-Drug using SciBERT with Positional Tagging

Developing an NLU pipeline to determine Adverse Drug Event (ADE) due to a Drug from Clinical Notes. SciBERT model is used for this purpose which is pretrained on Computer Science and Biomedical research papers

Task Overview: Obtain the established relation between a Drug with its Reason/ADE

▪ Approach: SciBERT tokenizer and model with positional tagging is in the input is taken as the base model, which is then concatenated it with a fully connected    neural network with dropout of 30%, and trained on n2c2 dataset to develop a relation-extraction model

▪ Positional Tagging is used in SciBERT, which helps learn the values of the newly added tokens to extract relations.

▪ Attained an accuracy (F1-score) of 78% for ADE-Drug


