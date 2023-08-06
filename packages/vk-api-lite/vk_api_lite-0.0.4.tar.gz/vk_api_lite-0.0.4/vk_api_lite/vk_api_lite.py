import requests
import json


class VkAPILite:
    def __init__(self, TOKEN: str):
        """Небольшая библиотека для работы с VK API через access_token (wall.post, wall.get, photos.save)."""
        self.__TOKEN = TOKEN

    @property
    def TOKEN(self):
        """Получить используемый access_token."""
        return self.__TOKEN

    @TOKEN.setter
    def TOKEN(self, TOKEN: str):
        """Изменить используемый access_token."""
        self.__TOKEN = TOKEN

    @staticmethod
    def saveJson(data, path) -> None:
        """Сохранить ответ от сервера в json формате. Пропустить, если при сохранении происходит ошибка."""
        try:
            json.dump(data, open(path, 'w', encoding="utf-8"), ensure_ascii=False)
        except TypeError:
            pass
        except OSError:
            pass

    @staticmethod
    def makePhotosAttachments(owner_id: int, photos_id: [list, tuple]):
        """Создание строки для параметра attachments (вложение к посту) по id"""
        if len(photos_id) == 0:
            raise EmptyAttachmentsException
        elif int(owner_id) <= 0:
            raise MustBePositiveException
        else:
            attachments = ''

            # Заполнение выходной строки
            for pid in photos_id:
                attachments += f'photo-{owner_id}_{pid},'

            # Вернуть строку
            return attachments[:-1]

    def wallGetById(self, owner_id: int = 1, offset: int = None, count: int = 100, filter: str = None,
                    extended: int = None, fields: str = None, v: float = 5.131, json_save_path: str = None) -> dict:
        """Возвращает список записей со стены пользователя или сообщества по идентификатору (id)."""

        if int(owner_id) <= 0:
            raise MustBePositiveException

        # Запрос к серверу
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': self.__TOKEN,
                                    'owner_id': -int(owner_id),
                                    'offset': offset,
                                    'count': count,
                                    'filter': filter,
                                    'extended': extended,
                                    'fields': fields,
                                    'v': float(v)
                                })

        # Сохранение ответа в файл
        if json_save_path:
            VkAPILite.saveJson(response.json(), json_save_path)

        return response.json()

    def wallGetByDomain(self, domain: str = None, offset: int = None, count: int = 100, filter: str = None,
                        extended: int = None, fields: str = None, v: float = 5.131, json_save_path: str = None) -> dict:
        """Возвращает список записей со стены пользователя или сообщества по домену (альтернативный короткий адрес)."""

        # Запрос к серверу
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': self.__TOKEN,
                                    'domain': domain,
                                    'offset': offset,
                                    'count': count,
                                    'filter': filter,
                                    'extended': extended,
                                    'fields': fields,
                                    'v': float(v)
                                })

        # Сохранение ответа в файл
        if json_save_path:
            VkAPILite.saveJson(response.json(), json_save_path)

        return response.json()

    def wallPost(self, owner_id: int, friends_only: int = None, from_group: int = None, message: str = None,
                 attachments: str = None, services: str = None, signed: int = None, publish_date: int = None,
                 lat: str = None, long: str = None, place_id: int = None, post_id: int = None, guid: str = None,
                 mark_as_ads: int = None, close_comments: int = None, donut_paid_duration: int = None,
                 mute_notifications: int = None, copyright: str = None, topic_id: int = None,
                 json_save_path: str = None) -> dict:
        """
        Позволяет создать запись на стене, предложить запись на стене публичной страницы, опубликовать существующую
        отложенную запись.Чтобы создать предложенную запись, необходимо передать в owner_id идентификатор публичной
        страницы, в которой текущий пользователь не является руководителем.Для публикации предложенных и отложенных
        записей используйте параметр post_id, значение для которого можно получить методом wall.get с filter=suggests
        и postponed соответственно. При публикации отложенной записи все параметры, кроме owner_id и post_id, игнорируются.
        После успешного выполнения возвращает идентификатор созданной записи (post_id).
        """

        if int(owner_id) <= 0:
            raise MustBePositiveException

        # Запрос к серверу
        response = requests.get('https://api.vk.com/method/wall.post',
                                params={
                                    'access_token': self.__TOKEN,
                                    'owner_id': -int(owner_id),
                                    'friends_only': friends_only,
                                    'from_group': from_group,
                                    'message': message,
                                    'attachments': attachments,
                                    'services': services,
                                    'signed': signed,
                                    'publish_date': publish_date,
                                    'lat': lat,
                                    'long': long,
                                    'place_id': place_id,
                                    'post_id': post_id,
                                    'guid': guid,
                                    'mark_as_ads': mark_as_ads,
                                    'close_comments': close_comments,
                                    'donut_paid_duration': donut_paid_duration,
                                    'mute_notifications': mute_notifications,
                                    'copyright': copyright,
                                    'topic_id': topic_id,
                                    'v': 5.92,
                                })

        # Сохранение ответа в файл
        if json_save_path:
            VkAPILite.saveJson(response.json(), json_save_path)

        return response.json()

    def photosSave(self, album_id: int, group_id: int, photos_list: list, latitude: 'str' = None,
                   longitude: 'str' = None, caption: 'str' = None, v: float = 5.131, json_save_path: str = None) -> tuple:
        """
        Сохраняет фотографии после успешной загрузки и возвращает id загруженных фотографий. Ограничения: не более
        5 фотографий за один раз, сумма высоты и ширины не более 14000px, файл объемом не более 50 МБайт, соотношение
        сторон не менее 1:20.
        """

        if int(album_id) <= 0:
            raise MustBePositiveException

        photos_id = []

        # Не более 5 фотографий за раз
        for i in range(0, len(photos_list) - 1, 5):
            tmp_lst = photos_list[i:5 + i * 5]
            files = {}

            # Поля должны содержать изображения в формате multipart/form-data (file1-file5)
            for j in range(len(tmp_lst)):
                files[f'file{j}'] = open(tmp_lst[j], 'rb')

            # Получение адреса для загрузки фото
            response = requests.get('https://api.vk.com/method/photos.getUploadServer',
                                    params={
                                        'access_token': self.__TOKEN,
                                        'album_id': album_id,
                                        'group_id': group_id,
                                        'v': v,
                                    })

            # Получение адреса upload_url для загрузки фото на сервер
            upload_url = response.json()['response']['upload_url']

            # Отправка фотографий на сервер пост запросом
            response = requests.post(upload_url, files=files).json()

            # Получение json-файла с полями server, photos_list, hash, aid после загрузки фото
            response = requests.get('https://api.vk.com/method/photos.save',
                                    params={
                                        'access_token': self.__TOKEN,
                                        'album_id': album_id,
                                        'group_id': group_id,
                                        'server': response['server'],
                                        'photos_list': response['photos_list'],
                                        'hash': response['hash'],
                                        'latitude': latitude,
                                        'longitude': longitude,
                                        'caption': caption,
                                        'v': v,
                                    })

            # Получение id загруженных фотографий
            try:
                for elem in response.json()['response']:
                    photos_id.append(elem['id'])
            except KeyError:
                pass

        # Сохранение ответа в файл
        if json_save_path:
            VkAPILite.saveJson(response.json(), json_save_path)

        return tuple(photos_id)


class MustBePositiveException(Exception):
    """Обязательные параметры должны быть положительными."""
    def __str__(self):
        return 'Parameters owner_id and album_id must be positive int.'


class EmptyAttachmentsException(Exception):
    """Список id фотографий не должен быть пустым."""
    def __str__(self):
        return 'Photos id list must not be empty.'
