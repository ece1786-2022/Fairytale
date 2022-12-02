from transformers import GPT2Tokenizer, GPT2Model
import openai as ai
import numpy as np
import json

API_KEY = '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'
orgID = "org-FamdhS456bzvQnGH0fUnw6aQ"
URL = 'https://api.openai.com/v1/completions'
filepath = "results/davinci003_bias.txt"

ai.organization = orgID
ai.api_key = API_KEY
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')


values = "friendship, determination"
story = ""
parts = ['beginning', 'middle', 'end']

realfic_starters = ['There is a', 'I knew that something very special was about to happen', 'Today', 'Dear Diary']
starters = ['A long time ago and far,', 'Once upon a time,', 'There is a', 'I knew that something very special was about to happen', 'In a faraway land', 'There was once a']

fillers = ['Suddenly', "But", "After a while,", "However,", "Then,", "So,", "In fact,", "Moreover", "In contrast,", "Consequently,", "Because of", "Furthermore"]
closers = ['The time had come', 'It was finally time', 'Finally', 'In the end', 'After a while']
genre = "Realistic Fiction"
grade = "5"
max_tokens = 200


def run_model(responseprompt, max_tokens, vocab):
    if vocab is not None:
        response = ai.Completion.create(model="text-davinci-003", prompt=responseprompt, temperature=0.75, top_p=1.0, max_tokens=max_tokens, logit_bias=vocab)
    else:
        response = ai.Completion.create(model="text-davinci-003", prompt=responseprompt, temperature=0.75, top_p=1.0, max_tokens=max_tokens)
    return response['choices'][0]['text']

def get_vocab(genre):
    vocab = {}
    genre = genre.lower()
    filepath = 'data/genre_words/processed/'
    if genre == 'science fiction':
        filepath = filepath + 'sci-fi.json'
    elif genre == "horror":
        filepath = filepath + 'horror.json'
    elif genre == "fantasy":
        filepath = filepath + "fantasy.json"
    elif genre == "realistic fiction":
        filepath = filepath + "realfic.json"

    fileObject = open(filepath, "r")
    jsonContent = fileObject.read()
    vocab = json.loads(jsonContent)
    return vocab


f = open(filepath, "a")
for part in parts:
    #create starting prompt
    startprompt = "Create the " + part + " of a " + genre + " story for grade " + grade + " children. The story should talk about " + values + "."
    if(part == "beginning"):
        story = starters[np.random.randint(0, len(starters))]
    responseprompt = startprompt + '\n' + story

    f.write("============================PROMPT=================================\n")
    f.write(responseprompt + '\n')

    #get the vocab/bags of words
    vocab = get_vocab(genre)
    # vocab = None

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

#since limit of 300 logit biases need to convert terms like this:
#Rewrite the above text, replacing science fiction terms with fantasy words.