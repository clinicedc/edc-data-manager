import uuid

from django.db import models
from django.db.models.deletion import PROTECT
from edc_adverse_event.model_mixins import (
    AeFollowupModelMixin,
    AeInitialModelMixin,
    AesiModelMixin,
    AeSusarModelMixin,
    AeTmgModelMixin,
    DeathReportModelMixin,
    DeathReportTmgModelMixin,
    DeathReportTmgSecondModelMixin,
)
from edc_appointment.models import Appointment
from edc_consent.field_mixins import PersonalFieldsMixin
from edc_consent.field_mixins.identity_fields_mixin import IdentityFieldsMixin
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO
from edc_crf.model_mixins import CrfWithActionModelMixin
from edc_identifier.managers import SubjectIdentifierManager
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_lab.model_mixins import RequisitionModelMixin
from edc_list_data.model_mixins import ListModelMixin
from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
from edc_metadata.model_mixins.updates import UpdatesCrfMetadataModelMixin
from edc_model.models import BaseUuidModel
from edc_model.models.historical_records import HistoricalRecords
from edc_offstudy.model_mixins import OffstudyModelMixin
from edc_reference.model_mixins import ReferenceModelMixin
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_sites.models import SiteModelMixin
from edc_visit_schedule.model_mixins import OffScheduleModelMixin, OnScheduleModelMixin
from edc_visit_tracking.model_mixins import (
    SubjectVisitMissedModelMixin,
    VisitModelMixin,
    VisitTrackingCrfModelMixin,
)


class BasicModel(SiteModelMixin, BaseUuidModel):
    f1 = models.CharField(max_length=10)
    f2 = models.CharField(max_length=10)
    f3 = models.CharField(max_length=10, null=True, blank=False)
    f4 = models.CharField(max_length=10, null=True, blank=False)
    f5 = models.CharField(max_length=10)
    f5_other = models.CharField(max_length=10, null=True)
    subject_identifier = models.CharField(max_length=25, default="12345")


class OnSchedule(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    pass


class OffSchedule(SiteModelMixin, OffScheduleModelMixin, BaseUuidModel):
    pass


class SubjectOffstudy(OffstudyModelMixin, BaseUuidModel):
    class Meta(OffstudyModelMixin.Meta):
        pass


class SubjectConsent(
    ConsentModelMixin,
    PersonalFieldsMixin,
    IdentityFieldsMixin,
    UniqueSubjectIdentifierFieldMixin,
    UpdatesOrCreatesRegistrationModelMixin,
    SiteModelMixin,
    BaseUuidModel,
):
    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.subject_identifier,)  # noqa


class SubjectReconsent(
    ConsentModelMixin,
    PersonalFieldsMixin,
    IdentityFieldsMixin,
    UniqueSubjectIdentifierFieldMixin,
    UpdatesOrCreatesRegistrationModelMixin,
    SiteModelMixin,
    BaseUuidModel,
):
    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.subject_identifier,)  # noqa


class SubjectVisit(
    VisitModelMixin,
    ReferenceModelMixin,
    CreatesMetadataModelMixin,
    SiteModelMixin,
    BaseUuidModel,
):
    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=50)

    reason = models.CharField(max_length=25)


class SubjectVisitMissedReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Subject Missed Visit Reasons"
        verbose_name_plural = "Subject Missed Visit Reasons"


class SubjectVisitMissed(
    SubjectVisitMissedModelMixin,
    CrfWithActionModelMixin,
    BaseUuidModel,
):
    missed_reasons = models.ManyToManyField(
        SubjectVisitMissedReasons, blank=True, related_name="+"
    )

    class Meta(
        SubjectVisitMissedModelMixin.Meta,
        BaseUuidModel.Meta,
    ):
        verbose_name = "Missed Visit Report"
        verbose_name_plural = "Missed Visit Report"


class SubjectRequisition(RequisitionModelMixin, BaseUuidModel):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    requisition_datetime = models.DateTimeField(null=True)

    is_drawn = models.CharField(max_length=25, choices=YES_NO, null=True)

    reason_not_drawn = models.CharField(max_length=25, null=True)


class BaseCrfModel(
    VisitTrackingCrfModelMixin,
    SiteModelMixin,
    UpdatesCrfMetadataModelMixin,
    ReferenceModelMixin,
    models.Model,
):
    f1 = models.CharField(max_length=50, default=uuid.uuid4)

    class Meta:
        abstract = True


class CrfOne(BaseCrfModel, BaseUuidModel):
    f1 = models.CharField(max_length=50, null=True)


class CrfTwo(BaseCrfModel, BaseUuidModel):
    pass


class CrfThree(BaseCrfModel, BaseUuidModel):
    pass


class CrfFour(BaseCrfModel, BaseUuidModel):
    pass


class CrfFive(BaseCrfModel, BaseUuidModel):
    pass


class CrfSix(BaseCrfModel, BaseUuidModel):
    pass


class CrfSeven(BaseCrfModel, BaseUuidModel):
    pass


class RedirectModel(BaseUuidModel):
    subject_identifier = models.CharField(max_length=25)


class RedirectNextModel(BaseUuidModel):
    subject_identifier = models.CharField(max_length=25)


class AeInitial(AeInitialModelMixin, BaseUuidModel):
    class Meta(AeInitialModelMixin.Meta):
        pass


class AeFollowup(AeFollowupModelMixin, BaseUuidModel):
    ae_initial = models.ForeignKey(AeInitial, on_delete=PROTECT)

    class Meta(AeFollowupModelMixin.Meta):
        pass


class Aesi(AesiModelMixin, BaseUuidModel):
    ae_initial = models.ForeignKey(AeInitial, on_delete=PROTECT)

    class Meta(AesiModelMixin.Meta):
        pass


class AeSusar(AeSusarModelMixin, BaseUuidModel):
    ae_initial = models.ForeignKey(AeInitial, on_delete=PROTECT)

    class Meta(AeSusarModelMixin.Meta):
        pass


class AeTmg(AeTmgModelMixin, BaseUuidModel):
    ae_initial = models.ForeignKey(AeInitial, on_delete=PROTECT)

    class Meta(AeTmgModelMixin.Meta):
        pass


class DeathReport(DeathReportModelMixin, BaseUuidModel):
    class Meta(DeathReportModelMixin.Meta):
        pass


class DeathReportTmg(DeathReportTmgModelMixin, BaseUuidModel):
    class Meta(DeathReportTmgModelMixin.Meta):
        pass


class DeathReportTmgSecond(DeathReportTmgSecondModelMixin, BaseUuidModel):
    class Meta(DeathReportTmgSecondModelMixin.Meta):
        pass
