|pypi| |travis| |codecov| |downloads|

edc-data-manager
----------------

Data manager administrative models and classes


User Roles
==========

``edc_data_manager`` adds the ``DATA MANAGER`` and the ``DATA_QUERY`` user groups. Members of the ``DATA_QUERY`` group can respond to existing data queries; that is edit existing ``data query`` instances. Members of the ``DATA MANAGER`` group have full access to add/change/delete any ``data_query``.


The Data Query Model
====================
The central model of ``edc_data_manager`` is the ``Data Query`` model. Upon reviewing the state of a research subject's data,
the data manager may decide to open a data query with the research staff. This is done by creating a new ``Data Query`` instance.
The ``data query`` describes an issue for the attention of the research staff at the clinical site. A data query might be general, described
by free text, or specific, indicating references to specific timepoints and form questions.

On the data query form, ``edc_data_manager`` provides access to the complete data dictionary of target model and all timepoints in the data collection schedule.


Data query status
+++++++++++++++++

A data manager, a member of the ``DATA_MANAGER`` group, creates a query. The ``data query`` model instance initially has a status of ``New``. 

The research staff, members of the ``DATA_QUERY`` group, can:

* Open the query -- indicating they are working on the issue. (``Open``)
* Request feedback -- indicating they need assistance from the data manager .(``Feedback``)
* Resolve the query -- indicating the issue is resolved. (``Resolved``)

This status field, managed by the research staff, is independent of the overall status of the query, which is managed by the data manager.

The data manager updates a seperate status field. He/She can:
* Resolve the query (but only if the site status is also ``Resolved``)
* Resolve with an action plan

The data manager can override the status set by the research staff. For example, the data manager may decide to re-open a query.


Using Query Rules to generate data queries
==============================================
Data queries can be automatically generated based on ``query rules`` configured in advance.


The Query Rule model
++++++++++++++++++++++++


Default rule handlers
+++++++++++++++++++++

The default rule handler checks the value of each question at each timepoint in the `QueryRule`. A question represents a model field. If the model field value has been set, e.g. is not ``None``, the question is considered answered.


Custom rule handlers
++++++++++++++++++++

In many cases the default rule handler is too simplistic. If so, a custom rule handler can be written, registered with ``edc_data_manager`` and selected on the ``CrfQueryRule`` form.

Custom rule handlers are classes placed in the ``data_manager.py`` at the root of any app. They subclass the default rule handler, ``ModelHandler`` and override the ``resolved`` method, returning either ``True`` or ``False``. 
If ``resolved`` returns ``True``, the overall data query will be set to ``resolved``. If ``False``, an open query will remain open and a resolved query will be re-opened.


For example:

.. code-block:: python

	# data_manager.py

	from ambition_subject.constants import AWAITING_RESULTS
	from edc_constants.constants import NOT_DONE, YES, NO
	from edc_data_manager.rule import ModelHandler
	from edc_data_manager.site_data_manager import site_data_manager


	class LumbarPunctureHandlerQ13(ModelHandler):

	    name = "lumbar_puncture_q13"
	    display_name = "Lumbar Puncture (Q13, 15, 21, 23, 24)"
	    model_name = "ambition_subject.lumbarpuncturecsf"

	    @property
	    def resolved(self):
	        """Lumbar Puncture/Cerebrospinal Fluid 13, 15, 21, 23, 24.
	        """
	        resolved = False
	        if self.get_field_value("csf_culture") == AWAITING_RESULTS:
	            pass
	        elif self.get_field_value("csf_culture") == NOT_DONE:
	            resolved = True
	        elif self.get_field_value("csf_culture") == YES:
	            if (self.get_field_value("other_csf_culture")
	                    and self.get_field_value("csf_wbc_cell_count")
	                    and self.get_field_value("csf_glucose")
	                    and self.get_field_value("csf_protein")
	                    and (self.get_field_value("csf_cr_ag")
	                         or self.get_field_value("india_ink"))):
	                resolved = True
	        elif self.get_field_value("csf_culture") == NO:
	            if (self.get_field_value("csf_wbc_cell_count")
	                    and self.get_field_value("csf_glucose")
	                    and self.get_field_value("csf_protein")
	                    and (self.get_field_value("csf_cr_ag")
	                         or self.get_field_value("india_ink"))):
	                resolved = True
	        return resolved

	site_data_manager.register(LumbarPunctureHandlerQ13)	

You write any valid python in the ``resolved`` method, but when accessing the model fields referred to in the CrfQueryRule, it is recommended to use the ``get_field_value`` method instead of directly accessing the model instance.


Updating query rules
++++++++++++++++++++

Query rules can be triggered manually to run from the admin action under the CrfQueryRule admin page.

If ``celery`` is enabled, the ``update_crf_query_rules_task`` will try to send proccessing to the MQ.

See also ``update_crf_query_rules``, ``update_crf_query_rules_task``, ``update_crf_query_rules_action``.

.. |pypi| image:: https://img.shields.io/pypi/v/edc-data-manager.svg
    :target: https://pypi.python.org/pypi/edc-data-manager
    
.. |travis| image:: https://travis-ci.com/clinicedc/edc-data-manager.svg?branch=develop
    :target: https://travis-ci.com/clinicedc/edc-data-manager
    
.. |codecov| image:: https://codecov.io/gh/clinicedc/edc-data-manager/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/clinicedc/edc-data-manager

.. |downloads| image:: https://pepy.tech/badge/edc-data-manager
   :target: https://pepy.tech/project/edc-data-manager

