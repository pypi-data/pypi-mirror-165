# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from ..utils.exceptions import GetComponentError
from .base import ComponentBase


class Workflows(ComponentBase):

    """Used to sync workflows from a source instance to a destination instance of Swimlane."""

    def _update_workflow_stages_with_new_id(self, source: dict, new_parent_id: str) -> dict:
        """Updates a workflows stages to match the new parentId.

        Args:
            source (dict): A source workflow dictionary object.
            new_parent_id (str): The new parentId value to replace in a workflows stages.

        Returns:
            dict: An updated source workflow dictionary object.
        """
        if source.get("stages") and source["stages"]:
            source_stages = []
            for source_stage in source["stages"]:
                if source_stage["parentId"] == source["id"]:
                    source_stage["parentId"] = new_parent_id
                source_stages.append(source_stage)
            source["stages"] = source_stages
        return source

    def sync_workflow(self, application_name: str):
        """This methods syncs a single applications workflow from a source Swimlane instance to
        a destination instance.

        If an application_name is in our include or exclude filters we will either ignore or
        process the workflow updates for that application.

        Once an application_name is provided we retrieve the workflow for that application from
        our workflow_dict. Additionally we retrieve the destination workflow for the provided
        application.

        We create a temporary object that compares the stages of a source workflow to a destination
        workflow. If they are exactly the same we skip updating the workflow. If they are not, we
        copy the source workflow to the destination and update it to reflect the new workflow ID.

        Finally we update the destination workflow with our changes.

        Args:
            application_name (str): The name of an application to check and update workflow if applicable.
        """
        # TODO: Add logic to handle when a piece of workflow does not exists. For example, when a task does not exist.
        workflow = self.source_instance.workflow_dict.get(application_name)
        if workflow:
            self.log(
                f"Processing workflow '{workflow['id']}' for application '{application_name}' "
                f"({workflow['applicationId']})."
            )
            dest_workflow = self.destination_instance.get_workflow(application_id=workflow["applicationId"])
            if dest_workflow:
                # We use the source workflow as truth and update it's parentId with the id of the destination
                # workflow.
                workflow = self._update_workflow_stages_with_new_id(source=workflow, new_parent_id=dest_workflow["id"])
                # once we have updated it, it should be similar to the destination workflow
                # So we check to see if they are NOT the same.
                if self.is_objects_different(source=workflow["stages"], destination=dest_workflow["stages"]):
                    if not ComponentBase.dry_run:
                        self.log("Source and destination workflows are different. Updating...")
                        for item in ["$type", "permissions", "version"]:
                            workflow.pop(item)
                        workflow["id"] = dest_workflow["id"]
                        resp = self.destination_instance.update_workflow(workflow=workflow)
                        self.log(f"Successfully updated workflow for application '{application_name}'.")
                    else:
                        self.add_to_diff_log(f"{application_name} - Workflow", "updated")
                else:
                    self.log("Source and destination workflow is the same. Skipping...")
            else:  # May be an edge case and could possibly be removed.
                if not ComponentBase.dry_run:
                    self.log(
                        f"Adding workflow for application '{application_name}' "
                        f"({self.source_instance.application_dict[application_name]['id']})."
                    )
                    dest_workflow = self.destination_instance.add_workflow(workflow=workflow)
                    self.log(f"Successfully added workflow for application '{application_name}'.")
                else:
                    self.add_to_diff_log(f"{application_name} - Workflow", "added")
        else:
            raise GetComponentError(type="Workflow", name=application_name)

    def sync(self):
        """This method is used to sync all workflows from a source instance to a destination instance."""
        raise NotImplementedError("General workflow syncing is currently not implemented.")
