# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import inspect
from string import Template

from .utils.logger import LoggingBase


class Base(metaclass=LoggingBase):

    DIFF_TEMPLATE = Template(
        "The '$name' '$component' with the '$subcomponent' value of $value would have been $diff_type on destination."
    )

    OUTPUT_LOG = []
    DIFF_LOG = []
    ZIP_FILE = None

    source_instance = None
    destination_instance = None
    group_exclusions = ["Everyone"]
    role_exclusions = ["Administrator"]
    dry_run = None
    source_host = None
    dest_host = None
    offline = False
    update_reports = False
    update_dashboards = False
    continue_on_error = False
    mirror_app_fields_on_destination = False
    update_default_reports = False
    include = None
    exclude = None
    __diff_types = ["added", "updated", "upgraded", "removed", "moved"]
    __tracking_id_map = {}
    _processed_task_list = []
    _homework = {}
    _dump_content = False
    _has_error_occurred = False
    _has_error_occurred_exception = None
    _components_used = []

    @property
    def tracking_id_map(self):
        """A dictionary map of tracking-ids.

        The key is the source instance trackingFieldId and the value is the destinations trackingFieldId equivalent.

        Returns:
            dict: A tracking-id map.
        """
        if not self.__tracking_id_map:
            for dapp in self.destination_instance.get_applications():
                sapp = self.source_instance.get_application(dapp["id"])
                if sapp:
                    self.__tracking_id_map[sapp["trackingFieldId"]] = dapp["trackingFieldId"]
        return self.__tracking_id_map

    @tracking_id_map.setter
    def tracking_id_map(self, value: tuple):
        """Sets a tuple value to the tracking_id_map dictionary.

        The first value being the source instance trackingFieldId and the second being the destinations trackingFieldId.

        Args:
            value (tuple): A tuple of source and destination trackingFieldIds.
        """
        if isinstance(value, tuple):
            source, dest = value
            self.__tracking_id_map[source] = dest

    def _get_formatted_diff_log(self):
        """Returns a formatted list of strings from the DIFF_LOG property.

        Returns:
            list: A list of strings.
        """
        return_list = []
        for item in Base.DIFF_LOG:
            log = self.DIFF_TEMPLATE.substitute(**item)
            self.log(log)
            return_list.append(log)
        return return_list

    def add_to_homework_list(self, component_name: str, value: str) -> None:
        """Adds a list of items to a dictionary of component name keys

        This method adds the provided value to a dictionary of component_name(s). Once Aqueduct is complete
        we will return this _homework dictionary in a formatted way so that users can have a quick way to understand
        any manual steps they must complete.

        Args:
            component_name (str): The name of the aqueduct component.
            value (str): The value to add to the list of component items.
        """
        if not self._homework.get(component_name):
            self._homework[component_name] = []
        self._homework[component_name].append(value)

    def add_to_diff_log(self, name, diff_type, subcomponent=None, value=""):
        """Adds a dictionary of values to the DIFF_LOG list.

        We create a dictionary of values and add them to our DIFF_LOG list but we also write the output to our log file.

        We gather the component name by inspecting the calling stack.

        Args:
            name (str): The name of the component content item.
            diff_type (str): The type of diff this is. Must be one of 'added','updated','upgraded','removed','moved'.
            subcomponent (str, optional): The subcomponent this is related to (e.g. fields in an app). Defaults to None.
            value (str, optional): str. A value of the subcomponent to add to our dictionary. Defaults to "".

        Raises:
            ValueError: Raises when the provided diff_type is not one of 'added','updated','upgraded','removed','moved'.
        """
        if diff_type in self.__diff_types:
            component = None
            parent = inspect.stack()[1][0].f_locals.get("self", None)
            component = parent.__class__.__name__
            if component and hasattr(f"_{component}", "__logger"):
                if subcomponent:
                    getattr(parent, f"_{component}__logger").info(
                        f"Dry Run: Component '{component}' named '{name}' with subcomponent '{subcomponent}' with value"
                        f" of '{value}' would have been {diff_type} on destination.",
                    )
                else:
                    getattr(parent, f"_{component}__logger").info(
                        f"Dry Run: Component '{component}' named '{name}' would have been {diff_type} on destination."
                    )
            self.DIFF_LOG.append(
                {
                    "component": component,
                    "subcomponent": subcomponent,
                    "name": name,
                    "value": value,
                    "diff_type": diff_type,
                }
            )
        else:
            raise ValueError(f"Unknown type of '{type}' provided. Cannot add to diff log...")

    def log(self, val, level="info"):
        """Used to centralize logging across components.

        We identify the source of the logging class by inspecting the calling stack.

        Args:
            val (str): The log value string to output.
            level (str, optional): The log level. Defaults to "info".
        """
        component = None
        parent = inspect.stack()[1][0].f_locals.get("self", None)
        component = parent.__class__.__name__
        try:
            getattr(getattr(parent, f"_{component}__logger"), level)(val)
            self.OUTPUT_LOG.append(f"{component} - {level.upper()} - {val}")
        except AttributeError as ae:
            self.OUTPUT_LOG.append(f"{component} - {level.upper()} - {val}")

    def _is_in_include_exclude_lists(self, name, type):
        """Checks to see if the name of the component content item is in a include or exclude list.

        Args:
            name (str): The component content item name.
            type (str): The component type.

        Returns:
            bool: Returns True if it is in the exclude or not in the include list else False.
        """
        if self.exclude and self.exclude.get(type) and name in self.exclude[type]:
            self.log(f"{type.capitalize()} '{name}' in exclude list. Skipping...")
            return True
        if self.include and self.include.get(type) and name not in self.include[type]:
            self.log(f"{type.capitalize()} '{name}' is not in include list. Skipping...")
            return True
        return False

    def scrub(self, obj, bad_key="$type"):
        """Used to remove a specific provided key from a dictionary
        that may contain both nested dictionaries and lists.

        This method is recursive.

        Args:
            obj (dict): A dictionary or list to remove keys from.
            bad_key (str, optional): The bad key to remove from the provided dict or list. Defaults to "$type".
        """
        if isinstance(obj, dict):
            for key in list(obj.keys()):
                if key == bad_key:
                    del obj[key]
                else:
                    self.scrub(obj[key], bad_key)
        elif isinstance(obj, list):
            for i in reversed(range(len(obj))):
                if obj[i] == bad_key:
                    del obj[i]
                else:
                    self.scrub(obj[i], bad_key)
        else:
            pass
