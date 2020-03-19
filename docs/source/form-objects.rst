窗口对象
========

窗口对象就是屏幕上一个容纳控件的区域. 窗口对象可以控制用户当前编辑哪个控件,并且还可能提供附加功能,比如弹出菜单和特定按键被按下应该产生的动作.

创建窗口
*********

.. py:class:: Form(name=None, lines=0, columns=0, minimum_lines=24, minimum_columns=80)

窗口具有以下类属性::

    DEFAULT_LINES      = 0
    DEFAULT_COLUMNS    = 0
    SHOW_ATX           = 0
    SHOW_ATY           = 0

使用这些默认值会创建一个显示在左上角并且填满整个屏幕的窗口. 控制窗口大小的细节参见传递进构造函数的参数.

以下参数能被传进窗口的构造函数里:

*name=*
    命名该窗口. 对于一些控件,这样会显示一个标题.

*lines=0, columns=0, minimum_lines=24, minimum_columns=80*

    要调整窗口的大小,要么给出其尺寸绝对值(使用 *lines=* 和 *columns=*),要么给出其最小尺寸值(*minimum_lines=* 与 *minimum_columns=*). 默认的最小值(24x80)给出了在终端上的标准大小. 如果你设计好让窗口适配到这个大小以内,那么他们应该在所有的系统的界面上不滚动窗口的情况下也全可见. 注意,你可以在一个方向使用绝对值大小,另一个方向上使用最小值大小,要是你想要的话.

标准的构造函数都会调用 *.create()* 方法, 你应该对它重写来给窗口创建控件. 请看下面.

把控件放到窗口
***************

要把控件放到窗口上, 要用这些方法:

.. py:method:: Form.add(WidgetClass, ...)

    WidgetClass 必须得是一个类,所有的附加参数都会被传递到控件自己的构造函数里. 控件的引用会被返回.


控件的位置和大小由控件的构造函数控制. 不过,有一些指示是窗口类给出的. 如果你不重写控件的位置,它会根据窗口实例的 *.nextrelx* 和 *nextrely* 属性值来归置. 这里的 *.nextrely* 属性是随每次的控件放置而自增长的. 你也可以自行把它加大,就像下面这样::

   self.nextrely += 1

这会在前一个被被放置的控件跟下一个之间留下一个间隔.

.. py:attribute:: Form.nextrely

    下一控件创建时, 在 y 轴的位置. 每当控件被加进窗口, 标准的窗口都会把它设成上一被创建控件的下一行.

.. py:attribute:: nextrelx

     下一控件被创时, 在 x 轴的位置.


标准窗口的其他特性
*******************

.. py:method:: Form.create

    该方法由窗口的构造函数调用. 默认它什么也不做 - 它是准备让你在子类中重写的, 不过它是对窗口上所有的控件进行配置的最佳位置. 所以, 等着这个方法装满 *self.add(...)* 方法的调用吧!


.. py:method:: Form.while_editing

    这个方法在用户于控件之间移动时被调用. 它也是打算让你在子类中重写的,做一些像是让一个控件按另一个的值改变之类的事情.


.. py:method:: Form.adjust_widgets

    用这个方法的时候要很小心. 窗口被编辑时,每次按键时它都被调用,并且不保证它不会被调用的更频繁. 默认它没有动作,并且是打算让你来重写的. 鉴于它被如此频繁地调用,这里大意的话就要拖慢你的整个应用了.

    比如,对重绘整个窗口(这是个缓慢的操作)就要尽量保守一点 - 要确保在代码中实际验证是否每个重绘都必要,试着只重绘那些真的需要被调整的控件,而不是重绘整个屏幕.

    如果窗口的 parentApp (父级的应用对象)也有叫 *adjust_widgets* 的方法,它也会被调用.


.. py:method:: Form.while_waiting

    如果你想在等待用户按下某个键时执行动作,你可以定义一个 *while_waiting* 方法. 同时你还要设置 *keypress_timeout* 属性,这是个以毫秒(ms)为单位的值. 每当开始等待输入, 如果时间超过了 *keypress_timeout* 的给定时间, *while_waiting* 就会被调用. 注意, npyscreen 没有采取任何流程来保证 *while_waiting()* 精确按照规律的时间间隔被调用, 实际要是用户持续按着键,它可能永远也不会被调用到.

    如果窗口的 parentApp 有叫 *while_waiting* 的方法,它也会被调用.

    一个 *keypress_timeout* 为 10 的值, 就意味着 *while_waiting* 方法每秒都会被调用到, 假设用户没有其它动作.

    功能完整的例子参见代码包含的 Example-waiting.py 样例文件.

