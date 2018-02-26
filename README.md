# Recommendation System 1
A simple recommendation system based on users similarity and items similarity. It was made using the knowledge of one of [Udemy's Recommendation System's course](https://www.udemy.com/inteligencia-artificial-sistemas-de-recomendacao-em-python/) 

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

## [Still working on this readme]
