=================================
Missing annotations
=================================

When we are defining our own objects, we can always annotate them and allow TkClassWizard to work without
any problems.
Unfortunately other (including Python's built-in) libraries may not have types annotated inside their classes and functions.
If we wish to use those libraries and graphically define objects with TkClassWizard, we will have problems.

To solve the issue of missing annotations, TkClassWizard contains an annotations module for dealing with missing
annotations.

If you feel the need to register additional class annotations, you can do so with the
:func:`~tkclasswiz.annotations.register_annotations` function.
This function accepts the class as an input and a set of keyword arguments which which map ``parameter=datatype``.
Example is shown below.

.. code-block:: python
    :linenos:

    from tkclasswiz.annotations import register_annotations

    class MissingAnnotations:
        def __init__(self, a, b, c):
            ...

    register_annotations(
        MissingAnnotations,
        a=int,
        b=float,
        c=str
    )


For convenience :class:`datetime.datetime`, :class:`datetime.timedelta` and :class:`datetime.timezone` already
have these annotations registered.

To obtain a mapping of registered annotations, :func:`~tkclasswiz.annotations.get_annotations` can be used.
It returns a dictionary mapping parameter to the data type for both code defined annotations and annotations defined
with :func:`~tkclasswiz.annotations.register_annotations`.
