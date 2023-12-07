=============================
Object conversion
=============================


.. |OBJECT_INFO| replace:: :class:`~tkclasswiz.convert.ObjectInfo`


When you have defined an abstract object through the GUI (|OBJECT_INFO| instance), you can
now either convert it to an actual Python object or into dictionary. You can also do the reverse.


ObjectInfo into Python object
===============================
Converting abstract objects (|OBJECT_INFO| instances) can be done with the
:class:`~tkclasswiz.convert.convert_to_objects` function, which only accepts a single parameter that can be:

- an |OBJECT_INFO| instance
- a :class:`list` of |OBJECT_INFO| instances
- a :class:`dict` whose values are |OBJECT_INFO| instances

Looking at the example from :ref:`First steps`, we can see this function utilized in the ``print_defined``
function.

.. code-block:: python
    :linenos:
    :emphasize-lines: 3

    def print_defined():
        data = combo.get()
        data = wiz.convert_to_objects(data)  # Convert any abstract ObjectInfo objects into actual Python objects
        print(f"Object: {data}; Type: {type(data)}",)  # Print the object and it's datatype


ObjectInfo into dictionary
===============================
To convert an abstract object (|OBJECT_INFO|) into a dictionary, the :func:`~tkclasswiz.convert.convert_to_dict`
can be used. The function accepts either an |OBJECT_INFO| instance or a list of |OBJECT_INFO| instances as a parameter
and outputs a dictionary.
Each |OBJECT_INFO| gets converted into ``{"type": <object type>, "data": <parameter dictionary>}``

For example, an abstract object of the following class

.. code-block:: python

    class MyClass:
        def __init__(self, a: int, b: float):
            ...

is converted into

.. code-block::

    {
        "type": "<module path>.MyClass",
        "data": {
            "a": <defined integer number>,
            "b": <defined floating point number>,
        }
    }

The dictionary only contains parameters that were not left empty inside the GUI's object definition window.


Dictionary into ObjectInfo
===============================
A dictionary displayed under :ref:`ObjectInfo into dictionary` can also be transformed back
into the abstract object (|OBJECT_INFO|) instance.
This can be done with the :func:`tkclasswiz.convert.convert_from_dict` function.



Python object into ObjectInfo
==================================
Converting an abstract |OBJECT_INFO| instance into a real Python object is easy, because the conversion
is simply done by passing the parameters to the class.

If we want to convert an actual Python object back into its abstract |OBJECT_INFO| representation,
things get a bit trickier. This is because the information about original parameters can be lost or
the parameters may not be stored under the same name as the attributes are.

Converting user-defined classes
--------------------------------
If we examine the following example, we can observe that parameter ``a`` is stored under a different name,
and parameter ``b`` is not only stored under a different name but also has a different attribute value.

.. code-block:: python

    class MyClass:
        def __init__(self, a: int, b: int):
            self._a = a   # Attribute name different from parameter
            self._b = a + b  # Attribute name different from parameter. Value is also different.


Python objects can be converted to abstract (|OBJECT_INFO|) objects with the
:func:`~tkclasswiz.convert.convert_to_object_info` function.
By default function tries to make conversions based on annotations, which also includes the additionally registered
annotations described in :ref:`Missing annotations`. It assumes that parameters are stored under the same attribute
name. Knowing this, the simplest and the recommended way of making conversion possible is to use :class:`property`
descriptors.

Here's the modified example from earlier, which uses the :class:`property` descriptor:

.. code-block:: python
    :linenos:
    :emphasize-lines: 6-8, 10-12

    class MyClass:
        def __init__(self, a: int, b: int):
            self._a = a   # Attribute name different from parameter
            self._b = a + b  # Attribute name different from parameter. Value is also different.

        @property
        def a(self):
            return self._a

        @property
        def b(self):
            return self._b - self._a  # Original value of the b parameter

The use of :class:`property` descriptor to support the conversion from a Python object into abstract (|OBJECT_INFO|)
instance is obviously only possible if we have the ability to modify the code of the class whose instance we want
to convert. We cannot utilize the above for any built-in Python libraries or libraries installed with PIP.


Converting 3rd party classes
--------------------------------
TkClassWizard allows users to define custom conversion parameter-attribute mappings and also
provides a way to create custom rules per parameter with the use of lambda functions.
This can be done with the :func:`~tkclasswiz.convert.register_object_objectinfo_rule` function, which
as a parameter accepts the class we want to register a conversion rule for, and a set of keyword-only arguments,
which map parameter names to either their attribute names or a lambda function. If a lambda function is given,
then this function must accept a single parameter, which is the actual object we are converting. Whatever this lambda
function returns is then used as the parameter value.

.. code-block:: python

    class FILE:
        def __init__(self, filename: str):
            self.fullpath = filename

        # FILE
        register_object_objectinfo_rule(
            FILE,
            filename="fullpath"
        )

        # Timezone
        import datetime
        register_object_objectinfo_rule(
            datetime.timezone,
            offset=lambda tz: tz.utcoffset(None)  # tz is the timezone object we are converting
        )


Defined conversion rules can be obtained with the :func:`~tkclasswiz.convert.get_object_objectinfo_rule_map` function.
It accepts a class as a parameter and returns a dictionary mapping parameter names to attribute names or lambda 
functions.
