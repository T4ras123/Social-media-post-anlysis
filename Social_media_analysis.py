import csv
import matplotlib.pyplot as plt
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
    w = []
    u = []
    for tweet in test_data:
        all_words = tweet[0].split(' ')
        for word in all_words:
            if (len(set(word).intersection(special_symbols)) == 0 and
                    len(word)>=length):
                words.append(word.lower())
    p = Counter(words).most_common(top_m)
    print(p)
    for i in p:
        w.append(i[0])
        u.append(i[1])
    print(w, u)

    fig, ax = plt.subplots()
    ax.pie(u, labels=w)
    plt.show()



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
    fig, ax = plt.subplots()
    ax.bar(list(srt_eng)[:15], number_of_tweets[:15])
    ax.set_ylabel('Number of posts')
    ax.set_xlabel('Engagement')
    ax.set_title("Engagement to tweets ratio")
    plt.show()

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


# find_hashtags(5)
find_words(10, 13)
# popular_tweets()






#%%
