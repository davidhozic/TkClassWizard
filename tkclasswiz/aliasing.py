"""
Module contains functionality for managing type aliases.
Type alias is an alternative type name.

E. g., we could have an alias for timedelta -> Duration.
"""
from typing import Dict, Optional
from .doc import doc_category


__all__ = (
    "register_alias",
    "get_aliased_name",
)


ALIASES: Dict[type, str] = {}


@doc_category("Aliasing")
def register_alias(cls: type, alias: str):
    """
    Creates an alias name for type ``cls``.
    Aliases will then be displayed in place of original name in:

    - Object definition "New" menu
    - Container values (e. g., inside Combobox)

    Parameters
    ------------
    cls: type
        The class (or function or type) to register an alias for.
    alias: str
        The alias.

    Example
    -----------
    
    .. code-block:: python

        from datetime import timedelta

        register_alias(timedelta, "Duration")
    """
    ALIASES[cls] = alias


@doc_category("Aliasing")
def get_aliased_name(class_) -> Optional[str]:
    """
    Returns the ``class_``'s aliased name. If class has no alias name,
    ``None`` is returned.
    """
    return ALIASES.get(class_)
