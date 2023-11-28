from uuid import uuid4

from django.conf import settings
from django.contrib import admin, messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls.base import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from edc_appointment.constants import IN_PROGRESS_APPT
from edc_constants.constants import CLOSED, DONE, NEW, OPEN
from edc_utils import formatted_datetime, get_utcnow

from ..form_validation_runners import SingleFormValidationRunner
from ..models import QueryRule
from ..rule import update_query_rules

DATA_MANAGER_ENABLED = getattr(settings, "DATA_MANAGER_ENABLED", True)


@admin.action(description="Refresh selected")
def validation_error_refresh(modeladmin, request, queryset):
    for obj in queryset:
        runner = SingleFormValidationRunner(validation_error_obj=obj)
        runner.run()


@admin.action(description="Mark selected as done")
def validation_error_flag_as_done(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = DONE
        obj.save()


@admin.action(description="Mark selected as in progress")
def validation_error_flag_as_in_progress(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = IN_PROGRESS_APPT
        obj.save()


@admin.action(description="Mark selected as new")
def validation_error_flag_as_new(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = NEW
        obj.save()


@admin.action(description=f"Toggle Active/Inactive {QueryRule._meta.verbose_name_plural}")
def toggle_active_flag(modeladmin, request, queryset):
    for obj in queryset:
        obj.active = False if obj.active else True
        obj.save()


@admin.action(description="Toggle DM Status (OPEN/CLOSED)")
def toggle_dm_status(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = OPEN if obj.status != OPEN else CLOSED
        obj.save()


@admin.action(description=f"Copy {QueryRule._meta.verbose_name}")
def copy_query_rule_action(modeladmin, request, queryset):
    if queryset.count() == 1:
        obj = queryset[0]
        options = {
            k: v for k, v in obj.__dict__.items() if not k.startswith("_") and k not in ["id"]
        }
        options["title"] = f"{options['title']} (Copy)"
        options["active"] = False
        options["reference"] = uuid4()
        try:
            queryset.model.objects.get(title=options["title"])
        except ObjectDoesNotExist:
            new_obj = queryset.model.objects.create(**options)
            for o in obj.visit_schedule.all().order_by("timepoint"):
                new_obj.visit_schedule.add(o)
            for o in obj.data_dictionaries.all().order_by("number"):
                new_obj.data_dictionaries.add(o)
            msg = f'Query rule has been copied. New title is "{options["title"]}"'
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            msg = f'Query rule already exists. Got "{options["title"]}"'
            messages.add_message(request, messages.ERROR, msg)
    else:
        messages.add_message(
            request,
            messages.ERROR,
            "Selecting multiple query rules is not allowed. Select just one.",
        )


@admin.action(description=f"Run selected {QueryRule._meta.verbose_name_plural}")
def update_query_rules_action(modeladmin, request, queryset):
    if not DATA_MANAGER_ENABLED:
        msg = (
            "Data manager features are currently disabled. "
            "See settings.DATA_MANAGER_ENABLED."
        )
        messages.add_message(request, messages.ERROR, msg)
    elif queryset:
        if settings.CELERY_ENABLED:
            update_query_rules.delay(pks=[o.pk for o in queryset])
            dte = get_utcnow()
            taskresult_url = reverse("admin:django_celery_results_taskresult_changelist")
            msg = format_html(
                "Updating data queries in the background. "
                "Started at {}. "
                "An updated digest will be email upon completion. "
                'You may also check in <a href="{}?"'
                'task_name=update_query_rules">task results</A>. ',
                mark_safe(formatted_datetime(dte)),  # nosec B703, B308
                mark_safe(taskresult_url),  # nosec B703, B308
            )
        else:
            results = update_query_rules(pks=[o.pk for o in queryset])
            msg = format_html(
                "Done updating data queries. Created {}, " "resolved {}.",
                mark_safe(results.get("created")),  # nosec B703, B308
                mark_safe(results.get("resolved")),  # nosec B703, B308
            )
        messages.add_message(request, messages.SUCCESS, msg)
