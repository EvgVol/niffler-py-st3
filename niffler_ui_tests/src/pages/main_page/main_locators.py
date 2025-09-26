from niffler_ui_tests.src.playwright.locator import Locator


class MainPageLocators:
    BUTTON_NEW_SPENDING = Locator(
        name="кнопка добавить трату",
        method="role",
        value="link",
        kwargs={"name": "New spending"},
    )
    BUTTON_MENU = Locator(
        name="меню пользователя",
        method="role",
        value="button",
        kwargs={"name": "Menu"},
    )
    BUTTON_ADD = Locator(
        name="кнопка добавить",
        method="role",
        value="button",
        kwargs={"name": "Add"},
    )
    BUTTON_CANCEL = Locator(
        name="кнопка отменить",
        method="role",
        value="button",
        kwargs={"name": "Cancel"},
    )
    BUTTON_CLOSE = Locator(
        name="кнопка закрыть",
        method="role",
        value="button",
        kwargs={"name": "Close"},
    )
    BUTTON_LOGOUT = Locator(
        name="кнопка выйти",
        method="role",
        value="button",
        kwargs={"name": "Sign out"},
    )
    FIELD_AMOUNT = Locator(
        name="поле суммы",
        method="role",
        value="spinbutton",
        kwargs={"name": "Amount"},
    )
    FIELD_CATEGORY = Locator(
        name="поле категории",
        method="role",
        value="textbox",
        kwargs={"name": "Add new category"},
    )
    WARNING_FIELD_AMOUNT = Locator(
        name="предупреждение поля сумма",
        selector="//input[@id='amount']/following-sibling::span",
    )
    WARNING_FIELD_CATEGORY = Locator(
        name="предупреждение поля категория",
        selector="//input[@id='category']/following-sibling::span",
    )
    LINK_PROFILE = Locator(
        name="ссылка профиль",
        method="role",
        value="link",
        kwargs={"name": "Profile"},
    )
    LINK_FRIENDS = Locator(
        name="ссылка друзья",
        method="role",
        value="link",
        kwargs={"name": "Friends"},
    )
    LINK_ALL_PEOPLE = Locator(
        name="ссылка все пользователи",
        method="role",
        value="link",
        kwargs={"name": "All People"},
    )
    LINK_LOGOUT = Locator(
        name="ссылка выйти",
        method="role",
        value="menuitem",
        kwargs={"name": "Sign out"},
    )
    MODAL_WINDOW_OF_LOGOUT = Locator(
        name="окно подтверждения выхода",
        method="role",
        value="dialog",
        kwargs={"name": "Want to logout?"},
    )
