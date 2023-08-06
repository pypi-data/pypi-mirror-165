# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from .base import Base
from .components.tasks import Tasks


class Collector(Base):
    """Collects information about a given application name from the provided instance. Defaults to source instance."""

    def __init__(self, application_name: str, instance=None) -> None:
        """Given the provided application name and optional instance, we will collect data about that application.

        Args:
            application_name (str): The name of an application.
            instance (SwimlaneInstance, optional): A SwimlaneInstance object. Defaults to source SwimlaneInstance.

        Raises:
            Exception: Raises when unable to find the provided application name on the instance.
        """
        if not instance:
            self.instance = self.source_instance
        else:
            self.instance = instance
        self.application_name = application_name
        self.application_id = self._get_application_id(self.application_name)
        if not self.application_id:
            raise Exception("Unable to find the provided application.")

    def _verify_application_exists(self, application_name: str) -> bool:
        """Verifies the application name provided exists on the provided instance.

        Args:
            application_name (str): The name of a Swimlane application.

        Returns:
            bool: Returns True if the application is found and exists. False if not.
        """
        if self.instance.application_dict.get(application_name):
            return True
        return False

    def _get_application_id(self, application_name: str) -> str:
        """Retrieves the application ID from the given application name.

        Args:
            application_name (str): The name of a Swimlane application.

        Returns:
            str: The application ID.
        """
        if self._verify_application_exists(application_name=application_name):
            return self.instance.application_dict[application_name]["id"]

    def _collect_reports(self, report_id: str) -> dict:
        """Collects information about a given report based on the provided ID.

        Args:
            report_id (str): A report ID.

        Returns:
            dict: A dictionary containing the name and ID of the report.
        """
        report = self.instance.get_report(report_id)
        if report:
            return {"name": report["name"], "id": report_id}

    def _collect_dashboards(self, dashboard_id: str) -> dict:
        """Collects information about a given dashboard based on the provided ID.

        Args:
            dashboard_id (str): A dashboard ID.

        Returns:
            dict: A dictionary containing the name, id, and list of reports within the dashboard.
        """
        report_card_list = []
        dashboard = self.instance.get_dashboard(dashboard_id)
        if dashboard:
            if dashboard.get("items"):
                for card in dashboard["items"]:
                    if card.get("reportId"):
                        report = self._collect_reports(card["reportId"])
                        if report:
                            report_card_list.append(report)
                    else:
                        report_card_list.append({"name": card.get("name")})
            return {"name": dashboard["name"], "id": dashboard_id, "reports": report_card_list}

    def _collect_workspaces(self, application_id) -> list:
        """Collects workspaces associated with a given application based on the provided ID.

        Args:
            application_id (_type_): A swimlane application ID.

        Returns:
            list: A list of workspaces containing the name, id, and list of dashboards within that workspace.
        """
        return_list = []
        dashboard_list = []
        workspaces = self.instance.get_application_workspaces(application_id)
        if workspaces:
            for workspace in workspaces:
                if workspace.get("dashboards"):
                    for dashboard in workspace["dashboards"]:
                        dashboard_list.append(self._collect_dashboards(dashboard_id=dashboard))
                return_list.append({"name": workspace["name"], "id": workspace["id"], "dashboards": dashboard_list})
        return return_list

    def _collect_assets(self, task: dict) -> list:
        """Collects assets based on the provided task.

        Args:
            task (dict): A Swimlane task dictionary object.

        Returns:
            list: A list of assets, if exists, containing a name and ID.
        """
        asset_list = []
        asset_id = None
        if task["action"].get("assetId"):
            asset_id = task["action"]["assetId"]
            if asset_id:
                asset_name = self.instance.get_asset(asset_id)["name"]
                asset_list.append(
                    {
                        "name": asset_name,
                        "id": asset_id,
                    }
                )
        return asset_list

    def _collect_plugins(self, task: dict) -> list:
        """Collects plugins based on the provided task.

        Args:
            task (dict): A Swimlane task dictionary object.

        Returns:
            list: A list of plugins containing a name, type, and version of the plugin.
        """
        plugin_name = Tasks()._get_plugin_name(task=task)
        action_type = Tasks()._get_action_type(task=task)
        plugin_list = []
        if plugin_name and action_type:
            plugin_version = None
            try:
                plugin_version = task["action"]["descriptor"]["packageDescriptor"]["version"]
            except Exception as e:
                raise e
            plugin_list.append({"name": plugin_name, "type": action_type, "version": plugin_version})
        return plugin_list

    def _collect_tasks(self, application_id: str) -> list:
        """Collects tasks associated with the provided application ID.

        Args:
            application_id (str): A Swimlane application ID.

        Returns:
            list: A list of tasks containing name, id, type, plugins, and assets if applicable.
        """
        return_list = []
        tasks_component = Tasks()
        tasks = self.instance.get_tasks_by_application(application_id)
        if tasks and tasks.get("tasks"):
            for task in tasks["tasks"]:
                src_task = self.instance.get_task(task["id"])
                if src_task:
                    if (
                        src_task["action"].get("type")
                        and src_task["action"]["type"] in tasks_component.BUILTIN_TASK_ACTION_TYPES
                    ):
                        # custom or built-in task type
                        return_list.append(
                            {
                                "name": src_task["name"],
                                "id": src_task["id"],
                                "type": src_task["action"]["type"],
                                "plugins": [],
                            }
                        )
                    else:
                        # This is a packaged task - meaning it came from an installed plugin
                        return_list.append(
                            {
                                "name": src_task["name"],
                                "id": src_task["id"],
                                "type": src_task["action"]["type"],
                                "assets": self._collect_assets(task=src_task),
                                "plugins": self._collect_plugins(task=src_task),
                            }
                        )
        return return_list

    def _collect_role(self, role_id: str) -> dict:
        """Collects roles, including associated groups and users from a role ID.

        Args:
            role_id (str): A Swimlane role ID.

        Returns:
            dict: Returns a dictionary containing a role name, list of groups, and list of users if applicable.
        """
        role = self.instance.get_role(role_id)
        if role:
            return {
                "name": role["name"],
                "groups": [group["name"] for group in role["groups"] if role.get("groups")],
                "users": [user["name"] for user in role["users"] if role.get("users")],
            }

    def _collect_permissions(self, application_id: str) -> list:
        """Collects permissions associated with a given application ID.

        Args:
            application_id (str): A Swimlane application ID.

        Returns:
            list: Returns a list of dictionaries containing any permissions found on the application.
        """
        return_list = []
        application = self.instance.get_application(application_id)
        if application.get("permissions"):
            for key, val in application["permissions"].items():
                if val and isinstance(val, dict):
                    if val.get("id") and val.get("type") and val["type"] == "Role":
                        return_list.append(self._collect_role(val["id"]))
        return return_list

    def prettify_collection_results(self, results: dict) -> str:
        """Prints and returns a prettified string format of collection results.

        Args:
            results (dict): The returned results from the collection method in this class.

        Returns:
            str: A prettified string format string.
        """
        prettify_output_string = ""
        for key, val in results.items():
            string_value = f"{key} (application)"
            print(string_value)
            prettify_output_string += string_value
            if results[key].get("workspaces"):
                for workspace in results[key]["workspaces"]:
                    string_value = f"\t{workspace['name']} (workspace)"
                    print(string_value)
                    prettify_output_string += string_value
                    if workspace.get("dashboards"):
                        for dashboard in workspace["dashboards"]:
                            string_value = f"\t\t{dashboard['name']} (dashboard)"
                            print(string_value)
                            prettify_output_string += string_value
                            if dashboard.get("reports"):
                                for report in dashboard["reports"]:
                                    string_value = f"\t\t\t{report['name']} (report)"
                                    print(string_value)
                                    prettify_output_string += string_value
            if results[key].get("tasks"):
                for task in results[key]["tasks"]:
                    string_value = f"\t{task['name']} (task)"
                    print(string_value)
                    prettify_output_string += string_value
                    if task.get("plugins"):
                        for plugin in task["plugins"]:
                            string_value = f"\t\t{plugin['name']} - {plugin['version']} (plugin)"
                            print(string_value)
                            prettify_output_string += string_value
                    if task.get("assets"):
                        for asset in task["assets"]:
                            string_value = f"\t\t\t{asset['name']} (asset)"
                            print(string_value)
                            prettify_output_string += string_value
            if results[key].get("permissions"):
                for permission in results[key]["permissions"]:
                    string_value = f"\t{permission['name']} (role)"
                    print(string_value)
                    prettify_output_string += string_value
                    if permission.get("groups"):
                        groups = "\n".join([x for x in permission["groups"]])
                        string_value = f"\t{groups} (group)"
                        print(string_value)
                        prettify_output_string += string_value
        return prettify_output_string

    def collect(self) -> dict:
        """Collects information about a given application based on its name.

        Returns:
            dict: Returns a dictionary containing an applications workspaces, tasks, permissions, and ID.
        """
        return {
            self.application_name: {
                "workspaces": self._collect_workspaces(application_id=self.application_id),
                "tasks": self._collect_tasks(application_id=self.application_id),
                "id": self.application_id,
                "permissions": self._collect_permissions(application_id=self.application_id),
            }
        }
