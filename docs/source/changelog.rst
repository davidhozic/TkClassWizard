========================
Changelog
========================
.. |BREAK_CH| replace:: **[Breaking change]**

.. |POTENT_BREAK_CH| replace:: **[Potentially breaking change]**

.. |UNRELEASED| replace:: **[Not yet released]**


Glossary
======================
.. glossary::

    |BREAK_CH|
        Means that the change will break functionality from previous version.

    |POTENT_BREAK_CH|
        The change could break functionality from previous versions but only if it
        was used in a certain way.


---------------------
Releases
---------------------

v1.2.1
================
- Replaced raw usage of ``.__annotations__`` with :func:`typing.get_typehints`.


v1.2.0
================
- Added the ability of nicknaming structured objects.
- Generic types support (Parametric types)
- :ref:`Type aliasing`
- Object nicknaming
- Tooltip when hovering over fields, which shows the full value.
- |BREAK_CH| Minimal Python version bumped to Python 3.9


v1.1.1
================
- Fixed template export on view-only mode, where the template exported wrong type.
- Fixed abstract classes, defined with ``__metaclass__ = ABCMeta``, not being treated as abstract.  


v1.1.0
================
- :ref:`Abstract classes` (those that directly inherit :class:`abc.ABC`) are no longer
  definable through TkClassWizard.
- :ref:`Polymorphism` support


v1.0.1
=================
- Fixed a bug where the window didn't close and couldn't be closed
  if an exception was raised when trying to define a class without annotations, and there
  were no previously opened frames.


v1.0.0
=================
- Initial release
