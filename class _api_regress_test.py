# класс тестов* апи на регресс

import allure
import pytest
from assertpy import assert_that

from src.api.abstract_api import AbstractApi
from src.tools.wait import wait_until


@pytest.mark.api
@pytest.mark.product
@pytest.mark.regress
@allure.label("type", "regress")
@allure.label("layer", "API")
@allure.label("microservice", "AbstractMicroservice")
class TestAbstractMicroserviceRegress:
    @allure.id("123456")
    @allure.title("Проверка наличия полей в данных отчета")
    @pytest.mark.parametrize("get_resource_id_by_name", ["Ресурс с данными"], indirect=True)
    def test_add_resource_in_report_and_check_fields(
        self, abstract_api, new_report_id, new_block, get_resource_id_by_name
    ):
        resource_template = abstract_api.get_resource(get_resource_id_by_name).send().value
        add_resource_in_report = (
            abstract_api.add_block_to_report_request(
                report_id=new_report_id,
                payload=AbstractBlockModel.get_default(resource_template),
            )
            .send()
            .value
        )
        report_update = abstract_api.update_report_by_id_request(
            new_report_id, AbstractReportFormModel.get_default()
        ).send()
        assert_that(report_update.status_code).is_equal_to(204)

        response = wait_until(
            statement=abstract_api.get_block_query_request(
                new_report_id, add_resource_in_report.id, section="all", block_version=1
            ).send,
            condition=lambda r: r.status_code == 200,  # type: ignore
            error_msg="Данные секции не получены",
            timeout=90,
            interval=10,
            error_type=AssertionError,
        )
        model = response.value

        all_fields = []

        for node in model["nodes"]:
            field = node["values"].get("Field")
            if field:
                all_fields.append(field)

        with allure.step("Проверить, что отображаются строки"):
            assert_that(all_fields).is_not_empty()

        issues = (
            abstract_api.create_issues_request(new_report_id, AbstractIssueFormModel.get_default()).send().value
        )
        wait_until(
            statement=abstract_api.get_report_issues_by_id_request(new_report_id, issues.id).send,
            condition=lambda r: r.status_code == 200 and r.value.canDownload,  # type: ignore
            error_msg="Отчет не успел выпуститься",
            timeout=360,
            interval=10,
            error_type=AssertionError,
        )
        download_issue = abstract_api.download_issue_request(new_report_id, issues.id).send()
        assert_that(download_issue.status_code).is_equal_to(200)
