# Pytest_project

## Фикстура для пере конфигурирования сервиса SERVICE - session_fixture.py
Эта фикстура используется для пере конфигурирования сервиса SERVICE в начале и конце тестового сценария.

**Использование**
Для использования фикстуры необходимо импортировать ее в тестовый файл и вызвать функцию service_extended_reconfig.

**Параметры**
- sftp_connection: объект подключения к серверу по протоколу SFTP
- ssh_connection: объект подключения к серверу по протоколу SSH
- session_scoped_product_api: объект API для работы с продуктом
- application_product_path: путь к директории продукта

**Пример использования**
```
import pytest

from src.fixtures.service_extended_reconfig import service_extended_reconfig

@pytest.mark.usefixtures("service_extended_reconfig")
def test_service():
    # выполнение тестового сценария
    pass
```
или
```
import pytest

from src.fixtures.service_extended_reconfig import service_extended_reconfig

@pytest.mark.api
@pytest.mark.product
@pytest.mark.regress
@allure.id("1")
@allure.label("type", "regress")
@allure.label("layer", "API")
@allure.label("microservice", "SERVICE")
@allure.label("team", "Team")
@allure.title("Тест-кейс")
@pytest.mark.parametrize("get_template_id_by_name", ["Шаблон_1"], indirect=True)
def test_service(service_extended_reconfig):
    # выполнение тестового сценария
    pass
```

**Настройка**
Для настройки фикстуры необходимо изменить параметры в функции reconfigure_service_product. Например, можно изменить новый конфиг для сервиса, добавив или удалив строки из списка new_config.
