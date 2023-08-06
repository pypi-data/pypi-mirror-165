# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import atexit
import os
import sys
from base64 import b64decode
from collections import OrderedDict

from packaging import version

from .base import Base
from .collector import Collector
from .components import (
    Applications,
    Assets,
    Dashboards,
    Groups,
    KeyStore,
    Packages,
    Plugins,
    Reports,
    Roles,
    Tasks,
    Users,
    Workspaces,
)
from .instance import SwimlaneInstance
from .utils.exceptions import UnsupportedSwimlaneVersion
from .utils.zip import OutputZip

COMPONENTS = OrderedDict(
    [
        ("keystore", KeyStore),
        ("packages", Packages),
        ("plugins", Plugins),
        ("assets", Assets),
        ("workspaces", Workspaces),
        ("applications", Applications),
        ("tasks", Tasks),
        ("reports", Reports),
        ("dashboards", Dashboards),
        ("users", Users),
        ("groups", Groups),
        ("roles", Roles),
    ]
)


class Aqueduct(Base):

    """Aqueduct is used to migrate content from one Swimlane instance to another."""

    __LOGO = "QEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCgvLy9AQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCMvLy8vLy8lQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCgvLy8vLy8vLy8lQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQC8vLy8vLy8vLy8vLy8lQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQC8vLy8vLy8vLy8vLy8vLy8lQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQC8vLy8vLy8vLy8vLy8vLy8vLy8lQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQC8vLy8vLy8vLy8vLy8vLy8vLy8vLy8lQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAJi8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8lQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAJS8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8lQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAKC8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8lQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBALy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8lQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEAmLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8lQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKKC8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8lQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vL0BAQEBAQEBAQC8vLy8vLy8vQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vL0BAQEBAQEBAJi8vLy8vLy8vLy8vLy8vJkBAQEBAQEBAQEBAQEBAQEBAQEAKLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vL0BAQEBAQEBAJi8vLy8vLy8vLy8vLy8vLy8vLy8vJkBAQEBAQEBAQEBAQEBAQEAKLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vL0BAQEBAQEBAJi8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vJkBAQEBAQEBAQEBAQEAKLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vI0BAQEBAQEBAJi8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vJUBAQEBAQEBAQEAKLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vJUBAQEBAQEBAQCgvLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vI0BAQEBAQEAKLy8vLy8vLy8vLy8vLy8vLy8vLy8vI0BAQEBAQEBAQEBAQC8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8oKCoqKkBAQEBAQEAKLy8vLy8vLy8vLy8vLy8vLy8vIyMjIyMjI0BAQEBAQEBAQEAmLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vKCgoLyoqKioqKkBAQEBAQEAKLy8vLy8vLy8vLy8vLy8oIyMjIyMjIyMjIygoKCZAQEBAQEBAQEAmLy8vLy8vLy8vLy8vLy8vLy8vLygoKCgoLyoqKioqKioqKkBAQEBAQEAKLy8vLy8vLy8vLy8oIyMjIyMjIyMoKCgoKCgoKCgoKCVAQEBAQEBAQEBALy8vLy8vLy8vLygoKCgoKCgoLyoqKioqKioqKioqKkBAQEBAQEAKLy8vLy8vLy8oIyMjIyMjKCgoKCgoKCgoKCgoKCgoKCgoKCVAQEBAQEBAQEBAKC8oKCgoKCgoKCgoLyoqKioqKioqKioqKioqKkBAQEBAQEAKLy8vLy8oIyMjKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCVAQEBAQEBAQEBAKCgoKCgoLyoqKioqKioqKioqKioqKioqKkBAQEBAQEAKLy8oKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoQEBAQEBAQEBAQEBAKioqKioqKioqKioqKioqKioqKioqKkBAQEBAQEAKQCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCglQEBAQEBAQEBAKioqKioqKioqKioqKioqKioqKioqKioqKkBAQEBAQEAKQEBAQCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCglQEBAQEBAQEAlKioqKioqKioqKioqKioqKioqKioqKioqKioqKkBAQEBAQEAKQEBAQEBAQCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgmQEBAQEBAQEAjKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKkBAQEBAQEAKQEBAQEBAQEBAQCgoKCgoKCgoKCgoKCgoKCgoKCgoQEBAQEBAQEAjKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKkBAQEBAQEAKQEBAQEBAQEBAQEBAQCMoKCgoKCgoKCgoKCglQEBAQEBAQEAjKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKkBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQCMoKCgoKCgmQEBAQEBAQEAoKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKkBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCUqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCUqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCUqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqJUBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCUqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCUqKioqKioqKioqKioqKioqKioqKioqKioqKiovQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCUqKioqKioqKioqKioqKioqKioqKioqKiooQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCUqKioqKioqKioqKioqKioqKioqKiooQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCUqKioqKioqKioqKioqKioqKiooQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCUqKioqKioqKioqKioqKiojQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCUqKioqKioqKioqKiolQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCUqKioqKioqKiolQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAKQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCUqKioqKiomQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAK"

    def __init__(
        self,
        source: SwimlaneInstance,
        destination: SwimlaneInstance,
        dry_run: bool = True,
        offline: bool = False,
        update_reports: bool = False,
        update_dashboards: bool = False,
        continue_on_error: bool = False,
        use_unsupported_version: bool = False,
        force_unsupported_version: bool = False,
        dump_content_path: str = None,
        mirror_app_fields_on_destination: bool = False,
        update_default_reports: bool = False,
    ):
        """To use aqueduct you must provide two SwimlaneInstance objects. One is the source of content wanting to
        migrate. The other is the destination of where the content will be migrated to.

        Args:
            source (SwimlaneInstance): The source Swimlane instance. Typically this is considered a
                                       development instance.
            destination (SwimlaneInstance): The destination Swimlane instance. Typically this is considered a production
                                            instance.
            dry_run (bool): Whether or not this run of aqueduct will transfer content to the destination instance.
                            Set to False to migrate content. Default is True.
            offline (bool): Whether or not the destination instance has access to the internet for the purpose of
                            downloading Python packages. Default is False
            update_reports (bool): Whether or not to force update reports if changes are detected. Default is False.
            update_dashboards: (bool): Whether or not to force update dashboards if changes are detected.
                                       Default is False.
            continue_on_error: (bool): Whether or not to continue when an API error occurs. Default is False.
            use_unsupported_version: (bool): Whether or not to transfer content from one version Swimlane to a different
                                             version of Swimlane. Use this at your own risk. Default is False.
            force_unsupported_version: (bool): Whether or not to force usage of an unsupported version. This is used
                                               when running aqueduct headless/non-interactive. Default is False.
            dump_content_path: (str, optional): The path to where content should be dumped. If provided, we will dump
                                                content to a zip file in the provided path.
            mirror_app_fields_on_destination: (bool, optional): Whether or not to mirror application fields from the
                                                                source to the destination. This may result in deletion
                                                                of fields on the destination instance. Defaults to
                                                                False.
            update_default_reports: (bool, optional): Whether or not to update Default reports on the destination.
                                                      Default is False.
        """
        src_version = version.parse(source.swimlane.product_version)
        dest_version = version.parse(destination.swimlane.product_version)
        if use_unsupported_version and src_version != dest_version:
            if src_version > dest_version:
                raise UnsupportedSwimlaneVersion(source=source, destination=destination)
            self.log(
                f"You specified you want to transfer of content from version {source.swimlane.product_version} to "
                f"{destination.swimlane.product_version}. This is not officially supported. "
                "Please use at your own risk.",
                level="info",
            )
            if not force_unsupported_version and not self.__want_to_continue():
                sys.exit()
        elif src_version != dest_version:
            raise UnsupportedSwimlaneVersion(source=source, destination=destination)
        Base.source_instance = source
        Base.source_instance.instance_type = "source"
        Base.destination_instance = destination
        Base.destination_instance.instance_type = "destination"
        Base.dry_run = dry_run
        Base.source_host = Base.source_instance.swimlane.host
        Base.dest_host = Base.destination_instance.swimlane.host
        Base.offline = offline
        Base.update_reports = update_reports
        Base.update_dashboards = update_dashboards
        Base.continue_on_error = continue_on_error
        Base.update_default_reports = update_default_reports
        Base.mirror_app_fields_on_destination = mirror_app_fields_on_destination

        if dump_content_path:
            Base._dump_content = True
            Base.ZIP_FILE = OutputZip(zip_path=dump_content_path)
        else:
            Base._dump_content = False
            Base.ZIP_FILE = OutputZip(zip_path=os.getcwd())
        atexit.register(self._return_homework_list)
        atexit.register(self._close_and_write_zip)

    def __want_to_continue(self):
        """A recursive method that will continually ask if you want to continue until you provide a correct answer.

        Returns:
            bool: Returns whether or not the user wants to continue.
        """
        response = input("Do you want to continue (y or n): ")
        if response.capitalize()[0] == "N":
            return False
        elif response.capitalize()[0] == "Y":
            return True
        else:
            return self.__want_to_continue()

    def _close_and_write_zip(self) -> None:
        """Used to close and write a zip file to disk at exit.

        The ZIP_FILE object will close no matter what when calling the write_to_disk method but it will only
        create a zip file on the disk when there are files in the BytesIO object.

        This will be called no matter what but there are two situations in which data will be saved to disk.

            1. If a dump_content_path is provided then we will dump all (defined) content into a zipfile in the
               provided path.
            2. No matter if the dump_content_path is provided, if an error occurs with an API call we will dump
               the content into a zipfile named aqueduct_errors.zip in the currently working directory.

        The created zipfile has the following structure (example only):

            📦aqueduct
            ┣ 📂content
            ┃ ┣ 📂altered
            ┃ ┃ ┣ 📂application
            ┃ ┃ ┃ ┗ 📜Phishing Triage.json
            ┃ ┃ ┗ 📂workspace
            ┃ ┃ ┃ ┣ 📜QuickStart Record Generator.json
            ┃ ┣ 📂destination
            ┃ ┃ ┣ 📂application
            ┃ ┃ ┃ ┗ 📜Phishing Triage.json
            ┃ ┃ ┣ 📂workflow
            ┃ ┃ ┃ ┗ 📜aM_t7AuBscJN_Orf9.json
            ┃ ┃ ┗ 📂workspace
            ┃ ┃ ┃ ┣ 📜QuickStart Record Generator.json
            ┃ ┗ 📂source
            ┃ ┃ ┣ 📂application
            ┃ ┃ ┃ ┣ 📜Alert & Incident Management.json
            ┃ ┃ ┗ 📂workflows
            ┃ ┃ ┃ ┣ 📜a7HOzfbLmUD7xOkKp.json
            ┣ 📜homework.txt
            ┗ 📜output.log

        The three folders under the `content` directory are altered, source, and destination.

            source - This means the original (GET) source JSON object from the source instance
            altered - The altered folder contains JSON objects that have been "massaged" or updated based on the
                      differences between both source and destination (if any). This it the JSON that is sent to the
                      destination instance.
            destination - This means the JSON response from the destination Swimlane instance.
        """
        if Base.ZIP_FILE:
            Base.ZIP_FILE.write_to_disk()

    def _return_homework_list(self):
        """Prints a summary homework list for quick actionable response.

        You can access the homework dictionary from your `Aqueduct` instance.
        Example:

            from aqueduct import Aqueduct

            aq = Aqueduct(source=src, destination=dest)

            print(aq._homework) # This will print out the dictionary of component lists.

        """
        if self._homework:
            print("HOMEWORK LIST:\n")
            for key in self._homework.keys():
                if self._homework[key]:
                    print(key.title())
                    for item in self._homework[key]:
                        print(f"\t{item}")

    def __sort_sync_order(self, components: list):
        """Ensures order of provided component name strings.

        Args:
            components (list): A list of component name strings.

        Returns:
            list: An ordered list of component names.
        """
        ordered = []
        for key, val in COMPONENTS.items():
            if key in components:
                ordered.append(key)
        return ordered

    def sync(self, components=COMPONENTS, exclude: dict = {}, include: dict = {}):
        """The main method to begin syncing components from one Swimlane instance to another.

        There are several available components you can specify. The order of these components if forced.
        The defaults are:

        * keystore
        * packages
        * plugins
        * assets
        * workspaces
        * applications (we update workflows here)
        * tasks
        * reports
        * dashboards
        * users
        * groups
        * roles

        You can include and exclude specific component items like specific applications, tasks, plugins, etc. To do so
        provide a dictionary for each argument (include or exclude). For example:

        exclude = {'applications': ["Phishing Triage"], 'tasks': ['PT - Get Emails'], etc.}
        include = {'applications': ["Security Alert & Incident Management"], 'reports': ['SAIM - New Incidents'], etc.}

        aq.sync(include=include, exclude=exclude)

        Args:
            components (list, optional): A list of one or more components to sync. Defaults to COMPONENTS.
            exclude (dict, optional): A dictionary of component name keys and their named values. Defaults to None.
            include (dict, optional): A dictionary of component name keys and their named values. Defaults to None.
        """
        Base.include = include
        Base.exclude = exclude
        for component in self.__sort_sync_order(components):
            if COMPONENTS.get(component):
                getattr(COMPONENTS[component](), "sync")()
                self._components_used.append(component)
                print("\n")
        if Base.dry_run:
            print("DRY RUN RESULTS:\n")
            return self._get_formatted_diff_log()
        print(b64decode(self.__LOGO).decode("ascii"))

    def gather(self) -> list:
        """Returns a list of application names on the provided source instance.

        Returns:
            list: A list of application names on the provided source instance.
        """
        atexit.unregister(self._close_and_write_zip)
        return list(self.source_instance.application_dict.keys())

    def collect(self, application_name_list: list) -> list:
        """Collects information about content based on one or more application names on the source instance.

        Args:
            application_name_list (list): A list of one or more application names to gather source content from.

        Returns:
            list: Returns a list of dictionary objects.
        """
        atexit.unregister(self._close_and_write_zip)
        return_list = []
        if not isinstance(application_name_list, list):
            application_name_list = [application_name_list]
        for application in application_name_list:
            return_list.append(Collector(application_name=application).collect())
        return return_list
