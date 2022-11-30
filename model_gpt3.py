from transformers import GPT2Tokenizer, GPT2Model
import openai as ai
import numpy as np
import json

API_KEY = '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'
orgID = "org-FamdhS456bzvQnGH0fUnw6aQ"
URL = 'https://api.openai.com/v1/completions'
filepath = "results/output_davinci003.txt"

ai.organization = orgID
ai.api_key = API_KEY
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')


values = "cleverness, friendship, teamwork"
story = ""
parts = ['beginning', 'middle', 'end']
starters = ['A long time ago and far,', 'Once upon a time,', 'There is a', 'I knew that something very special was about to happen', 'In a faraway land', 'There was once a']
fillers = ['Suddenly', "But", "After a while,", "However,", "Then,", "So,", "In fact,", "Moreover", "In contrast,", "Consequently,", "Because of", "Furthermore"]
closers = ['The time had come', 'It was finally time', 'Finally', 'In the end', 'After a while']
genre = "science fiction"
grade = "5"
max_tokens = 200


def run_model(responseprompt, max_tokens, vocab):
    response = ai.Completion.create(model="text-davinci-003", prompt=responseprompt, temperature=0.7, top_p=1.0, max_tokens=max_tokens, logit_bias=vocab)
    return response['choices'][0]['text']

def get_vocab(genre):
    vocab = {}
    filepath = 'data/genre_words/processed/'
    if genre == 'science fiction':
        filepath = filepath + 'sci-fi.json'

    fileObject = open(filepath, "r")
    jsonContent = fileObject.read()
    vocab = json.loads(jsonContent)
    return vocab


f = open(filepath, "a")
for part in parts:
    #create starting prompt
    startprompt = "Create the " + part + " of a " + genre + " story for Grade " + grade + " children. The story should talk about " + values + "."
    if(part == "beginning"):
        story = starters[np.random.randint(0, len(starters))]
    responseprompt = startprompt + '\n' + story

    f.write("============================PROMPT=================================\n")
    f.write(responseprompt + '\n')

    #get the vocab/bags of words
    vocab = get_vocab(genre)

    #get the model output
    text = run_model(responseprompt, max_tokens, vocab)
    max_tokens = len(tokenizer(text)['input_ids']) + 200
    
    f.write("............................RETURNED.................................\n")
    f.write(text + '\n')

    #if the story has not changed, retry with a filler
    story = story + text
    if(story == text or text.replace('\n', '') == ''):
        if(part == "middle"):
            story = story + text + fillers[np.random.randint(0, len(fillers))]
            responseprompt = startprompt + '\n' + story

            text = run_model(responseprompt, max_tokens, vocab)
            max_tokens = len(tokenizer(text)['input_ids']) + 200
            story = story + text

    f.write("----------------------------RESULT---------------------------------\n")
    f.write(story + '\n')
f.close()
