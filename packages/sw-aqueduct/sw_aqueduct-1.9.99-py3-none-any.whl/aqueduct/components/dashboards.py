# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from ..utils.exceptions import AddComponentError, UpdateComponentError
from .base import ComponentBase
from .reports import Reports


class Dashboards(ComponentBase):

    """Used to sync dashboards from a source instance to a destination instance of Swimlane."""

    def _process_reports(self, dashboard: dict):
        """Ensures that any referenced reports actually exist on the source instance.

        Args:
            dashboard (dict): A Swimlane dashboard dictionary object.

        Raises:
            GetComponentError: Raises when a defined report does not exist on a source Swimlane instance.
        """
        self.log(f"Processing dashboard '{dashboard['name']}' reports.")
        for item in dashboard["items"]:
            if item.get("reportId"):
                self.log(
                    f"Dashboard '{dashboard['name']}' contains a report ({item['reportId']}). "
                    "Checking to make sure it exists."
                )
                report = self.source_instance.get_report(report_id=item["reportId"])
                # TODO: Add main parameter to skip if the report does not exist on the source instance.
                # Sometimes a card on a dashboard exists on the dashboard but the associated report does not.
                if not report:
                    self.add_to_homework_list(
                        component_name="dashboards",
                        value="The dashboard '{dashboard['name']}' contains a card pointing to a report "
                        f"({item['reportId']}) that does not exist on the source instance. "
                        "It is recommended to remove this dashboard card from your source instance.",
                    )
                    self.log(
                        f"The dashboard '{dashboard['name']}' contains a report card that does not exist on the "
                        f"source instance. Look for report id '{item['reportId']}' and remove it from the dashboard."
                    )
                else:
                    # Attempting to sync the report
                    Reports().sync_report(report=report)
            else:
                self.log(
                    val=f"Dashboard '{dashboard['name']}' includes a report card that is a card type of "
                    f"'{item.get('cardType')}'."
                )

    def _get_destination_dashboard(self, source_dashboard_uid: str):
        """Returns a matching destination instance dashboard if it exists.

        Args:
            source_dashboard_uid (str): The source instance dashboard UID.
        """
        dest_dashboards = self.destination_instance.get_dashboards()
        if dest_dashboards:
            for d in dest_dashboards:
                if d["uid"] == source_dashboard_uid:
                    return d
        return None

    def sync_dashboard(self, dashboard: dict):
        """This method syncs a single dashboard from a source instance to a destination instance.

        This class first checks to see if the provided dashboard already exists on the destination instance.
        If it does not exist then we attempt to add the dashboard to the destination instance.

        If the dashboard already exists on the destination instance, we first check it against all destination
        instance dashboards. This check involves comparing the provided source dashboard dict with
        the `uid` and `name` of a destination instance dashboard.

        If a match is found, we then check if the version is the same.
        If it is we simply skip processing this dashboard.

        If a match is found but the versions are different, we first ensure that all the reports in the dashboard are on
        the destination instance. Once that is complete, we modify the dashboard to remove unneeded keys and then update
        it as provided by the source instance.

        Args:
            dashboard (dict): A source instance dashboard dictionary.
        """
        self.log(f"Processing dashboard '{dashboard['name']}' ({dashboard['id']})")
        self.scrub(dashboard)
        if not self._is_in_include_exclude_lists(dashboard["name"], "dashboards"):
            # making sure that all reports exist on the source instance.
            self._process_reports(dashboard=dashboard)
            dest_dashboard = self._get_destination_dashboard(source_dashboard_uid=dashboard["uid"])
            # if no dest_dashboard then we need to create it on the destination instance.
            if not dest_dashboard:
                if not ComponentBase.dry_run:
                    self.log(
                        f"Adding dashboard '{dashboard['name']}' for workspaces "
                        f"'{dashboard.get('workspaces')}' on destination"
                    )
                    # These keys need to be in our object but they need to be empty.
                    dashboard = self._set_unneeded_keys_to_empty_dict(component=dashboard)
                    dest_dashboard = self.destination_instance.add_dashboard(dashboard)
                    if not dest_dashboard:
                        raise AddComponentError(model=dashboard, name=dashboard["name"])
                    self.log(f"Successfully added dashboard '{dashboard['name']}' to destination.")
                else:
                    self.add_to_diff_log(dashboard["name"], "added")
            else:
                if self.update_dashboards:
                    self.log(
                        f"Dashboard '{dashboard['name']}' for workspaces '{dashboard.get('workspaces')}' was found."
                        " Checking differences..."
                    )
                    self.scrub(dest_dashboard)
                    if self.is_objects_different(source=dashboard, destination=dest_dashboard):
                        if not ComponentBase.dry_run:
                            self.log(f"Updating '{dashboard['name']}' now.")
                            dest_dashboard = self.destination_instance.update_dashboard(dashboard)
                            if not dest_dashboard:
                                raise UpdateComponentError(model=dashboard, name=dashboard["name"])
                            self.log(f"Successfully updated dashboard '{dashboard['name']}'.")
                        else:
                            self.add_to_diff_log(dashboard["name"], "updated")
                    else:
                        self.log(f"Dashboard '{dashboard['name']}' is the same on source and destination. Skipping...")
                else:
                    self.log(
                        f"Skipping check of dashboard '{dashboard['name']}' for changes since "
                        "update_dashboards is False."
                    )
        else:
            self.log(f"Skipping dashboard '{dashboard['name']}' since it is excluded.")

    def sync(self):
        """This method is used to sync all dashboards from a source instance to a destination instance"""
        self.log(f"Attempting to sync dashboards from '{self.source_host}' to '{self.dest_host}'")
        dashboards = self.source_instance.get_dashboards()
        if dashboards:
            for dashboard in dashboards:
                self.sync_dashboard(dashboard=dashboard)
        self.log(f"Completed syncing of dashboards from '{self.source_host}' to '{self.dest_host}'.")
