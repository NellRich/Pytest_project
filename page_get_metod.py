# page get metod

def get_abstract_component_tab_by_text(self, abstract_component_name: str) -> tuple[Locator, bool]:
    is_item = False
    if self.abstract_component_tabs.filter(has_text=re.compile(f"^{abstract_component_name}$")).is_visible():
        abstract_component_title_tab = self.abstract_component_tabs.locator(".locator").filter(
            has_text=re.compile(f"^{abstract_component_name}$")
        )
    elif self.abstract_button.is_visible():
        if not self.abstract_dropdown_menu.is_visible():
            self.abstract_button.click()
        for locator in self.abstract_dropdown_menu_option.all():
            if abstract_component_name in locator.inner_text():
                abstract_component_title_tab = self.abstract_list_dropdown_menu_option.locator(".locator").filter(
                    has_text=locator.inner_text()
                )
                abstract_component_title_tab.hover()
                is_item = True
                break
        else:
            raise Exception(f"Абстрактный component '{abstract_component_name}' не найден в дропдауне")
    else:
        raise Exception(f"Абстрактный component '{abstract_component_name}' не найден на панели")
    abstract_component_title_tab.__doc__ = f"Вкладка Абстрактного component '{abstract_component_name}'"
    return abstract_component_title_tab, is_item
