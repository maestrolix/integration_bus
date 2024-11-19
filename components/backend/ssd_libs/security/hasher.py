from hashlib import sha256


class Hasher:
    """ Класс для работы с хешами """

    @staticmethod
    def verify_hash(plain: str, hashed: str) -> bool:
        """Сравнивает исходный текст с некоторым хешем

        Args:
            plain (str): Обычный текст  \n
            hashed (str): Хеш   \n

        Returns:
            bool: Равен ли хеш текста с некоторым хешем
        """
        return Hasher.get_hash(plain) == hashed

    @staticmethod
    def get_hash(source: str) -> str:
        """Генерирует хеш алгоритмом sha256

        Args:
            source (str): Исходные данные

        Returns:
            str: Результат хеш-функции
        """
        return sha256(source.encode()).hexdigest()
