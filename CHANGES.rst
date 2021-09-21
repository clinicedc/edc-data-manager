0.3.19
------
- add data query `locked` field to form/changelist. (Lock
  prevents a query rule from re-opening a data query)
- update `edc-auth` default roles in `auths.py`
- set data_query.dm_status to closed for `generated` data queries
  when site_resolved_status set to resolved
- add admin action to toggle data_query.dm_status to open/close
- remove 'font' attribute from templates
- exclude site resolved data queries from `you have open queries` list
  on dashboard

< 0.3.18
--------
- fix looping on undistinct list when updating query rules.
- add management command to update query rules
- create query on save if model referred to in a query rule.
