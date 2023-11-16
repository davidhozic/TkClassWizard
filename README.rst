=================
TkClassWizard
=================

Library for graphically defining objects based on class annotations.
Works with Tkinter / TTKBootstrap

Example
============

.. code-block:: python

    import tkclasswiz as wiz


    class Wheel:
        def __init__(self, diameter: float):
            self.diameter = diameter

    class Car:
        def __init__(self, name: str, speed: float, wheels: list[Wheel]):
            self.name = name
            self.speed = speed
            self.wheels = wheels


    combo = wiz.ComboBoxObjects()
    window = ObjectEditWindow()
    window.open_object_edit_frame(Car, combo)
