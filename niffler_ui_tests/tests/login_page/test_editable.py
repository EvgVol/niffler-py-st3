import allure
import pytest

@allure.epic("Аутентификация")
@allure.feature("Форма авторизации (Login)")
class TestLoginPageEditable:
    """Тесты редактируемости полей на странице логина."""

    @allure.story("Редактируемость полей")
    @allure.title("Поля ввода логина и пароля доступны для редактирования")
    @pytest.mark.parametrize(
        "field", ["поле ввода логина", "поле ввода пароля"],
        ids=['editable field login', 'editable field password'],
    )
    def test_editable_field(self, login_page, field: str):
        with allure.step(f"Проверка возможности редактирования: {field}"):
            login_page.asserts(field).should_be_editable()
