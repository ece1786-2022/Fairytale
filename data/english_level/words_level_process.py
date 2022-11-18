import pandas as pd

def english_level_type_A(filename = "A2.txt", output_filename = "processed_words_level/A2.txt", start_line = 0):
    words = []
    with open(filename, "r", encoding="utf8") as f:
        lines = f.readlines()        
        for i in range(0, len(lines)):
            line = lines[i]        
            words.extend(line.strip().split(" "))
    words = set([w.lower().replace("(",'').replace(")",'')
                 .replace("]",'').replace("[",'').replace(",","").
                 replace(";","").replace(":","").replace(".","") for w in words if len(w)>1])
    return words
# pd.DataFrame.from_dict(data=output, orient='index').to_csv(output_filename, header=False)

def english_level_type_B(filename = "B2.txt", output_filename = "processed_words_level/B2.txt"):
    words = []
    with open(filename, "r", encoding="utf8") as f:
        lines = f.readlines()          
        for i in range(0, len(lines)):
            line = lines[i].strip()
            if line.count('/')>1:
                words.extend([line.strip().split(" ")[0]])
    words = set([w.lower().replace("(",'').replace(")",'')
                 .replace("]",'').replace("[",'').replace(",","").
                 replace(";","").replace(":","").replace(".","") for w in words if len(w)>1])
    return words

A1 = english_level_type_A("A1.txt", output_filename = "processed_words_level/A1.txt")
A2 = english_level_type_A("A2.txt", output_filename = "processed_words_level/A2.txt")
B1 = english_level_type_A("B1.txt", output_filename = "processed_words_level/B1.txt")
C = english_level_type_A("C1_C2.txt", output_filename = "processed_words_level/C.txt")
B2 = english_level_type_B("B2.txt", output_filename = "processed_words_level/B2.txt")

A2 = A2 - A1
B1 = B1 - A1 - A2
B2 = B2 - B1 - A2 - A1
C = C - B2 - B1 - A2 - A1
for level, words in enumerate([A1, A2, B1, B2, C]):
    with open("processed_words_level/level_{}.txt".format(level),'w') as f:   
        for w in words:
            try:
                f.write(w + '\n')
            except:
                pass
