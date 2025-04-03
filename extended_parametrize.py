# extended parametrize 

from datetime import datetime, timedelta

import allure
import pytest

from src.api.abstract_api import AbstractApi
from src.helpers.abstract_time_format_helper import abstract_time_format_helper
from src.tools.assertpy.response_assertions import assert_that
from src.tools.wait import wait_until


@pytest.mark.parametrize(
    "new_report_id", [pytest.param(AbstractReportFormModel.get_report_with_schedule(), id="report_id")], indirect=True
)
@pytest.mark.regress
@pytest.mark.api
@pytest.mark.product
@allure.label("type", "regress")
@allure.label("layer", "API")
@allure.label("microservice", "AbstractMicroservice")
class TestsAbstractReportScheduleConfigRegress:
    @pytest.mark.parametrize(
        "schedule_type, schedule_parameters",
        [
            ("В последний день месяца", {"days": [32], "daysOfWeek": [], "periodicity": AbstractPeriodicity.MONTHLY}),
            (
                "Каждый день с интервалом",
                {
                    "periodicity": AbstractPeriodicity.REPEATABLE_DAILY,
                    "enabledInterval": AbstractDailyEnabledIntervalScheduleModel(
                        to=abstract_time_format_helper.str_time_to_ms("19:00"), from_=abstract_time_format_helper.str_time_to_ms("09:00")
                    ),
                    "repeatInterval": abstract_time_format_helper.str_time_to_minutes("11:25"),
                },
            ),
        ],
    )
    @allure.title("Настройка расписания отчета")
    def test_abstract_report_schedule_parameters_config(self, abstract_api, new_report_id, schedule_type, schedule_parameters):
        schedule = abstract_api.reports_delivery.get_schedule_request(new_report_id).send().value
        for key, value in schedule_parameters.items():
            setattr(schedule, key, value)
        abstract_api.reports_delivery.update_schedule_request(new_report_id, schedule).send()
        with allure.step("Проверить, что расписание изменилось"):
            wait_until(
                statement=abstract_api.reports_delivery.get_schedule_request(new_report_id).send,
                condition=lambda r: assert_that(schedule).is_equal_model(r.value),  # type: ignore
                error_msg="Отчет не обновился",
                error_type=AssertionError,
                timeout=10,
            )

    @pytest.mark.parametrize(
        "schedule_type, schedule_parameters, error_type",
        [
            (
                "Несуществующий день месяца",
                {"days": [65], "daysOfWeek": [], "periodicity": AbstractPeriodicity.MONTHLY},
                "core.triggers.daysOfMonthInvalid.error",
            ),
            (
                "Интервал для еженедельного запуска",
                {
                    "periodicity": AbstractPeriodicity.WEEKLY,
                    "repeatInterval": abstract_time_format_helper.str_time_to_minutes("11:25"),
                },
                "validation.error",
            ),
            (
                "Интервал для ежемесячного запуска",
                {
                    "periodicity": AbstractPeriodicity.MONTHLY,
                    "repeatInterval": abstract_time_format_helper.str_time_to_minutes("11:25"),
                },
                "core.triggers.daysOfMonthNotSpecified.error",
            ),
            (
                "Несуществующее время запуска",
                {
                    "periodicity": AbstractPeriodicity.DAILY,
                    "fireAt": abstract_time_format_helper.str_time_to_ms("45:85"),
                },
                "core.triggers.fireAtTimeExceedsLimit.error",
            ),
            (
                "Несуществующий часовой пояс",
                {
                    "fireAt": abstract_time_format_helper.str_time_to_ms("11:25"),
                    "utcOffset": "+15:00",
                },
                "validation.error",
            ),
            (
                "Время активности вместе с временем запуска",
                {
                    "periodicity": AbstractPeriodicity.REPEATABLE_DAILY,
                    "repeatInterval": abstract_time_format_helper.str_time_to_minutes("05:00"),
                    "fireAt": abstract_time_format_helper.str_time_to_ms("11:25"),
                    "enabledInterval": AbstractDailyEnabledIntervalScheduleModel(
                        from_=abstract_time_format_helper.str_time_to_ms("09:00"),
                        to=abstract_time_format_helper.str_time_to_ms("19:00"),
                    ),
                },
                "validation.error",
            ),
            (
                "Время активности без интервала повтора",
                {
                    "periodicity": AbstractPeriodicity.REPEATABLE_DAILY,
                    "enabledInterval": AbstractDailyEnabledIntervalScheduleModel(
                        from_=abstract_time_format_helper.str_time_to_ms("09:00"),
                        to=abstract_time_format_helper.str_time_to_ms("19:00"),
                    ),
                },
                "validation.error",
            ),
            (
                "Начало планирования после конца",
                {
                    "periodicity": AbstractPeriodicity.DAILY,
                    "scheduledInterval": AbstractScheduledIntervalModel(
                        from_=(datetime.today() + timedelta(weeks=50)), to=datetime.today()
                    ),
                },
                "core.triggers.dateToLessThanDateFrom.error",
            ),
            (
                "Планирование в прошлом",
                {
                    "periodicity": AbstractPeriodicity.DAILY,
                    "scheduledInterval": AbstractScheduledIntervalModel(
                        from_=datetime.today() - timedelta(weeks=50), to=datetime.today() - timedelta(weeks=5)
                    ),
                },
                "core.triggers.dateToLessThanDateFrom.error",
            ),
        ],
    )
    @allure.title("Ошибка при указании некорректных параметров в настройках расписания отчета")
    def test_abstract_report_on_incorrect_schedule_parameters_config(
        self, abstract_api, new_report_id, schedule_type, schedule_parameters, error_type
    ):
        schedule = abstract_api.reports_delivery.get_schedule_request(new_report_id).send().value
        for key, value in schedule_parameters.items():
            setattr(schedule, key, value)
        response = abstract_api.reports_delivery.update_schedule_request(new_report_id, schedule).send()
        with allure.step(f"Проверить, что в ответе есть ошибка: {error_type}"):
            assert_that(response).to_have_status_code(400).to_have_error(error_type)
