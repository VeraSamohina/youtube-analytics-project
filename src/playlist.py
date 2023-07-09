import isodate
from src.channel import Channel
from datetime import timedelta

# создаем специальный объект для работы с API
youtube = Channel.get_service()


class PlayList:
    """
    Класс для работы с плейлистом Youtube
    """
    def __init__(self, playlist_id):
        """
        :param playlist_id: ID плейлиста
        """
        self.playlist_id = playlist_id
        playlists = youtube.playlists().list(id=self.playlist_id,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()
        self.title = playlists['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def get_video_response(self):
        """
        Получаем информацию о видео в плейлисте в виде списка словарей для дальнейшей работы с ним
        """
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        return video_response['items']

    @property
    def total_duration(self):
        """
        Возвращает длительность всех видео в плейлисте
        """
        video_response = self.get_video_response()
        duration = timedelta()
        for video in video_response:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        """
        Возвращает ссылку на видео с максимальным кол-вом лайков
        """
        best_video = None
        video_response = self.get_video_response()
        max_like = 0
        for video in video_response:
            if int(video['statistics']['likeCount']) > max_like:
                best_video = f"https://youtu.be/{video['id']}"
                max_like = int(video['statistics']['likeCount'])
        return best_video
