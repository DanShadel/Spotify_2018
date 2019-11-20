import matplotlib.pyplot as plt
import csv
import pprint
#percent of genres from whole

genres = []
plays = []
explode = []
totalplays = 0
# % of artists plays
with open('bpmvsplays.csv', newline="\n") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        genres.append(row[1])
        plays.append(row[3])
        totalplays += int(row[3])
        explode.append(.1)


fig1, ax1 = plt.subplots()
ax1.pie(plays, labels=genres, autopct='%1.1f%%', explode= explode, startangle=120)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Genres as % of total plays')
plt.show()

