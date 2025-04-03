# адаптер для эндпоинта Get c query_params

def get_data_request(
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
        self.request("GET", f"{self.path}/resources/{resource_id}/blocks/{block_id}/sections/{section}/data")
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
  
