# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from ..utils.exceptions import AddComponentError
from .base import ComponentBase


class Reports(ComponentBase):

    """Used to sync reports from a source instance to a destination instance of Swimlane."""

    def _update_destination_report(
        self, source: dict, destination: dict, source_tracking_field: str, application_name=None
    ):
        """Updates the destination report with values missing from the source report.

        Args:
            source (dict): Source Swimlane instance report.
            destination (dict): Destination Swimlane instance report.
            source_tracking_field (str): The source applications tracking-field id.
            application_name (str, optional): Swimlane application name used for logging. Defaults to None.

        Returns:
            dict: Updated destination Swimlane instance report dictionary object.
        """
        if source.get("columns") and destination.get("columns") and source["columns"] != destination["columns"]:
            if ComponentBase.dry_run:
                self.add_to_diff_log(
                    f"{application_name} - {destination['name']} Report",
                    "updated",
                    subcomponent="columns",
                )
            destination["columns"].extend(
                [x for x in source["columns"] if x != source_tracking_field and x not in destination["columns"]]
            )

        if source.get("filters") != destination.get("filters"):
            self.log(f"Updating filters on report '{destination['name']}' on destination.")
            destination["filters"] = source["filters"]
        else:
            self.log(f"No filter updates needed for report '{destination['name']}' report on destination.")

        if source.get("keywords") != destination.get("keywords"):
            self.log(f"Updating keywords on report '{destination['name']}' on destination.")
            destination["keywords"] = source["keywords"]
        else:
            self.log(f"No keywords updates needed for report '{destination['name']}' report on destination.")

        return destination

    def _process_default_report(self, source_report: dict):
        """Used to process 'Default' Swimlane application reports.

        This method has the following workflow/logic:

            We first grab the 'Default' report from the destination instance. 'Default' reports are created
            automatically when you add an application to Swimlane.

            If update_default_reports is set to True and we are NOT doing a dry_run then:

                * scrub to remove the $type keys recursively
                * Get the source application related to this 'Default' report and it's tracking-id
                * Update the 'Default' report by ensuring that the display columns, keywords, and filters match
                * Update the report on the destination instance

        Args:
            source_report (dict): The source swimlane instance report object.

        Raises:
            AddComponentError: Raises when unable to add the 'Default' report to the destination.
        """
        self.log(f"Checking for 'Default' report for application ID '{source_report['applicationIds'][0]}'")
        default_report = self.destination_instance.get_default_report_by_application_id(
            source_report["applicationIds"][0]
        )
        if default_report:
            if ComponentBase.update_default_reports:
                if not ComponentBase.dry_run:
                    self.log(f"Updating 'Default' report for application ID '{source_report['applicationIds'][0]}'.")
                    self.scrub(default_report)
                    source_application = self.source_instance.get_application(source_report["applicationIds"][0])
                    source_tracking_field = self._get_field_by_type(field_list=source_application["fields"])["id"]
                    dest_report = self._update_destination_report(
                        source=source_report,
                        destination=default_report,
                        source_tracking_field=source_tracking_field,
                        application_name=source_application["name"],
                    )
                    resp = self.destination_instance.update_default_report(dest_report)
                    self.log("Successfully updated 'Default' report.")
                else:
                    self.add_to_diff_log(source_report["name"], "updated")
            else:
                self.log(
                    "Default report was found. If you want to update the Default report use"
                    " update_default_reports=True. Skipping..."
                )
        else:
            # This should technically never be called but keeping here just in case.
            if not ComponentBase.dry_run:
                self.log(
                    f"Report '{source_report['name']}' for application IDs '{source_report['applicationIds']}' "
                    "was not found on destination. Adding report..."
                )
                resp = self.destination_instance.add_report(source_report)
                if not resp:
                    raise AddComponentError(model=source_report, name=source_report["name"])
                self.log(f"Successfully added report '{source_report['name']}' to destination.")
            else:
                self.add_to_diff_log(source_report["name"], "added")

    def _process_report(self, source_report: dict):
        """Used to process Swimlane reports (non-default reports).

        If the provided report object does not exist on the destination then we add it.

        If the provided report object does exist on the the destination and:

            1. update_default_reports is set to True
            2. we are NOT doing a dry_run

        Then we:

            * scrub to remove the $type keys recursively
            * Get the source application related to report and it's tracking-id
            * Update the report by ensuring that the display columns, keywords, and filters match
            * Update the report on the destination instance

        Args:
            source_report (dict): The source Swimlane instance report object.

        Raises:
            AddComponentError: Raises when unable to add the report to the destination.
        """
        dest_report = self.destination_instance.get_report(report_id=source_report["id"])
        if not dest_report:
            if not ComponentBase.dry_run:
                self.log(
                    f"Report '{source_report['name']}' for application IDs '{source_report['applicationIds']}'"
                    "was not found on destination. Adding report..."
                )
                resp = self.destination_instance.add_report(source_report)
                if not resp:
                    raise AddComponentError(model=source_report, name=source_report["name"])
                self.log(f"Successfully added report '{source_report['name']}' to destination.")
            else:
                self.add_to_diff_log(source_report["name"], "added")
        elif self.update_reports:
            self.log(
                f"Report '{source_report['name']}' for application IDs '{source_report['applicationIds']}' was found."
                " Checking difference...."
            )
            self.scrub(dest_report)
            if self.is_objects_different(source=source_report, destination=dest_report):
                if not ComponentBase.dry_run:
                    self.log("Source and destination report are different. Updating ...")
                    source_application = self.source_instance.get_application(source_report["applicationIds"][0])
                    source_tracking_field = self._get_field_by_type(field_list=source_application["fields"])["id"]
                    dest_report = self._update_destination_report(
                        source=source_report,
                        destination=dest_report,
                        source_tracking_field=source_tracking_field,
                        application_name=source_application["name"],
                    )
                    self.destination_instance.update_report(source_report["id"], dest_report)
                    self.log(f"Successfully updated report '{source_report['name']}' on destination.")
                else:
                    self.add_to_diff_log(source_report["name"], "updated")
            else:
                self.log(f"No differences found in report '{source_report['name']}'. Skipping...")
        else:
            self.log(f"Skipping check of report '{source_report['name']}' for changes since update_reports is False.")

    def sync_report(self, report: dict):
        """This method syncs a single Swimlane source report dictionary object.

        This method has two branches of processing. The first checks to see if the report is a "Default" report.

            If a report is a "Default" report (e.g. the record view report) then we first attempt to retrieve the
            associated application's default report by it's ID. If that report is not found then we attempt to
            retrieve the report the normal way.

            If we were able to retrieve the report and `update_reports` was set to `True` then we process the default
            report in the update_default_report method (see docs on that method for details). Finally, after processing
            that report we update it on the destination instance.

            If we are NOT able to retrieve the report then we add the report to the destination instance.

        If the report is NOT a "Default" report then we process it like most other components.

            We first check to see if the destination instance has the report. If the report is NOT found on the
            destination then we add the report.

            If the report is found on the destination and `update_reports` was set to `True` then we process the report
            by updating different pieces of the report that are missing from the destination instance.

        Args:
            report (dict): A source Swimlane instance report dictionary object.

        Raises:
            AddComponentError: Raises when we are unable to add a report dictionary object to the destination instance.
        """
        self.log(f"Processing report '{report['name']}' ({report['id']})")
        if not self._is_in_include_exclude_lists(report["name"], "reports"):
            self.scrub(report)
            if report["name"] == "Default":
                self._process_default_report(source_report=report)
            else:
                self._process_report(source_report=report)
        else:
            self.log(f"Skipping report '{report['name']}' since it is excluded.")

    def sync(self):
        """This method is used to sync all reports from a source instance to a destination instance."""
        self.log(f"Attempting to sync reports from '{self.source_host}' to '{self.dest_host}'.")
        reports = self.source_instance.get_reports()
        if reports:
            for report in reports:
                self.sync_report(report=report)
        self.log(f"Completed syncing of reports from '{self.source_host}' to '{self.dest_host}'.")
