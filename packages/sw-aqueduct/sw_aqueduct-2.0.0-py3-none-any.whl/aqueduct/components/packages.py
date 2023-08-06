# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from .base import ComponentBase


class Packages(ComponentBase):

    """Syncs Python packages from a source instance to destination.

    This class can transfer Python package wheels directly using the offline switch when creating an Aqueduct object.
    """

    @property
    def destination_packages(self):
        if not hasattr(self, "__dest_packages"):
            dest_packages = self.destination_instance.get_pip_packages()
            if dest_packages:
                self.__dest_packages = [x["name"] for x in dest_packages]
            else:
                self.__dest_packages = None
        return self.__dest_packages

    def _install_wheels(self, package: dict):
        """Used to install wheels directly from one Swimlane instance to another.

        This is considered an offline installation. To use this method please provide
        `offline=True` when instantiating the Aqueduct class.

        Args:
            package (dict): A Swimlane package dictionary object.
        """
        if package.get("fileId") and package["fileId"]:
            self.log(f"Attempting to transfer wheels for package '{package['name']}'")
            filename = f"{package['name']}-{package['version'].capitalize()}-py3-none-any.whl"
            self.log(f"Downloading package '{package['name']}' version '{package['version']}' from source.")
            stream = self.source_instance.download_plugin(file_id=package["fileId"])
            self.log(f"Successfully downloaded '{package['name']}' from source.")

            self.log(f"Uploading package '{package['name']}' to destination.")
            try:
                data = {"pythonVersion": package["pythonVersion"].capitalize()}

                self.destination_instance.install_package_offline(filename=filename, stream=stream, data=data)
                self.log(f"Successfully uploaded package '{package['name']}' to destination.")
            except Exception as e:
                self.log(
                    f"Error occurred when trying to upload wheels for package '{package['name']}' to destination."
                    " \t\t<-- Please install manually!!"
                )
                self.add_to_homework_list(
                    component_name="packages",
                    value=f"You must manually install '{package['name']}' version '{package['version']}' "
                    "on the destination instance.",
                )
        else:
            self.log(
                f"Unable to transfer wheel package '{package['name']}' to destination. \t\t<--- Must install manually!!"
            )

    def sync_package(self, package: dict):
        """Syncs a single Python package object based on the Swimlane exported dictionary

        Args:
            package (dict): A Swimlane Python package dictionary object.
        """
        if not self._is_in_include_exclude_lists(package["name"], "packages"):
            self.log(f"Processing package '{package['name']}'")
            if package["name"] not in self.destination_packages:
                if not ComponentBase.dry_run:
                    pstring = f"{package['name']}=={package['version']}"
                    self.log(f"Installing {package['pythonVersion']} package '{pstring}' on destination.")
                    if ComponentBase.offline:
                        self._install_wheels(package=package)
                    else:
                        try:
                            resp = self.destination_instance.install_package(package=package)
                        except Exception as e:
                            self.log(
                                f"Unable to install {package['pythonVersion']} package '{pstring}' on destination."
                                " \t\t<-- Please install manually..."
                            )
                            self.add_to_homework_list(
                                component_name="packages",
                                value=f"You must manually install '{package['name']}' version '{package['version']}' "
                                "on the destination instance.",
                            )
                            resp = None
                        if resp:
                            self.log(
                                f"Successfully installed {package['pythonVersion']} package '{pstring}' on destination."
                            )
                else:
                    self.add_to_diff_log(package["name"], "added")
            else:
                self.log(f"Package '{package['name']}' already exists on destination '{self.dest_host}'. Skipping....")

    def sync(self):
        """Sync will sync all installed Python packages on a source system with a destination system.

        If you specified the `offline` switch as `True` then it will transfer the packages directly and
        install them manually instead of relying on Swimlane to install them from pypi.
        """
        self.log(f"Attempting to sync packages from '{self.source_host}' to '{self.dest_host}'")
        packages = self.source_instance.get_pip_packages()
        if packages:
            for package in packages:
                self.sync_package(package=package)
        self.log(f"Completed syncing of packages from '{self.source_host}' to '{self.dest_host}'.")
