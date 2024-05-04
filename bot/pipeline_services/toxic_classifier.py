from transformers import BertTokenizer, BertForSequenceClassification
from  torch.nn import functional as F


tokenizer = BertTokenizer.from_pretrained('SkolkovoInstitute/russian_toxicity_classifier')
model = BertForSequenceClassification.from_pretrained('SkolkovoInstitute/russian_toxicity_classifier')

def is_toxic(comment, toxic_threshold=0.8):
    batch = tokenizer.encode(comment, return_tensors='pt')
    logits = model(batch).logits
    probs = F.softmax(logits, dim = 1).detach().numpy()[0]
    print(probs[1])
    return probs[1] > toxic_threshold