# Fairytale

## Introduction

Children’s tales are extremely important in child development as they improve literacy skills, communication skills, and assist with forming ideas of culture/race. Each story contains lessons that highlight important societal values and show children what is right and wrong. 

Our project, Fairytale, aims to allow anyone to generate a children’s tale given a simple prompt, the desired genre and grade level of the story, and some core values they want to appear in the text.

We believe the most appropriate approach is through machine learning as this is a text generation task. Based on the assignments and demonstrations from class, we think using transformer models like GPT-2 and GPT-3 would be most suitable. 

## Data

We collected 1079 stories from various sources on the Internet. These texts vary from 100-500 words in length. Stories are labeled with the genre, and the grade level. Some stories are also labeled with the values present in the text.

We also used a public dataset of 32032 plot summaries in addition to our collected stories for fine-tuning.

## Model

We used GPT-3 DaVinci-003 as the primary model to generate stories with a zero-shot learning approach, and a pre-trained GPT-2 model as the baseline but with fine-tuning to improve results. 
To begin generation, we start with the initial prompt shown in Figure 5. The prompt consists of the given genre, grade and values. Additionally, we restrict the sentence and word length relative to the grade to generate more grade appropriate text. Lastly, we append a randomly selected story starter to the initial prompt.

For the baseline model, we fine-tuned a pre-trained GPT-2. The model was fine-tuned in two steps. First, we fine-tune it on the public dataset and the collected dataset entries without a value label. Then, we fine-tune the model on the collected dataset entries with value labels.

## Results

We defined a scoring rubric that looks at 6 aspects of the story to evaluate our stories. It looks at the plot, grammar, flow, and how well the story captures values, genre, and grade level. Using this rubric, we scored stories from both models. GPT-3 scored an average of 94/100 while GPT-2 averaged 61/100. 

GPT-3 performed well across all categories, but excelled in capturing the given genre and values, scoring almost perfect in both categories. It was also able to generate meaningful plots that flowed smoothly, creating stories that were hard to distinguish from a real person’s work.

GPT-2 did decently in grammar and captured the genre somewhat, scoring 80s for both categories. However, it struggled to write coherent stories that flowed. The final result was more of a collection of words and sentences.
