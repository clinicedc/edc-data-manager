from django.contrib import admin
from django.urls.conf import include, path
from edc_action_item.admin_site import edc_action_item_admin
from edc_appointment.admin_site import edc_appointment_admin
from edc_lab.admin_site import edc_lab_admin
from edc_locator.admin_site import edc_locator_admin

from data_manager_app.admin_site import data_manager_app_admin
from edc_data_manager.admin_site import edc_data_manager_admin

from .views import HomeView

app_name = "edc_data_manager"


urlpatterns = []

for app_name in [
    "edc_action_item",
    "edc_appointment",
    "edc_consent",
    "edc_dashboard",
    "edc_data_manager",
    "edc_device",
    "edc_lab_dashboard",
    "edc_protocol",
    "edc_reference",
    "edc_subject_dashboard",
    "edc_visit_schedule",
    "data_manager_app",
]:
    urlpatterns.append(path(f"{app_name}/", include(f"{app_name}.urls")))


urlpatterns += [
    path("data_manager_app_admin/", data_manager_app_admin.urls),
    path("edc_data_manager_admin/", edc_data_manager_admin.urls),
    path("edc_action_item_admin/", edc_action_item_admin.urls),
    path("edc_lab_admin/", edc_lab_admin.urls),
    path("edc_appointment_admin/", edc_appointment_admin.urls),
    path("edc_locator_admin/", edc_locator_admin.urls),
    path("accounts/", include("edc_auth.urls")),
    path("edc_auth/", include("edc_auth.urls")),
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="administration_url"),
    path("", HomeView.as_view(), name="home_url"),
]
