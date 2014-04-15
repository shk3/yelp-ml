'''
Created on Apr 14, 2014

@author: Amod Samant
@updated: George Hongkai Sun
'''
import json
import pprint
import re
from string import punctuation
import csv

def create_csv(review_list,user_dict,business_dict):
        
    headers = [
        'review_id', 'true_stars', 'word_count', 
        'word_cap_count', 'text_polarity',
        'biz_stars', 'biz_review_count', 
        'usr_avrstars', 'usr_review_count', 'usr_fans', 
    ]
    with open('feature_review.csv', 'w') as csvfile:
        csvwriter = csv.DictWriter(csvfile, 
            fieldnames=headers, 
            delimiter=',',
            quotechar='"', 
            quoting=csv.QUOTE_MINIMAL,
            lineterminator='\n')
        csvwriter.writeheader()
        
        i = 0
        for review_obj in review_list:
            i += 1
            feature_data = {
                'review_id': i,
                'true_stars': review_obj['stars'],
            }
            
            # Text Features
            review_text = review_obj['text']
            [num_of_words,cap_words_count] = calc_words_plus_cap(review_text)
            feature_data['word_count'] = num_of_words
            feature_data['word_cap_count'] = cap_words_count
            feature_data['text_polarity'] = review_obj['text_polarity']
            
            # Reference to business' features
            biz_obj = business_dict[review_obj['business_id']]
            feature_data['biz_stars'] = biz_obj['stars']
            feature_data['biz_review_count'] = biz_obj['review_count']
            # TODO: Bag of Categories
            
            # Reference to user's features
            usr_obj = user_dict[review_obj['user_id']]
            feature_data['usr_avrstars'] = usr_obj['average_stars']
            feature_data['usr_review_count'] = usr_obj['review_count']
            feature_data['usr_fans'] = usr_obj['fans']
            # TODO: Bag of Elites and yelping_since
            #pprint.pprint(feature_data)
            csvwriter.writerow(feature_data)
               
    
    print len(review_list)
    
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




def build_review_list():
    # Reading the review dataset
    f = open('yelp_academic_dataset_review.json','r');
    
    review_list = []
    for line in f:
        review_obj = json.loads(line)
        review_list.append(review_obj)
#    pprint.pprint(review_list)

    f.close()
    return review_list

def build_business_dict():
    biz_categories = {}
    # Reading the business dataset
    f = open('yelp_academic_dataset_business.json','r');
    
    business_dict = {}
    for line in f:
        business_obj = json.loads(line)
        business_dict[business_obj['business_id']] = business_obj
        for cat in business_obj['categories']:
            biz_categories[cat] = biz_categories.get(cat, 0) + 1
    #pprint.pprint(business_dict)
    f.close()
    return business_dict, biz_categories

def build_user_dict():
    usr_elites = {}
    # Reading the user dataset
    f = open('yelp_academic_dataset_user.json','r');

    user_dict = {}
    for line in f:
        user_obj = json.loads(line)
        user_dict[user_obj['user_id']] = user_obj
        for elite in user_obj['elite']:
            usr_elites[elite] = usr_elites.get(elite, 0) + 1
    #pprint.pprint(user_dict)
        
    f.close()
    return user_dict, usr_elites

# Stat the elites of users and categories of businesses
# Store businesses and users as dict for random access
business_dict, biz_categories = build_business_dict()
user_dict, usr_elites = build_user_dict()
pprint.pprint(biz_categories)
pprint.pprint(usr_elites)
print 'Categories: %d' % (len(biz_categories.keys()))
print 'Elites: %d' % (len(usr_elites.keys()))

# List of dictionary objects(each JSON object)
review_list = []
review_list = build_review_list()

create_csv(review_list,user_dict,business_dict)
