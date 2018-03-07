import math
import operator
from collections import OrderedDict

class Recommender():
    
    base = {}
    inverted_base = None
    similarities_users = None
    similarities_items = None
    
    def __init__(self, base):
        self.base = base
    
    def __euclidian_distance(self, set_of_points, percentage=True):
        '''
            This function will get P1 and P2 and calculate the
            euclidian distance, by taking the square root of the 
            sum of the square of the difference of each coordinate
            sqrt(sum(pow((cip1 - cip2), 2)))
            
            Keyword arguments:
            set_of_points -- Matrix: first position is the point,
                                     second position is the coord
            Ex: [(1, 2, 3), (4, 5, 6)] -> P1 = (1, 2, 3) 
                                          P2 = (4, 5, 6)
        '''
        # This will be the total distance
        sum_difs = 0
        
        # j Is the index of the coordinate being calculated
        for j in range(len(set_of_points[0])):
            # Get the difference of the two coordinates squared
            dif_square = (set_of_points[0][j] - set_of_points[1][j])**2
            # Add this to the sum of differences
            sum_difs += dif_square
        
        # Take the square root of the difference
        distance = math.sqrt(sum_difs)
        
        ''' 
            If the user wants a percentage of equality, calculate
            it. The higher the value, the more alike they are, if 
            the value is 1, they are the same (distance is equal 
            to 0). 
        '''
        if(percentage):
            distance = 1/(1 + math.sqrt(distance))
        
        return distance
    
    def __reverse_base(self):
        '''
            This method will reverse the dictionary, so the secondary keys are
            going to be the primary keys. If the dictionary usually is: 
            user -> item -> rating, it will be item -> user -> rating instead
        '''
        inverted_base = {}
        
        for key, value in self.base.items():
            for key2, value2 in self.base[key].items():
                inverted_base.setdefault(key2, {})
                inverted_base[key2][key] = value2
        
        return inverted_base
    
    def __calculate_similarities(self, base):
        '''
            This function will calculate similarities between all
            primary keys, so it will take the euclidian distance in 
            percentage for each primary key to another. A primary key is
            defined as the first key in the dictionary, the usual base
            keeps a user as primary key and the item he rated as secondary
            key, and finally the rating as a value, so the primary key in this 
            case is the user name.
        '''
        
        # The name of the primary keys 
        primary_keys = []
        # The similarity of primary keys. This dictionary will work like this:
        # distances[p_key1][p_key2] will store the value of the similarity between 
        # primary key 1 and primary key 2
        distances = {}
        
        # For each primary key in the "base", store his name and create a key in
        # the distance dictionary.
        for key, value in base.items():
            primary_keys.append(key)
            distances[key] = {}
        
        # For each primary key, to another (this will create all combinations
        # of primary keys possible, except from one to itself)
        for pk1 in primary_keys:
            for pk2 in primary_keys:
                
                # Making sure it's not the same primary key, so we won't calculate
                # the distance from A to itself. And that we didn't already calculate
                # the rating
                if(pk1 != pk2 and not pk2 in distances[pk1]):
                    # Create a set of points that will be the values 
                    set_of_points = [[], []]
                    # Those points will be the secondary values (ratings) 
                    # present in both primary keys
                    for key, value in base[pk1].items():
                        if(key in base[pk2]):
                            set_of_points[0].append(value)
                            set_of_points[1].append(base[pk2][key])
                    
                    # Then calculate the distance based on all their common ratings
                    dist = self.__euclidian_distance(set_of_points)
                    # And add it to distances, mirrored (A's distance to B
                    # is B's distance to A)
                    distances[pk1][pk2] = dist
                    distances[pk2][pk1] = dist
        
        return distances
    
    def __calculate_similarities_items(self):
        '''
            This will consider the users' ratings as a factor of similarity
            So if a lot of users rate 2 items similarly, the items will have a 
            high similarity
        '''
        
        # If the similarity between all items wasn't calculated, do it.
        if(self.inverted_base == None):
            self.inverted_base = self.__reverse_base()
        
        sim = self.__calculate_similarities(self.inverted_base)
        
        return sim
    
    def __sort_dictionary(self, dict, limit=-1, rev=True):
        '''
            This will return a sorted dictionary. Why? Because it
            can be iterated easily and it is easy to find values.
            
            Keyword arguments:
            dict -- Dictionary to be sorted
            rev -- If true, the first value will be the biggest
            and go in decreasing order
            limimt -- Maximum of items allowed to be returned
        '''
        
        # Create an ordered dictionary, with a list of the items in 
        # "dict" sorted by their values (item in index 1)
        sorted_items = sorted(dict.items(), key=operator.itemgetter(1), reverse=rev)
        
        if(limit > 0):
            sorted_items = sorted_items[:limit]
        
        dict = OrderedDict(sorted_items)
        
        return dict
    
    def calculate_similarity_user_to(self, user, limit=-1):
        '''
            This function will calculate similarities from one user
            to others.
            
            Keyword arguments:
            user -- The user used as base to calculate other similarities
        '''
        
        # If the similarity between all users wasn't calculated, do it.
        if(self.similarities_users == None):
            self.similarities_users = self.__calculate_similarities(self.base)
        
        # Then get only the user's similarity with other users
        unord = self.similarities_users[user]
        # And order it in the dictionary
        ord = self.__sort_dictionary(unord, limit)
        
        return ord

    def calculate_similarity_item_to(self, item, limit=-1):
        '''
            This function will calculate similarities from one item
            to others.
            
            Keyword arguments:
            item -- The item used as base to calculate other similarities
        '''
        
        # If the similarity between all items wasn't calculated, do it.
        if(self.inverted_base == None):
            inverted_base = self.__reverse_base()
        
        # Then get only the item's similarity with other items
        unord = self.__calculate_similarities_items()[item]
        
        # And order it in the dictionary
        ord = self.__sort_dictionary(unord, limit)
    
        return sim_to_ind

    def predict_ratings_by_user_sim(self, user, limit=-1):
        '''
            This function will try to predict the user's rating of the
            movies he still didn't watch, this will use his similarity to
            other users x their ratings as weighted arithmetic mean. So 
            the more similar the other user is to "user" more worth is his
            rating.
            
            Keyword arguments:
            user -- The user used as base 
        '''
        
        # First we need to get a list of similarity between "user" and
        # other users
        sims_user = self.calculate_similarity_user_to(user)
        
        # This will store the value of the similarity of some user * the
        # Rating this user gave.
        weighted_review = {}
        # This will store how much is the sum of the similarity of users
        # for each movie.
        weights_considered = {}
        #This will store the weighted mean, weighted ratings/weights of users
        weighted_mean = {}
        
        # Since we don't really have the name of the movies "user" didn't 
        # watch, we need to get all the movies that only the other users
        # watched , so we start going through the similarity list.
        for key, value in sims_user.items():
            # If there's no similarity with that user, disconsider him
            if(value == 0): continue
            
            # Then for every movie that exists in that other user's ratings
            # but doesn't exists in "user"'s ratings, this will be the movie
            # we will try to predict the rating.
            for key2, value2 in self.base[key].items():
                if(key2 in self.base[user]):
                    continue
                
                if(not key2 in weighted_review):
                    weighted_review[key2] = 0
                    weights_considered[key2] = 0 
                
                weighted_review[key2] += value*value2
                weights_considered[key2] += value
        
        # Then we will finish the weighted mean
        for key in weighted_review.keys():
            weighted_mean[key] = weighted_review[key]/weights_considered[key]
        
        weighted_mean = self.__sort_dictionary(weighted_mean, limit)
        
        return weighted_mean
        
    def predict_ratings_by_item_sim(self, user, limit=-1):
        '''
            This function will try to predict the user's rating of the
            movies he still didn't watch, this will use his similarity to
            other items x his ratings on other items as weighted arithmetic mean. So 
            the more similar the other item is to the one it's being predicted
            more worth is its rating.
            
            Keyword arguments:
            user -- The user used as base 
        '''
        
        # This will store the predicted ratings, calculated by the 
        # weighted mean of the rating of the movies he rated with the
        # similarity to the movie he has to rate
        weighted_mean = {}
        
        # If the similarity between all items wasn't calculated, do it.
        if(self.similarities_items == None):
            self.similarities_items = self.__calculate_similarities_items()
        
        # For every item in the similarities, if he didn't rate yet
        for key, value in self.similarities_items.items():
            if(not key in self.base[user]):
                sum_reviews = 0
                sum_sim = 0
                for key2, value2 in self.base[user].items():
                    # This will be the sum of the ratings he gave to
                    # every other movie * the similarity of those movies
                    # to the current movie being predicted 
                    sum_reviews += value2*value[key2]
                    # This will be the sum of the similarities being 
                    # considered.
                    sum_sim += value[key2]
                    
                weighted_mean[key] = sum_reviews/sum_sim
        
        # Order the dictionary and get only the first n
        weighted_mean = self.__sort_dictionary(weighted_mean, limit)
        
        return weighted_mean  
