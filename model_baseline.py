from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import random

model_name = "pranavpsv/genre-story-generator-v2"
# model_name = "pranavpsv/gpt2-genre-story-generator"
# model_name = "openai-gpt"
# model_name = "pranavpsv/gpt2-story-gen"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

begin = ['A long time ago and far,', 'Once upon a time,']
skeletons = ["","","","","But", "After a while,", "However,", "Then,", "So,", "In fact,", "Moreover", "In contrast,", "Consequently,", "Because of", "Furthermore"]
end = ['Finally, ']

# genre = "<action>"
# genre = "<sci_fi>"
genre = "<horror>"

text = genre + " " + random.choice(begin)
flag = True
while flag:
    with torch.no_grad():
        # output = model.generate(**inputs, max_length=200, do_sample=True)

        print(text)
        print("---------------------")
        inputs  = tokenizer(text , return_tensors="pt")
        output = model.generate(**inputs, max_length=400,  do_sample=True)
        new_generated = tokenizer.decode(output[0])[len(text):]
        dot_point = new_generated.find('.')
        text = text + new_generated[:dot_point+1] + ' '
        for w in end:
            if w in text:
                flag = False
        if flag==True:
            if len(text.split(" "))>150:
                text = text + random.choice(end)
            else:
                text = text + random.choice(skeletons)
        

print(text)