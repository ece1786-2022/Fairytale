import csv
import pandas as pd


def story_7(filename = "story_7.txt", output_filename = "processed_data/story_7.csv"):
    with open(filename, "r") as f:
        lines = f.readlines()
        start_point = 4
        story_number = 0
        story = ""
        output = {}
        for i in range(start_point, len(lines)):
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
    
story_7()