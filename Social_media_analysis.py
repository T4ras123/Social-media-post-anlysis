import csv
import matplotlib as mpl
from collections import Counter
from geopy.geocoders import Nominatim


"""
Most active country
The most popular tweets  
"""


def find_hashtags(top_n):
    global test_data
    hashtags = [] 
    for tweet in test_data:
        all_words = tweet[0].split(' ')
        for word in all_words:
            if word[0] == '#':
                hashtags.append(word)
    print(Counter(hashtags).most_common(top_n))


def find_words(top_m, length=5):
    global test_data
    words = []
    for tweet in test_data:
        all_words = tweet[0].split(' ')
        for word in all_words:
            if (len(set(word).intersection(special_symbols)) == 0 and
                    len(word)>=length):
                words.append(word.lower())
    print(Counter(words).most_common(top_m))


def most_active_places(number):
    countries = {'Worldwide': 0,
                 'NoInfo': 0}
    countries_list = []
    loc = Nominatim(user_agent="GetLoc")
    for post in test_data:
        getLoc = loc.geocode(post[1])
        flag = 0
        if post[1] in countries.keys():
            countries[post[1]] += 1
        else:
            for country in countries_list:
                try:
                    getLoc1 = loc.geocode(country)
                    if (abs(getLoc.latitude - getLoc1.latitude) < 1
                            and abs(getLoc.longitude - getLoc1.longitude) < 1):
                        countries[country] += 1
                        flag += 1
                        break
                    else:
                        continue
                except AttributeError:
                    countries.update({post[1]: 1})
                    countries_list.append(post[1])
            if flag == 0:
                countries.update({post[1]: 1})
                countries_list.append(post[1])
    sorted_countries = sorted(countries)
    print(sorted_countries)


splited_data = []

with open(r"D:\Vova\Education\Uni\Intro to CS\Project\tweets_raw.csv", "r", encoding="utf8") as file:
    data = csv.reader(file)
    for row in data:
        splited_data.append([" ".join(element.split())
                             if element != '' else 'NoInfo'
                             for element in row][2:])
    

header = splited_data[0]

dataset = splited_data[1:]

test_data = dataset[1:100]

special_symbols = r'!@"#№$;:%^&?/\|*()_-+=><.,{}[]~`'


find_hashtags(5)
find_words(5, 10)
most_active_places(5)

#%%
