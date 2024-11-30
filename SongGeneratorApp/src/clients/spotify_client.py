import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .music_service_client import IMusicServiceClient
import logging

class SpotifyClient(IMusicServiceClient):
    def __init__(self, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.sp =spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id = config['spotify']['client_id'],
            client_secret = config['spotify']['client_secret'],
            redirect_uri=config['spotify']['redirect_uri'],
            scope=config['spotify']['scope']
        ))
        self.logger.debug("Spotify client initialized")
        
    
    def get_top_artists_by_genre(self, genre, top_n):
        try:
            results = self.sp.search(q = f'genre:"{genre}"'
                                     type='artist',
                                     limit=top_n)
            artists=results['artists']['items']
            self.logger.debug(f"Fetched top {top_n} artists for genre {genre}.")
            return [
                {
                    'name':artist['name'],
                    'genres':artist['genres'],
                    'popularity': artist['popularity'],
                    'followers': artist['followers']['total'],
                    'id': artist['id']
                } for artist in artists
            ]
            
        except Exception as e:
            self.logger.error(f"Error fetching top artists for genre {genre}: {e}")
            return []
        
    def get_songs_by_artist(self, artist_id):
        try:
            results = self.sp.artist_top_tracks(artist_id)
            tracks = results['tracks']
            self.logger.debug(f"Fetched top songs for artist ID {artist_id}.")
            return [
                {
                    'name': track['name'],
                    'album': track['album']['name'],
                    'preview_url': track['preview_url'],
                    'popularity': track['popularity']
                } for track in tracks
            ]
        
        except Exception as e:
            self.logger.error(f"Error in fetching songs for artist ID {artist_id}: {e}")
            return []
        