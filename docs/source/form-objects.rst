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


标准窗口类
***********

.. py:class:: Form

    基本的窗口类. 在编辑窗口的时候,用户可以通过选择右下角的 OK 按钮来退出.

   默认情况下,窗口会填满终端. 弹出式窗口只是具有更小的默认大小的窗口.


.. py:class:: Popup

   弹出式窗口只是个默认大小更小的窗口.


.. py:class:: ActionForm

    动作窗口 ActionForm 会创建 OK/确认 和 cancel/取消 按键. 选择任一个都会退出窗口. 当窗口退出时(假设是用户选择了这之中的一个按钮) *on_ok* 或 *on_cancel* 方法将被调用. 因此,在子类中可以有效重写其中一个或者两个,默认它们没有动作.

    .. py:method:: on_ok

        按下 ok 按钮的时被调用. 设置该方法的 `.editing` 属性为 True 会中止窗口的编辑.

    .. py:method:: on_cancel

        当按下 cancel按钮的时候被调用. 设置该方法的 `.editing` 属性为 True 会中止窗口的编辑.

.. py:class:: ActionFormV2

    在 4.3.0 版本中被新加入. 这个版本的动作窗口 ActionForm 的动作跟前面的 ActiveForm 类似,但是代码更清爽. 它应该更容易子类化.最终这个版本应该会完全取代 ActionForm.

.. py:class:: ActionFormMinimal

    于4.4.0版本被新加入. 这个版本的 ActionFormV2 只有一个 OK 按钮. 按用户的要求被添加用于特殊情况.

.. py:class:: ActionPopup

    是 ActionForm 小点的版本.


.. py:class::TitleForm

    更小版的窗口,只带个标题栏而没有完整的边框.

.. py:class::TitleFooterForm

    一个最小窗口, 只带一个标题和一条底线.

.. py:class:: SplitForm

   SplitForm 中间有一个水平线. 其 *get_half_way()* 方法会告诉你它被绘制在哪.

    .. py:attribute:: draw_line_at

       改属性定义了横穿屏幕的横线所绘制的位置. 它可以通过传递 `draw_line_at=` 到构造函数来设置, 或者根据 `get_half_way` 方法的返回值自动设定.

    .. py:method:: get_half_way

        返回穿过窗口中间的横线的y轴坐标. 实际上在此窗口的子类中,也没有什么特别原因,要让y轴坐标在实际上位于 窗口向下刚好一半的位置,其实子类可会返回任何方便的值.

    .. py:attribute:: MOVE_LINE_ON_RESIZE

        这个类属性指定了当窗口调整大小时,横线的位置是否应该要被移动. 因为横线下面的所有的控件也都需要被移动(设想到该窗口的子类中 `resize` 方被重写了的情况,该值默认被设为 False ).


.. py:class:: FormWithMenus

    类似于 Form类,但是提供了弹出菜单的附加功能.

   要添加新菜单到窗口,请使用 *new_menu(name='')* 方法. 这样会创建菜单并返回其代理. 更多细节参见下面菜单部分.


.. py:class:: ActionFormWithMenus

    类似于 ActionForm类,但是提供了弹出菜单的附加功能.

    要添加新菜单到窗口,请使用 *new_menu(name='')* 方法. 这样会创建菜单并返回其代理对象.更多细节参见下面菜单部分.

.. py:class:: ActionFormV2WithMenus

   在 4.3.0 版本被新加入. 这个版本的 ActionFormWithMenus 表现的跟上面的 ActionForm 类似,只是代码更加清爽. 子类操作上应该更容易. 最终, 这个版本应该会完全取代 ActionFormWithMenus.


.. py:class:: FormBaseNew

    这种窗口默认没有 *ok* 或 *cancel* 按钮. 附加方法 *pre_edit_loop* 和 *post_edit_loop* 会在该窗口被编辑之前与之后被调用. 默认版本中没有动作. 该类准备用作更复杂用户界面的基础.

    .. py:method:: pre_edit_loop

        窗口开始被编辑之前被调用.

    .. py:method:: post_edit_loop

        在编辑循环退出后被调用.

.. py:class:: FormBaseNewWithMenus

    开启菜单的 FormBaseNew.


类-Mutt 窗口
*************


