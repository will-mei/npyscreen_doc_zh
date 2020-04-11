关于键绑定
======================

这是怎么回事
****************

许多对象可以基于用户按键来操作。所有这样的对象继承自内部类InputHandler。该类定义了一个名为 *handlers* 的字典和一个名为 *complex_handlers* 的列表。它们两者都是通过在构造函数时调用一个名为 *set_up_handlers* 的方法来设置。

*handlers*
   可能看起来像这样::

        {curses.ascii.NL:   self.h_exit_down,
         curses.ascii.CR:   self.h_exit_down,
         curses.ascii.TAB:  self.h_exit_down,
         curses.KEY_DOWN:   self.h_exit_down,
         curses.KEY_UP:     self.h_exit_up,
         curses.KEY_LEFT:   self.h_exit_left,
         curses.KEY_RIGHT:  self.h_exit_right,
         "^P":              self.h_exit_up,
         "^N":              self.h_exit_down,
         curses.ascii.ESC:  self.h_exit_escape,
         curses.KEY_MOUSE:  self.h_exit_mouse,
         }

如果按下一个作为在字典中以键值对存在的键（注意，支持标记像“^N” 代表 “Control-N”和"!a" 代表 "Alt N"），与它关联的函数将被调用。没有采取进一步的动作。按照惯例，处理用户输入的函数以h\_为前缀。

*complex_handlers*  
    这个列表应包含列表或元组对类似这样(test_func, dispatch_func)。

    如果该键未在字典 *handlers* 中命名，则运行每个test_func。如果它返回True，则运行dispatch_func并停止搜索。

    例如，使用复杂的处理程序是为了保证只将可打印字符输入到文本框中。因为它们将被频繁运行，应尽可能少并且尽可能快地运行它们。

当一个用户正在编辑控件和按下按键，使用 *handlers* 和 *complex_handlers* 来尝试找到一个执行的函数。如果控件没有定义要执行的操作，则检查父表单的 *handlers* 和 *complex_handlers*。因此，如果你想覆盖已绑定键的处理程序，请记住你在控件上操作而不是在它们的所属表单上，因为控件处理程序优先。

添加自己的处理程序
************************

可以处理用户输入的对象定义了以下方法来帮助添加自己的键绑定::

*add_handlers(new_handlers)*
    *new_handlers* 应是一个字典。

*add_complex_handlers(new_handlers)*
    *new_handlers* 应是列表的列表。每个子列表必须是一对 *(test_function, callback)*
