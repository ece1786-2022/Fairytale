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

# # Stories for kides
# # text = '''Once upon a time there was a dear little girl who was loved by every one who looked at her, but most of all by her grandmother, and there was nothing that she would not have given to the child. Once she gave her a little cap of red velvet, which suited her so well that she would never wear anything else. So she was always called Little Red Riding Hood. One day her mother said to her, "Come, Little Red Riding Hood, here is a piece of cake and a bottle of wine. Take them to your grandmother, she is ill and weak, and they will do her good. Set out before it gets hot, and when you are going, walk nicely and quietly and do not run off the path, or you may fall and break the bottle, and then your grandmother will get nothing. And when you go into her room, don't forget to say, good-morning, and don't peep into every corner before you do it.'''    
# # text = '''The wolf thought to himself, "What a tender young creature. What a nice plump mouthful, she will be better to eat than the old woman. I must act craftily, so as to catch both." So he walked for a short time by the side of Little Red Riding Hood, and then he said, "see Little Red Riding Hood, how pretty the flowers are about here. Why do you not look round. I believe, too, that you do not hear how sweetly the little birds are singing. You walk gravely along as if you were going to school, while everything else out here in the wood is merry.'''
# # text = '''A long time ago and far, far away an old woman was sitting in her rocking chair thinking how happy she would be if she had a child. Then, she heard a knock at the door and opened it. A lady was standing there and she  said, "If you let me in, I will grant you a wish." The old woman let the woman in firstly because she felt pity, secondly because she knew what she'd wish for...a child. After she washed the lady up and fed her, she saw that she was really beautiful.'''
# text = '''One day while walking along the sea shore, Suzy discovered a mermaid washed up on the shore. She was surprised and went forward to take a look at the mermaid. The Mermaid was injured and she laid on the sea shore unconscious.

# Suzy had never seen a mermaid before. She had heard stories of mermaids from books. The mermaid looks like a human with two hands but her lower body is that of a fish. She looked beautiful. One of the mermaid’s fins was injured, she must have gotten injured from abrasion with sharp edges.

# Suzy decided to bring the mermaid home to tend to her injuries. She brought the mermaid home and put her into the bath tub. As mermaid may not be accustom to the environment since it was a sea creature, Suzy quickly turns on the water to fill up the bath tub with water to place her inside.'''

# # Stories for adults
# # text = '''Having an increased awareness of the possible differences in expectations and behaviour can help us avoid cases of miscommunication, but it is vital that we also remember that cultural stereotypes can be detrimental to building good business relationships. Although national cultures could play a part in shaping the way we behave and think, we are also largely influenced by the region we come from, the communities we associate with, our age and gender, our corporate culture and our individual experiences of the world. The knowledge of the potential differences should therefore be something we keep at the back of our minds, rather than something that we use to pigeonhole the individuals of an entire nation.'''
# # text = '''An American or British person might be looking their client in the eye to show that they are paying full attention to what is being said, but if that client is from Japan or Korea, they might find the direct eye contact awkward or even disrespectful. In parts of South America and Africa, prolonged eye contact could also be seen as challenging authority. In the Middle East, eye contact across genders is considered inappropriate, although eye contact within a gender could signify honesty and truthfulness.'''
# # text = '''If we want to know where our capability for complex language came from, we need to look at how our brains are different from other animals. This relates to more than just brain size; it is important what other things our brains can do and when and why they evolved that way. And for this there are very few physical clues; artefacts left by our ancestors don't tell us what speech they were capable of making. One thing we can see in the remains of early humans, however, is the development of the mouth, throat and tongue. By about 100,000 years ago, humans had evolved the ability to create complex sounds. Before that, evolutionary biologists can only guess whether or not early humans communicated using more basic sounds.'''

# print(is_for_kids(text)) # 1 is for kids, 0 is for adults



# filename = "data\processed_data\story_2.tsv"
# data = pd.read_csv(filename, header=None, names=['id', 'text'], sep='\t')

# ages = []
# for text in data['text']:
#     ages.append(round(calculate_grade(text)))

# print(ages)

# print(text)
# print(calculate_grade(text))
# print_scores(text)


