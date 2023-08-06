# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)


class MissingDependencyError(Exception):
    """Raised when a dependency is not found."""

    def __init__(self, message) -> None:
        super(MissingDependencyError, self).__init__(message)


class UnsupportedSwimlaneVersion(NotImplementedError):
    """Raised when a source and destination Swimlane instance do not match."""

    def __init__(self, source, destination) -> None:
        from ..base import Base

        message = f"The source instance ({source.swimlane.host}) version {source.swimlane.product_version} and "
        message += f"destination instance ({destination.swimlane.host}) version {destination.swimlane.product_version} "
        message += "must be the same version to continue."
        Base().log(val=message, level="critical")
        super(UnsupportedSwimlaneVersion, self).__init__(message)


class ModelError(TypeError):
    """Raised when a provided dictionary does not conform to the defined data model for that object."""

    def __init__(self, err: TypeError, name: str):
        from ..base import Base

        message = f"The provided dictionary object to the '{name}' data model is {str(err).split('()')[-1]}"
        message += "\nPlease report this issue here https://github.com/swimlane/aqueduct/issues"
        Base().log(val=message, level="critical")
        super(ModelError, self).__init__(message)


class ComponentError(Exception):
    """Raised when an error has occurred within a component class of aqueduct."""


class AddComponentError(ComponentError):
    """Raised when an error occurs attempting to add a component."""

    def __init__(self, model: dict, name: str = None, reason: str = None):
        from ..base import Base

        model_name = model.get("name") if isinstance(model, dict) else model.name
        message = f"Unable to add {name if name else model.__class__.__name__} '{model_name}' to destination instance!!"
        if reason:
            message += f"\t\t<--- {reason}"
        Base().log(val=message, level="critical")
        super(AddComponentError, self).__init__(message)


class UpdateComponentError(ComponentError):
    """Raised when an error occurs attempting to update an existing component."""

    def __init__(self, model: dict, name: str = None):
        from ..base import Base

        model_name = model.get("name") if isinstance(model, dict) else model.name
        name = name if name else model.__class__.__name__
        message = f"Unable to update {name} '{model_name}' on destination instance!!"
        Base().log(val=message, level="critical")
        super(UpdateComponentError, self).__init__(message)


class GetComponentError(ComponentError):
    """Raised when an error occurs attempting to get a component."""

    def __init__(self, type: str, name: str = None, id: str = None):
        from ..base import Base

        message = f"Unable to find {type} {name if name else ''} '({id})' on source Swimlane instance!!"
        Base().log(val=message, level="critical")
        super(GetComponentError, self).__init__(message)


class AccessKeyError(KeyError):
    """Raised when an error occurs attempting to access keys in a dictionary that do not exist."""

    def __init__(self, object_name, component_type, error=None):
        """Logs a formatted message when KeyError occurs.

        Args:
            object_name (str): The name of the component value.
            component_type (str): The type of component.
            error (Exception, optional): The error that occurred. Defaults to None.
        """
        from ..base import Base

        if error and error.args:
            args = ",".join([x for x in error.args])
        else:
            args = ""
        message = f"Unable to find key '{args}' in {component_type} '{object_name}'."
        Base().log(val=message, level="critical")
        super(AccessKeyError, self).__init__(message)
