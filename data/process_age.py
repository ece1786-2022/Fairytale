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
            


def is_for_kids(text='', levels_address = 'english_level/processed_words_level/'):
    # returns 1 for kids, 0 for adults
    A = []
    B = []
    C = []
    with open(levels_address + "level_0.txt",'r') as f:
        A.extend(f.readlines())
        A = [w.strip() for w in A]
    with open(levels_address + "level_1.txt",'r') as f:
        B.extend(f.readlines())
        B = [w.strip() for w in B]
    with open(levels_address + "level_2.txt",'r') as f:
        B.extend(f.readlines())
        B = [w.strip() for w in B]
    with open(levels_address + "level_3.txt",'r') as f:
        C.extend(f.readlines())
        C = [w.strip() for w in C]    
    with open(levels_address + "level_4.txt",'r') as f:
        C.extend(f.readlines())
        C = [w.strip() for w in C]    
    A_counts = 0
    B_counts = 0
    C_counts = 0
    words = text.replace('.','').split(' ')
    for word in words:
        if word in A:
            A_counts += 1
        else:
            if word in B:
                B_counts += 1
            else:
                if word in C:
                    C_counts += 1
                else:
                    A_counts += 1
    A_ratio = A_counts / len(words) # easy words
    B_ratio = B_counts / len(words) 
    C_ratio = C_counts / len(words) # advanced words  
    # print(A_ratio)
    # print(B_ratio)
    # print(C_ratio)
     
    if A_ratio < 0.80 or C_ratio>0.05:
        return 0
    return 1

text = "There was once a group of five friends, who were all incredibly clever and inventive. They were always working together to come up with innovative solutions to the problems that faced their small town. One day, a mysterious object appeared in a field near the town. It was a large, round, black disc that no one had ever seen before. The five friends immediately went to investigate, and they quickly realized that the disc was no ordinary object. Using their cleverness and teamwork, the five friends managed to figure out that the disc was actually a spaceship. After a few days of careful examination, they were able to figure out how to open the door and enter the ship. Inside they found a strange and futuristic control room, filled with strange technology they had never seen before. They soon realized that with this technology, they could travel to distant galaxies and explore the unknown. The five friends quickly realized that they could be pioneers of a new space exploration mission, and that together they could unlock the mysteries of the universe. With excitement and enthusiasm, they began to plan their journey. And so, with the help of their cleverness, friendship and teamwork, the five friends set off on a journey to explore the universe, and to find out what lies beyond."
text2 = "Once upon a time, there were five best friends. They were all very smart and clever, and they loved to work together to solve the problems of their small town. One day, while they were playing outside, they saw something strange in the field. It was a big, round, black disc! No one had ever seen anything like it before. The five friends were so excited and curious. They decided to investigate. To their surprise, they found out that the disc was actually a spaceship! The five friends used their intelligence and teamwork to figure out how to open the door and go inside the spaceship. Inside, they discovered a mysterious control room with strange technology. The five friends knew that this was an incredible opportunity. They could use this technology to explore the universe! With enthusiasm, they began to plan their intergalactic journey. So, with the help of their intelligence, friendship, and teamwork, the five friends set off to explore the universe and discover its mysteries."
# text3 = "I knew that something very special was about to happen.It all started the day I arrived at the space station. I was a young, curious scientist, eager to explore the unknown. I met my fellow scientists, and we all had the same mission: to find out what was making strange noises coming from deep in the space station.We searched high and low, but no matter how hard we tried, we couldn’t find the source of the mysterious noise. Until one day, I spotted something strange out of the corner of my eye. It was an alien spaceship!My team and I were both scared and excited. We knew that this could be our big chance to make a real difference. We had to be clever and use teamwork if we wanted to investigate the spaceship and find out what was making the noise.So, we used our cleverness, friendship, and teamwork to get inside the spaceship. What we found inside was a surprise. We discovered a tiny alien creature, one that had been trapped inside the spaceship for years.The alien was so excited to be free, and thanked us for rescuing him. We all celebrated with a big hug. We had not only solved the mystery of the strange noise, but we had also made a new friend!"

print(calculate_grade(text))
print_scores(text)

print(calculate_grade(text2))
print_scores(text2)
