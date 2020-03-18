应用对象
========

.. py:class: NPSAppManaged

NPSAppManaged 提供一个框架开始和结束应用程序, 以一种不会有递归深度问题的方式完成对你创建的各种窗口的显示管理.

除非你有什么特别好的理由要用其他方式, 否则 *NPSAppManaged* 应该就是管理你的应用的最好方法.

跟简朴的 NPSApp 类不同, 你不用自己写主循环 - *NPSAppManaged* 会管理好你的应用的每个窗口的显示. 设定好你的窗口对象,然后就只要调用你的 NPSAppManaged 实例的 *.run()* 方法就可以了.

让 NPSAppManaged 管理你的窗口
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

有3种方法来用 NPSAppManaged 实例注册一个窗口对象:


.. py:method:: NPSAppManaged.addForm(*id*, *FormClass*, ...)

    在种版本的写法会先创建一个新的窗口, 然后用 NPSAppManaged 实例来注册. 它从窗口对象返回一个 weakref.proxy [弱引用的对象代理]. 其 *.id* 需要是一个可以唯一标识该窗口的字符串. *FormClass* 应该是要创建的窗口的类. 任何额外的参数都会别传递到该窗口的构造函数中[用来指定窗口的创建规格]. 如果你没有单独存放窗口的引用的地方,就用这种写法.

.. py:method:: NPSAppManaged.addFormClass(*id*, *FormClass* ...)

    这种写法注册一个窗口类而不是一个实例. 每次被编辑完都会有一个新实例被创建. 额外的参数在每次创建的时被传递到窗口的构造函数中.

.. py:method:: NPSAppManaged.registerForm(id, fm)

    *id* 需要是一个可以唯一标识该窗口的字符串.  *fm* 需要是一个窗口对象.  要注意,跟 .addForm 的写法比起来 - 这种写法只在 NPSAppManaged 中存放一个 weakref.proxy .


所有用 NPSAppManaged 实例注册的窗口都可以用 *self.parentApp* 来访问到对应用对象的控制.

若因某些原因需要删除一个窗口, 你可以用 `.removeForm(*id*)` 方法来去做.

运行 NPSApplicationManaged 应用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:method:: run

    开始一个 NPSAppManaged 应用的主循环. 该方法会激活默认的窗口, 它应该被指定用 "MAIN" 来作为 id .

.. py:attribute:: NPSAppManaged.STARTING_FORM

    如果你出于什么原因要改默认窗口的名称,你可以在这改.

一旦程序开始运行, 下面的方法会控制哪个窗口展示给用户.

.. py:method:: NPSAppManaged.setNextForm(formid)

    设定在当前窗口退出后,要显示的窗口.

.. py:method:: NPSAppManaged.setNextFormPrevious

    设定在当前窗口退出到历史中的上一个窗口时,要显示的窗口.

.. py:method:: NPSAppManaged.switchForm(formid)

    立即切换到指定的窗口, 绕过一切当前窗口的退出逻辑.

.. py:method:: NPSAppManaged.switchFormPrevious()

    立即切换到历史记录中之前工作的窗口.


细节说明
++++++++

一旦所有的窗口都准备好并注册到 NPSAppManaged 实例, 你就该调用 .run() 方法了.

这个方法会激活默认的窗口, 它应该以 "MAIN" 为 id. 你可以通过修改类或者实例的 `.STARTING_FORM` 变量来改变这个默认 id.

这之后, 下一个被显示的窗口就是被实例的 *NEXT_ACTIVE_FORM* 变量所指定的. 不管什么时候当一个窗口的编辑循环退出了, 这个变量所指定的新窗口都会被激活. 如果此时 *NEXT_ACTIVE_FORM* 是 None, 主循环会退出. *NEXT_ACTIVE_FORM* 应该通过调用应用的 *setNextForm(formid)* 方法来设定. 这份文档在过去曾建议直接设置该属性. 虽然当前还没有立即弃用该属性的计划,不过还是要避免直接去设定它.

有 3 种 建议使用的在窗口中控制 `NEXT_ACTIVE_FORM` 的机制.

