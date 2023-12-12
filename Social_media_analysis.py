import csv
import matplotlib.pyplot as plt
from collections import Counter


"""
Most active country 
"""


# Main function that brings everything together
def main():
    inpt = get_user_input()
    do_analysis(inpt)
    do_continue()


# Continue function for UE
def do_continue():
    ipt = input("Do you wanna continue? Yes/No")
    if ipt.lower() == 'yes':
        main()
    else:
        print('okay, bye')
        exit()


# Function that shows first and last 5 rows of data
def show_data():
    global splited_data, special_symbols, words, hashtags, \
         header, test_data
    with (open(r"tweets_raw.csv",
               "r", encoding="utf8") as file):
        data = list(csv.reader(file))
        for i in range(6):
            print([" ".join(element.split(' '))
                   if element != '' else 'NoInfo'
                   for element in data[i]])
        print('------------------------------------------------\n'
              '------------------------------------------------')
        a = -5
        while a < 0:
            print([" ".join(element.split(' '))
                   if element != '' else 'NoInfo'
                   for element in data[a]])
            a += 1


# Function opens a file and gets words from tweets
def every_word(length):
    global words
    path = r"tweets_raw.csv"
    with open(path, "r", encoding="utf8") as file:
        data = csv.reader(file)
        for row in data:
            all_words = row[1].split(" ")
            while '' in all_words:
                all_words.remove('')
            for word in all_words:
                if len(set(word).intersection(special_symbols)) == 0 and len(word) >= length:
                    words.append(word.lower())


# Function opens a file and gets hashtags from tweets
def every_hashtag():
    global hashtags
    with (open(r"tweets_raw.csv", "r", encoding="utf8") as file):
        data = list(csv.reader(file))
        for row in data:
            all_words = row[1].split(" ")
            while '' in all_words:
                all_words.remove('')
            for word in all_words:
                if word[0] == '#':
                    hashtags.append(word)


# Function opens a file and finds an engagement with every tweet
def find_engagement():
    global engagement
    with (open(r"tweets_raw.csv", "r", encoding="utf8") as file):
        data = csv.reader(file)
        for row in list(data)[1:]:
            eng = int(int(row[4])*2 + int(row[5]))
            engagement.append(eng)


# Function gets user input
def get_user_input():
    global inputs
    user_input = input("What do you want to know?\n"
                       "A - The most popular words\n"
                       "B - the most popular hashtags\n"
                       "C - Popularity of the tweets\n"
                       "P - Most popular places\n"
                       "S - Show data\n"
                       "E - exit\t")
    if user_input.lower() not in inputs:
        print("invalid input")
        get_user_input()
    else:
        return user_input.lower()


# Does analysis according to input
def do_analysis(user_input):
    if user_input == 'e':
        print("okay, bye")
        exit()
    elif user_input.lower() == 'a':
        number = int(input("\nHow many top words?\n"))
        length = int(input("\nMinimum word length\n"))
        find_words(number, length)
    elif user_input.lower() == 'b':
        number = int(input("\nHow many top hashtags?\n"))
        find_hashtags(number)
    elif user_input.lower() == 'c':
        popular_tweets()
    elif user_input.lower() == 's':
        show_data()
    else:
        n = int(input("How many top places?"))
        most_active_places(n)


# Draws a matplotlib pie
def draw_pie(values, names):
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.pie(values, labels=names, autopct='%.0f%%')

    plt.show()


# Draws a matplotlib bars
def draw_bars(x_axis, y_axis, x_name='', y_name="", title=""):
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.bar(list(x_axis)[:15], y_axis[:15])
    ax.set_ylabel(y_name)
    ax.set_xlabel(x_name)
    ax.set_title(title)
    plt.show()


# Analyzes hashtags and draws top of them
def find_hashtags(top_n):
    global hashtags
    every_hashtag()
    u, w = [], []
    p = Counter(hashtags).most_common(top_n)
    for i in p:
        w.append(i[0])
        u.append(i[1])
    w.append('Else')
    u.append(len(hashtags)-len(u))
    draw_pie(u, w)
    draw_bars(w[:-1], u[:-1], 'top hashtags',
              'usage', f'top {top_n} hashtags')


# Analyzes words and draws top of them
def find_words(top_m, length=5):
    global words
    every_word(length)
    w = []
    u = []
    p = Counter(words).most_common(top_m)
    for i in p:
        w.append(i[0])
        u.append(i[1])
    w.append('Else')
    u.append(len(words)-len(u))
    draw_pie(u, w)
    draw_bars(w[:-1], u[:-1], 'top words',
              'usage', f'top {top_m} words with len >= {length}')


# Finds most active places and displays them
def most_active_places(n):
    global places
    with (open(r"tweets_raw.csv", "r", encoding="utf8") as file):
        data = csv.reader(file)
        for row in list(data)[1:]:
            if row[2] in places.keys():
                places[row[2]] += 1
            elif row[2] == '':
                places['No Info'] += 1
            else:
                places.update({row[2]: 1})
    pls = sorted(places.items(), key=lambda x: x[1], reverse=True)
    countries = [pls[i][0] for i in range(n)]
    users = [pls[i][1] for i in range(n)]
    draw_bars(countries, users, 'Top places',
              'Tweets', 'Most active places')


# Analyzes engagement
def popular_tweets():
    global test_data, engagement
    find_engagement()
    srt_eng = set(engagement)
    for i in srt_eng:
        number_of_tweets.append(engagement.count(i))
    draw_bars(srt_eng, number_of_tweets, 'Engagement',
              "Number of tweets", "Engagement to tweets ratio")


special_symbols = r'!@"#№$;:%^&?/\|*()_-+=><.,{}[]~`'

inputs = ['a', 'b', 'c', 'e', 's', 'p']
hashtags = []
words = []
splited_data = []
header = []
test_data = []
engagement = []
number_of_tweets = []
places = {
    "Worldwide": 0,
    "No Info": 0
}
main()

#%%
