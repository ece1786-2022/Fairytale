from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import random
from data import process_age
from data import process_genre
import csv
import pandas as pd
from transformers import DistilBertForSequenceClassification, Trainer, TrainingArguments
from transformers import AutoModelForSequenceClassification

def read_data(filename):
    # dataset = {}
    texts = []
    labels = []
    with open(filename, "r", encoding="utf8") as f:
        lines = f.readlines()  
        for line in lines[1:]:
            text = line.strip().split("\t")[2].replace('"','').replace("'", '')[1:]
            label = line.strip().split("\t")[4]
            # dataset["text"] = text
            # dataset["label"] = int(label)
            texts.append(text.replace("\'",''))
            labels.append(int(label))
    return texts, labels


texts = []
files = ['data/processed_data/story_3_with_age_genre.tsv','data/processed_data/story_2_with_age_genre.tsv']
for file in files:
    text, label = read_data(file)
    texts.extend(text)

with open("corpus_2_3.txt","w",encoding="ISO-8859-1") as f:
    for line in texts:
        try:
            f.write(line + "\n\n")
        except:
            pass