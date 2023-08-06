"""redcap tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
# TODO: Import your custom stream types here:
from tap_redcap.streams import (
    RedCapStream,
    RedCapFormStream,
    RedCapEnrollmentStream
)

STREAM_TYPES = [
    RedCapFormStream,
    RedCapEnrollmentStream
]

class TapRedCap(Tap):
    """redcap tap class."""
    name = "tap-redcap"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(    
        th.Property(
            "token",
            th.StringType,
            description="The token to authenticate against the API service"
        ),
        th.Property(
            "action",
            th.StringType,
            description="Specify form for export."
        ),
        th.Property(
            "content",
            th.StringType,
            description="Specify form for export."
        ),
        th.Property(
            "forms",
            th.ArrayType(th.StringType),
            description="Specify form for export."
        ),
        th.Property(
            "events",
            th.StringType,
            description="Specify events for export."
        ),
        th.Property(
            "format",
            th.StringType,
            description="Specify format for export."
        ),
        th.Property(
            "rawOrLabel",
            th.StringType,
            description="Specify raw or label data for export."
        ),
        th.Property(
            "rawOrLabelHeaders",
            th.StringType,
            description="Specify raw or label data headers for export."
        ),
        th.Property(
            "exportCheckboxLabel",
            th.StringType,
            description="Specify checbox labels for export."
        ),
        th.Property(
            "exportSurveyFields",
            th.StringType,
            description="Specify survey fields for export."
        ),
        th.Property(
            "returnFormat",
            th.StringType,
            description="Specify survey return format for export."
        ),
        th.Property(
            "type",
            th.StringType,
            description="Specify type for export."
        ),
        th.Property(
            "exportDataAccessGroups",
            th.StringType,
            description="Specify export for data access group."
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        forms: List[str] = self.config["forms"]
        stream_list = []
        for form in forms:
            if form == "enrollment":
                return [RedCapEnrollmentStream(self,form)]
            stream_list.append(RedCapFormStream(self, form))
        return stream_list
        
