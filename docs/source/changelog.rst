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

v1.0.1
=================
- Fixed a bug where the window didn't close and couldn't be closed
  if an exception was raised when trying to define a class without annotations, and there
  were no previously opened frames.


v1.0.0
=================
- Initial release
