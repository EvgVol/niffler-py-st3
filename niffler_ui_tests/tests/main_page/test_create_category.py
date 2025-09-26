import allure

from niffler_ui_tests.src.pages.main_page.main_page import MainPage

import allure

from niffler_ui_tests.src.pages.main_page.main_page import MainPage


@allure.epic("Финансы")
@allure.feature("Создание траты (Expense)")
class TestCreateCategory:

    @allure.story("Валидация обязательного поля 'Категория'")
    @allure.title("Создание траты без категории")
    def test_without_category(self, main_page: MainPage):
        with allure.step("Кликнуть на кнопку добавить трату"):
            main_page.actions("кнопка добавить трату").click()
        with allure.step("Заполнить значение суммы"):
            main_page.actions("поле суммы").fill("100")
        with allure.step("Нажать на кнопку добавить"):
            main_page.actions("кнопка добавить").click()
        with allure.step("Проверить что появилась ошибка"):
            main_page.asserts(
                "предупреждение поля категория"
            ).should_have_text("Please choose category")

    @allure.story("Валидация обязательного поля 'Сумма'")
    @allure.title("Создание траты без суммы")
    def test_without_amount(self, main_page: MainPage):
        with allure.step("Кликнуть на кнопку добавить трату"):
            main_page.actions("кнопка добавить трату").click()
        with allure.step("Заполнить значение категории"):
            main_page.actions("поле категории").fill("Fake category")
        with allure.step("Нажать на кнопку добавить"):
            main_page.actions("кнопка добавить").click()
        with allure.step("Проверить что появилась ошибка"):
            main_page.asserts("предупреждение поля сумма").should_have_text(
                "Amount has to be not less then 0.01"
            )
