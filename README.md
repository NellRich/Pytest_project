# Pytest_project

Фикстура для пере конфигурирования сервиса SERVICE - session_fixture.py
================
Эта фикстура используется для пере конфигурирования сервиса SERVICE в начале и конце тестового сценария.

**Использование**
------------
Для использования фикстуры необходимо импортировать ее в тестовый файл и вызвать функцию service_extended_reconfig.

**Параметры**
------------
- sftp_connection: объект подключения к серверу по протоколу SFTP
- ssh_connection: объект подключения к серверу по протоколу SSH
- session_scoped_product_api: объект API для работы с продуктом
- application_product_path: путь к директории продукта

**Пример использования**
------------
```python
import pytest

from src.fixtures.service_extended_reconfig import service_extended_reconfig

@pytest.mark.usefixtures("service_extended_reconfig")
def test_service():
    # выполнение тестового сценария
    pass
```
или
```python
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

Тестовый сценарий для проверки обновления дашборда после разблокировки пользователя - api_test_logout.py
================

**Описание**
------------
Этот тестовый сценарий проверяет, что дашборд обновляется успешно после разблокировки пользователя. Тест выполняет следующие шаги:

- Создает новый дашборд и добавляет виджет к нему.
- Блокирует пользователя.
- Разблокирует пользователя.
- Проверяет, что дашборд обновляется успешно после разблокировки пользователя.
- Проверяет, что можно добавить виджет к дашборду после разблокировки пользователя.

**Требования**
------------
- Python 3.x
- pytest
- assertpy
- time
  
**Установка**
------------
Установите необходимые пакеты: pip install pytest assertpy
Клонируйте репозиторий: git clone https://github.com/username/repository.git
Перейдите в папку с тестовым сценарием: cd repository

**Запуск**
------------
Запустите тестовый сценарий: pytest test_update_dashboard_when_user_is_unblocked.py

**Результаты**
------------
Тестовый сценарий проверяет, что дашборд обновляется успешно после разблокировки пользователя. Если тест проходит успешно, то дашборд обновляется корректно и можно добавить виджет к нему после разблокировки пользователя.


Абстрактный вид адаптера для получения данных для секции - service_adapter_api.py
================

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

```py
@pytest.mark.parametrize("get_resource_id_by_name", ["Ресурс с данными"], indirect=True)
@allure.title("Получить данные для секции ресурса")
def test_get_resource_section_block_query(self, api, get_resource_id_by_name, new_resource_id):
    resource = api.resources.get_resource(get_resource_id_by_name).send().value
    new_block = (
        api.resources.add_block_to_resource_request(
            resource_id=new_resource_id, payload=BlockModel.get_block_default(resource)
        )
        .send()
        .value
    )
    wait_until(
        statement=api.resources.get_resource_section_block_query_request(
            new_resource_id, new_block.id, section="data", block_version=1
        ).send,
        condition=lambda r: r.status_code == 200,  # type: ignore
        error_msg="Данные секции не получены",
        timeout=90,
        interval=10,
        error_type=AssertionError,
    )
```

Результаты
------------

Метод возвращает объект `HttpRequest` с данными для секции. Если запрос выполнен успешно, то данные будут содержаться в объекте `HttpRequest`.


Абстрактный тест для проверки настройки расписания отчета - extended_parametrize.py
================

Описание
--------

Этот тестовый сценарий проверяет функциональность настройки расписания отчета. Тесты выполняют следующие шаги:

* Создают новый отчет и добавляют расписание к нему.
* Проверяют, что расписание изменилось после обновления.
* Проверяют, что при указании некорректных параметров в настройках расписания отчета возвращается ошибка.

Требования
------------

* Python 3.x
* pytest
* assertpy
* time

Установка
------------

1. Установите необходимые пакеты: `pip install pytest assertpy`
2. Клонируйте репозиторий: `git clone https://github.com/username/repository.git`
3. Перейдите в папку с тестовым сценарием: `cd repository`

Запуск
--------

1. Запустите тестовый сценарий: `pytest test_abstract_report_schedule_config_regress.py`

Результаты
------------

Тестовый сценарий проверяет функциональность настройки расписания отчета. Если тест проходит успешно, то расписание изменилось после обновления и при указании некорректных параметров в настройках расписания отчета возвращается ошибка.

Тесты
--------

### test_abstract_report_schedule_parameters_config

* Создает новый отчет и добавляет расписание к нему.
* Проверяет, что расписание изменилось после обновления.

### test_abstract_report_on_incorrect_schedule_parameters_config

* Создает новый отчет и добавляет расписание к нему.
* Проверяет, что при указании некорректных параметров в настройках расписания отчета возвращается ошибка.

Примечания
------------

* Тесты выполняются с использованием библиотеки `pytest`.
* Тесты проверяют функциональность настройки расписания отчета.
* Тесты выполняют следующие шаги: создают новый отчет, добавляют расписание к нему, проверяют, что расписание изменилось после обновления, проверяют, что при указании некорректных параметров в настройках расписания отчета возвращается ошибка.

Абстрактный метод для получения вкладки компонента по тексту - page_get_metod.py
================

Описание
--------

Этот метод используется для получения вкладки компонента по тексту. Он проверяет, видима ли вкладка на панели, и если нет, то проверяет, есть ли она в дропдауне.

Требования
------------

* Python 3.x
* Playwright

Установка
------------

1. Установите необходимые пакеты: `pip install playwright`
2. Клонируйте репозиторий: `git clone https://github.com/username/repository.git`
3. Перейдите в папку с кодом: `cd repository`

Использование
-------------

1. Импортируйте класс: `from src.components.abstract.common_component import AbstractCommonComponent`
2. Создайте экземпляр класса: `component = AbstractCommonComponent()`
3. Вызовите метод: `tab, is_item = component.get_abstract_component_tab_by_text("Компонент")`

Параметры
------------

* `abstract_component_name`: имя компонента

Возвращаемые значения
--------------------

* `tab`: локатор вкладки
* `is_item`: флаг, указывающий, является ли вкладка элементом дропдауна

Пример использования
--------------------

```python
component = AbstractCommonComponent()
tab, is_item = component.get_abstract_component_tab_by_text("Компонент")
```
