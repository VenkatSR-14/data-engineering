from abc import ABC, abstractmethod

class IMusicServiceClient(ABC):
    @abstractmethod
    def get_top_artists_by_genre(self, genre, top_n):
        pass
    
    @abstractmethod
    def get_top_songs_by_artist(self, artist_id):
        pass
    