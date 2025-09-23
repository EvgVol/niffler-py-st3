from functools import wraps

from niffler_ui_tests.support.fake import Fake


class FakeGenerator:

    @staticmethod
    def provide(field: str, *args, **default_kwargs):
        """
        Декоратор для генерации тестовых данных через Fake.
        :param field: Имя метода в Fake
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*f_args, **f_kwargs):
                faker = Fake()
                generator = getattr(faker, field, None)
                if not generator:
                    raise AttributeError(f"Fake() не содержит генератора '{field}'")
                f_kwargs[field] = generator(*args, **default_kwargs)
                return func(*f_args, **f_kwargs)

            return wrapper

        return decorator

    @staticmethod
    def text(length: int = 20):
        return FakeGenerator.provide("text", length=length)

    @staticmethod
    def password(min_len: int = 8, max_len: int = 16):
        return FakeGenerator.provide("password", min_len=min_len, max_len=max_len)

    username = provide("username")