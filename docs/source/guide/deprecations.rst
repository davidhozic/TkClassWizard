========================
Deprecations
========================

TkClassWizard allows limited registration of deprecated parameters.
This can currently be done with the use of a class parameter.

To register a deprecated parameter, create a ``__deprecated_params__`` attribute under the
class in question. The attribute is a list of names of the deprecated parameters.


.. code-block:: python

    class MyClass
        __deprecated_params__ = ["a", "b"]

        def __init__(self, a: int, b: int, c: int):
            ...


The above example would allow the definition of the parameter ``c``, while parameters ``a`` and ``b``
will be grayed out. Editing is still allowed for the purposes of backwards compatibility.
