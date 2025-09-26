import allure
import pytest

from niffler_ui_tests.src.pages.main_page.main_page import MainPage

@allure.epic("Финансы")
@allure.feature("Навигация и переходы")
class TestTransition:
    """Проверка переходов между разделами."""

    @allure.story("Главная страница")
    @allure.title("Переход на главную страницу")
    def test_redirect_to_main_page(self, main_page: MainPage):
        with allure.step("Переходим на главную страницу"):
            main_page.should_contain_url("/main")

    @allure.story("Добавление траты")
    @allure.title("Открыть страницу добавления траты")
    def test_open_page_add_spending(self, main_page: MainPage):
        with allure.step("Кликнуть на кнопку добавить трату"):
            main_page.actions("кнопка добавить трату").click()
        with allure.step("Переходим на страницу добавления траты"):
            main_page.should_contain_url("/spending")

    @allure.story("Добавление траты")
    @allure.title("Закрыть страницу добавления траты")
    def test_close_page_add_spending(self, main_page: MainPage):
        with allure.step("Кликнуть на кнопку добавить трату"):
            main_page.actions("кнопка добавить трату").click()
        with allure.step("Нажать на кнопку назад"):
            main_page.actions("кнопка отменить").click()
        with allure.step("Переходим на главную страницу"):
            main_page.should_contain_url("/main")

    @allure.story("Меню пользователя")
    @allure.title("Переходы по меню")
    @pytest.mark.parametrize(
        "link, url",
        [
            ("профиль", "/profile"),
            ("друзья", "/people/friends"),
            ("все пользователи", "/people/all"),
        ],
    )
    def test_transition_in_menu(self, main_page: MainPage, link, url):
        with allure.step("Кликнуть на меню пользователя"):
            main_page.actions("меню пользователя").click()
        with allure.step(f"Нажать на ссылку {link}"):
            main_page.actions(f"ссылка {link}").click()
        with allure.step(f"Переходим на страницу {link}"):
            main_page.should_contain_url(url)

    @allure.story("Выход из аккаунта")
    @allure.title("Открыть модальное окно подтверждения выхода")
    def test_open_modal_window_of_logout(self, main_page: MainPage):
        with allure.step("Кликнуть на меню пользователя"):
            main_page.actions("меню пользователя").click()
        with allure.step("Нажать на ссылку выйти"):
            main_page.actions("ссылка выйти").click()
        with allure.step("Открыто окно подтверждения выхода"):
            main_page.asserts("окно подтверждения выхода").should_be_visible()

    @allure.story("Выход из аккаунта")
    @allure.title("Закрыть модальное окно подтверждения выхода")
    def test_close_modal_window_of_logout(self, main_page: MainPage):
        with allure.step("Кликнуть на меню пользователя"):
            main_page.actions("меню пользователя").click()
        with allure.step("Нажать на ссылку выйти"):
            main_page.actions("ссылка выйти").click()
        with allure.step("Нажать на кнопку закрыть"):
            main_page.actions("кнопка закрыть").click()
        with allure.step("Открыто окно подтверждения выхода"):
            main_page.asserts(
                "окно подтверждения выхода"
            ).should_be_not_visible()
