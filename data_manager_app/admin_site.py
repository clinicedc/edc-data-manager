from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

data_manager_app_admin = EdcAdminSite(name="data_manager_app_admin", app_label=AppConfig.name)
