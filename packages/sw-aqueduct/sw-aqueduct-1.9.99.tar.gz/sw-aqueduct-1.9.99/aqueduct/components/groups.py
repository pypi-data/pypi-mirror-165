# -*- coding: utf-8 -*-
from json.decoder import JSONDecodeError

from ..utils.exceptions import AddComponentError

# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from .base import ComponentBase


class Groups(ComponentBase):

    """Used to sync groups from a source instance to a destination instance of Swimlane."""

    def _get_destination_group(self, group: dict):
        """Attempts to retrieve a destination instance group.

        Args:
            group (dict): The source Swimlane instance group dictionary object.

        Returns:
            dict or bool: Returns a group dictionary object if found if not then a boolean.
        """
        try:
            return self.destination_instance.get_group_by_id(group["id"])
        except JSONDecodeError as jd:
            self.log(f"Unable to find group '{group['name']}' by id. Trying by name.")
        try:
            return self.destination_instance.get_group_by_name(group["name"])
        except JSONDecodeError as jd:
            self.log(f"Unable to find group '{group['name']}' by name. Assuming new group.")

    def _process_group(self, group: dict):
        """Processes a source Swimlane instance group objects related objects.

        This method processes any users or roles defined associated with the provided group dictionary object.

        Args:
            group (dict): A source Swimlane instance group dictionary object.

        Returns:
            dict: The source Swimlane instance group dictionary object with possible updates.
        """
        if group.get("users") and group["users"]:
            self.log(f"Processing user association on destination with group '{group['name']}'.")
            user_list = []
            from .users import Users

            for user in group["users"]:
                _user = Users().sync_user(user_id=user["id"])
                if _user:
                    user_list.append(_user)
            group["users"] = user_list

        if group.get("roles") and group["roles"]:
            self.log(f"Processing role association on destination with group '{group['name']}'.")
            role_list = []
            from .roles import Roles

            for role in group["roles"]:
                _role = Roles().sync_role(role=role)
                if _role:
                    role_list.append(_role)
            group["roles"] = role_list
        return group

    def sync_group(self, group: dict):
        """This class syncs a single source instance group to a destination instance.

        We begin by processing the provided group and ensuring that all roles and users
        associated with the provided group are added to the destination instance.

        Once that is complete, we then sync any nested groups within the provided source instance group.

        If the provided group is already on the destination instance, then we just skip processing but if
        the provided group is not on the destination instance we add it.

        Args:
            group (dict): A source instance group dictionary object.
        """
        if (
            not self._is_in_include_exclude_lists(group["name"], "groups")
            and group["name"] not in self.group_exclusions
        ):
            self.log(f"Processing group '{group['name']}' ({group['id']})")
            group = self._process_group(group=group)
            # since groups can have nested groups we are iterating through them as well and processing.
            if group.get("groups") and group["groups"]:
                group_list = []
                for group_ in group["groups"]:
                    group_list.append(self._process_group(group=group_))
                group["groups"] = group_list

            # after we are done processing we now attempt to get a destination instance group.
            dest_group = self._get_destination_group(group=group)

            if not dest_group:
                if not ComponentBase.dry_run:
                    self.log(f"Creating new group '{group['name']}' on destination.")
                    dest_group = self.destination_instance.add_group(group)
                    if not dest_group:
                        raise AddComponentError(model=group, name=group["name"])
                    self.log(f"Successfully added new group '{group['name']}' to destination.")
                else:
                    self.add_to_diff_log(group["name"], "added")
            else:
                self.log(f"Group '{group['name']}' already exists on destination.")
        else:
            self.log(f"Skipping group '{group['name']}' since it is excluded.")

    def sync(self):
        """This method is used to sync all groups from a source instance to a destination instance."""
        self.log(f"Attempting to sync groups from '{self.source_host}' to '{self.dest_host}'")
        groups = self.source_instance.get_groups()
        if groups:
            for group in groups:
                self.sync_group(group=group)
        self.log(f"Completed syncing of groups from '{self.source_host}' to '{self.dest_host}'.")
