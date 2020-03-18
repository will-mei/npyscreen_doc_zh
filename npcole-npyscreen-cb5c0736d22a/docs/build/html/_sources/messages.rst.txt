Displaying Brief Messages and Choices
=====================================

The following functions allow you to display a brief message or choice to the user.

Notify and related methods are implemented in ``npyscreen/utilNotify.py``

The examples on this page build from this basic program:

.. literalinclude:: ../examples/notify/notify_skeleton.py
    :linenos:

.. py:function:: notify(message, title="Message", form_color='STANDOUT', wrap=True, wide=False,)

    This function displays a message on the screen.  It does not block and the user cannot interact with it - use it to display messages like "Please Wait" while other things are happening.
    
    .. literalinclude:: ../examples/notify/notify.py
        :emphasize-lines: 2, 11, 14-17
        :lines: 1-17
        :linenos:
        :caption: ../examples/notify/notify.py snippet

.. py:function:: notify_wait(message, title="Message", form_color='STANDOUT', wrap=True, wide=False,)
    
    This function displays a message on the screen, and blocks for a brief amount of time. The user cannot interact with it.

    .. literalinclude:: ../examples/notify/notify_wait.py
        :lineno-start: 4
        :emphasize-lines: 7, 10-12
        :lines: 4-15
        :caption: ../examples/notify/notify_wait.py snippet

.. py:function:: notify_confirm(message, title="Message", form_color='STANDOUT', wrap=True, wide=False, editw=0)
    
    Display a message and an OK button.  The user can scroll the message if needed.  editw controls which widget is selected when the dialog is first displayed; set to 1 to have the OK button active immediately.

    .. literalinclude:: ../examples/notify/notify_confirm.py
        :lineno-start: 4
        :emphasize-lines: 6, 10-12
        :lines: 4-15
        :caption: ../examples/notify/notify_confirm.py snippet

.. py:function:: notify_ok_cancel(message, title="Message", form_color='STANDOUT', wrap=True, editw = 0,)

    Display a message and return True if the user selected 'OK' and False if the user selected 'Cancel'.

    .. literalinclude:: ../examples/notify/notify_ok_cancel.py
        :lineno-start: 4
        :emphasize-lines: 6, 10-13
        :lines: 4-16
        :caption: ../examples/notify/notify_ok_cancel.py snippet
    
.. py:function:: notify_yes_no(message, title="Message", form_color='STANDOUT', wrap=True, editw = 0)

    Similar to *notify_ok_cancel* except the names of the buttons are 'Yes' and 'No'.  Returns True or False.
    



.. py:function:: selectFile(select_dir=False, must_exist=False, confirm_if_exists=True,sort_by_extension=True,)

    Display a dialog box for the user to select a filename. Uses the called from directory as the initial folder.  The
    return value is the name of the file selected.

    **Warning:** This form is currently experimental.

    .. literalinclude:: ../examples/notify/select_file.py
        :lineno-start: 4
        :emphasize-lines: 6, 10-12
        :lines: 4-15
        :caption: ../examples/notify/select_file.py snippet

Blanking the Screen
===================

.. py:function:: blank_terminal()

    This function blanks the terminal.  It may sometimes be needed if Forms are being displayed that do not fill the whole screen.

    .. literalinclude:: ../examples/notify/blank_terminal.py
        :lineno-start: 1
        :emphasize-lines: 1, 14-18
        :caption: ../examples/notify/blank_terminal.py snippet
