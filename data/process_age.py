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

# text = "In a faraway land, a young prince named Edmund lived in a castle with his parents, the King and Queen. Edmund was loved and adored by all who knew him, but even so, the prince's life was far from perfect. Edmund had a deep-seated longing to find true love and he thought he had finally found it with a beautiful princess from a nearby kingdom. But when Edmund's parents found out about their relationship, they forbid him from ever seeing her again. Edmund was devastated and his heart was filled with anger and resentment. Unable to cope with his emotions, Edmund decided to run away from the castle. He traveled for weeks, eventually finding himself in a distant forest. There, he encountered a mysterious old man who told him of a powerful magic that could make his dreams come true. The old man warned Edmund that the magic was dangerous and could bring destruction if misused, but Edmund was desperate and wanted to take the chance. He agreed to the old man's terms and was given an enchanted staff with which he could cast powerful spells. Using the staff, Edmund created an illusion of himself that appeared to the princess and convinced her to come with him. But the deception was soon discovered and Edmund was forced to run away. Guilt-ridden and ashamed, Edmund had to find a way to atone for his wrong-doing. He set out on a journey of self-discovery and was eventually able to find peace and redemption. He returned home to his parents, who welcomed him with open arms, and was able to make amends with the princess, who had forgiven him for his mistake. Edmund and the princess eventually married, and Edmund's parents were happy to see their son so content. Edmund and the princess lived happily ever after, and they taught their children the importance of true love and the power of forgiveness."
# text2 = "A long time ago and far, far away, there was a magical kingdom called the Kingdom of Love. The King and Queen of Love ruled the kingdom with kindness and compassion. All the people of the kingdom were happy and contented. One day, however, an evil wizard named Greed appeared and cast a spell on the kingdom, turning the people against one another. Greed wanted to take control of the kingdom and rule with his own selfish desires.The King and Queen were heartbroken by the deception of their people and knew they had to do something to save the kingdom. They decided to go on a quest to find a magical artifact that could break Greed’s spell and restore peace to the kingdom.The King and Queen traveled far and wide, searching for the magical artifact. Finally, after many months of searching, they found a magical crystal that contained the power to break any spell. The King and Queen returned to the Kingdom of Love and held the crystal up high. As the crystal glowed with a bright, white light, the people of the kingdom were freed from Greed’s spell. The King and Queen were overjoyed and thanked the people of the kingdom for their loyalty and love. With the spell broken, the Kingdom of Love was restored and the people of the kingdom celebrated with joy and happiness. The King and Queen had learned a valuable lesson that love, not deception, is the most powerful force in the world. From then on, the King and Queen ruled their kingdom with love, kindness, and understanding. The End."

# print(calculate_grade(text2))
# print_scores(text2)
