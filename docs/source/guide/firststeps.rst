=====================================
First steps
=====================================


To define your first object parameters with TkClassWizard, you can create
a :class:`tkinter.TopLevel` inherited object :class:`~tkclasswiz.object_frame.window.ObjectEditWindow` and then
call its :py:meth:`~tkclasswiz.object_frame.window.ObjectEditWindow.open_object_edit_frame` method, which
will open up the window and then load in :class:`tkinter.Frame`, which will contain placeholders for all parameter
values.

The :py:meth:`~tkclasswiz.object_frame.window.ObjectEditWindow.open_object_edit_frame` method accepts the following
parameters:

- class\ _: This is the class or a function that we want the parameters for.
- return_widget: This is a widget that receives the value after saving the newly defined parameters.
- old_data: The old_data gui data.
- check_parameters: Boolean parameter, which if True will not test if the object parameters are correct. When
  editing a function this is not ignored.
- allow_save: Boolean parameter, which if False will prevent the defined data to be saved; This also means it will
  be read-only.


It's best we take a look at an example.

.. code-block:: python
    :linenos:

    import tkinter as tk
    import tkinter.ttk as ttk
    import tkclasswiz as wiz

    # Normal Python classes with annotations (type hints)
    class Wheel:
        def __init__(self, diameter: float):
            self.diameter = diameter

    class Car:
        def __init__(self, name: str, speed: float, wheels: list[Wheel]):

            if len(wheels) != 4:
                raise ValueError("The car must have 4 wheels")
            
            if not isinstance(wheels[0], Wheel):
                raise TypeError("The 'wheels' parameter must be of type Wheel")

            self.name = name
            self.speed = speed
            self.wheels = wheels

    # Tkinter main window
    root = tk.Tk("Test")

    # Modified tkinter Combobox that will store actual objects instead of strings
    combo = wiz.ComboBoxObjects(root)
    combo.pack(fill=tk.X, padx=5)

    def make_car(old = None):
        """
        Function for opening a window either in new definition mode (old = None) or
        edit mode (old != None)
        """
        assert old is None or isinstance(old, wiz.ObjectInfo)

        window = wiz.ObjectEditWindow()  # The object definition window / wizard
        window.open_object_edit_frame(Car, combo, old_data=old)  # Open the actual frame

    def print_defined():
        data = combo.get()
        data = wiz.convert_to_objects(data)  # Convert any abstract ObjectInfo objects into actual Python objects
        print(f"Object: {data}; Type: {type(data)}",)  # Print the object and it's datatype


    # Main GUI structure
    ttk.Button(text="Define Car", command=make_car).pack()
    ttk.Button(text="Edit Car", command=lambda: make_car(combo.get())).pack()
    ttk.Button(text="Print defined", command=print_defined).pack()
    root.mainloop()



In the above example we first import the library by typing ``import tkclasswiz as wiz``.
Then we define 2 classes, the class ``Wheel`` and class ``Car``.

The ``Wheel`` class accepts a single parameter annotated with the ``float`` type. It is VERY IMPORTANT
that all the parameters are annotated, else they will not be displayed when defining parameters through the GUI.

The ``Car`` class accepts parameters ``name`` of type ``str``, ``speed`` of type ``float`` and list of ``wheels`` 
f type ``Wheel``. From the ``wheels`` parameter we can see that we can define multiple nested objects as well.

Then we create an instance of ``Tk``, which is just the standard way for creating a tkinter app.

Then we create a ``combo`` variable of type :class:`~tkclasswiz.storage.ComboBoxObjects`, which will receive the defined
``Car`` object after we define the object successfully. But it won't receive an actual instance of ``Car``,
however it will receive an abstract representation of the defined object. The abstract representation is an instance of
:class:`tkclasswiz.convert.ObjectInfo` and its job is to store the class (in our case ``Car``) and the parameters
defined. When displaying the defined abstract ``Car`` object inside the GUI, it will be displayed as
``Class(parameter1=value1, ...)``.

Afterwards we define 2 functions, the first one will open the definition window, while the second one will
convert the abstract ``Car`` object into a real Python object.

Function ``make_car`` accepts a parameter ``old``, which will be later used to edit the existing object after we defined it.
But since it is not defined yet, this is currently irrelevant. Next lines of code in the function create the
:class:`~tkclasswiz.object_frame.window.ObjectEditWindow` definition window and load in the definition frame by calling
the :py:meth:`~tkclasswiz.object_frame.window.ObjectEditWindow.open_object_edit_frame`, which we pass
the class of an object we want to define (``Car``), the return widget (``combo``) that receives the defined object and
the ``old_data`` parameter which would load in previously defined values (which currently don't exist).

At the very bottom of the example, we define a few buttons:

- 'Define Car': Calls ``make_car`` function, opening the object definition window.
- 'Edit Car': Calls ``make_car`` function, opening the object definition window and loading in the already defined
  :class:`tkclasswiz.convert.ObjectInfo` abstract ``Car`` object.
- 'Print defined': Calls ``print_defined`` function which converts the abstract object into a real one and prints it out,
  including its type.

Now let's take a look at how our example looks :ref:`inside a GUI <Defining data>`.
