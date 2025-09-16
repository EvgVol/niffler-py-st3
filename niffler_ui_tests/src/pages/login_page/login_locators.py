from niffler_ui_tests.src.playwright.locator import Locator


class LoginPageLocators:
    LOGO = Locator(
        name="логотип",
        method="role",
        value="img",
        kwargs={"name": "Niffler logo"},
    )
    FIELD_LOGIN = Locator(
        name="поле ввода логина",
        method="role",
        value="textbox",
        kwargs={"name": "Username"},
    )
    FIELD_PASSWORD = Locator(
        name="поле ввода пароля",
        method="role",
        value="textbox",
        kwargs={"name": "Password"},
    )
    BUTTON_LOGIN = Locator(
        name="кнопка входа",
        method="role",
        value="button",
        kwargs={"name": "Log in"},
    )
    BUTTON_CREATE_ACCOUNT = Locator(
        name="кнопка регистрации",
        method="role",
        value="link",
        kwargs={"name": "Create new account"},
    )
