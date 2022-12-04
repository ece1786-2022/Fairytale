from transformers import GPT2Tokenizer, GPT2Model
import openai as ai
import numpy as np
from numpy import random
import json

API_KEY = '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'
orgID = "org-FamdhS456bzvQnGH0fUnw6aQ"
URL = 'https://api.openai.com/v1/completions'
filepath = "results/davinci003_bias.txt"

ai.organization = orgID
ai.api_key = API_KEY
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')


values = "love, determination"
genre = "fantasy"
grade = "1"
max_tokens = 50

story = ""
# parts = ['beginning', 'middle', 'end']
parts = ['beginning']

scifi_starters = ['In', 'Before', 'Deep in space', 'Somewhere in a galaxy far, far away', 'Out in space', 'Out of nowhere', 'There was a', 'After years of' , 'In the skies', 'A smart', 'The machines', 'The aliens', 'One day', 'Eureka!']
horror_starters = ['In', 'Before', 'Two dark figures', 'He was being chased', 'She was being chased', 'She awoke suddenly', 'He awoke suddenly', 'It was a dark, and rainy day', 'Somewhere deep underground', 'In an ancient', 'In a remote', 'In an old', 'Long ago', 'There was once', 'A long time ago']
fantasy_starters = ['In', 'Before', 'A long time ago and far,', 'Once upon a time,', 'There is a', 'In a faraway land', 'There was once a', 'Two figures stood', 'Across the seas', 'For many years', 'In a kingdom', 'King', 'Queen', 'In a tower', 'In a castle']
realfic_starters = ['In', 'Before', 'There is a', 'I knew that something very special was about to happen', 'Today', 'Dear Diary', 'On a', 'It was a', 'Somewhere in', 'One sunny morning', 'One hot afternoon', 'Today was', 'Today will']

fillers = ['In', 'The', 'One day', 'Later', "But", "After a while,", "However,", "Then,", "So,", "In fact,", "Moreover", "After", 'Soon', 'Meanwhile', 'While', 'At the same time', 'Eventually', "A"]
closers = ['The time had come', 'It was finally time', 'Finally', 'In the end', 'After a while', 'And with that', 'They day was', 'Finally,', 'And with that', 'So with that', 'Thus']


def run_model(responseprompt, max_tokens, vocab, temp=0.8):
    if vocab is not None:
        response = ai.Completion.create(model="text-davinci-003", prompt=responseprompt, temperature=temp, top_p=1.0, max_tokens=max_tokens, logit_bias=vocab)
    else:
        response = ai.Completion.create(model="text-davinci-003", prompt=responseprompt, temperature=temp, top_p=1.0, max_tokens=max_tokens)
    return response['choices'][0]['text']


def load_vocab(filepath):
    fileObject = open(filepath, "r")
    jsonContent = fileObject.read()

    return json.loads(jsonContent)


def get_genre_vocab(genre):
    filepath = 'data/genre_words/processed/'
    if genre == 'science fiction':
        filepath = filepath + 'sci-fi.json'
    elif genre == "horror":
        filepath = filepath + 'horror.json'
    elif genre == "fantasy":
        filepath = filepath + "fantasy.json"
    elif genre == "realistic fiction":
        filepath = filepath + "realfic.json"

    return load_vocab(filepath)


def get_value_vocab(value):
    filepath = 'data/genre_words/processed/'
    if value == "love":
        filepath = filepath + 'love.json'
    elif value == "friendship":
        filepath = filepath + 'friendship.json'
    elif value == "determination":
        filepath = filepath + 'determination.json'
    elif value == "honesty":
        filepath = filepath + 'honesty.json'

    return load_vocab(filepath)


def rand_selection(vocab):
    newvocab = {}
    keys = list(vocab.keys())
    randlist = np.random.choice(len(keys), 300, replace=False)
    for index in randlist:
        newvocab[keys[index]] = vocab[keys[index]]
    return newvocab


def get_vocab(genre, value1, value2):
    vocab0, vocab1, vocab2 = {}, {}, {}
    genre = genre.lower()
    value1 = value1.lower()
    value2 = value2.lower()

    #get genre vocab
    vocab0 = get_genre_vocab(genre)
    #get value #1 vocab 
    if value1 != '':
        vocab1 = get_value_vocab(value1)
    #get value #2 vocab 
    if value2 != '':
        vocab2 = get_value_vocab(value2)

    vocab = vocab0 | vocab1 | vocab2
    if len(vocab.keys()) > 300:
        vocab = rand_selection(vocab)
    return vocab


def get_starter(genre):
    if genre == 'science fiction':
        return scifi_starters
    elif genre == "horror":
        return horror_starters
    elif genre == "fantasy":
        return fantasy_starters
    elif genre == "realistic fiction":
        return realfic_starters


