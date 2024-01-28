"""
Module used for managing annotations.
"""
from typing import Union, Optional, Generic, Iterable, get_args, get_origin, get_type_hints
from datetime import datetime, timedelta, timezone
from inspect import isclass, isabstract
from itertools import product, chain
from contextlib import suppress

from .utilities import issubclass_noexcept
from .doc import doc_category


__all__ = (
    "register_annotations",
    "get_annotations",
    "convert_types",
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


def convert_types(input_type: type):
    """
    Type preprocessing method, that extends the list of types with inherited members (polymorphism)
    and removes classes that are wrapped by some other class, if the wrapper class also appears in
    the annotations.
    """
    def remove_classes(types: list):
        r = types.copy()
        for type_ in types:
            # It's a wrapper of some class -> remove the wrapped class
            if hasattr(type_, "__wrapped__"):
                if type_.__wrapped__ in r:
                    r.remove(type_.__wrapped__)

            # Abstract classes are classes that don't allow instantiation -> remove the class
            if isabstract(type_):
                r.remove(type_)

        return tuple({a:0 for a in r})


    if isinstance(input_type, str):
        raise TypeError(
            f"Provided type '{input_type}' is not a type - it is a string!\n"
            "Potential subscripted type problem?\n"
            "Instead of e. g., list['type'], try using typing.List['type']."
        )

    origin = get_origin(input_type)
    if issubclass_noexcept(origin, Generic):
        # Patch for Python versions < 3.10
        input_type.__name__ = origin.__name__

    # Unpack Union items into a tuple
    if origin is Union or issubclass_noexcept(origin, (Iterable, Generic)):
        new_types = []
        for arg_group in get_args(input_type):
            new_types.append(remove_classes(list(convert_types(arg_group))))

        if origin is Union:
            return tuple(chain.from_iterable(new_types))  # Just expand unions

        # Process abstract classes and polymorphism
        new_origins = []
        for origin in convert_types(origin):
            if issubclass_noexcept(origin, Generic):
                for comb in product(*new_types):
                    new_origins.append(origin[comb])
            elif issubclass_noexcept(origin, Iterable):
                new = origin[tuple(chain.from_iterable(new_types))] if len(new_types) else origin
                new_origins.append(new)
            else:
                new_origins.append(origin)

        return remove_classes(new_origins)

    if input_type.__module__ == "builtins":
        # Don't consider built-int types for polymorphism
        # No removal of abstract classes is needed either as builtins types aren't abstract
        return (input_type,)

    # Extend subclasses
    subtypes = []
    if hasattr(input_type, "__subclasses__"):
        for st in input_type.__subclasses__():
            subtypes.extend(convert_types(st))

    # Remove wrapped classes (eg. wrapped by decorator) + ABC classes
    return remove_classes([input_type, *subtypes])
