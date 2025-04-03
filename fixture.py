# fixture

@pytest.fixture()
def new_abstract_widget(
    abstract_api: AbstractApi,
    get_resource_id_by_name: int,
    new_abstract_dashboard: AbstractDashboardDtoModel,
) -> AbstractDataWidgetModel:
    """
    Создание абстрактного дашборда, создание абстрактного виджета и размещение его на дашборде и удаление
    """
    abstract_template = abstract_api.get_abstract_template(get_resource_id_by_name).send()

    new_abstract_widget = (
        abstract_api.add_abstract_widget_to_dashboard_request(
            new_abstract_dashboard.id, abstract_template.extract(dict)
        ).send().value
    )

    yield new_abstract_widget

    abstract_api.delete_abstract_widget_request(
        new_abstract_dashboard.id, new_abstract_widget.id
    ).send()

# OR без удаления

@pytest.fixture()
def new_abstract_widget(
    abstract_api: AbstractApi,
    get_resource_id_by_name: int,
    new_abstract_dashboard: AbstractDashboardDtoModel,
) -> AbstractDataWidgetModel:
    """
    Создание абстрактного дашборда, создание абстрактного виджета и размещение его на дашборде
    """
    abstract_template = abstract_api.get_abstract_template(get_resource_id_by_name).send()

    new_abstract_widget = (
        abstract_api.add_abstract_widget_to_dashboard_request(
            new_abstract_dashboard.id, abstract_template.extract(dict)
        ).send().value
    )

    return abstract_api.get_abstract_widget_request(
        new_abstract_dashboard.id, new_abstract_widget.id
    ).send().value
