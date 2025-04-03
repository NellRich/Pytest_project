# адаптеры для эндпоинтов

def data_request(
    self,
    resource_id: str,
    block_id: int,
    section: str,
    *,
    block_version: int,
    token: str | None = None,
    execution_time: datetime | None = None,
    limit: int | None = None,
    offset: int = 0,
) -> HttpRequest[dict]:
    return (
        self.request("POST", f"{self.path}/resources/{resource_id}/blocks/{block_id}/sections/{section}/data")
        .set_summary("Получить данные для секции")
        .set_query_params(
            {
                "version": block_version,
                "token": token,
                "limit": limit,
                "offset": offset,
                "executionTime": execution_time,
            }
        )
        .set_model_on_status(200, dict)
    )

    def get_abstract_report_issues_by_id_request(self, abstract_report_id: str, abstract_issue_id: str) -> HttpRequest[AbstractIssueInfoModel]:
        return (
            self.request("GET", f"{self.path}/abstract_reports/{abstract_report_id}/abstract_issues/{abstract_issue_id}")
            .set_summary("Получить детальную информацию по выпуску абстрактного отчета")
            .set_model_on_status(200, AbstractIssueInfoModel)
        )

    def abort_abstract_issue_request(self, abstract_report_id: str, abstract_issue_id: str) -> HttpRequest:
        return self.request("GET", f"{self.path}/abstract_reports/{abstract_report_id}/abstract_issues/{abstract_issue_id}/abort").set_summary(
            "Отмена выпуска абстрактного отчета"
        )
  
def get_abstract_pool_request(self, abstract_pool_id: str) -> HttpRequest[AbstractPoolModel]:
    return (
        self.request("GET", f"{self.path}/{abstract_pool_id}")
        .set_summary("Открыть Абстрактный Пул")
        .set_model_on_status(200, AbstractPoolModel)
    )

def update_abstract_pool_request(self, abstract_pool_id: str) -> HttpRequest:
    return self.request("PUT", f"{self.path}/{abstract_pool_id}").set_summary("Отредактировать Абстрактный Пул")

def remove_abstract_pool_request(self, abstract_pool_id: str) -> HttpRequest:
    return self.request("DELETE", f"{self.path}/{abstract_pool_id}").set_summary("Удалить Абстрактный Пул")

def test_abstract_server_pool_request(self, payload: AbstractTestModel) -> HttpRequest[AbstractTestResponseListModel]:
    return (
        self.request("POST", f"{self.path}/test")
        .set_summary("Получить Таблицу Соединений С Абстрактным Пулом")
        .set_body_as_model(payload)
        .set_model_on_status(200, AbstractTestResponseListModel)
    )