.. py:class:: FormMutt

    受类似 *mutt* [一个字符界面邮件客户端] 或 *irssi* [一个字符界面IRC程序] 用户界面的启发,这种窗口定义了 4 种默认控件:

    *wStatus1*
        它位于屏幕的顶部. 你可以通过调整窗口的 *STATUS_WIDGET_CLASS* 类属性改变要使用的控件类型(注意,它在两个状态行里面都要用到).
    *wStatus2*
        它占据了屏幕的倒数第二行. 你可以通过调整窗口的 *STATUS_WIDGET_CLASS* 类属性改变要使用的控件类型(注意,它在两个状态行里面都要用到).
    *wMain*
        它占据 wStatus1 和 wStatus2 之间的区域,而且是一个多行控件. 你可以改变出现在这里的控件的类型,先子类化 *FormMutt* ,然后改变 *MAIN_WIDGET_CLASS* 类属性即可.
    *wCommand*
        这个区域占据屏幕的最后一行. 你可以通过改变 *COMMAND_WIDGET_CLASS* 类属性来改变要用的控件类型.

    默认, wStatus1 和 wStatus2 都把 *editable* 属性设为了 False.

FormMuttActive, FormMuttActiveWithMenus, FormMuttActiveTraditional, FormMuttActiveTraditionalWithMenus
    这些类都是用来简化创建更复杂应用的. 每个类都用了额外的 *NPSFilteredDataBase*, *ActionControllerSimple*, *TextCommandBox*, *TextCommandBoxTraditional* 类.

    常见的 \*nix 风格终端应用(像 mutt和 irssi 等用到的)都有个带中央显示的时间列表或网格,一个底部的命令行,还有一些状态信息行.

    这些类让配置一个类似的窗口变得容易. *FormMuttActive* 和 *FormMuttActiveTraditional* 类的不同点是, 在后者中,用户最终实质编辑的唯一控件,是屏幕底部的命令行控件. 不过,如果这些控件没有在编辑命令行,按键动作会被传递到在显示中央的多行控件里, 以允许用户来回滚动并选择屏幕上的条目.

    实际上什么要被显示到屏幕上,是由 *ActionControllerSimple* 类控制的, 以它为基础, 数据不是被任意独立控件, 而是由 *NPSFilteredDatabase* 类来存储的.

    更多信息参见该文档后续的 编写 类-Mutt 应用程序 部分.


多页面窗口
***********

.. py:class:: FormMultiPage (new in version 2.0pre63)

    这个 *实验性的* 类添加了多页面窗口的支持. 默认,在一个页面上向下滚动超出上最后一个控件,就会移动到下一个页面, 而从第一个控件继续向上移动就会回到上一页面.

    默认的该类会你把所在的页面显示在屏幕的右下角, 如果 *display_pages* 属性为 True 且页面多于一个的话. 你也可以把 *display_pages=False* 传递到构造函数. 用来进行显示的颜色存在 *pages_label_color* 属性中. 默认它的值是 'NORMAL'. 其他好用的值有 'STANDOUT', 'CONTROL' 或 'LABEL'. 同样,你也能把他们传进构造函数.

    要注意这个类是 實驗性的. 其 API 还在审查中,并且可能会在以后的版本中有所调整. 它计划用于那些可能不得不动态地去创建窗口的应用程序上, 它们可能需要创建比屏幕还要大的单个窗口(比如一个要显示服务器所指定的 xmpp表 的 Jabber 客户端). 它 *不是* 用来显示任意大的项目列表的. 要打算那样的话, multiline 类的控件可能会高效得多.


    有3个新的方法被加到该窗口对象中:

.. py:method:: FormMultiPage.add_page()

        用于窗口的创建时期. 这会添加一个新的页面,并且重置新控件添加点的位置. 新添页面的索引页数将被返回.

.. py:method:: FormMultiPage.switch_page(*index*)

        该方法将活跃页面改为由 *index* 指定的页.

.. py:method:: FormMultiPage.add_widget_intelligent(*args, **keywords)

        该方法会添加一个控件到窗口. 如果当前页面没有足够的空间,它会尝试创建一个新页面然后再把控件加到那儿. 要注意, 如果用户指定了哪怕是在新页面是也会防止控件被显示的选项, 这个方法可能依然会抛出异常.


