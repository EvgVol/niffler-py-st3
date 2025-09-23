import allure

from niffler_ui_tests.src.pages.login_page.login_page import LoginPage


def register_user(login_page: LoginPage, username: str, password: str):
    with allure.step("Кликнуть на кнопку регистрации"):
        login_page.actions("кнопка регистрации").click()
    with allure.step("Заполнить поле логина"):
        login_page.actions("поле ввода логина").fill(username)
    with allure.step("Заполнить поле пароля"):
        login_page.actions("поле ввода пароля (регистрация)").fill(password)
    with allure.step("Заполнить поле повтора пароля"):
        login_page.actions("поле ввода пароля (подтверждение)").fill(password)
    with allure.step("Нажать кнопку зарегистрироваться"):
        login_page.actions("кнопка зарегистрироваться").click()
