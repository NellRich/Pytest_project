# api_test c прелогином пользователя и созданием дашборда

import time
import pytest
from assertpy import assert_that

@pytest.mark.api
@pytest.mark.product
@pytest.mark.regress
def test_update_dashboard_when_user_is_unblocked(
    api_client,
    user_service,
    new_user,
    get_template_id,
    service_extended_reconfig,
):
    dashboard_name = get_random_string(10)

    api_client.login(new_user.username, get_password())
    endpoint_service = Endpoint_Service(api_client)

    endpoint_service.get_dashboards()
    new_dashboard = endpoint_service.create_dashboard(dashboard_name)
    endpoint_service.add_widget_to_dashboard(new_dashboard.id, get_template_id)

    user_service.block_user(new_user.id)
    user_service.unblock_user(new_user.id)

    api_client.logout()
    api_client.login(new_user.username, get_password())
    endpoint_service = Endpoint_Service(api_client)

    with pytest.step("Wait for 2 minutes for user data to be updated"):
        time.sleep(120)

    with pytest.step("Verify that dashboard is updated successfully after user is unblocked"):
        refresh_dashboard = endpoint_service.refresh_dashboard_widgets(new_dashboard.id)
        assert_that(refresh_dashboard.status_code).is_equal_to(204)

    with pytest.step("Verify that widget can be added to dashboard after user is unblocked"):
        endpoint_service.add_widget_to_dashboard(new_dashboard.id, get_template_id)