.. py:class:: FormMultPageAction (new in version 2.0pre64)

    这是个 *实验* 版的 FormMultiPage 类, 添加了 ActionForm 的 on_ok 和 on_cancel 方法,并且窗口的最后一页页自动创建 cancel 和 ok 按钮.

.. py:class:: FormMultiPageWithMenus

    开启菜单版的 MultiPage.

.. py:class:: FormMultiPageActionWithMenus

    开启菜单版的 MultiPageAction.


菜单
*****

一些窗口支持使用弹出窗口. 理论上菜单也可以作为独立的控件来使用. 我们选择使用弹出菜单而不是下拉菜单(实际上受 RiscOS 的菜单系统启发),因其更适合键盘环境使用,并有效利用可用的屏幕空间, 也更容易部署到各种大小的终端上.

默认,支持的窗口都会显示一个带菜单系统的广告页给用户,及一个菜单列表的快捷键. 如果窗口有多个菜单,那么一个将其全部列出的 '根' 菜单会被显示出来.

菜单通常是调用(支持的)窗口的 *new_menu* 方法创建的. 2.0pre82 版本添加了 *shortcut=None* 参数到该方法. 在窗口显示的菜单列表中,这个快捷键也会被显示. 在一个菜单被创建之后,该对象的以下方法会很有用:

.. py:method:: NewMenu.addItem(text='', onSelect=function, shortcut=None, arguments=None, keywords=None)

    *text* 应该是菜单上显示的字符串. `onSelect` 应该是菜单项被用户选中后需要调用的函数. 这是仅有的几个 npyscreen 中容易创建循环引用的地方之一 - 你可能希望只传递一个代理进来. 我一直在尽力保护你远离循环引用,而这也只其中一次,很多时候我也无法猜测你的应用程序结构. 2.0pre82 版本增加了添加快捷键的功能.

    从 3.6 版本以后, 菜单项可以使用 *参数* 列表 加上或者只用一个关键字字典来指定.

.. py:method:: NewMenu.addItemsFromList(item_list)

    该函数的参数应该是一个列表或者元组. 其中的每个元素都应该是创建一个菜单的项参数的元组. 该方法已经*废弃*,并且可能在以后的版本中被移除或者修改.

.. py:method:: NewMenu.addNewSubmenu(name=None, shortcut=None, preDisplayFunction=None, pdfuncArguments=None, pdfuncKeywords=None)

    创建一个子菜单(返回其代理). 这是创建子菜单的最佳方式. 2.0pre82 版本增加了添加键盘快捷键的功能.

    从 3.7 版本之后,你可以在这个菜单显示之前定义一个被调用的函数及参数. 这可能意味着你可以在菜单显示的时刻调整其内容. 应用户要求添加.

.. py:method:: NewMenu.addSubmenu(submenu)

    将一个已经存在的菜单添加到菜单中作为子菜单. 综合考虑, addNewSubmenu 通常都是更好的选择.


(在内部,这个菜单系统被叫做 "新" 菜单系统 - 它替代了我一直不怎么喜欢的下拉菜单系统.)


窗口重调大小 (2.0pre88 版本新增)
****************************************

当窗口的大小被重新调整,会有一个信号发往屏幕上的当前窗口. 该窗口是否处理它取决于 3 件事.

如果你设置 `npyscreen.DISABLE_RESIZE_SYSTEM` 变量为 True. 窗口将完全不会调整大小.

类属性 `ALLOW_RESIZE` (默认 =True).
    如果它被设置为 False,窗口不会调整自身大小.

类属性 `FIX_MINIMUM_SIZE_WHEN_CREATED` 控制着窗口是否可以变得比创建时更小. 默认它被设为 `False`. 这是因为十多年来,npyscreen都假设窗口永远不会改变大小,并且很多程序可能都依赖于窗口大小永远不被调整这一现实. 如果你是在从头开始写新代码,你可以把这个值设成 True,  只是要确保你测试过结果,以确定调整窗口大小不会让你的应用程序崩溃.

当窗口被重新调整大小, `resize` 方法会在新的窗口大小被确定后被调用. 窗口都可以重写此方法,来将控件移动到新的位置,或修改任何相关让窗口布局更合适的东西.

当你使用 `NPSAppManaged` 系统时,窗口会在显示之前被自动调整大小.
