import random

from faker import Faker


class Fake:

    def __init__(self, language: str = 'ru_RU'):
        self.fake = Faker(language)

    def username(self) -> str:
        """Сгенерировать имя пользователя."""
        return self.fake.user_name()

    def password(self, min_len: int = 8, max_len: int = 16) -> str:
        """
        Сгенерировать пароль.

        :param min_len: Минимальная длина пароля.
        :param max_len: Максимальная длина пароля.
        """
        return self.fake.password(
            length=random.randint(min_len, max_len),
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )

    def text(self, length: int = 20) -> str:
        """
        Сгенерировать текст фиксированной длины.

        :param length: Длина текста.
        """
        max_chars = max(5, length * 2)
        txt = self.fake.text(max_nb_chars=max_chars)
        return txt[:length]
