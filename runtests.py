#!/usr/bin/env python
import django
import logging
import os
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings
from os.path import abspath, dirname


app_name = 'edc_data_manager'
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    APP_NAME=app_name,
    BASE_DIR=base_dir,
    ETC_DIR=os.path.join(base_dir, app_name, "tests", "etc"),
    DATA_DICTIONARY_APP_LABELS=["data_manager_app"],
    SUBJECT_VISIT_MODEL="data_manager_app.subjectvisit",
    SUBJECT_REQUISITION_MODEL="data_manager_app.subjectrequisition",
    CELERY_ENABLED=False,
    DATA_MANAGER_ENABLED=True,
    EDC_NAVBAR_WARN_ONLY=True,
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "django_crypto_fields.apps.AppConfig",
        "django_revision.apps.AppConfig",
        "edc_action_item.apps.AppConfig",
        "edc_auth.apps.AppConfig",
        "edc_consent.apps.AppConfig",
        "edc_dashboard.apps.AppConfig",
        "edc_lab_dashboard.apps.AppConfig",
        "edc_device.apps.AppConfig",
        "edc_identifier.apps.AppConfig",
        "edc_lab.apps.AppConfig",
        "edc_locator.apps.AppConfig",
        "edc_navbar.apps.AppConfig",
        "edc_metadata_rules.apps.AppConfig",
        "edc_model_admin.apps.AppConfig",
        "edc_notification.apps.AppConfig",
        "edc_protocol.apps.AppConfig",
        "edc_permissions.apps.AppConfig",
        "edc_reference.apps.AppConfig",
        "edc_registration.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "edc_subject_dashboard.apps.AppConfig",
        "edc_timepoint.apps.AppConfig",
        "edc_visit_schedule.apps.AppConfig",
        "edc_data_manager.apps.EdcVisitTrackingAppConfig",
        "edc_data_manager.apps.EdcFacilityAppConfig",
        "edc_data_manager.apps.EdcAppointmentAppConfig",
        "edc_data_manager.apps.EdcMetadataAppConfig",
        "edc_data_manager.apps.AppConfig",
        "data_manager_app.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
    use_test_urls=True,
    add_lab_dashboard_middleware=True,
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split('=')[1] for t in sys.argv if t.startswith('--tag')]
    failures = DiscoverRunner(failfast=False, tags=tags).run_tests(
        [f'{app_name}.tests'])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
