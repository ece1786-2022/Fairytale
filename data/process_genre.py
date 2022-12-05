import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def get_genre(text = ''):    
    tokenizer = AutoTokenizer.from_pretrained("Tejas3/distillbert_110_uncased_movie_genre")    
    model = AutoModelForSequenceClassification.from_pretrained("Tejas3/distillbert_110_uncased_movie_genre")
    inputs  = tokenizer(text, return_tensors="pt",truncation=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    # all_labels = [model.config.id2label[i] for i in range(6)]
    label = model.config.id2label[predicted_class_id]
    return label


