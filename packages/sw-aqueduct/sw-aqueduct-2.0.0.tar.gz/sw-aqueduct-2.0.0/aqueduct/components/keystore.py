# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from .base import ComponentBase


class KeyStore(ComponentBase):

    """Used to sync keystore items from a source instance to a destination instance of Swimlane."""

    def sync(self):
        """Syncing of the keystore will only create new entries into the destination systems keystore.

        The creation of these items does not transfer or implement the transfer of the value since
        these are encrypted within Swimlane themselves.

        Once items are created in the keystore on the destination system then you must manually enter
        the value for that keystore item.
        """
        self.log(f"Attempting to sync keystore from '{self.source_host}' to '{self.dest_host}'")
        credentials = self.source_instance.get_credentials()
        if credentials:
            credentials.pop("$type")
            for key, val in credentials.items():
                if not self._is_in_include_exclude_lists(key, "keystore"):
                    self.log(f"Processing '{key}' credential")
                    if not self.destination_instance.get_credential(key):
                        credential_ = self.source_instance.get_credential(key)
                        if not ComponentBase.dry_run:
                            self.log(f"Adding Keystore item '{key}' to destination.")
                            self.destination_instance.add_credential(credential_)
                            self.log(f"Successfully added new keystore item '{key}'")
                            self.add_to_homework_list(
                                component_name="keystore",
                                value=f"You must manually enter the value for the keystore item '{key}'.",
                            )
                        else:
                            self.add_to_diff_log(key, "added")
                    else:
                        self.log(f"Keystore item '{key}' exists on destination. Skipping....")
                else:
                    self.log(f"Skipping keystore item '{key}' since it is not included.")
        else:
            self.log("Unable to find any keystore values on the source Swimlane instance. Skipping....")
        self.log(f"Completed syncing of keystore from '{self.source_host}' to '{self.dest_host}'.")
