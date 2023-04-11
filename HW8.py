# Your name: Zack Eisman
# Your student id: 33829100
# Your email: zeisman@umich.edu
# List who you have worked with on this homework: Liam Kendall

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    restaurants_dict = {}
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()

    cur.execute('SELECT restaurants.name, categories.category, buildings.building, restaurants.rating FROM restaurants JOIN categories ON restaurants.category_id = categories.id JOIN buildings ON restaurants.building_id = buildings.id')
    for row in cur:
        #print(row)
        restuarant_name = row[0]
        restaurants_dict[restuarant_name] = {}
        category = row[1]
        building = row[2]
        rating = row[3]
        restaurants_dict[restuarant_name]['category'] = category
        restaurants_dict[restuarant_name]['building'] = building
        restaurants_dict[restuarant_name]['rating'] = rating
    #print(restaurants_dict)
    return restaurants_dict

        

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    restaurant_type_dict = {}
    plt.figure(1, figsize=(8,8))
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()

    cur.execute('SELECT restaurants.category_id, categories.category, COUNT(*) FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY categories.category')
    for row in cur:
        category = row[1]
        count = row[2]
        restaurant_type_dict[category] = count
    #print(restaurant_type_dict)
    sorted_by_count = sorted(restaurant_type_dict.items(), key = lambda x: x[1])
    restaurant_types = []
    counts = []
    for tup in sorted_by_count:
        restaurant_types.append(tup[0])
        counts.append(tup[1])
    plt.barh(restaurant_types, counts)
    plt.xlabel('Number of Restaurants')
    plt.xlim([0, 5])
    plt.ylabel('Restaurant Categories')
    plt.suptitle('Types of Restaurants on South University Ave')
    plt.show()
    return restaurant_type_dict


def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    building_restaurants = []

    cur.execute(f"SELECT buildings.building, restaurants.name, restaurants.rating FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id WHERE buildings.building = {building_num} ORDER BY restaurants.rating DESC")
    for row in cur:
        building_restaurants.append(row[1])
    return building_restaurants


#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    highest_ratings = []
    plt.figure(1, figsize = (8,8))
    plt.subplot(211)

    
    cur.execute('SELECT categories.category, avg(restaurants.rating) FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY categories.category ORDER BY avg(restaurants.rating)')
    categories = []
    ratings1 = []
    highest_rating1 = 0
    highest_category = ''
    for row in cur:
        #print(row)
        if row[1] > highest_rating1:
            highest_rating1 = row[1]
            highest_category = row[0]
        categories.append(str(row[0]))
        ratings1.append(row[1])
    highest_ratings.append((highest_category, highest_rating1))
    plt.barh(categories, ratings1)
    plt.xlabel('Ratings')
    plt.xlim([0, 5])
    plt.ylabel('Categories')
    plt.title('Average Restaurant Ratings by Category')

    
    cur.execute('SELECT buildings.building, avg(restaurants.rating) FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id GROUP BY buildings.building ORDER BY avg(restaurants.rating)')
    i = 0
    buildings = []
    ratings2 = []
    highest_rating2 = 0
    highest_building = ''
    for row in cur:
        #print(row)
        if row[1] > highest_rating2:
            highest_rating2 = row[1]
            highest_building = row[0]
        buildings.append(str(row[0]))
        ratings2.append(row[1])
    highest_ratings.append((highest_building, highest_rating2))
    plt.subplot(212)
    plt.barh(buildings, ratings2)
    plt.xlabel('Ratings')
    plt.xlim([0, 5])
    plt.ylabel('Buildings')
    plt.title('Average Restaurant Ratings by Building')
    
    plt.show()
    #print(highest_ratings)
    return highest_ratings


#Try calling your functions here
def main():
    load_rest_data('South_U_Restaurants.db')
    #plot_rest_categories('South_U_Restaurants.db')
    find_rest_in_building('1140', 'South_U_Restaurants.db')

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
