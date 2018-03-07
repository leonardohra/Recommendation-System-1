# -*- coding: utf-8 -*-

from recommendation import Recommender

# This function generates a csv with the information on a dictionary
def dictionary_to_csv(dict, file_name):
    with open(file_name, 'w') as file:
        for key, value in dict.items():
            for key2, value2 in value.items():
                file.write('{0},{1},{2}\n'.format(key, key2, value2))

# This function reads a csv and generates a dictionary
def csv_to_dictionary(file_name):
    dict = {}
    with open(file_name, 'r') as file:
        lines = file.read().splitlines()
        for line in lines:
            pars = line.split(',')
            dict.setdefault(pars[0], {})
            dict[pars[0]][pars[1]] = float(pars[2])
    
    return dict

# This function prints what's inside a dictionary
def nice_print_sing(single_dict, limit=-1):
    count = 0
    
    for key, item in single_dict.items():
        count += 1
        print('\t' + key + ':', item)
        
        if(limit != -1 and count == limit):
            break

# Creates the dictionary with the base in "data_users.csv"
users_ratings = csv_to_dictionary('./Data/Sample Base/data_users.csv')

# Instantiates the Recommender
rec = Recommender(users_ratings)
# Chooses the user to recommend
user = 'Leonardo'

# Predicts the rating of unwatched movies using user similarity
recommendations = rec.predict_ratings_by_user_sim(user)
print(user, 'Pela similaridade de usuarios')
nice_print_sing(recommendations)

#Predicts the rating of unwatched movies using item similarity
recommendations = rec.predict_ratings_by_item_sim(user)
print(user, 'Por similaridade de itens')
nice_print_sing(recommendations)