"""
Module can be used to mark deprecated classes / parameters / parameter types.
"""
from typing import overload, get_origin
from itertools import chain

from .utilities import issubclass_noexcept
from .annotations import convert_types
from .doc import doc_category


__all__ = (
    "register_deprecated",
    "is_deprecated",
)


@overload
@doc_category("Deprecations", manual=True)
def register_deprecated(cls: type):
    """
    Mark ``cls`` deprecated globally. This function cannot be
    used on built-in Python classes.
    """

@overload
@doc_category("Deprecations", manual=True)
def register_deprecated(cls: type, parameter: str):
    """
    Marks a ``parameter`` to be deprecated under specific ``cls``.
    """

@overload
@doc_category("Deprecations", manual=True)
def register_deprecated(cls: type, parameter: str, *types: type):
    """
    Marks multiple ``types`` to be deprecated for a certain ``parameter`` under ``cls``.
    """

def register_deprecated(cls, parameter: str = None, *types: type):
    if parameter is None:
        cls.__deprecated__ = True

    elif not types:
        cls.__wiz_deprecated_params__ = getattr(cls, "__wiz_deprecated_params__", set())
        cls.__wiz_deprecated_params__.add(parameter)
    else:
        types = tuple(chain.from_iterable(map(convert_types, types)))
        cls.__wiz_deprecated_param_types__ = getattr(cls, "__wiz_deprecated_param_types__", dict())
        cls.__wiz_deprecated_param_types__[parameter] = cls.__wiz_deprecated_param_types__.get(parameter, set())
        cls.__wiz_deprecated_param_types__[parameter].update(types)

@overload
@doc_category("Deprecations", manual=True)
def is_deprecated(cls: type):
    """
    Checks if ``cls`` is deprecated globally.
    """

@overload
@doc_category("Deprecations", manual=True)
def is_deprecated(cls: type, parameter: str):
    """
    Checks if ``parameter`` is deprecated under ``cls``.
    """

@overload
@doc_category("Deprecations", manual=True)
def is_deprecated(cls: type, parameter: str, type_: type):
    """
    Checks if ``type_`` is deprecated for a certain ``parameter`` under ``cls``.
    """

def is_deprecated(cls: type, parameter: str = None, type_: type = None):
    if parameter is None:
        return hasattr(cls, "__deprecated__")

    if type_ is None:
        params = getattr(cls, "__wiz_deprecated_params__", set())
        return parameter in params

    depr_types = getattr(cls, "__wiz_deprecated_param_types__", dict()).get(parameter, set())
    if is_deprecated(type_) or type_ in depr_types:
        return True
    
    origin = get_origin(type_)
    if origin is not None and origin in depr_types:
        return True

    type_ = origin or type_
    for depr_type in depr_types:
        if issubclass_noexcept(type_, depr_type):
            return True

    return False
