# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from ..utils.exceptions import AddComponentError
from .base import ComponentBase


class Roles(ComponentBase):

    """Used to sync roles from a source instance to a destination instance of Swimlane."""

    def _process_role(self, role: dict):
        """Used to ensure any referenced user and groups are processed before continuing with adding / updating roles.

        Args:
            role (dict): A source Swimlane instance role dictionary object.

        Returns:
            dict: A modified source Swimlane instance role dictionary object.
        """
        if role.get("users") and role["users"]:
            self.log(f"Processing users in role '{role['name']}'")
            user_list = []
            from .users import Users

            for user in role["users"]:
                _user = Users().sync_user(user_id=user["id"])
                if _user:
                    user_list.append(_user)
            role["users"] = user_list
        if role.get("groups") and role["groups"]:
            self.log(f"Processing groups in role '{role['name']}'")
            group_list = []
            from .groups import Groups

            for group in role["groups"]:
                _group = Groups().sync_group(group=group)
                if _group:
                    group_list.append(_group)
            role["groups"] = group_list
        return role

    def sync_role(self, role: dict):
        """Syncs a single source Swimlane instance role dictionary object.

        Args:
            role (dict): A source Swimlane instance role dictionary object.

        Raises:
            AddComponentError: Raises when unable to add a role dictionary object to a destination Swimlane instance.

        Returns:
            dict: A destination Swimlane instance `role dictionary object.
        """
        if not self._is_in_include_exclude_lists(role["name"], "roles") and role["name"] not in self.role_exclusions:
            self.log(f"Processing role '{role['name']}' ({role['id']})")
            self.scrub(role)
            role = self._process_role(role=role)
            dest_role = self.destination_instance.get_role(role_id=role["id"])
            if not dest_role:
                if not ComponentBase.dry_run:
                    self.log(f"Creating new role '{role['name']}' on destination.")
                    dest_role = self.destination_instance.add_role(role)
                    if not dest_role:
                        raise AddComponentError(model=role, name=role["name"])
                    self.log(f"Successfully added new role '{role['name']}' to destination.")
                    return dest_role
                else:
                    self.add_to_diff_log(role["name"], "added")
            else:
                self.log(f"Role '{role['name']}' already exists on destination.")
        else:
            self.log(f"Skipping role '{role['name']}' since it is excluded.")

    def sync(self):
        """This method is used to sync all roles from a source instance to a destination instance."""
        self.log(f"Attempting to sync roles from '{self.source_host}' to '{self.dest_host}'.")
        roles = self.source_instance.get_roles()
        if roles:
            for role in roles:
                self.sync_role(role=role)
        self.log(f"Completed syncing of roles from '{self.source_host}' to '{self.dest_host}'.")
