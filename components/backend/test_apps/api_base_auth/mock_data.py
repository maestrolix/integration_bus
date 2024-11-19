from datetime import datetime
from random import uniform
from typing import Final, Any

from entities import Composition, Album, Artist


# Моковые данные для композиций
composition_data: Final[list[dict[str, Any]]] = [
    {'id': 1, 'title': 'Композиция #1', 'rating': uniform(0, 5)},
    {'id': 2, 'title': 'Композиция #2', 'rating': uniform(0, 5)},
    {'id': 3, 'title': 'Композиция #3', 'rating': uniform(0, 5)},
    {'id': 4, 'title': 'Композиция #4', 'rating': uniform(0, 5)},
    {'id': 5, 'title': 'Композиция #5', 'rating': uniform(0, 5)},
]

COMPOSITIONS: Final[list[Composition]] = [
    Composition(id=data['id'], title=data['title'], rating=data['rating'])
    for data in composition_data
]

# Моковые данные для альбомов
album_data: Final[list[dict[str, Any]]] = [
    {'id': 1, 'title': 'Альбом #1', 'release_date': datetime.now(), 'compositions': COMPOSITIONS[:3], 'rating': uniform(0, 5)},
    {'id': 2, 'title': 'Альбом #2', 'release_date': datetime.now(), 'compositions': COMPOSITIONS[2:5], 'rating': uniform(0, 5)},
    {'id': 3, 'title': 'Альбом #3', 'release_date': datetime.now(), 'compositions': COMPOSITIONS[:2], 'rating': uniform(0, 5)},
    {'id': 4, 'title': 'Альбом #4', 'release_date': datetime.now(), 'compositions': COMPOSITIONS[1:4], 'rating': uniform(0, 5)},
    {'id': 5, 'title': 'Альбом #5', 'release_date': datetime.now(), 'compositions': COMPOSITIONS[3:5], 'rating': uniform(0, 5)},
]

ALBUMS: Final[list[Album]] = [
    Album(
        id=data['id'],
        title=data['title'],
        release_date=data['release_date'],
        compositions=data['compositions'],
        rating=data['rating']
    )
    for data in album_data
]

# Моковые данные для исполнителей
artist_data: Final[list[dict[str, Any]]] = [
    {'id': 1, 'name': 'Исполнитель #1', 'albums': ALBUMS[:3], 'rating': uniform(0, 5)},
    {'id': 2, 'name': 'Исполнитель #2', 'albums': ALBUMS[2:5], 'rating': uniform(0, 5)},
    {'id': 3, 'name': 'Исполнитель #3', 'albums': ALBUMS[:2], 'rating': uniform(0, 5)},
    {'id': 4, 'name': 'Исполнитель #4', 'albums': ALBUMS[1:4], 'rating': uniform(0, 5)},
    {'id': 5, 'name': 'Исполнитель #5', 'albums': ALBUMS[3:5], 'rating': uniform(0, 5)},
]

ARTISTS: Final[list[Artist]] = [
    Artist(
        id=data['id'],
        name=data['name'],
        albums=data['albums'],
        rating=data['rating']
    )
    for data in artist_data
]
