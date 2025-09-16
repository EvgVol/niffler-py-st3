from niffler_ui_tests.configs.loader.pytest_plugins import get_pytest_plugins

pytest_plugins = get_pytest_plugins(service_name=["frontend_niffler"])


if __name__ == "__main__":
    print(pytest_plugins)
