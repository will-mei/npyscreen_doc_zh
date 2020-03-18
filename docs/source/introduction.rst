npyscreen简介
=============

*'甩开其他维度的脏活,专心写好界面'*

项目目标
--------

npyscreen 是一个用于编写命令行终端和控制台程序的 python 的部件库和应用程序框架.它构建于标准库中的 ncurses 库之上.

如果询问用户给出信息可以变得简单一点那该有多好啊? 简单的就像这样::


	MyForm = Form()

	usrn_box = MyForm.add_widget(TitleText, name="Your name:")
	internet = MyForm.add_widget(TitleText, name="Your favourite internet page:")

	MyForm.edit()

	# usrn_box.value and internet.value now hold the user's answers.

要是你也这么想, 这个软件库很适合你.


代码示例
--------

.. image:: screen-capture.png
	:align: center


这里是一个简单的,单屏幕的应用程序的例子.  更多其他的高级应用将会用到 NPSAppManaged 框架::

	#!/usr/bin/env python
	# encoding: utf-8

	import npyscreen
	class TestApp(npyscreen.NPSApp):
	    def main(self):
	        # 这几行代码会创建一个窗口并放上控件.
	        # 一个挺复杂的窗口只花了 8 行代码 - 一行一个控件.
	        F  = npyscreen.Form(name = "Welcome to Npyscreen",)
	        t  = F.add(npyscreen.TitleText, name = "Text:",)
	        fn = F.add(npyscreen.TitleFilename, name = "Filename:")
	        fn2 = F.add(npyscreen.TitleFilenameCombo, name="Filename2:")
	        dt = F.add(npyscreen.TitleDateCombo, name = "Date:")
	        s  = F.add(npyscreen.TitleSlider, out_of=12, name = "Slider")
	        ml = F.add(npyscreen.MultiLineEdit,
	               value = """try typing here!\nMutiline text, press ^R to reformat.\n""",
	               max_height=5, rely=9)
	        ms = F.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One",
	                values = ["Option1","Option2","Option3"], scroll_exit=True)
	        ms2= F.add(npyscreen.TitleMultiSelect, max_height =-2, value = [1,], name="Pick Several",
	                values = ["Option1","Option2","Option3"], scroll_exit=True)

	        # This lets the user interact with the Form.
	        F.edit()

	        print(ms.get_selected_objects())

	if __name__ == "__main__":
	    App = TestApp()
	    App.run()






优势
----

这个框架应该足够强大到能用来创建所有从快捷,简便的小程序,到复杂的多屏幕的应用程序.它被设计成可快速完成简单任务,并大幅度减轻编写大型程序的负担.

它拥有种类非常丰富的默认控件 - 从简单的文本字段到更复杂的树和网格视图,应有尽有.

这个库的关注点一直是提供一个快速的开发控制台程序方法.通常给屏幕增加个控件就只需一行.

不足
----

在2.0pre88 版本中引进了窗体随终端大小自动调整的能力.而之前的版本都一直假定使用固定大小的终端.

兼容性
------

当前版本是在 python3 下完成的,但是这些代码也兼容较新的 python2. 一些涉及 Unicode 的特性在 python3 下会运行的更好.

它被设计成了仅使用 python 的标准库即可运行, 只需可运行的 python (2.6或更高)和 curses 库被安装即可. Npyscreen 也因此可以运行在几乎所有的通用平台,甚至在 window 中的 Cygwin 环境下. Windows 下的另一个选择是从 http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses 直接使用 curses 的 Python库.

Python 3.4.0
------------

在python3.4.0的curses模块中有一个灾难性的bug: http://bugs.python.org/issue21088

该 bug 在 python3.4.1 中被修复,而直到 3.4.1 发布出来也没有人提醒我这件事,我不打算在 npyscreen 里发布一个的解决方案,因为我觉得坚守 python3.4.0 的人数应该很小.如果这给你带来了问题,请与我联系.



Unicode
-------

从 2.0pre47 版本开始所有的文本控件在兼容 utf-8 的终端上应该都支持 utf-8 字符显示和输入了. 这也解决了该库一个长期存在的限制, 并且也让其适合在针对 非英语用户 的项目中使用了.

自 2.0pre48 版本开始,该库即计划 在所有控件的 Unicode 处理上变得更加健壮.目前系统的还有一些地方在 utf-8/Unicode 的支持上仍需要进一步的努力.如果你碰到了的话 请向我们发送 bug 报告文档.

类似的项目
----------

你可能还会喜欢看一下 http://excess.org/urwid/

与 npyscreen 相比, urwid(二胡) 更像一个传统的事件驱动的GUI库, 主要针对其他的显示设备与光标.
