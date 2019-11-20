import os
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import numpy as np
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict
import pprint
import time
#  displays track information locally
def show_tracks(results):

    for i, item in enumerate(results['items']):

        #  gathers track information
        track = item['track']
        track_id = item['track']['id']
        bpm = sp.audio_features(track_id)[0]['tempo']
        length = sp.audio_features(track_id)[0]['duration_ms']
        artist_id = sp.track(track_id)['album']['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        genres = artist_info['genres']

        #  pulls genre from spreadsheet if manually defined
        #  genres = sheet.cell(i+2, 7).value

        tup = [i, bpm, genres]
        track_list.append(tup)

        # update google sheet if you want to export the data

        time.sleep(.5)
        '''
        sheet.update_cell(i+2, 1, i+1)
        sheet.update_cell(i+2, 2, track['artists'][0]['name'])
        sheet.update_cell(i+2, 3, track['name'])
        sheet.update_cell(i+2, 4, bpm)
        sheet.update_cell(i+2,5, length)
      
        if genres:
            sheet.update_cell(i+2, 7, genres[0])
        '''
        print("%d    %32.32s     %36s                 %s            %s" % (i, track['artists'][0]['name'], track['name'], bpm, genres))

#  G sheet authorization

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Top2018-c0d08a34034f.json', scope)
client = gspread.authorize(creds)


#  spotipy token authorization
#  replace with your own authentication token
client_credentials_manager = SpotifyClientCredentials('5e82f2972bd243868a27d41952e8d129', 'ccd707641b6342efb336b19177b46dbb')


sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Find a workbook by name and open the first sheet
# Make sure you use the right name here.

sheet = client.open("top2018").sheet1
'''
sheet.update_cell(1, 1, "Ranking")
sheet.update_cell(1, 2, "Artist")
sheet.update_cell(1, 3, "Title")
sheet.update_cell(1, 4, "BPM")
sheet.update_cell(1, 5, "Length(ms)")
sheet.update_cell(1, 6, "Length(min)")
sheet.update_cell(1, 7, "Genre")
time.sleep(10)
'''

uri = 'spotify:user:spotify:playlist:37i9dQZF1EjmHb8Jcu5gzU'
username = uri.split(':')[2]
playlist_id = uri.split(':')[4]

results = sp.user_playlist(username, playlist_id)
tracks = results['tracks']

track_list = []
show_tracks(tracks)

while tracks['next']:
    show_tracks(tracks)
    tracks = sp.next(tracks)


list_of_genres = defaultdict(list)


genre_other = []
for i in track_list:

        if len(i[2]) is 0:
            genre_other.append(i)
        else:
            list_of_genres[i[2][0]].append(i)


fig, ax = plt.subplots()

x = []
y = []


length_of_genres = {}
for genre in list_of_genres:

    length_of_genres[genre] = len(list_of_genres[genre])


for counter in range(9):

    temp = 0

    for i in length_of_genres:
        if temp < length_of_genres[i]:
            largest = i
            temp = length_of_genres[i]

    del length_of_genres[largest]
    print(largest)
    x.clear()
    y.clear()

    for item in list_of_genres[largest]:
        print(item)
        x.append(item[1])
        y.append(item[0])

    ax.scatter(x, y, label=largest)


for i in length_of_genres:
    for item in list_of_genres[i]:
        genre_other.append(item)

x.clear()
y.clear()

for item in genre_other:
    x.append(item[1])
    y.append(item[0])


ax.scatter(x, y, label="other")


plt.title('Spotify 2018 Wrapped')
plt.ylabel('Ranking')
plt.xlabel('Beats per minute')
plt.xlim(60, 205)
plt.ylim(105, -5)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()