.. py:attribute:: Form.keypress_timeout

参考上面的 `while_waiting` 方法.


.. py:method:: Form.set_value(value)

    将 *value* 存到 *Form* 对象的 *.value* 属性中,然后调用所有控件的 *when_parent_changes_value* 方法, 如果它们有的话.


.. py:attribute:: Form.value

    所有的窗口类可能都有 *set_value(value)* 方法.  这会设定 *value* 属性的值并调用内部窗口所含的每一控件的 *when_parent_changes_value* 方法.


显示并编辑窗口
***************

.. py:method:: Form.display()

    重绘窗口及其每个控件.

.. py:method:: Form.DISPLAY()

    重绘窗口,并额外确认显示器被重置. 这是一个缓慢的操作,要尽量避免调用它. 你有些时候可能需要使用到它,比如外部进程破坏了终端.

.. py:method:: Form.edit()

    允许用户交互式地编辑每个控件的值. 如果正确使用 *NPSAppManaged* 类,你应该不需要用到这个方法. 你应该尽可能避免调用该方法, 不过有时候可能用到, 要是写简单应用用不上 NPSAppManaged 类的话. 直接调用该方法更类似于在 GUI 应用中创建一个模式对话框[模态框,覆盖在父窗体上的子窗体]. 尽可能地去把这个方法当成一个内部的 API 调用.

窗口退出的情况
~~~~~~~~~~~~~~~

    窗口可能因为很多原因需要退出其编辑模式. 在 NPSAppManaged 应用中,控制它的应用也可能导致窗口退出.

    自行把 `.editing` 属性设定为 False, 其实也会导致窗口退出.


Standard Form Classes
*********************

.. py:class:: Form

   The basic Form class.  When editing the form, the user can exit by selecting the OK button in the bottom right corner.

   By default, a Form will fill the Terminal.  Popup is simply a Form with a smaller default size.


.. py:class:: Popup

   Popup is simply a Form with a smaller default size.


.. py:class:: ActionForm

   The ActionForm creates OK and Cancel buttons.  Selecting either exits the form.  The method *on_ok* or *on_cancel* is called when the Form exits (assuming the user selected one of these buttons).  Subclasses may therefore usefully override one or both of these methods, which by default do nothing.

    .. py:method:: on_ok

        Called when the ok button is pressed.  Setting the attribute `.editing` to True in this method will abort editing the form.

    .. py:method:: on_cancel

        Called when the cancel button is pressed. Setting the attribute `.editing` to True in this method will abort editing the form.

.. py:class:: ActionFormV2

   New in Version 4.3.0.  This version of ActionForm behaves similarly to ActionForm above, but the code is much cleaner.  It should
   be much easier to subclass.  Eventually, this version may entirely replace ActionForm.

.. py:class:: ActionFormMinimal

    New in Version 4.4.0.  This version of ActionFormV2 only features an OK button.  Added at user request for use in
    special circumstances.

.. py:class:: ActionPopup

    A smaller version of the ActionForm.


.. py:class::TitleForm

    A more minimal form with just a title bar, rather than a full border.

.. py:class::TitleFooterForm

    A minimal form with a title bar and a bar along the bottom.

.. py:class:: SplitForm

   The SplitForm has a horizontal line across the middle.  The method *get_half_way()* will tell you where it has been drawn.

    .. py:attribute:: draw_line_at

       This attribute defines the position at which the line should be drawn across the screen.  It can be set by passing `draw_line_at=`
       to the constructor, or will be set automatically at the value returned by the method `get_half_way`.

    .. py:method:: get_half_way

        return the y co-ordinate of the bar across the middle of the form.  In fact in subclasses of this form, there is no
        particular reason why the y co-ordinate should in fact be half way down the form, and subclasses may return whatever
        value is convenient.

    .. py:attribute:: MOVE_LINE_ON_RESIZE

        This class attribute specifies whether the position of the line should be moved when the form is resized.  Since
        any widgets below the line would also need to be moved (presumably in an overriden `resize` method on subclasses of
        this form, this value is set to False by default).


