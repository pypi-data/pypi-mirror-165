"""Module to create and use templated search presets for the discovery search

Use templated search from the "Equity" template that was defined in the config:
>>> import refinitiv.data as rd
>>> rd.content.search._templates["Equity"].search()
"""
__all__ = ["templates"]

import operator
import string
import itertools
from functools import reduce
from typing import Iterable, Optional, Dict, Set, List, Any

from humps import depascalize

from refinitiv.data import get_config
from refinitiv.data._tools import inspect_parameters_without_self
from refinitiv.data.errors import ConfigurationError
from refinitiv.data.content.search._definition import Definition
from refinitiv.data.content.search._views import Views

CONFIG_PREFIX = "search.templates"


def join_sets(sets: Iterable[set]) -> set:
    """Join multiple sets into one"""
    iterator = iter(sets)
    try:
        # Can't pass an empty iterator to `reduce`, that's the way to handle it
        default = next(iterator)
    except StopIteration:
        return set()
    else:
        return reduce(operator.or_, iterator, default)


def get_placeholders_names(template_string: str) -> Set[str]:
    """Get list of placeholder names in format-style string

    >>> get_placeholders_names("{a}, {b}, {a}")
    {'b', 'a'}
    """
    return set(x[1] for x in string.Formatter().parse(template_string) if x[1])


def generate_docstring(description: str, methods: Dict[str, dict]):
    doc = [
        description,
        "",
        "    Methods",
        "    -------",
    ]

    for method_name, method_desc in methods.items():
        doc.append(f"    {method_name}")

        for param, desc in method_desc["args"].items():
            doc.append(f"        {param}")
            if "description" in desc:
                doc.append(f"            {desc['description']}")
            if "default" in desc:
                doc.append(f"            default: {repr(desc['default'])}")
            doc.append("")

    return "\n".join(doc)


class SearchTemplate:
    """Discovery search preset

    Initialized with default values for content.search.Definition.
    Any string value acts as template string. You can use placeholder variables
    like for `str.format` method, and that variables will be required to prepare
    search parameters through `._search_kwargs()` or to launch search through `.search()`.

    Attributes
    ----------

    name: str
        name of the template

    Examples
    --------

    >>> SearchTemplate(filter="ExchangeName xeq '{name}'")._search_kwargs(name="<name>")
    {'filter': "ExchangeName xeq '<name>'"}
    >>> SearchTemplate(filter="ExchangeName xeq '{name}'")._search_kwargs()
    Traceback (most recent call last):
        ...
    KeyError: 'Those keyword arguments must be defined, but they are not: name'
    >>> SearchTemplate(filter="ExchangeName xeq '{name}'", placeholders_defaults={"name": "<name>"})._search_kwargs()
    {'filter': "ExchangeName xeq '<name>'"}
    """

    def __init__(
        self,
        name=None,
        placeholders_defaults: Optional[Dict[str, Any]] = None,
        pass_through_defaults: Optional[Dict[str, Any]] = None,
        **search_defaults,
    ):
        """
        Parameters
        ----------
        name : str, optional
            name of the template
        placeholders_defaults: dict, optional
            <placeholder_name> : <placeholder_default_value>
        search_defaults
            default values for discovery search Definition
        """
        self._available_search_kwargs = inspect_parameters_without_self(Definition)
        """ List search keyword arguments we can use in this template """
        self._placeholders_defaults = (
            {} if placeholders_defaults is None else placeholders_defaults
        )
        """ Default template variables values for a templated defaults """
        if pass_through_defaults is None:
            pass_through_defaults = {}

        bad_pass_through_params = (
            set(pass_through_defaults) - self._available_search_kwargs
        )
        if bad_pass_through_params:
            raise ValueError(
                "All the parameters described in 'parameters' section of search "
                "template configuration, must be either placeholders variables or "
                "parameters of the discovery search Definition. Those parameters are "
                "neither of them: " + ", ".join(bad_pass_through_params)
            )

        self.name = name

        unknown_defaults = set(search_defaults) - set(self._available_search_kwargs)
        if unknown_defaults:
            raise ValueError(
                "This arguments are defined in template, but not in search Definition: "
                + ", ".join(unknown_defaults)
            )

        self._placeholders_names: Set[str] = set()
        self._templated_defaults: Dict[str, str] = {}
        self._pass_through_defaults: Dict[str, Any] = {}

        for name, value in search_defaults.items():

            if not isinstance(value, str):
                self._pass_through_defaults[name] = value
                continue

            placeholders = get_placeholders_names(value)
            if placeholders:
                self._templated_defaults[name] = value
                self._placeholders_names |= placeholders
            else:
                self._pass_through_defaults[name] = value

        self._pass_through_defaults.update(pass_through_defaults)

        bad_tpl_var_names = self._placeholders_names & self._available_search_kwargs
        if bad_tpl_var_names:
            raise ValueError(
                "You can't use template arguments with the same name"
                " as search arguments. You are used: " + ", ".join(bad_tpl_var_names)
            )

    def _defaults(self):
        return itertools.chain(self._templated_defaults, self._pass_through_defaults)

    def __repr__(self):
        return f"<SearchTemplate '{self.name}'>"

    def _search_kwargs(self, **kwargs) -> dict:
        """Get dictionary of arguments for content.search.Definition"""

        undefined_placeholders = (
            self._placeholders_names - set(kwargs) - set(self._placeholders_defaults)
        )

        if undefined_placeholders:
            raise KeyError(
                "Those keyword arguments must be defined, but they are not: "
                + ", ".join(undefined_placeholders)
            )

        unexpected_arguments = (
            set(kwargs)
            - self._placeholders_names
            # templated defaults can't be redefined
            - (self._available_search_kwargs - self._templated_defaults.keys())
        )

        if unexpected_arguments:
            raise KeyError(f"Unexpected arguments: {', '.join(unexpected_arguments)}")

        kwargs = kwargs.copy()
        # Applying template variables defaults
        for name, value in self._placeholders_defaults.items():
            if name not in kwargs:
                kwargs[name] = value

        result = self._pass_through_defaults.copy()

        # Apply variables to templated defaults
        for name, value in self._templated_defaults.items():
            result[name] = value.format(**kwargs)

        # Apply other variables from kwargs
        for name, value in kwargs.items():
            if name not in self._placeholders_names:
                result[name] = value

        return result

    def search(self, **kwargs):
        """Please, use help() on a template object itself to get method documentation"""
        # ^ we need this docstring because we can't easily generate docstring for
        # the method, but can change __doc__ for class instance
        return Definition(**self._search_kwargs(**kwargs)).get_data().data.df


