# -*- coding: utf-8 -*-

from recommendation import Recommender

# This function prints what's inside a dictionary
def nice_print_sing(single_dict, limit=-1):
    count = 0
    
    for key, item in single_dict.items():
        count += 1
        print('\t' + key + ':', item)
        
        if(limit != -1 and count == limit):
            break


# Generate a dictionary with the csv file
def load_base(path_to_items, path_to_data):
    movies = {}
    
    for line in open(path_to_items):
        #Pars[0] -> movie code
        #Pars[1] -> movie name
        pars = line.split('|')
        movies[pars[0]] = pars[1]
    
    base = {}
    
    for line in open(path_to_data):
        #Pars[0] -> user code
        #Pars[1] -> movie code
        #Pars[2] -> review
        pars = line.split('\t')
        base.setdefault(pars[0], {})
        base[pars[0]][movies[pars[1]]] = float(pars[2])
    
    return movies, base
    
# Generates the base with u.item e u.data
movies, base = load_base('./Data/Movielens Base/u.item', './Data/Movielens Base/u.data')
user_id = '101'

# Instantiate the recommender
rec = Recommender(base)

#Predict the ratings for the top 30 movies the user might want to watch
recommendations = rec.predict_ratings_by_user_sim(user_id, 30)

print(user_id, 'Por similaridade de usuarios')
nice_print_sing(recommendations)

#Predict the ratings for the top 30 movies the user might want to watch
recommendations = rec.predict_ratings_by_item_sim(user_id, 30)

print(user_id, 'Por similaridade de itens')
nice_print_sing(recommendations)