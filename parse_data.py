'''
Created on Apr 3, 2014

@author: Amod Samant
'''
import json
import pprint
import re
from string import punctuation
import csv

def create_csv(review_dict,user_dict,business_dict):
        
    headers = ['word_count,word_cap_count']    
    with open('feature_review.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=" ", lineterminator = '\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(headers)
     
        for review_obj in review_dict:
            feature_data = [`review_obj['review_wc']`+","+`review_obj['review_cap_wc']`]
            #pprint.pprint(feature_data)
            csvwriter.writerow(feature_data)
               
    headers = ['avg_stars,fans,review_count']    
    with open('feature_user.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=" ", lineterminator = '\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(headers)
     
        for user_obj in user_dict:
            feature_data = [`user_obj['average_stars']`+","+`user_obj['fans']`+","+`user_obj['review_count']`]
            #pprint.pprint(feature_data)
            csvwriter.writerow(feature_data)        
            
    headers = ['stars,total_reviews']    
    with open('feature_business.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=" ", lineterminator = '\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(headers)
     
        for business_obj in business_dict:
            feature_data = [`business_obj['stars']`+","+`business_obj['review_count']`]
            #pprint.pprint(feature_data)
            csvwriter.writerow(feature_data)
            
    
    
    print len(review_dict)
    print len(user_dict)
    print len(business_dict)
    
    return 

def calc_words_plus_cap(text_string):
    
    # cap_word_count: Count of capital first  letter words in the review text
    cap_word_count = 0
    
    reg_exp = re.compile(r'[{}]'.format(punctuation))
    new_strs = reg_exp.sub(' ',text_string)
    
    for w in new_strs:
        if w[0].isupper():
            cap_word_count +=1
    
    # word_len: Count of total words in review text
    word_len = len(new_strs.split())
    
    return word_len,cap_word_count




def build_review_dict():
    # Reading the review dataset
    f = open('yelp_academic_dataset_review.json','r');
    
    for line in f:
        review_obj = json.loads(line)
        
        # review_text: Maintains individual review text per object
        review_text = review_obj['text']
        
        [num_of_words,cap_words_count] = calc_words_plus_cap(review_text)
        
        # Adding review text word count and capital word count in dictionary object
        review_obj['review_wc'] = num_of_words
        review_obj['review_cap_wc'] = cap_words_count
        
        review_dict.append(review_obj)
        
#    pprint.pprint(review_dict)

    f.close()
    return review_dict

def build_business_dict():
    # Reading the business dataset
    f = open('yelp_academic_dataset_business.json','r');
    
    for line in f:
        business_obj = json.loads(line)
        business_dict.append(business_obj)
        
    #pprint.pprint(business_dict)
    f.close()
    return business_dict

def build_user_dict():
    
    # Reading the user dataset
    f = open('yelp_academic_dataset_user.json','r');

    for line in f:
        user_obj = json.loads(line)
        user_dict.append(user_obj)
        
    #pprint.pprint(user_dict)
        
    f.close()
    return user_dict

# List of dictionary objects(each JSON object)
review_dict = []
review_dict = build_review_dict()

business_dict = []
business_dict = build_business_dict()

user_dict = []
user_dict = build_user_dict()

create_csv(review_dict,user_dict,business_dict)