.. py:class:: FormWithMenus

    Similar to the Form class, but provides the additional functionality of Popup menus.

    To add a new menu to the Form use the method *new_menu(name='')*.  This will create the menu and return a proxy to it.  For more details see the section on Menus below.


.. py:class:: ActionFormWithMenus

   Similar to the ActionForm class, but provides the additional functionality of Popup menus.

   To add a new menu to the Form use the method *new_menu(name='')*.  This will create the menu and return a proxy to it.  For more details see the section on Menus below.

.. py:class:: ActionFormV2WithMenus

   New in Version 4.3.0.  This version of ActionFormWithMenus behaves similarly to ActionForm above, but the code is much cleaner.  It should
   be much easier to subclass.  Eventually, this version may entirely replace ActionFormWithMenus.


.. py:class:: FormBaseNew

    This form does not have an *ok* or *cancel* button by default.  The additional methods *pre_edit_loop* and *post_edit_loop* are called before and after the Form is edited.  The default versions do nothing.  This class is intended as a base for more complex user interfaces.

    .. py:method:: pre_edit_loop

        Called before the form is edited.

    .. py:method:: post_edit_loop

        Called after the edit loop exits.

.. py:class:: FormBaseNewWithMenus

    Menu-enabled version of FormBaseNew.


Mutt-like Forms
***************


.. py:class:: FormMutt

    Inspired by the user interfaces of programs like *mutt* or *irssi*, this form defines four default widgets:

    *wStatus1*
        This is at the top of the screen.  You can change the type of widget used by changing the *STATUS_WIDGET_CLASS* class attribute (note this is used for both status lines).
    *wStatus2*
        This occupies the second to last line of the screen. You can change the type of widget used by changing the *STATUS_WIDGET_CLASS* class attribute (note this is used for both status lines).
    *wMain*
        This occupies the area between wStatus1 and wStatus2, and is a MultiLine widget.  You can alter the type of widget that appears here by subclassing *FormMutt* and changing the *MAIN_WIDGET_CLASS* class attribute.
    *wCommand*
        This Field occupies the last line of the screen. You can change the type of widget used by altering the *COMMAND_WIDGET_CLASS* class attribute.

    By default, wStatus1 and wStatus2 have *editable* set to False.

FormMuttActive, FormMuttActiveWithMenus, FormMuttActiveTraditional, FormMuttActiveTraditionalWithMenus
    These classes are intended to make the creation of more complicated applications easier.  Each class uses the additional classes *NPSFilteredDataBase*, *ActionControllerSimple*, *TextCommandBox*, *TextCommandBoxTraditional*.

    A very common \*nix style of terminal application (used by applications like mutt and irssi) has a central display with a list or grid of times, a command line at the bottom and some status lines.

    These classes make setting up a similar form easy.  The difference between the *FormMuttActive* and *FormMuttActiveTraditional* classes is that in the latter the only widget that the user ever actually edits is the command line at the bottom of the screen.  However, keypresses will be passed to the multiline widget in the centre of the display if these widgets are not editing a command line, allowing the user to scroll around and select items.

    What is actually displayed on the screen is controlled by the *ActionControllerSimple* class, which uses as a base the data stored not by any of the individual widgets but by the *NPSFilteredDatabase* class.

    See the section on writing Mutt-like applications later in this documentation for more information.


Multi-page Forms
****************

.. py:class:: FormMultiPage (new in version 2.0pre63)

    This *experimental* class adds support for multi-page forms.  By default, scrolling down off the last widget on a page moves to the next page, and moving up from the first widget moves back a page.

    The default class will display the page you are on in the bottom right corner if the attribute *display_pages* is True and if there is more than one page.  You can also pass *display_pages=False* in to the constructor.  The color used for this display is stored in the attribute *pages_label_color*.  By default this is 'NORMAL'.  Other good values might be 'STANDOUT', 'CONTROL' or 'LABEL'. Again, you can pass this in to the constructor.

    Please note that this class is EXPERIMENTAL.  The API is still under review, and may change in future releases.  It is intended for applications which may have to create forms dynamically, which might need to create a single form larger than a screen (for example, a Jabber client that needs to display an xmpp form specified by the server.)  It is *not* intended to display arbitrarily large lists of items.  For that purpose, the multiline classes of widgets are much more efficient.


    Three new methods are added to this form:

