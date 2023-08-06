# -*- coding: utf-8 -*-
import json
import random
import warnings
from functools import wraps

from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout
from swimlane.exceptions import SwimlaneHTTP400Error

# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from .base import Base


def save_content_to_zip(response, function_name, args):
    """This method is used by the dump_content decorator.

    Used to save Swimlane content to a in-memory zip file.

    The combination of the function_name and other arguments make up the folder structure within the ZIP file.

    The function_name is split before provided to this method (e.g. get_applications = applications folder in the zip)

    Args:
        response (Any): The HTTP Response from an instance class method.
        function_name (str): The name of the instance class method.
        args (_type_): Arguments provided to the instance class method.
    """
    if response is not None:
        # if the response is a bool then we return.
        # bool occurs when the response is basically not found on the instance
        if isinstance(response, bool):
            return response
        temp_response = response
        if not isinstance(temp_response, list):
            temp_response = [temp_response]
        # for each of the items in our response, we will add it to our in-memory zip file
        for item in temp_response:
            # not all items in a response (e.g. workflows) do not contain a name property so we have options to handle
            # those edge cases here.
            name = None
            if item.get("name"):
                name = item["name"]
            elif item.get("id"):
                name = item["id"]
            else:
                name = f"{function_name}_{random.randint(0,100)}"
            type_and_file_name = f"{function_name}/{name}"
            # args is a tuple of 2 items or more.
            # the first argument of args is the calling class.
            # this means that the calling class will be a SwimlaneInstance class
            # we check to see which instance type it is by checking the instance_type property.
            # this determines which folder our content is saved in
            if args[0].instance_type == "source":
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        Base.ZIP_FILE.add_file(name=f"content/source/{type_and_file_name}.json", data=json.dumps(item))
                except UserWarning as ue:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        Base.ZIP_FILE.add_file(
                            name=f"content/source/{type_and_file_name}_{item.get('id')}.json", data=json.dumps(item)
                        )
            elif args[0].instance_type == "destination":
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        Base.ZIP_FILE.add_file(
                            name=f"content/destination/{type_and_file_name}.json", data=json.dumps(item)
                        )
                except UserWarning as ue:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        Base.ZIP_FILE.add_file(
                            name=f"content/destination/{type_and_file_name}_{item.get('id')}.json",
                            data=json.dumps(item),
                        )
    # the second argument of args, if it exists, is going to be a dict of an altered component object.
    # For example, the source (above) would be the source object returned from get_applications.
    # the destination (above) would be the response from updating or adding said application on the destination
    # the final altered content is the modified object from teh applications component and about to be added/updated
    # on the destination.
    if args and len(args) == 2:
        if args[1] and isinstance(args[1], dict) or args[1] and isinstance(args[1], list):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                Base.ZIP_FILE.add_file(name=f"content/altered/{function_name}.json", data=json.dumps(args[1]))


def dump_content(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except Exception as e:
            Base._has_error_occurred = True
            Base._has_error_occurred_exception = str(e)
            save_content_to_zip(response=None, function_name=func.__name__.split("_")[-1], args=args)
            return None
        else:
            if Base._dump_content:
                save_content_to_zip(response=response, function_name=func.__name__.split("_")[-1], args=args)
            return response

    return wrapper


def log_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SwimlaneHTTP400Error as sw:
            Base().log(sw.args)
            if not Base.continue_on_error:
                raise sw
        except HTTPError as he:
            log = f"Unable to process '{func.__name__}' request"
            if kwargs:
                log += f" with the requested parameters '{', '.join([x for x in kwargs.keys()])}' {kwargs}."
            Base().log(log)
            if not Base.continue_on_error:
                raise he
        except ConnectionError as errc:
            Base().log(f"An Error Connecting to the API occurred: {repr(errc)}")
            if not Base.continue_on_error:
                raise errc
        except Timeout as errt:
            Base().log(f"A timeout error occurred: {repr(errt)}")
            if not Base.continue_on_error:
                raise errt
        except RequestException as err:
            Base().log(f"An Unknown Error occurred: {repr(err)}")
            if not Base.continue_on_error:
                raise err
        except Exception as e:
            Base().log(f"There was an unknown exception that occurred in '{func.__name__}': {e}")
            if not Base.continue_on_error:
                raise e

    return wrapper
