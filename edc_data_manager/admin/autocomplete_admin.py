from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.sites.shortcuts import get_current_site
from edc_auth.admin import UserAdmin as BaseUserAdmin
from edc_lab.admin import PanelAdmin as BasePanelAdmin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import VisitScheduleAdmin as BaseVisitScheduleAdmin

from ..admin_site import edc_data_manager_admin
from ..auth_objects import DATA_MANAGER
from ..models import (
    CrfDataDictionary,
    DataManagerUser,
    QuerySubject,
    QueryUser,
    QueryVisitSchedule,
    RequisitionDataDictionary,
    RequisitionPanel,
    VisitDataDictionary,
)


@register(VisitDataDictionary, site=edc_data_manager_admin)
class VisitDataDictionaryAdmin(TemplatesModelAdminMixin, admin.ModelAdmin):
    ordering = ("model",)
    search_fields = ("model",)


@register(CrfDataDictionary, site=edc_data_manager_admin)
class CrfDataDictionaryAdmin(TemplatesModelAdminMixin, admin.ModelAdmin):
    ordering = ("model", "number")
    search_fields = ("model", "prompt", "number")


@register(RequisitionDataDictionary, site=edc_data_manager_admin)
class RequisitionDataDictionaryAdmin(TemplatesModelAdminMixin, admin.ModelAdmin):
    ordering = ("model", "number")
    search_fields = ("model", "prompt", "number")


@register(QuerySubject, site=edc_data_manager_admin)
class QuerySubjectAdmin(SiteModelAdminMixin, admin.ModelAdmin):
    ordering = ("subject_identifier",)
    search_fields = ("subject_identifier",)


@register(RequisitionPanel, site=edc_data_manager_admin)
class RequisitionPanelAdmin(TemplatesModelAdminMixin, BasePanelAdmin):
    ordering = ("display_name",)
    search_fields = ("display_name", "name")


@register(DataManagerUser, site=edc_data_manager_admin)
class DataManagerUserAdmin(BaseUserAdmin):
    ordering = ("first_name", "last_name")
    search_fields = ("first_name", "last_name", "username", "email")

    inlines = []

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(
                groups__name=DATA_MANAGER,
                userprofile__sites__id=get_current_site(request).id,
            )
        )


@register(QueryUser, site=edc_data_manager_admin)
class QueryUserAdmin(BaseUserAdmin):
    ordering = ("first_name", "last_name")
    search_fields = ("first_name", "last_name", "username", "email")

    inlines = []

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(userprofile__sites__id=get_current_site(request).id)
            .exclude(groups__name=DATA_MANAGER)
        )


@register(QueryVisitSchedule, site=edc_data_manager_admin)
class QueryVisitScheduleAdmin(TemplatesModelAdminMixin, BaseVisitScheduleAdmin):
    pass