.. py:method:: FormMultiPage.add_page()

        Intended for use during the creation of the form.  This adds a new page, and resets the position at which new widgets will be added.  The index of the page added is returned.

.. py:method:: FormMultiPage.switch_page(*index*)

        This method changes the active page to the one specified by *index*.

.. py:method:: FormMultiPage.add_widget_intelligent(*args, **keywords)

        This method adds a widget to the form.  If there is not enough space on the current page, it tries creating a new page and adding the widget there.  Note that this method may still raise an exception if the user has specified options that prevent the widget from appearing even on the new page.


.. py:class:: FormMultPageAction (new in version 2.0pre64)

    This is an *experimental* version of the FormMultiPage class that adds the on_ok and on_cancel methods of the ActionForm class and automatically creates cancel and ok buttons on the last page of the form.

.. py:class:: FormMultiPageWithMenus

    Menu-enabled version of MultiPage.

.. py:class:: FormMultiPageActionWithMenus

    Menu-enabled version of MultiPageAction.


Menus
*****

Some Form classes support the use of popup menus.  Menus could in theory be used as widgets on their own.  Popup menus (inspired, in fact, by the menu system in RiscOS) were selected instead of drop-down menus as being more suitable for a keyboard environment, making better use of available screen space and being easier to deploy on terminals of varied sizes.

By default, the supporting forms will display an advert that the menu system is available to the user, and a shortcut to the list of menus.  If the form has multiple menus, a 'root' menu listing all of them will be displayed.

Menus are usually created by calling a (supporting) Form's *new_menu* method.  Version 2.0pre82 adds the argument *shortcut=None* to this method.  In the list of menus that the Form displays, this shortcut will be displayed.  After a menu has been created, the following methods on that object are useful:

.. py:method:: NewMenu.addItem(text='', onSelect=function, shortcut=None, arguments=None, keywords=None)

   *text* should be the string to be displayed on the menu.  `onSelect` should be a function to be called if that item is selected by the user.  This is one of the few easy opportunities in npyscreen to create circular references - you may wish to pass in a proxy to a function instead.  I've tried to guard you against circular references as much as possible - but this is just one of those times I can't second-guess your application structure. Version 2.0pre82 adds the ability to add a shortcut.

   From version 3.6 onwards, menu items can be specified with a list of *arguments* and/or a dictionary of keywords.

.. py:method:: NewMenu.addItemsFromList(item_list)

	The agument for this function should be a list or tuple. Each element of this should be a tuple of the arguments that are used for creating each item.  This method is DEPRECATED and may be removed or altered in a future version.

.. py:method:: NewMenu.addNewSubmenu(name=None, shortcut=None, preDisplayFunction=None, pdfuncArguments=None, pdfuncKeywords=None)

   Create a new submenu (returning a proxy to it).  This is the preferred way of creating submenus. Version 2.0pre82 adds the ability to add a keyboard shortcut.

   From version 3.7 onwards, you can define a function and arguments to be called before this menu is displayed.  This might mean you
   can adjust the content of the menu at the point it is displayed.  Added at user request.

.. py:method:: NewMenu.addSubmenu(submenu)

    Add an existing Menu to the Menu as a submenu.  All things considered, addNewSubmenu is usually a better bet.


(Internally, this menu system is referred to as the "New" menu system - it replaces a drop-down menu system with which I was never very happy.)


Resizing Forms (New in version 2.0pre88)
****************************************

When a form is resized, a signal is sent to the form currently on the screen.  Whether or not the form handles this is decided by three things.

If you set the variable `npyscreen.DISABLE_RESIZE_SYSTEM` to True, forms will not resize at all.

The class attribute `ALLOW_RESIZE` (=True by default).
	If this is set to false the form will not resize itself.

The class attribute `FIX_MINIMUM_SIZE_WHEN_CREATED` controls whether the form can be made smaller than the size it was when it was created.  By default this is set to `False`.  This is because for over a decade, npyscreen assumed that forms would never change size, and many programs may rely on the fact that the form will never be resized.  If you are writing new code from scratch, you can set this value to True, provided that you test the results to make sure that resizing the form will not crash your application.

When a form is resized, the method `resize` will be called *after* the new size of the form has been fixed.  Forms may override this method to move widgets to new locations or alter anything else about the layout of the form as appropriate.

When using the `NPSAppManaged` system, forms will be automatically resized before they are displayed.
