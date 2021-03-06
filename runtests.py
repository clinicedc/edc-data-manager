#!/usr/bin/env python
import logging
import os
import sys
from os.path import abspath, dirname

import django
from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_constants.constants import IGNORE
from edc_test_utils import DefaultTestSettings

app_name = "edc_data_manager"
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    APP_NAME=app_name,
    BASE_DIR=base_dir,
    ETC_DIR=os.path.join(base_dir, app_name, "tests", "etc"),
    DATA_DICTIONARY_APP_LABELS=["data_manager_app", "edc_offstudy", "edc_registration"],
    SUBJECT_CONSENT_MODEL="data_manager_app.subjectconsent",
    SUBJECT_VISIT_MODEL="data_manager_app.subjectvisit",
    SUBJECT_REQUISITION_MODEL="data_manager_app.subjectrequisition",
    ADVERSE_EVENT_ADMIN_SITE="adverse_event_app_admin",
    ADVERSE_EVENT_APP_LABEL="adverse_event_app",
    CELERY_ENABLED=False,
    DATA_MANAGER_ENABLED=True,
    EDC_NAVBAR_VERIFY_ON_LOAD=IGNORE,
    EDC_NAVBAR_DEFAULT=app_name,
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
        "edc_adverse_event.apps.AppConfig",
        "adverse_event_app.apps.AppConfig",
        "edc_auth.apps.AppConfig",
        "edc_consent.apps.AppConfig",
        "edc_crf.apps.AppConfig",
        "edc_dashboard.apps.AppConfig",
        "edc_export.apps.AppConfig",
        "edc_lab_dashboard.apps.AppConfig",
        "edc_device.apps.AppConfig",
        "edc_identifier.apps.AppConfig",
        "edc_lab.apps.AppConfig",
        "edc_locator.apps.AppConfig",
        "edc_navbar.apps.AppConfig",
        "edc_model_admin.apps.AppConfig",
        "edc_notification.apps.AppConfig",
        "edc_offstudy.apps.AppConfig",
        "edc_protocol.apps.AppConfig",
        "edc_randomization.apps.AppConfig",
        "edc_reference.apps.AppConfig",
        "edc_pharmacy.apps.AppConfig",
        "edc_registration.apps.AppConfig",
        "edc_review_dashboard.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "edc_subject_model_wrappers.apps.AppConfig",
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
    tags = [t.split("=")[1] for t in sys.argv if t.startswith("--tag")]
    failfast = any([True for t in sys.argv if t.startswith("--failfast")])
    failures = DiscoverRunner(failfast=failfast, tags=tags).run_tests([f"{app_name}.tests"])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
