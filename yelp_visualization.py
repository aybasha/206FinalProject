import os
import sys
import json
import sqlite3
import matplotlib.pyplot as plt

#Visualization
def visualize(file):
    data = json.loads(f.read())
    cities = ['Boston', 'New York', 'Miami', 'Detroit', 'Los Angeles']
    ratings = [data['Boston'],data['New York'],data['Miami'],data['Detroit'],data['Los Angeles']]

    x = []
    for i, value in enumerate(cities):
        x.append(i)

    plt.xlabel("City")
    plt.ylabel("Rating")
    plt.title("Business Ratings")
    bars = plt.bar(x, ratings, color=['black', 'red', 'green', 'blue', 'orange'])
    position1 = 'center'
    position2 = 'bottom'
    for bar in bars:
        position0 = bar.get_x() + ((bar.get_width())/2)
        plt.text(position0, bar.get_height(), bar.get_height(), ha=position1, va=position2)
    plt.xticks(x, cities)
    plt.show()


f = open('ratings.json')
visualize(f)
