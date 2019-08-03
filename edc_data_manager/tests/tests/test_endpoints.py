from data_manager_app.lab_profiles import lab_profile
from data_manager_app.reference_model_configs import register_to_site_reference_configs
from data_manager_app.visit_schedules import visit_schedule
from django.contrib.auth import get_user_model
from django.test import tag
from django.urls.base import reverse
from django_webtest import WebTest
from edc_data_manager.models import CrfDataDictionary
from edc_data_manager.models.user import DataManagerUser
from edc_lab.site_labs import site_labs
from edc_permissions.constants.group_names import EVERYONE, DATA_MANAGER
from edc_permissions.permissions_updater import PermissionsUpdater
from edc_registration.models import RegisteredSubject
from edc_test_utils.webtest import login
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from model_mommy import mommy

User = get_user_model()


class AdminSiteTest(WebTest):
    def setUp(self):
        self.user = User.objects.create(
            username="user_login",
            email="u@example.com",
            password="pass",
            is_active=True,
            is_staff=True,
        )
        PermissionsUpdater()
        site_labs._registry = {}
        site_labs.loaded = False
        site_labs.register(lab_profile=lab_profile)

        register_to_site_reference_configs()
        site_visit_schedules._registry = {}
        site_visit_schedules.loaded = False
        site_visit_schedules.register(visit_schedule)

    def test_default_rule_handler_names(self):
        """Assert default rule handler names on queryrule ADD form
        """
        login(
            self,
            superuser=False,
            groups=[EVERYONE, DATA_MANAGER],
            redirect_url="admin:index",
        )

        self.app.get(reverse(f"data_manager_app:home_url"), user=self.user, status=200)

        response = self.app.get(
            "/admin/edc_data_manager/queryrule/add/", user=self.user, status=200
        )

        self.assertIn('<option value="do_nothing"', response)
        self.assertIn('<option value="default"', response)

    def test_query_rule_questions_from_single_form(self):
        login(
            self,
            superuser=False,
            groups=[EVERYONE, DATA_MANAGER],
            redirect_url="admin:index",
        )

        query_rule = mommy.make_recipe(
            "edc_data_manager.queryrule",
            sender=DataManagerUser.objects.get(username=self.user.username),
        )

        qs = CrfDataDictionary.objects.all()
        for obj in qs:
            query_rule.data_dictionaries.add(obj)

        res = self.app.get(
            f"/admin/edc_data_manager/queryrule/{str(query_rule.pk)}/change/",
            user=self.user,
        )

        form = res.form
        res = form.submit()
        self.assertIn("Invalid. Select questions from one CRF only", str(res))

    def test_data_query_questions_from_single_form(self):
        login(
            self,
            superuser=False,
            groups=[EVERYONE, DATA_MANAGER],
            redirect_url="admin:index",
        )

        registered_subject = RegisteredSubject.objects.create(
            subject_identifier="092-123456789"
        )

        data_query = mommy.make_recipe(
            "edc_data_manager.dataquery",
            registered_subject=registered_subject,
            sender=DataManagerUser.objects.get(username=self.user.username),
        )

        qs = CrfDataDictionary.objects.all()
        for obj in qs:
            data_query.data_dictionaries.add(obj)

        res = self.app.get(
            f"/admin/edc_data_manager/dataquery/{str(data_query.pk)}/change/",
            user=self.user,
        )

        form = res.form
        res = form.submit()
        self.assertIn("Invalid. Select questions from one CRF only", res)

    @tag("1")
    def test_data_query(self):
        login(
            self,
            superuser=False,
            groups=[EVERYONE, DATA_MANAGER],
            redirect_url="admin:index",
        )

        registered_subject = RegisteredSubject.objects.create(
            subject_identifier="092-123456789"
        )

        data_query = mommy.make_recipe(
            "edc_data_manager.dataquery",
            registered_subject=registered_subject,
            sender=DataManagerUser.objects.get(username=self.user.username),
        )

        crf = CrfDataDictionary.objects.all()[0]
        data_query.data_dictionaries.add(crf)

        res = self.app.get(
            f"/admin/edc_data_manager/dataquery/{str(data_query.pk)}/change/",
            user=self.user,
        )
        form = res.form
        res = form.submit()
        self.assertIn("was changed successfully", str(res))
