import csv
import pandas as pd


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
                    story = story + " " + lines[i].strip().replace("’", "'")
    pd.DataFrame.from_dict(data=output, orient='index').to_csv(output_filename, header=None, sep='\t')
    
story_type_A(filename = "data\story_7.txt", output_filename = "data\processed_data/story_7.tsv")
story_type_A(filename = "data\story_3.txt", output_filename = "data\processed_data/story_3.tsv")
story_type_A(filename = "data\story_2.txt", output_filename = "data\processed_data/story_2.tsv")