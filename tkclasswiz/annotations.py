"""
Module used for managing annotations.
"""
from typing import Union, Optional, get_args, Generic, get_origin, get_type_hints
from datetime import datetime, timedelta, timezone
from contextlib import suppress
from inspect import isclass
from .doc import doc_category
from .utilities import issubclass_noexcept


__all__ = (
    "register_annotations",
    "get_annotations",
)


ADDITIONAL_ANNOTATIONS = {
    timedelta: {
        "days": float,
        "seconds": float,
        "microseconds": float,
        "milliseconds": float,
        "minutes": float,
        "hours": float,
        "weeks": float
    },
    datetime: {
        "year": int,
        "month": Union[int, None],
        "day": Union[int, None],
        "hour": int,
        "minute": int,
        "second": int,
        "microsecond": int,
        "tzinfo": timezone
    },
    timezone: {
        "offset": timedelta,
        "name": str
    },
}


@doc_category("Annotations")
def register_annotations(cls: type, mapping: Optional[dict] = {}, **annotations):
    """
    Extends original annotations of ``cls``.

    This can be useful eg. when the class your
    are adding is not part of your code and is also not annotated.

    Classes that already have additional annotations:

    - datetime.timedelta
    - datetime.datetime 
    - datetime.timezone

    Parameters
    ------------
    cls: type
        The class (or function) to register additional annotations on.
    mapping: Optional[Dict[str, type]]
        Mapping mapping the parameter name to it's type.
    annotations: Optional[Unpack[str, type]]
        Keyword arguments mapping parameter name to it's type (``name=type``).

    Example
    -----------
    
    .. code-block:: python

        from datetime import timedelta, timezone

        register_annotations(
            timezone,
            offset=timedelta,
            name=str
        )    
    """
    if cls not in ADDITIONAL_ANNOTATIONS:
        ADDITIONAL_ANNOTATIONS[cls] = {}

    ADDITIONAL_ANNOTATIONS[cls].update(**annotations, **mapping)


@doc_category("Annotations")
def get_annotations(class_) -> dict:
    """
    Returns class / function annotations including the ones extended with ``register_annotations``.
    It does not return the return annotation.

    Additionally, this function resolves any generic types to their parameterized types, but
    only for classes, functions don't support this yet as support for generics on functions was added
    in Python 3.12.
    """
    annotations = {}
    with suppress(AttributeError, TypeError):
        if isclass(class_):
            annotations = get_type_hints(class_.__init__)
        elif isclass(origin_class := get_origin(class_)) and issubclass_noexcept(origin_class, Generic):
            # Resolve generics
            annotations = get_type_hints(origin_class.__init__)
            generic_types = get_args(origin_class.__orig_bases__[0])
            generic_values = get_args(class_)
            generic_name_value = {generic_types[i]: generic_values[i] for i in range(len(generic_types))}
            for k, v in annotations.items():
                annotations[k] = generic_name_value.get(v, v)
        else:
            annotations = get_type_hints(class_)

    additional_annotations = ADDITIONAL_ANNOTATIONS.get(class_, {})
    annotations = {**annotations, **additional_annotations}

    if "return" in annotations:
        del annotations["return"]

    return annotations