f = open(filepath, "a")
for part in parts:
    #create starting prompt
    starters = get_starter(genre)
    startprompt = "Create the " + part + " of a " + genre + " story for grade " + grade + " children. The story should talk about " + values + ". The word length of most words should be no longer than 6 characters. Most sentences should be no longer than 7 words long. Do not end the story."
    if(part == "beginning"):
        story = starters[np.random.randint(0, len(starters))]
    responseprompt = startprompt + '\n' + story

    f.write("============================PROMPT=================================\n")
    f.write(responseprompt + '\n')

    #get the vocab/bags of words
    value_list = values.strip().replace(' ', '').split(',')
    vocab = get_vocab(genre, value_list[0], value_list[1])
    # vocab = None

    #get the model output
    text = run_model(responseprompt, max_tokens, vocab)
    max_tokens = len(tokenizer(text)['input_ids']) + 200
    
    f.write("............................RETURNED.................................\n")
    f.write(text + '\n')

    #if the story has not changed, retry with a filler
    story = story + text
    # if(story == text or text.replace('\n', '') == ''):
    #     if(part == "middle"):
    #         story = story + text + fillers[np.random.randint(0, len(fillers))]
    #         responseprompt = startprompt + '\n' + story

    #         text = run_model(responseprompt, max_tokens, vocab)
    #         max_tokens = len(tokenizer(text)['input_ids']) + 200
    #         story = story + text

    f.write("----------------------------RESULT---------------------------------\n")
    f.write(story + '\n')

for i in range(10):
    continueprompt = "Write the next sentence of the following " + genre + " story for grade " + grade + " children. The story should talk about " + values + ". The word length of most words should be no longer than 6 characters. Most sentences should be no longer than 7 words long. Do not end the story."
    responseprompt = continueprompt + '\n' + story
    
    f.write("============================PROMPT=================================\n")
    f.write(responseprompt + '\n')

    value_list = values.strip().replace(' ', '').split(',')
    vocab = get_vocab(genre, value_list[0], value_list[1])

    text = run_model(responseprompt, max_tokens, vocab)
    max_tokens = len(tokenizer(text)['input_ids']) + 200
    story = story + text

    f.write("............................RETURNED.................................\n")
    f.write(text + '\n')

    f.write("----------------------------RESULT---------------------------------\n")
    f.write(story + '\n')

    if(text == '' or text == "\n"):
        responseprompt = "Give me the next word to the following story. Do not end the story.\n" + story
        next_word = run_model(responseprompt, max_tokens=max_tokens + 10, vocab=vocab, temp=1.0)
        
        responseprompt = "Finish the sentence of the following "  + genre + " story for grade " + grade + " children. The story should talk about " + values + ". The word length of most words should be no longer than 6 characters. Most sentences should be no longer than 7 words long. Do not end the story."
        responseprompt = responseprompt + '\n' + story + ' ' + next_word
        
        f.write("----------------------------ADDED FILLER---------------------------------\n")
        f.write(responseprompt + '\n')

        text = run_model(responseprompt, max_tokens, vocab)
        max_tokens = len(tokenizer(text)['input_ids']) + 200
        story = story + text

endprompt = "Write the end sentence of the following " + genre + " story for grade " + grade + " children. The story should talk about " + values + ". The word length of most words should be no longer than 6 characters. Most sentences should be no longer than 7 words long."
responseprompt = endprompt + story

f.write("============================PROMPT=================================\n")
f.write(responseprompt + '\n')

value_list = values.strip().replace(' ', '').split(',')
vocab = get_vocab(genre, value_list[0], value_list[1])

text = run_model(responseprompt, max_tokens, vocab)
max_tokens = len(tokenizer(text)['input_ids']) + 200
story = story + text

f.write("............................RETURNED.................................\n")
f.write(text + '\n')

f.write("----------------------------RESULT---------------------------------\n")
f.write(story + '\n')

f.close()

#since limit of 300 logit biases need to convert terms like this:
#Rewrite the above text, replacing science fiction terms with fantasy words.

#couple of ways to approach age issue
#could just brute force it by collecting massive collection of commonly used words by the grade group
#could also do a selective choice of words --> ie if the genre is sci-fi and the age group is grade 5,
#we choose the most commonly used sci-fi words in grade 5 books --> this requires a lot of searching + data processing
#could also try to have the LM learn this intrinsically by feeling it more children's stories that are fully labelled
#--> this also requires a lot of searching + data processing

#if more words --> could also include different tenses/conjugations of words
#ex commitment --> commit, committed, commits, commitments, committing

#more lessons
#-->GPT3 probably knows better than you --> need to lead/guide GPT3 step by step
#ex. if GPT3 stops generating --> just need to explicitly ask it to generate a new word with max temperature
#ex. if GPT3 needs more filler words or similar words --> should probably just ask it explicitly