# page modal

import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.components.base_component import ParentType, RootType
from src.components.abstract.common_modal_component import AbstractCommonModalComponent
from src.components.abstract.select.abstract_mc_select_component import AbstractMcSelectComponent


class AbstractModalComponent(AbstractCommonModalComponent):
    def __init__(self, parent: ParentType, root: RootType = ".locator") -> None:
        super().__init__(parent, root)
        self.root.__doc__ = "Модальное окно"

        self.name_input = self.root.locator("input[formcontrolname='Name']")
        self.name_input.__doc__ = "Поле 'Название'"

        self.show_description_link = self.root.locator(".locator", has_text="Добавить описание")
        self.show_description_link.__doc__ = "Ссылка 'Добавить описание'"

        self.description_input = self.root.locator("[name='description']")
        self.description_input.__doc__ = "Поле 'Описание'"

        self.dinput = self.root.locator("[e2e-id='dinput']")
        self.dinput.__doc__ = "Поле 'Доп Описание'"

        self.select = AbstractMcSelectComponent(self.root)
        self.select.__doc__ = "Поле с выпадающим списком"

        self.save_button = self.get_button_by_text("Сохранить")
        self.cancel_button = self.get_button_by_text("Отмена")

    @allure.step("Отредактировать")
    def edit_components(self, **fields: str | bool) -> None:
        self.fill_form(**fields)
        self.save_button.click()

    def fill_form(self, **fields: str | bool) -> None:
        for field_name, field_value in fields.items():
            # Поле ввода описания по умолчанию скрыто
            if field_name == "description_input":
                try:
                    self.description_input.wait_for(timeout=1000)
                except PlaywrightTimeoutError:
                    self.show_description_link.click()

            getattr(self, field_name).fill(field_value)
