import matplotlib.pyplot as plt
import csv
import pprint
# percent of artists from whole

artists = []
plays = []
totalplays = 23404
countedtotal = 0
explode = []

# % of artists plays
with open('artistplays.csv', newline="\n") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        artists.append(row[0])
        plays.append(row[1])
        countedtotal += int(row[1])
        explode.append(.1)


artists.append('Other')
plays.append((totalplays-countedtotal))
explode.append(0)
fig1, ax1 = plt.subplots()
ax1.pie(plays, labels=artists, autopct='%1.1f%%', explode= explode, startangle=120)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Artists as % of total plays')
plt.show()

