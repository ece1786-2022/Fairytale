import csv
import pandas as pd
import process_age
import process_genre

def story_type_A(filename = "data\story_7.txt", output_filename = "data\processed_data/story_7.tsv", start_line = 0):
    with open(filename, "r", encoding="utf8") as f:
        lines = f.readlines()        
        story_number = 0
        story = ""
        output = {}
        for i in range(start_line, len(lines)):
            line = lines[i]
            if "." in line and line.strip().split(".")[0].isnumeric():
                if len(story)>0:
                    output[story_number] = story            
                story_number = int(lines[i].strip().split(".")[0])
                story = ""            
            else:
                if len(line)>1:
                    story = story + lines[i].strip()
    pd.DataFrame.from_dict(data=output, orient='index').to_csv(output_filename, header=False, sep='\t')

def story_type_B(filename = "story_7.txt", output_filename = "processed_data/story_7.csv", start_line = 0):
    with open(filename, "r", encoding="utf8") as f:
        lines = f.readlines()        
        story_number = 0
        story = ""
        output = {}
        for i in range(start_line, len(lines)):
            line = lines[i]        
            if "." in line and line.strip().split(".")[0].isnumeric():
                if len(story)>0:
                    output[story_number] = story            
                story_number = int(lines[i].strip().split(".")[0])
                story = ""            
            else:
                if len(line)>1:
                    story = story + lines[i].strip()
    pd.DataFrame.from_dict(data=output, orient='index').to_csv(output_filename, header=False)
    
# story_type_A(filename = "story_7.txt", output_filename = "processed_data/story_7.csv")
# story_type_A(filename = "story_3.txt", output_filename = "processed_data/story_3.csv")
# story_type_A(filename = "story_2.txt", output_filename = "processed_data/story_2.csv")
# story_type_B(filename = "story_2.txt", output_filename = "processed_data/story_2.csv")

def add_genre_to_text_data(filename = "processed_data\story_2.tsv"):
    data = pd.read_csv(filename, header=None, names=['id', 'text'], sep='\t')
    genres = []
    ages = []
    is_for_kids = []
    for text in data['text']:
        genre = process_genre.get_genre(text)
        genres.append(genre)
        ages.append(round(process_age.calculate_grade(text)))
        is_for_kids.append(process_age.is_for_kids(text))
        
    se = pd.Series(genres)
    data['genre'] = se.values
    se = pd.Series(ages)
    data['ages'] = se.values
    se = pd.Series(is_for_kids)
    data['kids'] = se.values
    
    data.to_csv(filename[:-4] + "_with_age_genre.tsv", sep='\t')

def process_childrenstories():
    filename="data\childrenstories.txt"
    output_filename="data\processed_data/childrenstories.tsv"
    numrows = 72

    df = pd.read_table('childrenstories.tsv', nrows=numrows)
    for i in range (numrows):
        #strip whitespace
        text = df['text'][i].strip()
        df['text'][i] = text

        #add age
        df['age'] = round(process_age.calculate_grade(text))

    df.to_csv("processed_data/childrenstories.tsv", sep='\t')

add_genre_to_text_data("processed_data\story_3.tsv")



