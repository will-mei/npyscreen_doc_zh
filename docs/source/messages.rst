显示简明的消息和选择
=====================================

下列函数允许你向用户显示一个简短的消息或选择。

通知相关的方法是在 ``npyscreen/utilNotify.py`` 中实现的。

本页的例子从这个基本程序上建立的:

.. literalinclude:: ../examples/notify/notify_skeleton.py
    :linenos:

.. py:function:: notify(message, title="Message", form_color='STANDOUT', wrap=True, wide=False,)

    这个函数在屏幕上显示一条消息。它不阻塞，且用户不会与它交互 - 在其他事情正在发生时，使用它来显示类似“Please wait”的消息。

    .. literalinclude:: ../examples/notify/notify.py
        :emphasize-lines: 2, 11, 14-17
        :lines: 1-17
        :linenos:
        :caption: ../examples/notify/notify.py snippet

.. py:function:: notify_wait(message, title="Message", form_color='STANDOUT', wrap=True, wide=False,)

    这个函数在屏幕上显示一条消息，且阻塞很短的一段时间。用户不会与它进行交互。

    .. literalinclude:: ../examples/notify/notify_wait.py
        :lineno-start: 4
        :emphasize-lines: 7, 10-12
        :lines: 4-15
        :caption: ../examples/notify/notify_wait.py snippet

.. py:function:: notify_confirm(message, title="Message", form_color='STANDOUT', wrap=True, wide=False, editw=0)

    显示一条消息和OK按钮。如果需要，用户可以滚动消息。editw控制对话框首次显示时选择哪一个控件；设置为1则立刻激活OK按钮。

    .. literalinclude:: ../examples/notify/notify_confirm.py
        :lineno-start: 4
        :emphasize-lines: 6, 10-12
        :lines: 4-15
        :caption: ../examples/notify/notify_confirm.py snippet

.. py:function:: notify_ok_cancel(message, title="Message", form_color='STANDOUT', wrap=True, editw = 0,)

    显示一条消息,如果用户选择‘OK’,则返回True；如果用户选择‘Cancel’，则返回False。

    .. literalinclude:: ../examples/notify/notify_ok_cancel.py
        :lineno-start: 4
        :emphasize-lines: 6, 10-13
        :lines: 4-16
        :caption: ../examples/notify/notify_ok_cancel.py snippet

.. py:function:: notify_yes_no(message, title="Message", form_color='STANDOUT', wrap=True, editw = 0)

    与 *notify_ok_cancel* 相似，除了按钮名称是‘Yes’和‘No’，返回True或False。




.. py:function:: selectFile(select_dir=False, must_exist=False, confirm_if_exists=True,sort_by_extension=True,)

    显示一个提示用户选择文件名的对话框。使用来自目录的调用作为初始化文件夹。返回值是所选文件的名称。

    **Warning:** 这个形式当前还是试验阶段。

    .. literalinclude:: ../examples/notify/select_file.py
        :lineno-start: 4
        :emphasize-lines: 6, 10-12
        :lines: 4-15
        :caption: ../examples/notify/select_file.py snippet

空白的屏幕
===================

.. py:function:: blank_terminal()

    这个函数使终端消失。如果显示的表单没有占满整个屏幕，它有时可能被需要。

    .. literalinclude:: ../examples/notify/blank_terminal.py
        :lineno-start: 1
        :emphasize-lines: 1, 14-18
        :caption: ../examples/notify/blank_terminal.py snippet
