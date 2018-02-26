# Recommendation System 1
A simple recommendation system based on users similarity and items similarity. It was made using the knowledge of one of [Udemy's Recommendation System's course](https://www.udemy.com/inteligencia-artificial-sistemas-de-recomendacao-em-python/) 

## Table of Contents
* [What does it do?](#what-does-it-do)
* [Requirements](#requirements)
* [How does it work?](#how-does-it-work)
  * [Similarity of Users](#similarity-of-users)

## What does it do?
The actual project is the class Recommender that will only require a dictionary of dictionaries, in which the primary key can be an user, for example, and the secondary key can be an object that this user rated (this is shown in the picture below). The goal of the program is to try to analyze the behavior and similarities between users or items and generate the rating (or other feedback) this user would give.

|Usuários/Filmes|Freddy vs Jason|The Bourne Ultimatum|Star Trek|The Terminator|Norbit|Star Wars|
|     :---:     |     :---:     |        :---:       |  :---:  |     :---:    | :---:|  :---:  |
|      Ana      |      2.5      |         3.5        |   3.0   |      3.5     | 2.5  |   3.0   |
|     Marcos    |      3.0      |         3.5        |   1.5   |      5.0     | 3.5  |   3.0   |
|     Pedro     |      2.5      |         3.0        |         |      3.5     |      |   4.0   |
|    Claudia    |               |         3.5        |   3.0   |      4.0     | 2.5  |   4.5   |
|    Adriano    |      3.0      |         4.0        |   2.0   |      3.0     | 2.0  |   3.0   |
|    Janaina    |      3.0      |         4.0        |   3.0   |      5.0     | 3.5  |   3.0   |
|    Leonardo   |               |         4.5        |         |      4.0     | 1.0  |         |

So the goal is to correlate users that rate the same for the same movies and use them to predict the rating of an user for a movie that he didn't watch.

## Requirements

* Python 3.6 

## How does it work?
There were implemented 2 approaches for predicting results: using similarity of users (Ana, Marcos, Pedro, for example) or using similarity of items (Freddy vs Jason, The Bourne Ultimatum, for example).

### Similarity of Users
To calculate how close the ratings of the users are, for each user the similarity will be the euclidean distance between all their ratings. 
\
The formula for the [Euclidean Distance](https://en.wikipedia.org/wiki/Euclidean_distance) is the following:

![euclidean distance formula](https://wikimedia.org/api/rest_v1/media/math/render/svg/dc0281a964ec758cca02ab9ef91a7f54ac00d4b7)

In python (being p1 the first point, p2 second point):
```
sum = 0

for i in range(len(p1)):
    sum += (p1[i] - p2[i])**2

result = math.sqrt(sum)
```
\
So, for example, if I want the similarity between Ana and Pedro, this would be:

|Usuários/Filmes|Freddy vs Jason|The Bourne Ultimatum|Star Trek|The Terminator|Norbit|Star Wars| Euc |
|     :---:     |     :---:     |        :---:       |  :---:  |     :---:    | :---:|  :---:  |:---:|
|      Ana      |      2.5      |         3.5        |   3.0   |      3.5     | 2.5  |   3.0   |     |
|     Pedro     |      2.5      |         3.0        |         |      3.5     |      |   4.0   |     |
|       d²      |      0.0      |         0.5        |    -    |      0.0     |  -   |   1.0   |1.22 |

The Euclidean distance is 1.22, but this doesn't tell much, so we will need to get this to a more intuitive number. We want the number of the similarity to get closer to 1 when the they are very close (euclidean is near 0), and to get as close to 0 as possible when the distance is bigger, so we can use the following formula: similarity = 1/(1 + euclidean). If the euclidean is 0 (they are very close), the similarity is 1, if the euclidean is big (they are very distant), the similarity gets closer to 0, so for the previous scenario, the similarity between Pedro and Ana is 0.45 (1/2.22).


The next step is to use this similarity as a weight for future ratings: if the other user is more similar to the user (Let's say Pedro, for example) we are evaluating now, his ratings are more important, since when it comes around ratings he's closer than others. Then with the similarities of other users to Pedro, we need to calculate the rating every other user gave to the movie we want to find out multiplied by the value of similarity, and taking an weighted average mean of this.


In this scenario, Pedro's rating predicted for Star Trek will be:
\
(Ana's rating * Ana's similarity to Pedro + Marcos' rating * Marcos' similarity to Pedro + Claudia's rating * Claudia similarity to Pedro + Adriana's rating * Adriana's similarity to Pedro + Janaina's rating * Janaina's similarity to Pedro)/(Ana's similarity to Pedro + Marcos' similarity to Pedro + Claudia similarity to Pedro + Adriana's similarity to Pedro + Janaina's similarity to Pedro)


## [Still working on this readme]
