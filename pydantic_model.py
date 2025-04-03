# pydantic model + staticmethod

class AbstractIntervalModel(CustomBaseModel):
    to: int
    from_: int = Field(..., alias="from")

    @staticmethod
    def get_default() -> "AbstractIntervalModel":
        return AbstractIntervalModel(  # type: ignore
            to=int((datetime.today() + timedelta(weeks=50)).timestamp()), from_=int(datetime.today().timestamp())
        )


class AbstractSchedulingModel(CustomBaseModel):
    enabled: bool | None = None
    timezone: str
    periodicity: AbstractPeriodicity
    days: list[int] | None = None
    daysOfWeek: list[AbstractDayOfWeek] | None = None
    fireAt: int
    repeatInterval: int | None = None
    enabledInterval: AbstractEnabledIntervalScheduleModel | None = None
    scheduledInterval: AbstractIntervalModel

    @staticmethod
    def get_default() -> "AbstractSchedulingModel":
        return AbstractSchedulingModel(
            enabled=False,
            timezone="+00:00",
            periodicity=AbstractPeriodicity.WEEKLY,
            days=[],
            daysOfWeek=[AbstractDayOfWeek.MONDAY],
            fireAt=0,
            scheduledInterval=AbstractIntervalModel.get_default(),
        )

    @staticmethod
    def get_abstract_report_with_schedule() -> "AbstractScheduleModel":
        return AbstractScheduleModel(
            enabled=False,
            utcOffset="+00:00",
            periodicity=AbstractPeriodicity.WEEKLY,
            delivery=AbstractDeliveryModel(email=AbstractEmailModel.get_default()),
            days=[],
            daysOfWeek=[AbstractDayOfWeek.MONDAY],
            fireAt=0,
            scheduledInterval=AbstractScheduledIntervalModel.get_default(),
        )

    @staticmethod
    def get_abstract_report_with_schedule() -> "AbstractReportFormModel":
        return AbstractReportFormModel(
            blocks=[],
            format=AbstractReportFormat.PDF,
            layout=AbstractReportLayoutSettingsModel.get_default(),
            name=f"Report_{HelperRandom().random_string}",
            schedule=AbstractScheduleModel.get_abstract_report_with_schedule(),
            description="",
            type="custom",
        )
