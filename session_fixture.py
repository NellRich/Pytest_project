# session fixture
from pathlib import Path
from typing import Generator

import allure
import pytest
from paramiko import SFTPClient, SSHClient

from src.api.product_api import ProductApi
from src.tools.ssh_helper import execute_command_and_get_output
from src.tools.wait import wait_until


def reconfigure_service_product(
    sftp_connection: SFTPClient,  # объект подключения к серверу по протоколу SFTP
    ssh_connection: SSHClient,  # объект подключения к серверу по протоколу SSH
    session_scoped_product_api: ProductApi,  # объект API для работы с продуктом
    application_product_path: Path,  # путь к директории продукта
    new_config: list[str],  # список строк, представляющий новый конфиг для сервиса
) -> None:
    """
    Заменить содержимое файла custom.env сервиса на новый конфиг.
    """
    with allure.step(f"Заменить содержимое файла custom.env сервиса на новый конфиг '{new_config}'"):
        # определение путей к файлам
        SERVICE_EXTENDED_PATH = application_product_path / "images/service.extended/"
        SERVICE_EXTENDED_YAML_PATH = SERVICE_EXTENDED_PATH / "docker-compose.yaml"
        SERVICE_EXTENDED_CUSTOM_ENV_PATH = SERVICE_EXTENDED_PATH / "config/custom.env"

        # преобразование списка конфига в строку
        new_config_str = "\n".join(new_config)

        # запись нового конфига в файл custom.env
        with sftp_connection.open(SERVICE_EXTENDED_CUSTOM_ENV_PATH.as_posix(), "w") as f:
            f.write(new_config_str)

        # перезапуск сервиса
        command = f"docker-compose -f {SERVICE_EXTENDED_YAML_PATH.as_posix()} up --no-build -d"
        stdout, stderr = execute_command_and_get_output(ssh_connection, command)

    # проверка, что сервис перезапустился успешно
    if not stderr.splitlines()[-1].endswith("Running"):
        wait_until(
            statement=session_scoped_product_api.service.get_default_request().send,
            condition=lambda response: response.status_code == 200,  # type: ignore
            error_msg="Сервис SERVICE не перезапустился за 1 минуту",
        )


@pytest.fixture(scope="session")
def service_extended_reconfig(
    sftp_connection: SFTPClient,
    ssh_connection: SSHClient,
    session_scoped_product_api: ProductApi,
    application_product_path: Path,
) -> Generator[None, None, None]:
    """
    Фикстура для пере конфигурирования сервиса SERVICE в начале и конце тестового сценария.
    """
    # вызов функции reconfigure_service_product с новым конфигом для сервиса
    reconfigure_service_product(
        application_product_path=application_product_path,
        sftp_connection=sftp_connection,
        ssh_connection=ssh_connection,
        session_scoped_product_api=session_scoped_product_api,
        new_config=[
            "Interval=00:01:00",
            "Period=00:01:00",
        ],
    )

    # выполнение тестового сценария
    yield

    # вызов функции reconfigure_service_product с конфигом по умолчанию для сервиса
    reconfigure_service_product(
        application_product_path=application_product_path,
        sftp_connection=sftp_connection,
        ssh_connection=ssh_connection,
        session_scoped_product_api=session_scoped_product_api,
        new_config=["\n"],
    )
