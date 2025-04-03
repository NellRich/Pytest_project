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


## Тестовый сценарий для проверки обновления дашборда после разблокировки пользователя - api_test_logout.py

**Описание**
Этот тестовый сценарий проверяет, что дашборд обновляется успешно после разблокировки пользователя. Тест выполняет следующие шаги:

- Создает новый дашборд и добавляет виджет к нему.
- Блокирует пользователя.
- Разблокирует пользователя.
- Проверяет, что дашборд обновляется успешно после разблокировки пользователя.
- Проверяет, что можно добавить виджет к дашборду после разблокировки пользователя.

**Требования**
- Python 3.x
- pytest
- assertpy
- time
  
**Установка**
Установите необходимые пакеты: pip install pytest assertpy
Клонируйте репозиторий: git clone https://github.com/username/repository.git
Перейдите в папку с тестовым сценарием: cd repository

**Запуск**
Запустите тестовый сценарий: pytest test_update_dashboard_when_user_is_unblocked.py

**Результаты**
Тестовый сценарий проверяет, что дашборд обновляется успешно после разблокировки пользователя. Если тест проходит успешно, то дашборд обновляется корректно и можно добавить виджет к нему после разблокировки пользователя.

README
================

Абстрактный вид адаптера для получения данных для секции.

Описание
--------

Этот адаптер предоставляет метод для получения данных для секции. Метод принимает следующие параметры:

* `resource_id`: идентификатор ресурса
* `block_id`: идентификатор блока
* `section`: название секции
* `block_version`: версия блока
* `token`: токен для аутентификации
* `execution_time`: время выполнения запроса
* `limit`: ограничение количества данных
* `offset`: смещение данных

Метод возвращает объект `HttpRequest` с данными для секции.

Требования
------------

* Python 3.x
* requests

Установка
------------

1. Установите необходимые пакеты: `pip install requests`
2. Клонируйте репозиторий: `git clone https://github.com/username/repository.git`
3. Перейдите в папку с адаптером: `cd repository`

Использование
-------------

1. Импортируйте адаптер: `from adapter import get_data_request`
2. Создайте экземпляр адаптера: `adapter = get_data_request()`
3. Вызовите метод для получения данных: `data = adapter.get_data_request(resource_id, block_id, section, block_version, token, execution_time, limit, offset)`

Результаты
------------

Метод возвращает объект `HttpRequest` с данными для секции. Если запрос выполнен успешно, то данные будут содержаться в объекте `HttpRequest`.

Автор
-------

Имя автора: [Ваше имя]
Email: [Ваш email]
