# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import json
import platform
from datetime import datetime

from ..base import Base


class MetaCollector(Base):

    """A class to hold metadata properties about the run time environment."""

    def __init__(self):
        """Instantiate the MetaCollector class to set value defaults."""
        self.hostname = platform.node()
        self.start_timestamp = datetime.now()
        self.components = self._components_used

    @property
    def source(self):
        """Returns a dictionary containing host and version keys of a source Swimlane instance.

        Returns:
            dict: Returns a dict containing host and version information about a source Swimlane instance.
        """
        if hasattr(self.source_instance, "swimlane"):
            return {"version": self.source_instance.swimlane.product_version, "host": str(self.source_host)}
        else:
            return {
                "host": None,
                "version": None,
            }

    @property
    def destination(self):
        """Returns a dictionary containing host and version keys of a destination Swimlane instance.

        Returns:
            dict: Returns a dict containing host and version information about a destination Swimlane instance.
        """
        if hasattr(self.destination_instance, "swimlane"):
            return {"version": self.destination_instance.swimlane.product_version, "host": str(self.dest_host)}
        else:
            return {
                "host": None,
                "version": None,
            }

    @property
    def parameters(self):
        """Returns a dictionary containing parameters used when calling aqueduct.

        Returns:
            dict: Returns a dict the values of the parameters passed into aqueduct.
        """
        for param in [
            "dry_run",
            "offline",
            "update_reports",
            "update_dashboards",
            "continue_on_error",
            "use_unsupported_version",
            "dump_content_path",
            "mirror_app_fields_on_destination",
            "update_default_reports",
        ]:
            return {param: getattr(self, param)}

    @property
    def end_timestamp(self):
        """Returns a time stamp string for now whenever this property is called.

        Returns:
            str: A timestamp.
        """
        return datetime.now()

    def to_json(self):
        """Method to convert properties in this class into an exportable JSON string.

        Returns:
            json: Returns a JSON object that can be written to disk.
        """
        return json.dumps(
            {
                "hostname": self.hostname,
                "start_timestamp": self.start_timestamp.isoformat(),
                "end_timestamp": self.end_timestamp.isoformat(),
                "components": self.components,
                "source": self.source,
                "destination": self.destination,
                "parameters_used": self.parameters,
            }
        )
