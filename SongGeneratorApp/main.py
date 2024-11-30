import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lyricsgenius


sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
    client_id = "c4c5260ea0f64680b1e3043c430eb567",
    client_secret = "9b2db4d2398441528c30fe2056672f10",
    redirect_uri = "http://localhost:3000",
    scope = "user-top-read"
))

genius = lyricsgenius.Genius("PuJYHWUPPue7lCiG330tZRS5sPjU4v6ZAc1mXz2OvMFIqGgfPwutJelziCBtcOmt")

def get_lyrics(song_name, artist_name):
    try:
        song = genius.search_song(song_name, artist_name)
        if song:
            return song.lyrics
        else:
            return "Lyrics not found"
    except Exception as e:
        print(f"Error fetching lyrics for {song_name} by {artist_name}: {e}")
        return "Lyrics not found"
    
def get_top_artist_by_genre(sp, genre, top_n = 10):
  results = sp.search(q = f'genre:"{genre}"', type = 'artist', limit = top_n)
  artists= results['artists']['items']
  top_artists = []

  for artist in artists:
    print(f"Scraping artist {artist['name']}")
    top_artists.append({
        'name' : artist['name'],
        'genres' : artist['genres'],
        'popularity' : artist['popularity'],
        'followers' : artist['followers']['total'],
        'id' : artist['id']
    })
  return top_artists

def get_songs_by_artists(sp, artist_id):
  results = sp.artist_top_tracks(artist_id)
  tracks  = results['tracks']
  songs = []

  for track in tracks:
    songs.append({
        'name' : track['name'],
        'album' : track['album']['name'],
        'preview_url' : track['preview_url'],
        'popularity' : track['popularity']
    })
  return songs

import csv

genres = ['pop', 'rock', 'hip-hop', 'classical', 'jazz', 'blues', 'country', 'electronic', 'folk', 'reggae']

def scrape_top_artists_songs(sp, genres, top_n = 10, output_file = "top_artists_songs.csv"):
  with open(output_file, 'w',newline = '', encoding = 'utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Genre', 'Artist', 'Song', 'Album', 'Popularity', 'Preview URL'])

    for genre in genres:
      top_artists = get_top_artist_by_genre(sp, genre, top_n)
      for artist in top_artists:
        songs = get_songs_by_artists(sp, artist['id'])
        for song in songs:
            lyrics = get_lyrics(song['name'], artist['name'])
            writer.writerow([genre, artist['name'], song['name'], song['album'], song['popularity'], song['preview_url'], lyrics])

      print(f"Scraped top {top_n} artists and their songs for genre: {genre}")

# Run the script
scrape_top_artists_songs(sp, genres, top_n=10)
