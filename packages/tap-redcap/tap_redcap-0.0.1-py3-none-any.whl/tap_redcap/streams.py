"""Stream type classes for tap-redcap."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.plugin_base import PluginBase as TapBaseClass
from tap_redcap.client import RedCapStream

class RedCapFormStream(RedCapStream):    
    def __init__(self, tap: TapBaseClass, form: str):
        super().__init__(tap, f"stream_{form}")
        self.forms = form

    path = ""
    schema = th.PropertiesList(
        th.Property(
            "record",
            th.StringType,
            description="The RedCap record ID"
        ),
        th.Property(
            "redcap_event_name",
            th.StringType,
            description="RedCap event name"
        ),
        th.Property(
            "field_name",
            th.StringType,
            description="RedCap field name"
        ),
        th.Property(
            "value",
            th.StringType,
            description="Field value entered by user"
        ),
        th.Property(
            "redcap_repeat_instrument",
            th.StringType,
            description="RedCap repeating instrument name"
        ),
        th.Property(
            "redcap_repeat_instance",
            th.NumberType,
            description="RedCap repeat instance"
        ),
    ).to_dict()
    
    
class RedCapEnrollmentStream(RedCapStream):    
    def __init__(self, tap: TapBaseClass, form: str):
        super().__init__(tap, f"stream_{form}")
        self.forms = form
    
    path = ""   
    schema = th.PropertiesList(
        th.Property(
            "study_id",
            th.StringType,
            description="The RedCap record ID"
        ),
        th.Property(
            "redcap_event_name",
            th.StringType,
            description="RedCap event name"
        ),
        th.Property(
            "redcap_repeat_instrument",
            th.StringType,
            description="RedCap repeating instrument name"
        ),
        th.Property(
            "redcap_repeat_instance",
            th.NumberType,
            description="RedCap repeat instance"
        ),
        th.Property(
            "redcap_data_access_group",
            th.StringType,
            description="The RedCap Data Access Group"
        ),
        th.Property(
            "subject_consent_date",
            th.StringType,
            description="The Subject Consent Date"
        ),
        th.Property(
            "enrollment_status",
            th.StringType,
            description="The Subject Enrollment Status"
        ),
        th.Property(
            "first_name",
            th.StringType,
            description="The Subject First Name"
        ),
        th.Property(
            "last_name",
            th.StringType,
            description="The Subject Last Name"
        ),
        th.Property(
            "mrn",
            th.StringType,
            description="The Subject Medical Record Number"
        ),
        th.Property(
            "dob",
            th.StringType,
            description="The Subject Date of Birth"
        ),
        th.Property(
            "enrollment_complete",
            th.StringType,
            description="Completion status of the Enrollment Form"
        ),
    ).to_dict()
        