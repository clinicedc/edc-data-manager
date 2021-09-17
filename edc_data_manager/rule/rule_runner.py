import sys

import arrow
from edc_metadata import KEYED, REQUIRED
from edc_metadata.metadata_inspector import MetaDataInspector

from ..models import QueryVisitSchedule
from .query_rule_wrapper import QueryRuleWrapper


class RuleRunner:
    def __init__(self, query_rule_obj=None, now=None, verbose=None):
        self.query_rule_obj = query_rule_obj  # query rule model instance
        self.now = now or arrow.utcnow().datetime
        self.verbose = verbose

    @property
    def reference(self):
        return self.query_rule_obj.reference

    def run(self, query_rules_data=None):
        """Returns number of created and resolved queries after
        running all wrapped query rule objs included in
        query_rules_data.
        """
        created_counter = 0
        resolved_counter = 0
        query_rules_data = query_rules_data or self.query_rules_data
        for key, wrapped_query_rules in query_rules_data.items():
            for wrapped_query_rule in wrapped_query_rules:
                if self.verbose:
                    sys.stdout.write(f"     - running {wrapped_query_rule}\n")
                created, resolved = wrapped_query_rule.run_handler()
                if self.verbose:
                    sys.stdout.write(
                        f"       (queries created: {created}, queries resolved: {resolved})\n"
                    )
                created_counter += created
                resolved_counter += resolved
        return created_counter, resolved_counter

    def run_one(
        self,
        subject_identifier=None,
        visit_schedule_name=None,
        schedule_name=None,
        visit_code=None,
        timepoint=None,
    ):
        visit_schedule_obj = QueryVisitSchedule.objects.get(
            visit_schedule_name=visit_schedule_name,
            schedule_name=schedule_name,
            visit_code=visit_code,
        )
        return self.run(
            query_rules_data={
                visit_schedule_obj.visit_code: [
                    QueryRuleWrapper(
                        query_rule_obj=self.query_rule_obj,
                        subject_identifiers=[subject_identifier],
                        visit_schedule_obj=visit_schedule_obj,
                        timepoint=timepoint,
                        now=self.now,
                    )
                ]
            }
        )

    # @staticmethod
    # def get_timepoints(visit_schedule_obj):
    #     """Returns the timepoints for which there is metadata."""
    #     qs = (
    #         MetaDataInspector.metadata_model_cls.objects.values("timepoint")
    #         .filter(
    #             visit_schedule_name=visit_schedule_obj.visit_schedule_name,
    #             schedule_name=visit_schedule_obj.schedule_name,
    #             visit_code=visit_schedule_obj.visit_code,
    #             visit_code_sequence=0,
    #         )
    #         .distinct()
    #     )
    #     return list(set([obj.get("timepoint") for obj in qs]))

    @property
    def query_rules_data(self):
        """Returns a dictionary of QueryRuleWrappers format
        {visit_code: [wrappper, ...]}.
        """
        query_rules = {}
        for visit_schedule_obj in self.query_rule_obj.visit_schedule.all():
            wrapped_query_rules = []
            if self.verbose:
                sys.stdout.write(
                    f"     - query {visit_schedule_obj.visit_schedule_name}."
                    f"{visit_schedule_obj.schedule_name}.{visit_schedule_obj.visit_code}"
                    f" (timepoint {visit_schedule_obj.timepoint})\n"
                )
            metadata_inspector = MetaDataInspector(
                model_cls=self.query_rule_obj.model_cls,
                visit_schedule_name=visit_schedule_obj.visit_schedule_name,
                schedule_name=visit_schedule_obj.schedule_name,
                visit_code=visit_schedule_obj.visit_code,
                timepoint=visit_schedule_obj.timepoint,
            )
            if metadata_inspector.required:
                wrapped_query_rules.append(
                    QueryRuleWrapper(
                        query_rule_obj=self.query_rule_obj,
                        subject_identifiers=metadata_inspector.required,
                        visit_schedule_obj=visit_schedule_obj,
                        timepoint=visit_schedule_obj.timepoint,
                        now=self.now,
                        entry_status=REQUIRED,
                        verbose=self.verbose,
                    )
                )
            if metadata_inspector.keyed:
                wrapped_query_rules.append(
                    QueryRuleWrapper(
                        query_rule_obj=self.query_rule_obj,
                        subject_identifiers=metadata_inspector.keyed,
                        visit_schedule_obj=visit_schedule_obj,
                        timepoint=visit_schedule_obj.timepoint,
                        now=self.now,
                        entry_status=KEYED,
                        verbose=self.verbose,
                    )
                )
            if wrapped_query_rules:
                query_rules.update({visit_schedule_obj.visit_code: wrapped_query_rules})
        return query_rules
