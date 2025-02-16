import json
import os
from googleapiclient.discovery import build

# Задаем переменную api_key из переменных среды пользователя
api_key: str = os.getenv('YT_API_KEY')

# создаем специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id                                                   # id канала
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']                             # Название канала
        self.description = channel['items'][0]['snippet']['description']                 # Описание канала
        self.url = f'https://www.youtube.com/channel/{channel_id}'                       # ссылка на канал
        self.subscriber_count = int(channel['items'][0]['statistics']['subscriberCount']) # количество подписчиков
        self.video_count = int(channel['items'][0]['statistics']['videoCount'])          # количество видео
        self.view_count = int(channel['items'][0]['statistics']['viewCount'])            # количество просмотров

    def __str__(self):
        """Выводит в консоль информацию о канале."""
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """Сложение двух экземпляров класса канала."""
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """Вычитание двух экземпляров класса канала."""
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        """Сравнение двух экземпляров класса."""
        return self.subscriber_count > other.subscriber_count

    def __lt__(self, other):
        """Сравнение двух экземпляров класса"""
        return self.subscriber_count < other.subscriber_count

    def __ge__(self, other):
        """Сравнение двух экземпляров класса"""
        return self.subscriber_count >= other.subscriber_count

    def __le__(self, other):
        """Сравнение двух экземпляров класса"""
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        """Сравнение двух экземпляров класса"""
        return self.subscriber_count == other.subscriber_count


    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return youtube

    def to_json(self, filename):
        data = self.__dict__
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))
