import allure

from niffler_ui_tests.src.database.db_manager import DbManager
from niffler_ui_tests.src.pages.login_page.login_page import LoginPage
from niffler_ui_tests.support.asserting_db import AssertDB
from niffler_ui_tests.support.fake_generator import FakeGenerator

from niffler_ui_tests.steps import register_user


@allure.epic("Аутентификация")
@allure.feature("Регистрация пользователя (Sign Up)")
class TestSignUp:
    """Тесты регистрации пользователя."""

    @allure.story("Успешная регистрация")
    @allure.title("Пользователь сохраняется в БД после успешной регистрации")
    @FakeGenerator.username
    @FakeGenerator.password(min_len=8, max_len=12)
    def test_user_persisted_in_db_after_successful_signup(
        self,
        login_page: LoginPage,
        auth_niffler_db: DbManager,
        delete_user,
        **fake,
    ):
        register_user(login_page, fake["username"], fake["password"])
        with allure.step(
            f"Добавить {fake['username']} в список на удаление после теста"
        ):
            delete_user.update({"username": fake["username"]})

        with allure.step(
            "Проверить, что запись с новым username появилась в таблице users"
        ):
            resp = auth_niffler_db.use_table("user").filter_by(
                {"username": fake["username"]}
            )
            AssertDB.db_contains(resp, {"username": fake["username"]})

    @allure.story("Валидация username")
    @allure.title(
        "Имя пользователя уникально (нельзя зарегистрировать дважды)"
    )
    @FakeGenerator.username
    @FakeGenerator.password(min_len=8, max_len=12)
    def test_username_must_be_unique(
        self,
        login_page: LoginPage,
        auth_niffler_db: DbManager,
        delete_user,
        **fake,
    ):
        register_user(login_page, fake["username"], fake["password"])
        with allure.step(
            f"Добавить {fake['username']} в список на удаление после теста"
        ):
            delete_user.update({"username": fake["username"]})

        with allure.step("Кликнуть на кнопку войти"):
            login_page.actions("кнопка войти").click()
        with allure.step("Повторная регистрация с тем же username"):
            register_user(login_page, fake["username"], fake["password"])
        with allure.step(
            "Проверить, что в базе данных нет дубликатов username"
        ):
            resp = auth_niffler_db.use_table("user").count(
                {"username": fake["username"]}
            )
            AssertDB.equal(resp, 1)

    @allure.story("Хранение пароля")
    @allure.title("Пароль хранится в хэшированном виде")
    @FakeGenerator.username
    @FakeGenerator.password(min_len=8, max_len=12)
    def test_password_stored_as_hash(
        self,
        login_page: LoginPage,
        auth_niffler_db: DbManager,
        delete_user,
        **fake,
    ):
        register_user(login_page, fake["username"], fake["password"])
        with allure.step(
            f"Добавить {fake['username']} в список на удаление после теста"
        ):
            delete_user.update({"username": fake["username"]})

        with allure.step("Проверить, что пароль хранится в хэшированном виде"):
            resp = auth_niffler_db.use_table("user").filter_by(
                {"username": fake["username"]}
            )
            AssertDB.db_password_hashed(resp, hash_type="bcrypt")

    @allure.story("Обработка ошибок")
    @allure.title("При ошибке регистрации запись не создается")
    @FakeGenerator.text(length=2)
    @FakeGenerator.password(min_len=8, max_len=12)
    def test_no_db_entry_after_failed_signup(
        self,
        login_page: LoginPage,
        auth_niffler_db: DbManager,
        delete_user,
        **fake,
    ):
        register_user(login_page, fake["text"], fake["password"])
        with allure.step(
            "Проверить, что отсутствует запись после ошибки регистрации"
        ):
            resp = auth_niffler_db.use_table("user").count(
                {"username": fake["text"]}
            )
            AssertDB.equal(resp, 0)
