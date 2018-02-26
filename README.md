# Recommendation System 1
A simple recommendation system based on users similarity and items similarity. It was made using the knowledge of [one of Udemy's Recommendation System's course](https://www.udemy.com/inteligencia-artificial-sistemas-de-recomendacao-em-python/) 

## Table of Contents
* [What does it do?](#what-does-it-do)
* [Requirements](#requirements)
* [How does it work?](#how-does-it-work)
  * [Similarity of Users](#similarity-of-users)
  * [Similarity of Items](#similarity-of-items)
* [Which one to use?](#which-one-to-use)
* [Examples](#examples)

## What does it do?
The actual project is the class Recommender that will only require a dictionary of dictionaries, in which the primary key can be an user, for example, and the secondary key can be an object that this user rated (this is shown in the picture below). The goal of the program is to analyze the behavior and similarities between users or items and generate the rating (or other feedback) this user would give.

|  Users/Movies |Freddy vs Jason|The Bourne Ultimatum|Star Trek|The Terminator|Norbit|Star Wars|
|     :---:     |     :---:     |        :---:       |  :---:  |     :---:    | :---:|  :---:  |
|      Ana      |      2.5      |         3.5        |   3.0   |      3.5     | 2.5  |   3.0   |
|     Marcos    |      3.0      |         3.5        |   1.5   |      5.0     | 3.5  |   3.0   |
|     Pedro     |      2.5      |         3.0        |         |      3.5     |      |   4.0   |
|    Claudia    |               |         3.5        |   3.0   |      4.0     | 2.5  |   4.5   |
|    Adriano    |      3.0      |         4.0        |   2.0   |      3.0     | 2.0  |   3.0   |
|    Janaina    |      3.0      |         4.0        |   3.0   |      5.0     | 3.5  |   3.0   |
|    Leonardo   |               |         4.5        |         |      4.0     | 1.0  |         |

With the data from the table, for example, it's possible to correlate users that rate the same for the same movies and use them to predict the rating of an user for a movie that he didn't watch.

## Requirements

* Python 3.6 

## How does it work?
2 approaches were implemented for predicting results: using similarity of users (Ana, Marcos, Pedro, for example) or using similarity of items (Freddy vs Jason, The Bourne Ultimatum, for example).

### Similarity of Users
To calculate how close the ratings of the users are, for each user the similarity will be the euclidean distance between all their ratings. 

The formula for the [Euclidean Distance](https://en.wikipedia.org/wiki/Euclidean_distance) is the following:

![euclidean distance formula](https://wikimedia.org/api/rest_v1/media/math/render/svg/dc0281a964ec758cca02ab9ef91a7f54ac00d4b7)

In python (being p1 the first point, p2 second point):

```
sum = 0

for i in range(len(p1)):
    sum += (p1[i] - p2[i])**2

result = math.sqrt(sum)
```

So, for example, if I want the similarity between Ana and Pedro, this would be:

|Usuários/Filmes|Freddy vs Jason|The Bourne Ultimatum|Star Trek|The Terminator|Norbit|Star Wars| Euc |
|     :---:     |     :---:     |        :---:       |  :---:  |     :---:    | :---:|  :---:  |:---:|
|      Ana      |      2.5      |         3.5        |   3.0   |      3.5     | 2.5  |   3.0   |     |
|     Pedro     |      2.5      |         3.0        |         |      3.5     |      |   4.0   |     |
|       d²      |      0.0      |         0.5        |    -    |      0.0     |  -   |   1.0   |1.22 |

The Euclidean distance is 1.22, but this doesn't tell much, so we will need to get this to a more intuitive number. We want the number of the similarity to get closer to 1 when the they are very close (euclidean is near 0), and to get as close to 0 as possible when the distance is bigger, so we can use the following formula: similarity = 1/(1 + euclidean). If the euclidean is 0 (they are very close), the similarity is 1, if the euclidean is big (they are very distant), the similarity gets closer to 0, so for the previous scenario, the similarity between Pedro and Ana is 0.45 (1/2.22).


The next step is to use this similarity as a weight for future ratings: if the other user is more similar to the user (Let's say Pedro, for example) we are evaluating now, his ratings are more important, since when it comes around ratings he's closer than others. Then with the similarities of other users to Pedro, we need to calculate the rating every other user gave to the movie we want to find out multiplied by the value of similarity, and taking an weighted average mean of this.


In this scenario, Pedro's rating predicted for Star Trek will be:

> (Ana's rating * Ana's similarity to Pedro + Marcos' rating * Marcos' similarity to Pedro + Claudia's rating * Claudia similarity to Pedro + Adriana's rating * Adriana's similarity to Pedro + Janaina's rating * Janaina's similarity to Pedro)/(Ana's similarity to Pedro + Marcos' similarity to Pedro + Claudia similarity to Pedro + Adriana's similarity to Pedro + Janaina's similarity to Pedro)

### Similarity of Items
There's also the option to do the same thing with items inverting the base, so instead of "the user Ana gave the movie Freddy vs Jason the rating 2.5" it would be "the movie Freddy vs Jason received the rating 2.5 by the user Ana", as you can see in the table below. 

|      Users/Movies    |  Ana  | Marcos | Pedro | Claudia | Adriano | Janaina | Leonardo |
|         :---:        | :---: | :---:  | :---: |  :---:  |  :---:  |  :---:  |  :---:   |
|    Freddy vs Jason   |  2.5  |  3.0   |  2.5  |         |   3.0   |   3.0   |          |
| The Bourne Ultimatum |  3.5  |  3.5   |  3.0  |   3.5   |   4.0   |   4.0   |   4.5    |
|       Star Trek      |  3.0  |  1.5   |       |   3.0   |   2.0   |   3.0   |          |
|     The Terminator   |  3.5  |  5.0   |  3.5  |   4.0   |   3.0   |   5.0   |   4.0    |
|         Norbit       |  2.5  |  3.5   |       |   2.5   |   2.0   |   3.5   |   1.0    |
|       Star Wars      |  3.0  |  3.0   |  4.0  |   4.5   |   3.0   |   3.0   |          |

If we were to apply the euclidean distance between the items (in this case movies) we would see which movies were rated similarly, if 2 movies are rated similarly the weight of the ratings of this movie is more important then others. So, for example, if we wanted to find out the rating Star Wars will receive from Leonardo, we first need to calculate the similarity to other movies (in the table below I'll just show the example for one movie)


|      Users/Movies    |  Ana  | Marcos | Pedro | Claudia | Adriano | Janaina | Leonardo |  Euc  |
|         :---:        | :---: | :---:  | :---: |  :---:  |  :---:  |  :---:  |  :---:   | :---: |
|         Norbit       |  2.5  |  3.5   |       |   2.5   |   2.0   |   3.5   |   1.0    |       |
|       Star Wars      |  3.0  |  3.0   |  4.0  |   4.5   |   3.0   |   3.0   |          |       |
|           d²         |  0.25 |  0.25  |   -   |   4.0   |   1.0   |   0.25  |    -     |  0.14 |

This means that Norbit is rated way different than Star Wars, so its rating isn't going to matter that much. After calculating all the similarities we can take the weighted average mean of the other movies ratings (that Leonardo rated) with their similarity to the movie being rated to figure out how much would it be:

> (The Bourne Ultimatum' rating * The Bourne Ultimatum' similarity to Star Wars + The Terminator's rating * The Terminator similarity to Star Wars + Norbit's rating * Norbit's similarity to Star Wars)/(The Bourne Ultimatum' similarity to Star Wars + The Terminator similarity to Star Wars + Norbit's similarity to Star Wars)

Since the user only rated The Bourne Ultimatum, The Terminator and Norbit, those were the only ones that were taken in consideration. So the idea is "If he rated high for a movie that is similar (in ratings) to the movie being evaluated, he'll rate this movie high as well".

## Which one to use?

The user similarity approach is a good choice when you have enough information about an user, since you need a lot of ratings (or any other feedback) to define an accurate similarity to other people, but if the user is new to the database, you won't have this much information, so you can't predict anything for him in the start.

On the other hand the item similarity is a good option if you have a lot of feedback about the items, since it can calculate the similarity between each item and an item the user gave a positive feedback, to suggest him the one most similar, but if you have, for example, an e-commerce website, where it's extremally difficult that a great percentage of the users will buy every item, to give the feedback, the similarity is not going to be properly defined, again because of the lack of information. One way to avoid this is categorizing items, probably a great percentage of a specific group of users will buy a set of items (the category book will have a great feedback from a group of users, the category eletronics will have a great feedback from another group of users, and etc).

## Examples

There are 2 demo projects: example_base.py and movielens_rec.py

* example_base.py: The one used as example in this readme, it's a small base, and it's great to show a little bit of the difference between the two approaches. Note that both approached have a nice result, because most of the users rated most of the movies.

* movielens_rec.py: Movielens is a [public dataset](https://grouplens.org/datasets/movielens/) that has movies' ratings for a lot of users. This dataset shows how item similarity might not be a good approach without any other thing to avoid the lack of feedback, since the *average* quantity of ratings/user is 105.71 (yeah I made it calculate to be sure) movies rated out of 1682 as opposing to 5 movies rated out of 6 in the previous dataset.
