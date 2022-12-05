from transformers import GPT2Tokenizer, GPT2Model
import openai as ai
import numpy as np
from numpy import random
import json
import sys

API_KEY = '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'
orgID = "org-FamdhS456bzvQnGH0fUnw6aQ"
URL = 'https://api.openai.com/v1/completions'
filepath = "results/davinci003_evalstories.txt"

ai.organization = orgID
ai.api_key = API_KEY
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

maxtokenlist = [100, 120, 140, 200, 300, 500]
maxwordlength = ['6', '7', '8', '9', '10', 'no limit']
maxsentencelength = ['7', '9', '11', '13', '15', 'no limit']

story = ""
parts = ['beginning']

scifi_starters = ['In', 'Before', 'Deep in space', 'Somewhere in a galaxy far, far away', 'Out in space', 'Out of nowhere', 'There was a', 'After years of' , 'In the skies', 'A smart', 'The machines', 'The aliens', 'One day', 'Eureka!']
horror_starters = ['In', 'Before', 'Two dark figures', 'He was being chased', 'She was being chased', 'She awoke suddenly', 'He awoke suddenly', 'It was a dark, and rainy day', 'Somewhere deep underground', 'In an ancient', 'In a remote', 'In an old', 'Long ago', 'There was once', 'A long time ago']
fantasy_starters = ['In', 'Before', 'A long time ago and far,', 'Once upon a time,', 'There is a', 'In a faraway land', 'There was once a', 'Two figures stood', 'Across the seas', 'For many years', 'In a kingdom', 'King', 'Queen', 'In a tower', 'In a castle']
realfic_starters = ['In', 'Before', 'There is a', 'I knew that something very special was about to happen', 'Today', 'Dear Diary', 'On a', 'It was a', 'Somewhere in', 'One sunny morning', 'One hot afternoon', 'Today was', 'Today will']

fillers = ['The', "A"]
# fillers = ['In', 'The', 'Later', "But", "However,", "Then,", "So,", "In fact,", "Moreover", "After", 'Soon', 'Meanwhile', 'While', 'At the same time', 'Eventually', "A"]
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


def get_vocab(genre, value1, value2=None):
    vocab0, vocab1, vocab2 = {}, {}, {}
    genre = genre.lower()
    value1 = value1.lower()
    
    if value2 is not None:
        value2 = value2.lower()
    else:
        value2 = ''

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


def age_restriction(age, prompt):
    wordlength = maxwordlength[int(age)-1]
    sentencelength = maxsentencelength[int(age)-1]

    if wordlength != "no limit":
        prompt = prompt + " The word length of most words should be no longer than " + wordlength + " characters."
    if sentencelength != "no limit":
        prompt = prompt + " Most sentences should be no longer than " + sentencelength + " words long."
    prompt = prompt + " Do not end the story."

    return prompt

#===================================Start============================================
def main():
    
    #set values, genre, grade from user args
    genre = str(sys.argv[1])
    grade = str(sys.argv[2])
    v1 = str(sys.argv[3])
    v2 = str(sys.argv[4])

    values = v1
    if v2 != 'none':
        values = values + ', ' + v2

    if genre == "scifi":
        genre = "science fiction"
    if genre == "realfic":
        genre = "realistic fiction"

    max_token_amt = maxtokenlist[int(grade)-1]
    max_tokens = max_token_amt
    
    f = open(filepath, "a")

    #creating starter prompt
    part = parts[0]
    starters = get_starter(genre)

    #getting the max word length and max sentence length
    wordlength = maxwordlength[int(grade)-1]
    sentencelength = maxsentencelength[int(grade)-1]

    #get the values and vocab for each value
    value_list = values.strip().replace(' ', '').split(',')
    value_sentence = values
    vocab = {}
    if len(value_list) > 1:
        value_sentence = value_list[0] + ", and " + value_list[1]

    if len(value_list) > 1:
        vocab = get_vocab(genre, value_list[0], value_list[1])
    else:
        vocab = get_vocab(genre, value_list[0])

    #put all the parts together to make starterprompt
    startprompt = "Create the " + part + " of a " + genre + " story for grade " + grade + " children. The story should talk about " + value_sentence + "." 
    startprompt = age_restriction(grade, startprompt)

    if(part == "beginning"):
        story = starters[np.random.randint(0, len(starters))]
    responseprompt = startprompt + '\n' + story
    print("STARTING PROMPT: " + responseprompt)

    f.write("============================PROMPT=================================\n")
    f.write(responseprompt + '\n')

    #get the model output
    text = run_model(responseprompt, max_tokens, vocab)
    story = story + text
    max_tokens = len(tokenizer(responseprompt + story)['input_ids']) + max_token_amt

    # f.write("............................RETURNED.................................\n")
    # f.write(text + '\n')
    # f.write("----------------------------RESULT---------------------------------\n")
    # f.write(story + '\n')


    #middle of the story --> write sentence by sentence
    print("WRITING MIDDLE OF STORY")
    for i in range(10):
        continueprompt = "Write the next sentence of the following " + genre + " story for grade " + grade + " children. The story should talk about " + value_sentence + "."
        continueprompt = age_restriction(grade, continueprompt)
        continueprompt = continueprompt + '\n' + story
        
        # f.write("============================PROMPT=================================\n")
        # f.write(responseprompt + '\n')

        text = run_model(continueprompt, max_tokens, vocab)
        story = story + text
        max_tokens = len(tokenizer(continueprompt + story)['input_ids']) + max_token_amt

        #if we don't get anything from the model --> run again but force it to add a new word with temp = 1.0
        if(text == '' or text == "\n"):
            fillprompt = "Write the next word to the following story.\n" + story
            max_tokens = len(tokenizer(story)['input_ids']) + 50
            next_word = run_model(fillprompt, max_tokens, vocab=vocab, temp=1.0)
            
            if next_word == '' or next_word == '\n':
                next_word = fillers[np.random.randint(len(fillers))]

            fillprompt = "Finish the sentence of the following "  + genre + " story for grade " + grade + " children. The story should talk about " + value_sentence + "."
            fillprompt = age_restriction(grade, fillprompt)
            fillprompt = fillprompt + '\n' + story + ' ' + next_word
            
            # f.write("----------------------------ADDED FILLER---------------------------------\n")
            # f.write(fillprompt + '\n')

            max_tokens = len(tokenizer(fillprompt)['input_ids']) + max_token_amt
            text = run_model(fillprompt, max_tokens, vocab)
            story = story + ' ' + next_word + text

        # f.write("............................RETURNED.................................\n")
        # f.write(text + '\n')
        # f.write("----------------------------RESULT---------------------------------\n")
        # f.write(story + '\n')


    #end of the story
    print("WRITING END OF STORY")

    endprompt = "Write the ending of the following " + genre + " story for grade " + grade + " children. The story should talk about " + value_sentence + "."
    endprompt = age_restriction(grade, endprompt)
    responseprompt = endprompt + story

    # f.write("============================PROMPT=================================\n")
    # f.write(responseprompt + '\n')

    text = run_model(responseprompt, max_tokens, vocab)
    story = story + text

    # f.write("............................RETURNED.................................\n")
    # f.write(text + '\n')

    f.write("----------------------------RESULT---------------------------------\n")
    f.write(story + '\n\n')

    f.close()

if __name__ == "__main__":
    main()

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