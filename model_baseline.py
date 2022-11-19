from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# model_name = "pranavpsv/genre-story-generator-v2"
# model_name = "pranavpsv/gpt2-genre-story-generator"
model_name = "Deniskin/gpt3_medium"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


text = '''Once upon a time there was a dear little girl'''

inputs  = tokenizer(text , return_tensors="pt")

with torch.no_grad():
    output = model.generate(**inputs, max_length=200)

print(tokenizer.decode(output[0]))