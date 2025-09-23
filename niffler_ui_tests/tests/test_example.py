from uuid import UUID

import allure

from niffler_ui_tests.src.database.db_manager import DbManager
from niffler_ui_tests.src.pages.login_page.login_page import LoginPage
from niffler_ui_tests.support.asserting import Assert
from niffler_ui_tests.support.asserting_db import AssertDB


@allure.title("Логотип виден на странице")
def test_logo(client: LoginPage):
    with allure.step("Открытие страницы"):
        login_page = client.open()
    with allure.step("Проверка видимости логотипа"):
        login_page.asserts("логотип").should_be_visible()


def test_example(auth_niffler_db: DbManager):
    resp = auth_niffler_db.use_table('user').filter_by({'username': "vol"})
    AssertDB.db_contains(
        resp,
        {"id": UUID("3fb31bcc-3af7-45a3-b2af-4de25384c9ac")},
        description="В таблице user должен существовать vol с заданным ID"
    )

def test_password_hash(auth_niffler_db: DbManager):
    resp = auth_niffler_db.use_table('user').filter_by({'username': "vol"})
    AssertDB.db_password_hashed(
        resp,
        hash_type="bcrypt",
        description="Пароль пользователя vol должен быть хэширован через bcrypt"
    )
    # assert result[0]['id'] == UUID('3fb31bcc-3af7-45a3-b2af-4de25384c9ac'), print(result.body)