class Templates:
    """Easy access to search templates from the library config

    Check if search template with the name "Equity" is defined in the config:
    >>> templates = Templates()
    >>> "Equity" in templates
    True
    Get "Equity" search template:
    >>> templates["Equity"]
    Get list of available search template names:
    >>> templates.keys()
    ["Equity"]
    """

    def __iter__(self):
        config = get_config()
        return config.get(CONFIG_PREFIX, {}).keys().__iter__()

    def __getitem__(self, name: str) -> SearchTemplate:
        config = get_config()
        key = f"{CONFIG_PREFIX}.{name}"
        if key not in config:
            raise KeyError(f"Template '{name}' is not found in the config")
        data = config[key].as_attrdict() if config[key] is not None else {}

        # <param_name>: {"default": <default>, "description": <doc>}
        tpl_strs_defaults = {
            name: attrs["default"]
            for name, attrs in data.get("parameters", {}).items()
            if "default" in attrs
        }
        params = depascalize(data.get("request_body", {}))

        if "view" in params:
            # Convert string value to enum for the view argument
            view = params["view"]
            try:
                params["view"] = getattr(Views, depascalize(view).upper())
            except AttributeError:
                raise ConfigurationError(
                    -1,
                    f"Wrong search template value: View={view}. "
                    "It must be one of the following: "
                    f"{', '.join(Views.possible_values())}",
                )
        tpl = SearchTemplate(name, placeholders_defaults=tpl_strs_defaults, **params)

        method_args = {}
        # Some placeholders may be only in string, but not in "parameters"
        for param in sorted(tpl._placeholders_names):
            method_args[param] = data.get("parameters", {}).get(param, {})

        # That's why we can get them all in one cycle with pass-through parameters
        # that is located in "parameters" config session, but not in template string
        for param, desc in data.get("parameters", {}).items():
            if param not in tpl._placeholders_names:
                method_args[param] = desc

        tpl.__doc__ = generate_docstring(
            description=data.get("description", ""),
            methods={"search": {"description": "", "args": method_args}},
        )

        return tpl

    def keys(self) -> List[str]:
        """Get list of available search template names"""
        return list(self)


templates = Templates()
