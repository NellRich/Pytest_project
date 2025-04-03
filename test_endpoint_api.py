# test endpoint api

import allure
import pytest
from assertpy import assert_that

from src.api.reports_delivery.reports_models import (Model)
from src.tools.wait import wait_until

    @allure.title("Создать выпуск абстрактного отчета")
    def test_create_abstract_issues(self, abstract_api, new_abstract_report_id):
        payload = AbstractIssueFormModel.get_default()
        response = abstract_api.abstract_reports_delivery.create_abstract_issues_request(new_abstract_report_id, payload).send()
        assert_that(response.status_code).is_equal_to(201)

    @allure.title("Получает системный абстрактный отчет по всем источникам")
    def test_get_abstract_report_task(self, abstract_api, new_abstract_system_report):
        response = abstract_api.abstract_reports_delivery.get_abstract_report_task_request(new_abstract_system_report.id).send()
        assert_that(response.status_code).is_equal_to(200) 

    @allure.title("Обновить информацию об абстрактном отчете")
    def test_update_abstract_report_by_id(self, abstract_api, new_abstract_report_id):
        payload = AbstractCustomReportFormModel.get_default()
        response = abstract_api.abstract_reports_delivery.update_abstract_report_by_id_request(new_abstract_report_id, payload).send()
        assert_that(response.status_code).is_equal_to(204) 
    @allure.title("Скачивание выпуска абстрактного отчета")
    def test_download_abstract_issue(self, abstract_api, new_abstract_report_id, new_abstract_report_issues):
        wait_until(
            statement=abstract_api.abstract_reports_delivery.get_abstract_report_issues_by_id_request(
                new_abstract_report_id, new_abstract_report_issues.id
            ).send,
            condition=lambda r: r.status_code == 200 and r.value.canDownload,  # type: ignore
            error_msg="Абстрактный отчет не успел выпуститься",
            timeout=360,
            interval=5,
        )
        response = abstract_api.abstract_reports_delivery.download_abstract_issue_request(new_abstract_report_id, new_abstract_report_issues.id).send()
        assert_that(response.status_code).is_equal_to(200)
