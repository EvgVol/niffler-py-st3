import allure
import pytest

from niffler_ui_tests.src.database.db_manager import DbManager
from niffler_ui_tests.support import fake


@pytest.fixture(scope="session")
def delete_user(auth_niffler_db: DbManager):

    contest = {}

    yield contest

    username = contest.get("username")
    if not username:
        return

    with allure.step(f"Удаление пользователя {username} и его зависимостей"):
        with allure.step("Получение id пользователя"):
            user = auth_niffler_db.use_table("user").filter_by({"username": username})
            if not user or not user.body:
                allure.attach(f"Пользователь {username} не найден в таблице user", name="DB Cleanup")
                return
            user_id = user.body[0]["id"]
            allure.attach(str(user_id), name="User ID")

        with allure.step("Удаление записей из authority"):
            auth_niffler_db.use_table("authority").delete({"user_id": user_id})

        with allure.step("Удаление записи из user"):
            auth_niffler_db.use_table("user").delete({"username": username})