# ui test POM

import allure
import pytest
from playwright.sync_api import expect

from src.api.abstract.abstract_models import AbstractModel
from src.api.abstract.abstract_models import AbstractDtoModel
from src.components.abstract.common_component import AbstractCommonComponent
from src.pages.abstract.abstract.components.abstract_component import AbstractComponent
from src.pages.abstract.abstracts.abstract_page import AbstractPage

abstract_filter = 'filter(e_src.title = "windows") | select(time, e_src.host, text) | sort(time desc) | group(key: [e_src.id], agg: COUNT(*) as Cnt) | sort(Cnt desc) | limit(10000)'  # noqa: E501
abstract_filter = AbstractDtoModel.get_default()
abstract_filter.pdqlQuery = abstract_filter

abstract_filter_template_3v = AbstractFilterModel.get_default()


@allure.title("Переход на страницу из элемента")
@allure.label("component", "component")
@allure.label("layer", "UI")
@allure.label("type", "regress")
@allure.label("team", "team")
@allure.label("epic", "General", "Release")
@allure.label("suite", "Переходы")
@allure.label("subsuite", "Переход из элемента на страницу")
@allure.id("12345")
@pytest.mark.ui
@pytest.mark.product
@pytest.mark.bvt
@pytest.mark.parametrize(
    "new_abstract_filter, create_abstract_filter",
    [(abstract_filter, abstract_filter_template_3v)],
    indirect=True,
)
def test_transitions_from_component_to_page(
    new_abstract_filters,
    create_abstract_filter,
    new_abstract_component,
    add_component_to_components,
    page,
    open_abstract_page,
    abstract_page,
):
    abstract_page.wait_for_page_update()
    abstract_page.action_bar.select_component(new_abstract_component.name)
    abstract_page.wait_for_page_update()
    abstract_custom = AbstractCommonComponent(page, abstract_filter_template_3v.name)

    abstract = AbstractComponent(abstract_custom.page)

    cell_locator = abstract.get_cell_locator_by_row_value_and_column_index(
        "service", 1
    )
    link_locator = abstract.get_list_link_locator_from_component(cell_locator)
    count = int(link_locator.text_content())
    new_page = abstract.click_locator_to_open_new_tab(link_locator)
    new_tab_page = AbstractPage(new_page)
    new_tab_abstract_page.wait_for_page_update()

    with allure.step("Проверить ..."):
        expect(new_tab_abstract_page.query_filter.query_filtration_button).to_contain_text(
            "e_src.id = 'service'"
        )

    with allure.step("Проверить, что ..."):
        new_tab_abstract_page.wait_for_page_update()
        new_count = new_tab_abstract_page.grid_footer.get_footer_total()
        assert count == new_count

    cell_locator = abstract_.get_cell_locator_by_row_value_and_column_index("Нет данных", 1)
    link_locator = abstract.get_events_list_link_locator_from_grid(cell_locator)
    count_2 = int(link_locator.text_content())
    new_page_2 = abstract.click_locator_to_open_new_tab(link_locator)
    new_tab_abstract_page_2 = AbstractsPage(new_page_2)

    new_tab_abstract_page_2.page.wait_for_load_state()
    new_tab_abstract_page_2.wait_for_page_update()

    with allure.step("Проверить, ...):
        expect(new_tab_abstract_page_2.query_filter.query_filtration_button).to_contain_text("e_src.id = null")

    with allure.step("Проверить, ..."):
        new_tab_abstract_age_2.wait_for_page_update()
        count_2 = new_tab_abstract_page_2.grid_footer.get_footer_total()
        assert count_2 == count_2
