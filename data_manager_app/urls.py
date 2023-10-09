from django.contrib import admin
from django.urls import include, path
from edc_utils.paths_for_urlpatterns import paths_for_urlpatterns

from .admin_site import data_manager_app_admin
from .views import (
    HomeView,
    SubjectDashboardView,
    SubjectListboardView,
    SubjectReviewListboardView,
)

app_name = "data_manager_app"

urlpatterns = SubjectReviewListboardView.urls(app_name, label="subject_review_listboard")
urlpatterns += SubjectDashboardView.urls(app_name, label="subject_dashboard")
urlpatterns += SubjectListboardView.urls(app_name, label="subject_dashboard")

urlpatterns += [
    *paths_for_urlpatterns("edc_data_manager"),
    path("data_manager_app/admin/", data_manager_app_admin.urls),
    path("/admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", HomeView.as_view(), name="home_url"),
    path("", HomeView.as_view(), name="administration_url"),
]