1.所有用 NPSAppManaged 注册的窗口里面那些 *没有* *.activate()* 特殊方法的, 其 *.afterEditing* 方法会被调用, 如果后者能有的话. 判定哪个应该是 *NEXT_ACTIVE_FORM* 逻辑应该放到这里. *NEXT_ACTIVE_FORM* 应该是通过调用应用的  *setNextForm(formid)* 方法来配置的. 如果你是希望用户来选择 ok/确认 或者 cancel/取消 按钮的话, 这是你切换屏幕的首选方法.

2.应用的 *switchForm(formid)* 方法会造成应用立即停止编辑当前窗口,并切换到指定的窗口. 依窗口的类型而定,它们相关联的退出逻辑可能也会被绕过.

3.用 NPSAppManaged 注册的窗口可能被赋予一个 *.activate()* 方法, NPSAppManaged 会调用它来代替较常用的  *.edit()* 方法. 这可以包含进一步的逻辑. 这 **不是** 最优方法, 但是却能允许有更大的灵活性. 要注意这种情况下, 除非你指明要调用, 否则通常的 .edit() 方法不会被调用. 举个栗子, 一个 .activate() 方法看着可能是这样的::

    def activate(self):
         self.edit()
         self.parentApp.setNextForm(None)

这就会导致主循环在窗口结束后会退出.

NPSAppManaged 提供的附加服务
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

下面这些方法可以在 NPSAppManaged 子类里有效重写. 默认他们什么也不做.

.. py:method:: NPSAppManaged.onInMainLoop

  在程序运行时,在每个屏幕[切换]之间被调用. 但不在第一个屏幕之前被调用.

.. py:method:: NPSAppManaged.onStart

  重写该方法可执行一切初始化任务. 如果你愿意,你可以在这里布置应用的窗口.

.. py:method:: NPSAppManaged.onCleanExit

    重写该方法以便在程序无错退出时,执行一切清理任务.

.. py:attribute:: NPSAppManaged.keypress_timeout_default

    如果配置了该项, 新窗口在创建时会将 keypress_timeout 配置成它, 只要它们知道自己所属的应用程序 - 也就是说, 它们在创建时被传递了 *parentApp=* 属性. 如果你用了 NPSAppManaged, 这些都是自动的.

.. py:method:: NPSAppManaged.while_waiting

  应用可能都还有一个 *while_waiting* 方法. 你可以自由地定义和重写这部分, 它会在应用程序等待用户输入的时候被调用(参考其他窗口里的 while_waiting 方法).

.. py:method:: NPSAppManaged._internal_while_waiting

  该方法用于 npyscreen 内部使用.

.. py:method:: NPSAppManaged.switchForm(formid)

    立即停止编辑当前窗口并切换到指定的窗口.

.. py:method:: NPSAppManaged.switchFormPrevious()

    立即切换到历史中的前一个窗口.

.. py:method:: NPSAppManaged.resetHistory

    遗忘之前访问过的窗口[重置历史记录].

.. py:method:: NPSAppManaged.getHistory

    获取之前访问过的窗口的列表.


这个类管理的窗口的方法和属性
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

为 NPSAppManaged 所调用的窗口可提供的方法

.. py:method:: Form.beforeEditing()

    在窗口的编辑循环被调用之前调用.

.. py:method:: Form.afterEditing()

    窗口退出时被调用.

.. py:method:: Form.activate()

    该方法的存在会完全覆盖已有的 .beforeEditing .edit 和 afterEditing 方法.


.. py:attribute::parentApp

    由 NPSAppManaged 类创建的窗口会有一个 `parentApp` 属性, 这是个回溯到控制它们的应用的引用.





其他应用类
==========


.. py:class::  NPSApp

要用 NPSApp 要将它子类化, 然后给出你自己的 `.main()` 定义. 当你准备好调用 `.run()` 运行应用程序的时候, 你的主循环就会被执行.

虽然它提供了尽可能大的灵活性, 但是 NPSApp 几乎在其他各方面都次于 NPSAppManaged. 别在新项目中使用它, 要把它当成只在内部使用的基类.
