
====================================
Editing structured data
====================================

This is how our example from the previous page looks inside a GUI:

.. image:: ./images/example_gui_view.png
    :width: 15cm



Defining objects
==================

Now let's click on the **'Define Car'** button. Doing so will open up an object definition window:

.. image:: ./images/new_define_frame_struct.png
    :width: 15cm

Looking at the above image, we can see a lot of stuff going on, so let's just go down from the top.
At the very top row we have 3 buttons:

.. image:: ./images/new_define_frame_struct_top3_buttons.png
    :width: 15cm

- "Close": This button causes the entire definition frame (page) to close. Since this is the very first level of our definition
  frames (pages), it will also close the entire window. If we were to change anything inside the frame, this button would first
  ask us if we want to save our changes.
- "Save": As the name suggests, this button will save all the defined data into the return widget, that was passed as
  parameter to the :py:meth:`~tkclasswiz.object_frame.window.ObjectEditWindow.open_object_edit_frame` method, which in
  our case was :class:`~tkclasswiz.storage.ComboBoxObjects` the held by the ``combo`` variable.
  Finally the definition frame will be closed.
- "Keel on top": This button will keep the entire window on top of other windows, even if you clicked
  away. You can imagine it as a pin (on top) button.

Going downward we see a "Template" menu button, which allows us to either save the defined values into a JSON file, or
load them from a JSON file back into the GUI.

.. image:: ./images/new_define_frame_struct_template.png
    :width: 15cm

.. note::
    
    For verification purposes, the JSON file contains the full path to the defining class.
    Changing the class path requires users to update the corresponding path within the JSON files as well.

Going down further we can see multiple rows, each one of the corresponding to a parameter.

.. image:: ./images/new_define_frame_struct_parameters.png
    :width: 15cm


On the left side of our rows, we see labels that contain the name of each individual parameter.
The next item on the right is a Combobox (:class:`~tkclasswiz.storage.ComboBoxObjects`),
which is a dropdown menu used for storing the value of each defined parameter.
This dropdown menu can contain multiple values while we are still editing,
which we can access through the down arrow-like symbol located on the rightmost side of the Combobox.
When the definition frame is closed, all other values that were not selected inside the Combobox get discarded.
The dropdown menu is followed by 3 buttons:

- "New": is a dropdown menu button, which allows to define multiple data types that the parameter accepts. It can
  also be used to defined other structured data. Clicking on this button will open up a new page (definition frame),
  where the new data type can be defined.
- "✏️": is a button used for editing the selected value inside the dropdown menu. Clicking on this button will open
  up a new page (definition frame), where you can edit the existing value of a parameter.
- "C/P": is a menu button containing 2 options - "Copy" and "Paste". These can be used to copy and paste values from
  other dropdown menus and Listbox (talked about in later chapters) menus.
