# -*- coding: utf-8 -*-
from collections import OrderedDict

# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from ..utils.exceptions import GetComponentError
from .base import ComponentBase
from .workflows import Workflows
from .workspaces import Workspaces


class Applications(ComponentBase):

    """Used to sync applications from a source instance to a destination instance of Swimlane."""

    __applications_needing_updates = []

    def _is_field_in_fields(self, application_fields: list, field: dict) -> bool:
        """Checks to see if a field matches in a list of application fields.

        Args:
            application_fields (list): A Swimlane instance application fields list.
            field (dict): A Swimlane instance application field.

        Returns:
            bool: Whether or not the field is in the provided list of fields.
        """
        for app_field in application_fields:
            if field.get("id") and app_field.get("id") and app_field["id"] == field["id"]:
                return True
        return False

    def _add_fields(self, source: dict, destination: dict):
        """Appends fields to a destination application.

        This method will append fields to a destination application which
        are in the source application but missing from the destination
        application.

        Args:
            source (dict): A Swimlane source instance application.
            destination (dict): A Swimlane destination instance application.

        Returns:
            dict: A Swimlane destination application.
        """
        self.log(f"Checking application '{source['name']}' application for missing fields.")
        if ComponentBase.mirror_app_fields_on_destination:
            self.log(val=f"Force updating application '{source['name']}' fields on destination instance from source.")
            dest_tracking_id_field = self._remove_tracking_field(application=destination)
            self._remove_tracking_field(application=source)
            destination["fields"] = source["fields"]
            destination["fields"].append(dest_tracking_id_field)
            self.log(val=f"Force update of application '{source['name']}' fields successful.")
        else:
            for sfield in source["fields"]:
                if sfield.get("fieldType") and sfield["fieldType"].lower() == "tracking":
                    continue
                if not self._is_field_in_fields(application_fields=destination["fields"], field=sfield):
                    self.log(f"Field '{sfield['name']}' not in destination application.")
                    destination["fields"].append(sfield)
                    self.log(f"Successfully added '{sfield['name']}' to destination application")
                    if ComponentBase.dry_run:
                        self.add_to_diff_log(source["name"], "added", subcomponent="field", value=sfield["name"])
        return destination

    def _remove_tracking_field(self, application: dict):
        """Removes the tracking-id field from an application.

        This method removes an applications tracking field since
        Swimlane automatically generates this for every new application.

        Args:
            application (dict): A Swimlane application to remove the tracking field from
        """
        return_dict = {}
        for field in application.get("fields"):
            if field.get("fieldType") and field["fieldType"].lower() == "tracking":
                if not ComponentBase.dry_run:
                    self.log(f"Removing tracking-id field from application '{application['name']}'.")
                    application["fields"].remove(field)
                    return_dict = field
                else:
                    self.add_to_diff_log(application["name"], "removed", subcomponent="tracking-field")
        return return_dict

    def _process_workspaces(self, application: dict) -> None:
        """Ensures that Swimlane workspaces exist before processing applications.

        Args:
            application (dict): A Swimlane instance application.

        Raises:
            GetComponentError: Raised when an applications Workspace does not exist on the source instance.
        """
        if application.get("workspaces") and application["workspaces"]:
            for workspace in application["workspaces"]:
                workspace_ = self.source_instance.get_workspace(workspace_id=workspace)
                if not workspace_:
                    raise GetComponentError(name="workspace", id=workspace)
                if workspace_ and not self.destination_instance.get_workspace(workspace_id=workspace):
                    Workspaces().sync_workspace(workspace=workspace_)

    def get_reference_app_order(self):
        """Creates a ordered dictionary based on most to least referenced applications.

        This method creates an order of applications to be added or updated on a destination
        instance based on most to least reference relationships. For example, a source application
        that references 5 applications will be before an application which has 3 references to applications.

        Returns:
            dict: An reference application ordered (sorted) application dictionary
        """
        reference_dict = {}
        for application in self.source_instance.get_applications():
            if application:
                application_ = self.source_instance.get_application(application_id=application["id"])
                if application_["id"] not in reference_dict:
                    reference_dict[application_["id"]] = []
                for field in application_["fields"]:
                    if field.get("$type") and field["$type"] == "Core.Models.Fields.Reference.ReferenceField, Core":
                        reference_dict[application_["id"]].append(field["targetId"])

        return_dict = OrderedDict()
        for item in sorted(reference_dict, key=lambda k: len(reference_dict[k]), reverse=True):
            return_dict[item] = reference_dict[item]
        return return_dict

    def sync_application(self, application_id: str):
        """This method syncs a single application from a source instance to a destination instance.

        Once an application_id on a source instance is provided we retrieve this application JSON.
        Next we remove the tracking_field from the application since Swimlane automatically generates
        a unique value for this field.

        If workspaces are defined in the application and do not currently exist will attempt to create
        or update them using the Workspaces class.

        If the source application does not exist on the destination, we will create it with the same IDs for
            1. application
            2. fields
            3. layout
            4. etc.

        By doing this, syncing of applications (and their IDs) is much easier.

        If the application exists, we proceed to remove specific fields that are not needed.

        Next, we check for fields which have been added to the source application but do not
        exist on the destination instance. If fields are found we add them to the destination
        object.

        Next, we check to see if the destination has fields which are not defined in the source instance.
        If fields are found, we then remove them from the layout view of the source application. This equates
        to moving them to the "hidden" field section within the application builder so they can still be retrieved
        and reorganized as needed.

        Finally, we update the application on the destination instance.

        After updating the application we then check to ensure that the workflow of that application is up to date
        and accurate.

        Args:
            application_id (str): A source application ID.
        """
        application = self.source_instance.get_application(application_id=application_id)
        if not application:
            raise GetComponentError(name="application", id=application_id)
        self.log(f"Processing source instance application '{application['name']}'.")
        self._process_workspaces(application=application)
        source_tracking_field = self._remove_tracking_field(application)
        # scrubbing application dict to remove $type keys recursively.
        self.scrub(application)
        if not self._is_in_include_exclude_lists(application["name"], "applications"):
            dest_application = self.destination_instance.get_application(application["id"])
            if not dest_application:
                if not ComponentBase.dry_run:
                    self.log(f"Adding application '{application['name']}' on destination.")
                    dest_application = self.destination_instance.add_application(application)
                    self.__applications_needing_updates.append(application_id)
                    self.log(f"Successfully added application '{application['name']}' on destination.")
                    # Setting tracking_id_map just in case tasks are added and need updating
                    # Tasks would need updating if they use an applications 'Tracking Id' field as an
                    # input or output since Swimlane randomizes the Tracking ID when created
                    self.tracking_id_map = (source_tracking_field["id"], dest_application["trackingFieldId"])
                else:
                    self.add_to_diff_log(application["name"], "added")
            else:
                # removing these keys since they are not needed and only cause issues.
                dest_application = self._set_unneeded_keys_to_empty_dict(component=dest_application)
                dest_application = self._add_fields(source=application, destination=dest_application)
                if not ComponentBase.dry_run:
                    self.log(f"Updating application '{dest_application['name']}' on destination.")
                    # Here we are setting the destination applications layout key to the source applications layout key
                    # we consider the source application layout to be the source of truth
                    dest_application["layout"] = application["layout"]
                    self.destination_instance.update_application(dest_application)
                    self.__applications_needing_updates.append(application_id)
                    self.tracking_id_map = (source_tracking_field["id"], dest_application["trackingFieldId"])
                    self.log(f"Successfully updated application '{dest_application['name']}' on destination.")
                else:
                    self.add_to_diff_log(application["name"], "updated")
            self.log(f"Checking for changes in workflow for application '{application['name']}'")
            Workflows().sync_workflow(application_name=application["name"])
        else:
            self.log(f"Skipping application '{application['name']}' since it is excluded.")

    def sync(self):
        """This method will sync all applications on a source instance with a destination instance."""
        self.log(f"Starting to sync 'Applications' from '{self.source_host}' to '{self.dest_host}'")
        for application_id, values in self.get_reference_app_order().items():
            self.sync_application(application_id=application_id)

        # Checking if we need to update applications reference fields that contain old (source instance)
        # tracking-ids in their columns. If so we remove them and update it with the new ones on the destination.
        if self.__applications_needing_updates:
            for application_id in self.__applications_needing_updates:
                dest_application = self.destination_instance.get_application(application_id)
                needs_update = False
                for field in dest_application["fields"]:
                    if field.get("columns"):
                        column_list = []
                        for column in field["columns"]:
                            if self.tracking_id_map.get(column):
                                self.log(f"Removing old tracking-id '{column}' from application field '{field['key']}'")
                                column_list.append(self.tracking_id_map[column])
                                self.log(
                                    f"Adding new tracking-id '{self.tracking_id_map[column]}' to application field "
                                    f"'{field['key']}'"
                                )
                                needs_update = True
                            else:
                                column_list.append(column)
                        field["columns"] = column_list
                if needs_update:
                    if not ComponentBase.dry_run:
                        self.log(f"Updating application '{dest_application['name']}' on destination with new.")
                        dest_application = self.destination_instance.update_application(dest_application)
                        self.log(f"Successfully updated application '{dest_application['name']}' on destination.")
                    else:
                        self.add_to_diff_log(dest_application["name"], "updated")
