import uuid

from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from edc_appointment.models import Appointment
from edc_consent.field_mixins import PersonalFieldsMixin
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO
from edc_identifier.managers import SubjectIdentifierManager
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_lab.model_mixins import RequisitionModelMixin
from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
from edc_model.models import BaseUuidModel
from edc_offstudy.model_mixins import OffstudyModelMixin
from edc_reference.model_mixins import ReferenceModelMixin
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_sites.models import SiteModelMixin
from edc_visit_schedule.model_mixins import OnScheduleModelMixin, OffScheduleModelMixin
from edc_visit_tracking.model_mixins import CrfModelMixin, VisitModelMixin
from edc_consent.field_mixins.identity_fields_mixin import IdentityFieldsMixin
from edc_metadata.model_mixins.updates.updates_crf_metadata_model_mixin import UpdatesCrfMetadataModelMixin


class BasicModel(SiteModelMixin, BaseUuidModel):

    f1 = models.CharField(max_length=10)
    f2 = models.CharField(max_length=10)
    f3 = models.CharField(max_length=10, null=True, blank=False)
    f4 = models.CharField(max_length=10, null=True, blank=False)
    f5 = models.CharField(max_length=10)
    f5_other = models.CharField(max_length=10, null=True)
    subject_identifier = models.CharField(max_length=25, default="12345")


class OnSchedule(OnScheduleModelMixin, BaseUuidModel):

    pass


class OffSchedule(OffScheduleModelMixin, BaseUuidModel):

    pass


class SubjectOffstudy(OffstudyModelMixin, BaseUuidModel):
    class Meta(OffstudyModelMixin.Meta):
        pass


class DeathReport(UniqueSubjectIdentifierFieldMixin, SiteModelMixin, BaseUuidModel):

    objects = SubjectIdentifierManager()

    def natural_key(self):
        return (self.subject_identifier,)


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

    def natural_key(self):
        return (self.subject_identifier,)


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


class SubjectRequisition(RequisitionModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    requisition_datetime = models.DateTimeField(null=True)

    is_drawn = models.CharField(max_length=25, choices=YES_NO, null=True)

    reason_not_drawn = models.CharField(max_length=25, null=True)


class BaseCrfModel(CrfModelMixin, SiteModelMixin, UpdatesCrfMetadataModelMixin,
                   ReferenceModelMixin, models.Model):

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
