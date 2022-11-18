import pandas as pd
import textstat as ts

def print_scores(text):
    #indicates approximate grade 
    print("Flesch Kincaid Grade ", ts.flesch_kincaid_grade(text))
    #indicates approximate grade 
    print("Smog Index ", ts.smog_index(text))
    #indicates approximate grade level - 1
    print("Automated Readability ", ts.automated_readability_index(text))
    #indicates approximate grade level
    print("Coleman Liau Index ", ts.coleman_liau_index(text))
    #indicates approximate grade level
    print("Linsear Write Formula ", ts.linsear_write_formula(text))
    #score of <4.9 means 4th grade or lower, score of 5-5.9 means grade 5-6
    print("Dale Chall Readability Score ", ts.dale_chall_readability_score(text))
    #indicates approximate grade level (meant for grade 4 or lower)
    print("Spache Readability ", ts.spache_readability(text))
    #prints the estimated text standard
    print("Text Standard ", ts.text_standard(text))
    #number of difficult words in the text
    print("Difficult Words ", ts.difficult_words(text))
    return

def calculate_grade(text):
    f = filter(str.isdigit, ts.text_standard(text))

    textstandard_avg = 0
    count = 0
    for each in f:
        textstandard_avg = textstandard_avg + int(each)
        count+=1
    textstandard_avg = float(textstandard_avg/count)

    grade = ts.flesch_kincaid_grade(text) + \
            ts.smog_index(text) + \
            ts.automated_readability_index(text) + \
            ts.coleman_liau_index(text) + \
            ts.linsear_write_formula(text) + \
            ts.dale_chall_readability_score(text) + \
            ts.spache_readability(text) + \
            textstandard_avg
    
    return grade/8
            

filename = "data\processed_data\story_2.tsv"
data = pd.read_csv(filename, header=None, names=['id', 'text'], sep='\t')

ages = []
for text in data['text']:
    ages.append(round(calculate_grade(text)))

print(ages)

# print(text)
# print(calculate_grade(text))
# print_scores(text)
