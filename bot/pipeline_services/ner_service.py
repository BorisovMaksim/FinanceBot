from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from pathlib import Path
import numpy as np

tokenizer = AutoTokenizer.from_pretrained("yqelz/xml-roberta-large-ner-russian")
model = AutoModelForTokenClassification.from_pretrained("yqelz/xml-roberta-large-ner-russian")

ner = pipeline("ner", model=model, tokenizer=tokenizer)


def get_company_name(example):
    ner_results =  ner(example)
    organization = ""
    
    for result in ner_results:
        if result['entity'] == 'B-ORG':
            organization = result['word'] 
        elif  result['entity'] == 'I-ORG':
            organization += result['word']
    organization = organization.replace("▁", "").strip()
    print(f"{organization=}")
    return organization
    
 