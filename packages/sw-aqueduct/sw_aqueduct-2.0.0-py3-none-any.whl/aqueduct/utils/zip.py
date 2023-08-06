# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import os
import random
import string
from io import BytesIO
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from ..base import Base
from .meta import MetaCollector


class OutputZip(Base):
    """Creates an in-memory zipfile that can be written to disk."""

    def __init__(self, zip_path: str, zip_name: str = "aqueduct.zip"):
        """Creates an in-memory zipfile that can be written to disk.

        This zipfile can be written to disk using the provided zip_path and zip_name.

        Args:
            zip_path (str): The path you want the zipfile to be saved to.
            zip_name (str, optional): The name of the zipfile to be saved to disk. Defaults to "aqueduct.zip".
        """
        self.metadata = MetaCollector()
        self.zip_path = self.get_abs_path(zip_path)
        if not os.path.exists(self.zip_path):
            os.makedirs(self.zip_path)
        self.zip_name = zip_name
        self._save_path = os.path.join(self.zip_path, self.zip_name)
        self.in_memory_zip = BytesIO()
        self._zip_file = ZipFile(self.in_memory_zip, "a", ZIP_DEFLATED, False)

    def get_abs_path(self, value: str) -> str:
        """Formats and returns the absolute path for a path value.

        Args:
            value (str): A path string in many different accepted formats.

        Returns:
            str: The absolute path of the provided string.
        """
        return os.path.abspath(os.path.expanduser(os.path.expandvars(value)))

    def add_file(self, name: str, data: Any) -> None:
        """Adds a file to the in-memory zipfile containing the provided contents.

        Args:
            name (str): The name of the file within the in-memory zipfile.
            data (Any): The data, however provided, written to the file within the zipfile.
        """
        self.log(val=f"Writing file '{name}' to zip.", level="debug")
        self._zip_file.writestr(name, data)

    def write_to_disk(self) -> None:
        """Writes the in-memory zipfile to disk."""
        self.add_file("meta.json", self.metadata.to_json())
        self.add_file("output.log", "\n".join([x for x in self.OUTPUT_LOG]))
        if self._homework:
            return_list = []
            for key, val in self._homework.items():
                for v in val:
                    return_list.append(v)
            self.add_file("homework.txt", "\n".join([x for x in return_list]))
        if Base.dry_run:
            self.add_file("dry_run.log", "\n".join([x for x in self._get_formatted_diff_log()]))
        if Base._has_error_occurred:
            self.add_file("ERROR HAS OCCURRED.txt", Base._has_error_occurred_exception)
        else:
            self.add_file("NO ERRORS OCCURRED.txt", "")
        self.log(val="Closing in memory zip file", level="debug")
        self._zip_file.close()
        if os.path.exists(self._save_path):
            random_string = "".join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6)
            )
            self.zip_name = self.zip_name.replace(".zip", f"_{random_string}.zip")
            self._save_path = os.path.join(self.zip_path, self.zip_name)
        self.log(val=f"Writing  zip '{self.zip_name}' to disk.")
        with open(self._save_path, "wb") as f:
            f.write(self.in_memory_zip.getbuffer())
        return self._save_path
