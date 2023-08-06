# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from ..utils.exceptions import AccessKeyError, GetComponentError, UpdateComponentError
from .base import ComponentBase


class Tasks(ComponentBase):

    """Used to sync tasks from a source instance to a destination instance of Swimlane."""

    BUILTIN_TASK_ACTION_TYPES = ["python", "python3", "powershell", "api", "email", "networkFile"]

    def __init__(self):
        self._destination_plugin_dict = {}

    @property
    def destination_plugin_dict(self):
        """Creates a destination Swimlane instance plugin dict used to update tasks.

        We need to create this plugin dict since once you upload a plugin to a Swimlane instance
        the plugin `imageId`, `fileId` and `actionId` all change. So we gather the installed plugin
        ids and update any tasks so that they reference the new installed plugin.

        The general structure of this plugin dict is:

            {
                "sw_virus_total": {
                    "GetAnalyses": {
                        "id": "a2dA20RlvfcV5jf34",
                        "imageId": "a8dvYs1Hjn3kFRxCi"
                    },
                    "fileId": "a2cwJFkbVYqB0xfVs"
                }
            }

        Returns:
            dict: A dictionary of values used to update a Swimlane task.
        """
        if not self._destination_plugin_dict:
            plugins = self.destination_instance.get_plugins()
            if plugins:
                for plugin in plugins:
                    action_dict = {}
                    # we get the actual full plugin response from the destination instance.
                    _plugin = self.destination_instance.get_plugin(plugin["id"])
                    # we need the action descriptors (e.g. plugin defined tasks)
                    if _plugin.get("availableActionDescriptors"):
                        for action in _plugin["availableActionDescriptors"]:
                            # for each of these plugin defined tasks
                            if action.get("actionType") and action["actionType"] not in action_dict:
                                # we add the actionType (e.g. task name) to our action_dict
                                action_dict[action["actionType"]] = {}
                            # we update our action_dict with the action id and imageId (every action has it's own
                            # unique ID on the swimlane platform)
                            action_dict[action["actionType"]].update({"id": action["id"], "imageId": action["imageId"]})
                    if _plugin.get("name") and _plugin["name"] not in self._destination_plugin_dict:
                        # we we this new action_dict to the key of the plugin name
                        self._destination_plugin_dict[_plugin["name"]] = action_dict
                    # we also add in the new destination instance plugin fileId. Every time you install a plugin
                    # it gets a new fileId and we must update our tasks with this so they can point to the right
                    # file within the platform.
                    self._destination_plugin_dict[_plugin["name"]].update({"fileId": _plugin["fileId"]})
        return self._destination_plugin_dict

    def _update_task_image_id(self, task: dict, plugin_name: str, action_type: str) -> dict:
        """Updates the provided task with a new plugin imageId.

        When a plugin is installed on a destination system it generates a new imageId.
        We must update our tasks with this new imageId in order for them to work correctly.

        Args:
            task (dict): A source Swimlane instance task dictionary.
            plugin_name (str): The plugin name that the task belongs to.
            action_type (str): The action name within a plugin for this task.

        Raises:
            AccessKeyError: Raises when we are unable to access a certain key in the task dictionary.

        Returns:
            dict: An updated source Swimlane instance task dictionary.
        """
        try:
            task["action"]["descriptor"]["imageId"] = self.destination_plugin_dict[plugin_name][action_type]["imageId"]
        except KeyError as ke:
            raise AccessKeyError(object_name=task["name"], component_type="task", error=ke)
        return task

    def _update_task_file_id(self, task: dict, plugin_name: str) -> dict:
        """Updates the provided task with a new plugin fileId.

        When a plugin is installed on a destination system it generates a new fileId.
        We must update our tasks with this new fileId in order for them to work correctly.

        Args:
            task (dict): A source Swimlane instance task dictionary.
            plugin_name (str): The plugin name that the task belongs to.

        Raises:
            AccessKeyError: Raises when we are unable to access a certain key in the task dictionary.

        Returns:
            dict: An updated source Swimlane instance task dictionary.
        """
        try:
            task["action"]["descriptor"]["packageDescriptor"]["fileId"] = self.destination_plugin_dict[plugin_name][
                "fileId"
            ]
        except KeyError as ke:
            raise AccessKeyError(object_name=task["name"], component_type="task", error=ke)
        return task

    def _update_package_descriptor_id(self, task: dict, plugin_name: str, action_type: str) -> dict:
        """Updates the provided task with a new plugin task id.

        When a plugin is installed on a destination system it generates new ids for the plugin.
        We must update our tasks with this new action id in order for them to work correctly.

        Args:
            task (dict): A source Swimlane instance task dictionary.
            plugin_name (str): The plugin name that the task belongs to.
            action_type (str): The action name within a plugin for this task.

        Raises:
            AccessKeyError: Raises when we are unable to access a certain key in the task dictionary.

        Returns:
            dict: An updated source Swimlane instance task dictionary.
        """
        try:
            task["action"]["packageDescriptorId"] = self.destination_plugin_dict[plugin_name][action_type]["id"]
        except KeyError as ke:
            raise AccessKeyError(object_name=task["name"], component_type="task", error=ke)
        return task

    def _get_action_type(self, task: dict) -> str:
        """Returns the actionType from the current task.

        Args:
            task (dict): A source Swimlane instance task dictionary.

        Raises:
            AccessKeyError: Raises when we are unable to access a certain key in the task dictionary.

        Returns:
            str: An actionType string.
        """
        try:
            return task["action"]["descriptor"]["actionType"]
        except KeyError as ke:
            raise AccessKeyError(object_name=task["name"], component_type="task", error=ke)

    def _get_plugin_name(self, task: dict) -> str:
        """Returns the descriptor name from the current task.

        Args:
            task (dict): A source Swimlane instance task dictionary.

        Raises:
            AccessKeyError: Raises when we are unable to access a certain key in the task dictionary.

        Returns:
            str: An actions descriptor name string.
        """
        try:
            return task["action"]["descriptor"]["packageDescriptor"]["name"]
        except KeyError as ke:
            raise AccessKeyError(object_name=task["name"], component_type="task", error=ke)

    def update_task_plugin_ids(self, task: dict):
        """Used to update tasks with newly uploaded plugin Ids so it can reference the correct plugin in Swimlane.

        Args:
            task (dict): A source Swimlane instance task dictionary.

        Returns:
            Task: An updated source Swimlane instance task dictionary.
        """
        self.log("Retrieving plugins from destination instance", level="debug")
        action_type = self._get_action_type(task=task)
        if action_type and action_type not in self.BUILTIN_TASK_ACTION_TYPES:
            plugin_name = self._get_plugin_name(task=task)
            self.log(f"Updating task '{task['name']}' with correct plugin IDs")
            if self.destination_plugin_dict.get(plugin_name):
                if self.destination_plugin_dict[plugin_name].get(action_type):
                    # We are updating the current source task_ so that it contains the correct Ids for the
                    # destination plugin
                    self.log(
                        f"Updating task '{task['name']}' with correct packageDescriptor fileId "
                        f"'{self.destination_plugin_dict[plugin_name]['fileId']}'"
                    )
                    task = self._update_task_file_id(task=task, plugin_name=plugin_name)
                    self.log(
                        f"Updating task '{task['name']}' with correct imageId "
                        f"'{self.destination_plugin_dict[plugin_name][action_type]['imageId']}'"
                    )
                    task = self._update_task_image_id(task=task, plugin_name=plugin_name, action_type=action_type)
                    self.log(
                        f"Updating task '{task['name']}' with correct packageDescriptorId "
                        f"'{self.destination_plugin_dict[plugin_name][action_type]['id']}'"
                    )
                    task = self._update_package_descriptor_id(
                        task=task, plugin_name=plugin_name, action_type=action_type
                    )
            else:
                self.log(f"Unable to find plugin '{plugin_name}' on destination!")
        return task

    def _update_task_mappings(self, task_mappings: list, task_name: str) -> list:
        """Used to updated task inputs and output mappings with the correct tracking-id.

        Args:
            task_mappings (list): A list of input or output field mappings.
            task_name (str): The name of task these field mappings belong to.

        Returns:
            list: The original or updated task field mappings.
        """
        return_list = []
        for mapping in task_mappings:
            if mapping.get("value") and mapping["value"] and isinstance(mapping["value"], str):
                if self.tracking_id_map.get(mapping["value"]):
                    self.log(
                        f"Updating task '{task_name}' with the correct tracking-id "
                        f"'{self.tracking_id_map[mapping['value']]}'."
                    )
                    mapping["value"] = self.tracking_id_map[mapping["value"]]
            return_list.append(mapping)
        return return_list

    def _check_tasks_using_tracking_id(self, task: dict) -> dict:
        """Updates a task dictionary object that is using tracking-id as input or output with the correct tracking-id.

        Args:
            task (dict): A source Swimlane instance task dictionary.

        Returns:
            dict: A updated source Swimlane instance dictionary.
        """
        if task.get("inputMapping") and task["inputMapping"]:
            task["inputMapping"] = self._update_task_mappings(
                task_mappings=task["inputMapping"], task_name=task["name"]
            )
        if task.get("outputs") and task["outputs"]:
            for output in task["outputs"]:
                if (
                    output.get("backReferenceFieldId")
                    and output["backReferenceFieldId"]
                    and isinstance(output["backReferenceFieldId"], str)
                ):
                    if self.tracking_id_map.get(output["backReferenceFieldId"]):
                        self.log(
                            f"Updating task '{task['name']}' output reference field with the correct tracking-id "
                            f"'{self.tracking_id_map[output['backReferenceFieldId']]}'."
                        )
                        output["backReferenceFieldId"] = self.tracking_id_map[output["backReferenceFieldId"]]
                if output.get("mappings") and output["mappings"]:
                    output["mappings"] = self._update_task_mappings(
                        task_mappings=output["mappings"], task_name=task["name"]
                    )
        return task

    def sync_task(self, task: dict) -> dict:
        """This method syncs a single task from a source Swimlane instance to a destination instance.

        Using the provided task dictionary from Swimlane source instance we first get the actual task
        object from the source.

        Next, we attempt to retrieve the task from the destination system. If the task does not exist
        on the destination instance, we add it. If it does exist, we check if the `uid` and the `version` are the same.
        If they are the same we skip updating the task. If they are different, we update the task on the destination
        instance.

        Args:
            task (dict): A Swimlane task object from a source system.

        Returns:
            dict: If we failed to add a task we return it so we can try again. Only if called using the sync method.
        """
        if not self._is_in_include_exclude_lists(task["name"], "tasks"):
            self.log(f"Processing task '{task['name']}'.")
            task_ = self.source_instance.get_task(task["id"])
            if not task_:
                raise GetComponentError(type="task", name=task["name"], id="")
            if not ComponentBase.dry_run:
                task_ = self.update_task_plugin_ids(task=task_)
            dest_task = self.destination_instance.get_task(task_["id"])
            if not dest_task:
                if not ComponentBase.dry_run:
                    self.log(f"Creating task '{task_['name']}' on destination.")
                    try:
                        # checking tasks for inputs and outputs mapped to source application
                        # tracking-ids and replacing them with the new ones
                        task_ = self._check_tasks_using_tracking_id(task=task_)
                        dest_task = self.destination_instance.add_task(task_)
                        self.log(f"Successfully added task '{task_['name']}' to destination.")
                    except Exception as e:
                        self.log(
                            f"Failed to add task '{task_['name']}' to destination.",
                            level="warning",
                        )
                else:
                    self.add_to_diff_log(task_["name"], "added")
            else:
                self.log(f"Task '{task_['name']}' already exists on destination.")
                if task_["uid"] == dest_task["uid"]:
                    dest_task = self._check_tasks_using_tracking_id(task=task_)
                    if not ComponentBase.dry_run:
                        self.log(f"Task '{task_['name']}' has changed. Updating...")
                        try:
                            dest_task = self.destination_instance.update_task(dest_task["id"], dest_task)
                            if not dest_task:
                                raise UpdateComponentError(model=task_, name=task_["name"])
                            self.log(f"Successfully updated task '{task_['name']}' on destination.")
                        except Exception as e:
                            raise UpdateComponentError(model=task_)
                    else:
                        self.add_to_diff_log(task_["name"], "updated")
                else:
                    self.log(
                        f"The source task '{task['name']}' has a different UID ({task_['uid']}) then the "
                        f"destination task ({dest_task['uid']})"
                    )
        else:
            self.log(f"Skipping task '{task['name']}' since it is excluded.")

    def sync(self):
        """This method is used to sync all tasks from a source instance to a destination instance."""
        self.log(f"Starting to sync tasks from '{self.source_host}' to '{self.dest_host}'.")
        tasks = self.source_instance.get_tasks()
        if tasks:
            for task in tasks:
                self.sync_task(task=task)
        self.log(f"Completed syncing of tasks from '{self.source_host}' to '{self.dest_host}'.")
