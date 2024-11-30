from abc import ABC, abstractmethod

class ILyricsServiceClient(ABC):
    @abstractmethod
    def get_lyrics(self, song_name, artist_name):
        pass
