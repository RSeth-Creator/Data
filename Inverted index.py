# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 09:22:40 2021

@author: rajseth
"""
import re 
import pandas as pd 
import nltk
df = pd.read_csv('tweet.txt', delimiter = "\t",header=None)
df.columns = ['doc_id','tweets']
df.head()
#preprocessing
df['tweets'] = df['tweets'].str.lower()
df['tweets'] = df['tweets'] .map(lambda x: re.sub(r'[^A-Za-z0-9]+', ' ', x))

#WhitespaceTokenizer used to tokenize the words in a sentence
# WordNetLemmatizer used to find the root words
#Creating posting list for the corpus

w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()
posting_list = {}
for i, doc in enumerate(df['tweets']):
    for term in w_tokenizer.tokenize(doc):
         l_term = lemmatizer.lemmatize(term)
         if l_term in posting_list:
            posting_list[l_term].add(df['doc_id'][i])
         else: posting_list[l_term] = {df['doc_id'][i]}
         
posting_list = {key: val for key, val in sorted(posting_list.items(),
                                                key = lambda x: x[0])}


#Function to find out the posting list for any item

def item(text):
    x = list(posting_list[text])
    return x

#Merge Algorithm for AND operation

def merge_and(list1,list2):
    
    out=[]
    for i in range(len(list1)):
        for j in range(len(list2)):
            if list1[i] == list2[j]:
                out.append(list1[i])
            
    return out

merge_and(item('egg'),item('cheese')) 
item('egg')
item('cheese')

# used dataset (id , tweets)
'''
576 	Bandaging up my paper-cuts , having cheesecake for dinner , and calling it a night . We're doin it big here in NYC .
896	    Bacon/cheddar slider topped w/fried egg & Blue cheese slider topped w/avocado & purple cherokee tomato
680	    Nacho w/ cheese on my shirt ! Uggghhh
072	    you aint nuffin but a piece of cheese without the corners .. in other words , you will never be a slice .
904	    TAG_USERNAME TAG_USERNAME Mmmm ... cheese ... dreaming of a squirrel burger with cheese !
905	    Mmmm cheese
976	    TAG_USERNAME 1st off I'm like 1 year younger than u , 2nd age is just a number , 3rd ima cater ur wedding wit patty n cheese
896	    RT TAG_USERNAME : I want a steak and cheese egg roll right now .
264	    think imma eat some cheesecake befor i lay down ... Havent had it in a while
368	    A mixed one mostly strawberry peach little white cherry dr pepper or coke etc
584	    My stomach was yelling at me telling me to get my ass up nd get somethin to eat . So I went nd got cheesesticks nd a waterbottle .
075	    chocolate mint , cookies & cream , very berry strawberry , and chocolate caramel~ all blend perfectly in my mouth
184	    I think I want some cheese eggs and pancakes ... but will I cook ? Where's my gf . This ain't right to make such a hard decision
080	    TAG_USERNAME Totally . It's also good on fish , chicken , veggies . Oh , and desserts . Drizzling it over strawberry tarts for a party tonight ! -C
090	    TAG_USERNAME I want to get the strawberry cheesecake and candy bear . When does the 2 for $ 38 expire ?
778	    Made myself some scrambled eggs with cheese and bacon bits
360	    TAG_USERNAME you could try it but its not great haha if i could recommend , get the strawberry one thats ma fave !
576	    TAG_USERNAME then im 100% pure strawberry flavoured hmmm tasty
516	    just had the most beautiful pink coloured raspberry , strawberry & banana smoothie
376	    I went swimming , then ate asparagus bacon egg cheese biscuit goodness , then watched Date Night . It was ... it was good . TAG_FINAL_HASHTAGS
280	    Cheese hashbrowns , turkey bacon , veggie tofu scramble , rice , french toast , scrambled eggs , strawberries & cantaloupe . TAG_FINAL_HASHTAGS
168	    TAG_HASHTAGS using cream cheese icing on chocolate cake .. just use vanilla or strawberry
664	    RT TAG_USERNAME : RT TAG_USERNAME : Pancakes , bacon , eggs w/ cheese , & hashbrown casserole on deck TAG_HASHTAGS < ~i want sum !!!!! Ok it's good too       
904	    TAG_USERNAME TAG_USERNAME Mmmm ... cheese ... dreaming of a squirrel burger with cheese !

'''