# -*- coding: utf-8 -*-
from packaging import version

# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from ..utils.exceptions import GetComponentError
from .base import ComponentBase


class Plugins(ComponentBase):

    """Used to sync plugins from a source instance to a destination instance of Swimlane."""

    def _check_for_compatibility(self, plugin_name: str) -> None:
        """Checks the source plugin for compatibility with the destination accepted plugins.

        Args:
            plugin_name (str): The name of the plugin on the source instance.
        """
        dest_version = self.destination_instance.swimlane.product_version
        response = self.source_instance.get_plugin(plugin_name)
        if response and response.get("supportedSwimlaneVersion"):
            if response["supportedSwimlaneVersion"] == ">=10.0.0 <10.5.0":
                if version.parse(dest_version) >= version.parse("10.5.0"):
                    log_string = f"The plugin '{plugin_name}' is not compatible with the destination instance version "
                    log_string += f"({dest_version}). "
                    log_string += "Please upgrade the plugin on the source instance before continuing."
                    self.log(val=log_string, level="warning")
                    self.add_to_homework_list(component_name="plugins", value=log_string)

    def _download_plugin(self, name: str, id: str):
        """Downloads a plugin from a source Swimlane instance.

        Args:
            name (str): The name of the plugin to download.
            id (str): The id of the plugin to download.

        Raises:
            GetComponentError: Raises when unable to download plugin from the source Swimlane instance.

        Returns:
            Plugin: Returns a Swimlane source instance plugin object.
        """
        try:
            self.log(f"Downloading plugin '{name}' from source.")
            return self.source_instance.download_plugin(id)
        except Exception as e:
            raise GetComponentError(type="Plugin", name=name, id=id)

    def sync_plugin(self, name: str, id: str):
        """This class syncs a single Swimlane plugin based on the provided name and ID.

        We first check to see if the provided name of the plugin exists in our destination instances plugin_dict.

        If it is, then we download the plugin from the source instance. If we are successful, we
        then add it to the destination instance.

        If the provided plugin name does not exist in our destination instance plugin_dict then we retrieve the
        plugin from both the source and destination instances. We compare their versions and if the source has
        a version greater than the destination we then add it to the destination instance by upgrading the plugin.

        Args:
            name (str): The name of a Swimlane plugin
            id (str): The internal ID of a Swimlane plugin
        """
        self.log(f"Processing '{name}' plugin with id '{id}'")
        if not self._is_in_include_exclude_lists(name, "plugins"):
            # checking to see if the destination instance already has source instance plugin.
            if not self.dest_plugin_dict.get(name):
                if not ComponentBase.dry_run:
                    plugin = self._download_plugin(name=name, id=id)
                    if plugin:
                        try:
                            self.log(f"Uploading plugin '{name}' to destination.")
                            self.destination_instance.upload_plugin(name, plugin)
                            self.log(f"Successfully uploaded plugin '{name}' to destination.")
                        except Exception as e:
                            self._check_for_compatibility(plugin_name=name)
                            if not ComponentBase.continue_on_error:
                                raise e
                            self.log(
                                f"Failed to upload plugin '{name}' to destination '{self.dest_host}'",
                                level="warning",
                            )
                            self.add_to_homework_list(
                                component_name="plugins",
                                value=f"You must manually install plugin '{name}' and all tasks associated with it. "
                                "This also means you must hookup those tasks with the appropriate items in "
                                "workflow and push-button integrations.",
                            )
                else:
                    self.add_to_diff_log(name, "added")
            else:
                self.log(
                    f"Plugin '{name}' already exists on destination '{self.dest_host}'. Checking for differences...."
                )
                # getting source and destination instance plugins to check differences between them.
                dest_plugin = self.destination_instance.get_plugin(name=name)
                if not dest_plugin:
                    raise GetComponentError(type="Plugin", name=name)
                source_plugin = self.source_instance.get_plugin(name=name)
                if not source_plugin:
                    raise GetComponentError(type="Plugin", name=name)
                if version.parse(source_plugin["version"]) > version.parse(dest_plugin["version"]):
                    # now we actually download the source instance plugin so we can upgrade it on
                    # the destination instance.
                    plugin = self._download_plugin(name=name, id=id)
                    if plugin:
                        if not ComponentBase.dry_run:
                            self.log(f"Upgrading plugin '{name}' on destination.")
                            self.destination_instance.upgrade_plugin(filename=name, stream=plugin)
                            self.log(f"Successfully upgraded plugin '{name}' on destination.")
                        else:
                            self.add_to_diff_log(name, "upgraded")
                else:
                    self.log("Source and destination have the same version plugin. Skipping...")
        else:
            self.log(f"Skipping plugin '{name}' since it is excluded.")

    def sync(self):
        """This method is used to sync all plugins from a source instance to a destination instance"""
        self.log(f"Attempting to sync plugins from '{self.source_host}' to '{self.dest_host}'")
        self.dest_plugin_dict = self.destination_instance.plugin_dict
        plugin_dict = self.source_instance.plugin_dict
        if plugin_dict:
            for name, file_id in plugin_dict.items():
                self.sync_plugin(name=name, id=file_id)
        self.log(f"Completed syncing of plugins from '{self.source_host}' to '{self.dest_host}'.")
