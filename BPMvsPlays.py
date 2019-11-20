import matplotlib.pyplot as plt
import csv
from collections import defaultdict
import pprint
import math
# percent of artists from whole


class Song:
    def __init__(self, title, genre, bpm, plays):
        self.title = title
        self.genre = genre
        self.bpm = bpm
        self.plays = plays




songs = []

genres = {}

genre_other = []
list_of_genres = defaultdict(list)

# % of artists plays
with open('bpmvsplays.csv', newline="\n") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        if row[1] in genres:
            genres[row[1]] += 1
        else:
            genres[row[1]] = 1

        songs.append(Song(row[0], row[1], round(float(row[2])), row[3]))







fig, ax = plt.subplots()

x = []
y = []

length_of_genres = {}


for item in genres:

    length_of_genres[item] = genres[item]


# get 10 most common genres
for counter in range(9):

    temp = 0

    # item is the genre, temp is the # of appearances
    # find the largest # of appearances

    for item in length_of_genres:
        if temp < length_of_genres[item]:
            largest = item
            temp = length_of_genres[item]

    # remove it from the remaining genres
    del length_of_genres[largest]
    print(largest)
    x.clear()
    y.clear()

    for song in songs:
        if song.genre == largest:
            x.append(int(song.bpm))
            y.append(int(song.plays))
            songs.remove(song)

    ax.scatter(x, y, label=largest)


for i in length_of_genres:
    for item in list_of_genres[i]:
        genre_other.append(item)


x.clear()
y.clear()

# add bpms and plays for non genre'd

for song in songs:

    x.append(int(song.bpm))
    y.append(int(song.plays))
    del song
ax.scatter(x, y, label="other")


plt.title('Spotify 2018 Wrapped')
plt.ylabel('plays')
plt.xlabel('Beats per minute')
plt.xlim(60, 205)
plt.ylim(30, 250)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
