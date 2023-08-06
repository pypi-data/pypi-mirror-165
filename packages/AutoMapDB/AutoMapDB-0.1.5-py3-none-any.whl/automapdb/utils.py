#!/usr/bin/python3
# -*- coding: utf-8 -*-
import functools
import json
import logging
import os
import sys
from pprint import pformat
from typing import Any, Callable
from xml.dom import minidom

import yaml

log = logging.getLogger(__name__)


def set_logger(lvl, log_file="/tmp/automapdb.log"):
    sys.tracebacklimit = None if lvl == "DEBUG" else 0
    numlvl = 10 if lvl == "DEBUG" else 40
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file and os.path.isdir(log_file):
        handlers += [logging.FileHandler(log_file)]
    logging.basicConfig(
        handlers=handlers,
        level=numlvl,
        format="%(asctime)s | %(levelname)s | %(funcName)s: | %(message)s",
        datefmt="%H:%M:%S",
    )
    log.debug(f"Log level: {lvl}")
    log.debug(f"Traceback: {sys.tracebacklimit}")
    return log


def joinsep(lst, sep=", ", caps="__repr__"):
    return sep.join([getattr(x, caps)() for x in lst])


def filter_dict(data: dict, excl: list = None, incl: list = None) -> dict:
    """Filter given keys+values from dict either in- or exclusive.
    Args:
        data (dict): Dictionary to filter
        excl (list): If set, the keys in the list are excluded
        incl (list): If set, only the keys in the list are included
    """
    data = data if isinstance(data, dict) else data.__dict__
    new_data = {}
    for k, v in data.items():
        if excl and k in excl or k.startswith("_"):
            continue
        if incl and k not in incl:
            continue
        new_data[k] = v
    return new_data


class Singleton(type):
    # Registry for Singleton classes
    _instance_registry = {}

    def __call__(cls, *args, **kwargs):
        # If class is not in registry
        if cls not in cls._instance_registry:
            # Execute call to the actual class and its meta class (this)
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            # Register instance as only object on the dict of classes
            cls._instance_registry[cls] = instance
        # Return instance of given class
        return cls._instance_registry[cls]


def fmt_data(data, fmt):
    """Formats data input to given output format
    Options:
    * str: Simply dump the data to its str() representation
    * yaml: Dump data to yaml. Be careful, yaml will serialize the whole data tree, often resulting in a mess
    * json: Dump data to json. Data may be truncated as json only dumps basic data structures (dict, list)
    * pretty: Return pformat(data). Trys to pretty-print python objects
    """
    try:
        if fmt == "pretty":
            data = pformat(data)
        if fmt == "str":
            data = str(data)
        if fmt in ["yaml", "yml"]:
            data = yaml.dump(data, sort_keys=False)
        if fmt == "jsonl":
            try:
                data = [json.dumps(i, default=lambda o: str(o)) for i in data]
            except TypeError as err:
                log.warning(f"Data not iterable: {data} ({err})")
                data = json.dumps(data, default=lambda o: str(o))
        if fmt == "json":
            data = json.dumps(data, default=lambda o: str(o))
        # If data is an XML Document or Element Object
        if isinstance(data, (minidom.Element, minidom.Document)):
            # Return prettified XML representation
            data = data.toprettyxml(indent="  ").replace("\n\n", "")
        if isinstance(data, (dict,)):
            data = str(data)
    except Exception as e:  # If something goes wrong:
        log.debug(f"{fmt}: {data}")  # Log format, data and error
        log.error(repr(e))
        data = str(data)
    return data  # Return data, formatted or not


def format_return(default_format: str = None) -> Callable:
    def format_return_decorator(func: Callable) -> Callable:
        """
        Format output of the decorated method
        This decorator looks for the keyword "fmt" in the decorated method and returns the formatted output.
        """

        @functools.wraps(
            func, updated=()
        )  # Preserves function attributes, e.g. __doc__
        def format_return_wrapper(self="None", *args, **kwargs) -> Any:
            fmt = kwargs.get("fmt", default_format)  # Find "fmt" in kwargs
            data = func(self, *args, **kwargs)  # Store method output in data
            cls = self.__class__.__name__ if isinstance(self, object) else __name__
            log.debug(f"{func.__name__}, {cls}, {args}, {kwargs}")
            return fmt_data(data, fmt) if fmt else data

        # Preserve function docstring
        format_return_wrapper.__doc__ = func.__doc__
        return format_return_wrapper

    return format_return_decorator


class SQLException(Exception):
    pass
