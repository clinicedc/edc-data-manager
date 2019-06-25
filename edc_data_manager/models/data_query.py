from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from django.template.loader import render_to_string
from edc_action_item.models.action_model_mixin import ActionModelMixin
from edc_constants.constants import OPEN, FEEDBACK, RESOLVED, NEW, NORMAL, HIGH_PRIORITY
from edc_model.models import BaseUuidModel
from edc_sites.models import SiteModelMixin, CurrentSiteManager
from edc_utils.date import get_utcnow

from ..action_items import DATA_QUERY_ACTION
from ..constants import RESOLVED_WITH_ACTION
from .data_dictionary import DataDictionary
from .requisition_panel import RequisitionPanel
from .query_subject import QuerySubject
from .query_visit_schedule import QueryVisitSchedule
from .user import QueryUser, DataManagerUser


RESPONSE_STATUS = (
    (NEW, "New"),
    (OPEN, "Open"),
    (FEEDBACK, "Feedback"),
    (RESOLVED, "Resolved"),
)


TCC_STATUS = (
    (OPEN, "Open"),
    (RESOLVED, "Resolved"),
    (RESOLVED_WITH_ACTION, "Resolved, with plan of action"),
)

QUERY_PRIORITY = ((HIGH_PRIORITY, "High"), (NORMAL, "Normal"))


class DataQuery(ActionModelMixin, SiteModelMixin, BaseUuidModel):

    tracking_identifier_prefix = "DQ"

    action_name = DATA_QUERY_ACTION

    report_datetime = models.DateTimeField(
        verbose_name="Query date", default=get_utcnow
    )

    subject_identifier = models.CharField(max_length=50, null=True, editable=False)

    title = models.CharField(max_length=150, null=True, blank=True)

    sender = models.ForeignKey(
        DataManagerUser,
        related_name="+",
        on_delete=PROTECT,
        verbose_name="Query raised by",
        help_text="select a name from the list",
    )

    recipients = models.ManyToManyField(
        QueryUser,
        related_name="+",
        verbose_name="Sent to",
        help_text="select all that apply",
        blank=True,
    )

    registered_subject = models.ForeignKey(
        QuerySubject,
        verbose_name="Subject Identifier",
        on_delete=PROTECT,
        null=True,
        blank=False,
    )

    query_priority = models.CharField(
        verbose_name="Priority", max_length=25, choices=QUERY_PRIORITY, default=NORMAL
    )

    visit_schedule = models.ForeignKey(
        QueryVisitSchedule,
        verbose_name="Visit",
        on_delete=PROTECT,
        null=True,
        blank=True,
    )

    visit_code_sequence = models.IntegerField(
        verbose_name="Visit code sequence",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(25)],
        help_text=(
            "Defaults to '0'. For example, when combined with the "
            "visit code `1000` would make `1000.0`."
        ),
    )

    timepoint = models.DecimalField(null=True, decimal_places=1, max_digits=6)

    data_dictionaries = models.ManyToManyField(
        DataDictionary,
        verbose_name="CRF question(s)",
        blank=True,
        help_text="select all that apply",
    )

    requisition_panel = models.ForeignKey(
        RequisitionPanel,
        verbose_name="Are responses linked to a requisition? If so, which",
        related_name="+",
        on_delete=PROTECT,
        null=True,
        blank=True,
        help_text="Requisition will be expected on day of visit.",
    )

    query_text = models.TextField(help_text="Describe the query in detail.")

    site_resolved_datetime = models.DateTimeField(
        verbose_name="Site resolved on", null=True, blank=True
    )

    site_response_text = models.TextField(null=True, blank=True)

    site_response_status = models.CharField(
        verbose_name="Site status", max_length=25, choices=RESPONSE_STATUS, default=NEW
    )

    status = models.CharField(
        verbose_name="TCC status", max_length=25, choices=TCC_STATUS, default=OPEN
    )

    tcc_user = models.ForeignKey(
        DataManagerUser,
        verbose_name="TCC resolved by",
        related_name="tcc_user",
        on_delete=PROTECT,
        null=True,
        blank=True,
        help_text="select a name from the list",
    )

    resolved_datetime = models.DateTimeField(
        verbose_name="TCC resolved on", null=True, blank=True
    )

    plan_of_action = models.TextField(
        null=True, blank=True, help_text="If required, provide a plan of action"
    )

    auto_generated = models.BooleanField(
        default=False, help_text="This query was auto-generated by a query rule."
    )

    auto_reference = models.CharField(
        verbose_name="Query rule reference", max_length=150, null=True
    )

    on_site = CurrentSiteManager()

    objects = models.Manager()

    def __str__(self):
        return f"{self.action_identifier[-9:]}"

    def save(self, *args, **kwargs):
        self.subject_identifier = self.registered_subject.subject_identifier
        super().save(*args, **kwargs)

    @property
    def action_item_reason(self):
        template_name = (
            f"edc_data_manager/bootstrap{settings.EDC_BOOTSTRAP}/"
            f"columns/query_text.html"
        )
        context = dict(
            query_priority=self.query_priority,
            query_text=self.query_text,
            questions=self.data_dictionaries.all().order_by("model", "number"),
            report_datetime=self.report_datetime,
            requisition_panel=self.requisition_panel,
            resolved_datetime=self.resolved_datetime,
            site_resolved_datetime=self.site_resolved_datetime,
            site_response_text=self.site_response_text,
            status=self.status,
            tcc_user=self.tcc_user,
            title=self.title,
            visit_schedule=self.visit_schedule,
        )
        return render_to_string(template_name, context=context)

    @property
    def model_names(self):
        models = list(set([dd.model for dd in self.data_dictionaries.all()]))
        return "|".join(models)

    class Meta:
        verbose_name = "Data Query"
        verbose_name_plural = "Data Queries"
        unique_together = ["title", "registered_subject", "visit_schedule"]
