from src.channel import Channel

# создаем специальный объект для работы с API
youtube = Channel.get_service()


class Video(Channel):
    """
    Класс для хранения информации о видео
    """
    def __init__(self, video_id):
        self.video_id = video_id                                                             # id видео
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id).execute()
        self.video_title = video_response['items'][0]['snippet']['title']                    # название видео
        self.video_url = f'https://www.youtube.com/watch?v={video_id}'                       # ссылка на видео
        self.views = video_response['items'][0]['statistics']['viewCount']                   # количество просмотров
        self.likes = video_response['items'][0]['statistics']['likeCount']                   # количество лайков

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта
        """
        return self.video_title


class PLVideo(Video):
    """
    Класс для хранения информации о видео из плейлиста
    """
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
