import csv
import matplotlib.pyplot as plt
from collections import Counter
from geopy.geocoders import Nominatim


"""
Most active country 
"""


def get_user_input():
    global inputs
    user_input = input("What do you want to know?\n"
                       "A - The most popular words\n"
                       "B - the most popular hashtags\n"
                       "C - Popularity of the tweets\n"
                       "E - exit")
    if user_input.lower() not in inputs:
        print("invalid input")
        get_user_input()
    elif user_input.lower() == 'a':
        number, length = int(input("How many top words?")), int(input("Minimum word length"))
        find_words(number, length)
    elif user_input.lower() == 'b':
        number = int(input("How many top hashtags?"))
        find_hashtags(number)
    elif user_input.lower() == 'c':
        popular_tweets()
    else:
        print("okay")
        exit()



def draw_pie(values, names):
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.pie(values, labels=names, autopct='%.0f%%')
    plt.show()


def draw_bars(x_axis, y_axis, x_name='', y_name="", title=""):
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.bar(list(x_axis)[:15], y_axis[:15])
    ax.set_ylabel(y_name)
    ax.set_xlabel(x_name)
    ax.set_title(title)
    plt.show()


def find_hashtags(top_n):
    global test_data
    u, w = [], []
    hashtags = []
    for tweet in test_data:
        all_words = tweet[0].split(' ')
        for word in all_words:
            if word[0] == '#':
                hashtags.append(word)

    p = Counter(hashtags).most_common(top_n)
    for i in p:
        w.append(i[0])
        u.append(i[1])
    draw_pie(u, w)


def find_words(top_m, length=5):
    global test_data
    words = []
    w = []
    u = []
    for tweet in test_data:
        all_words = tweet[0].split(' ')
        for word in all_words:
            if (len(set(word).intersection(special_symbols)) == 0 and
                    len(word) >= length):
                words.append(word.lower())
    p = Counter(words).most_common(top_m)
    for i in p:
        w.append(i[0])
        u.append(i[1])

    draw_pie(u, w)


def most_active_places():
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


def popular_tweets():
    engagement = []
    number_of_tweets = []
    global test_data
    for tweet in test_data:
        eng = int(int(tweet[3])*2 + int(tweet[4]))
        engagement.append(eng)
    srt_eng = set(engagement)
    for i in srt_eng:
        number_of_tweets.append(engagement.count(i))
    draw_bars(srt_eng, number_of_tweets, 'Engagement',
              "Number of tweets", "Engagement to tweets ratio")


splited_data = []


with open(r"D:\Vova\Education\Uni\Intro to CS\Project\tweets_raw.csv", "r", encoding="utf8") as file:
    data = csv.reader(file)
    for row in data:
        splited_data.append([" ".join(element.split())
                             if element != '' else 'NoInfo'
                             for element in row][2:])
    

header = splited_data[0]

dataset = splited_data[1:]

test_data = dataset[1:100000]

special_symbols = r'!@"#№$;:%^&?/\|*()_-+=><.,{}[]~`'

inputs = ['a', 'b', 'c', 'e']

get_user_input()
