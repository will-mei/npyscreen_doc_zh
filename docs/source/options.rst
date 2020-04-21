应用支持
===================

选项和选项列表
************************

一个常见问题就是显示一个选项列表给用户.  在简单应用中, 为了这个目的可能会用一个自定义设计的窗口, 但是很多任务中自动生成的窗口会更合适.  一个支持该特性的 *实验性的* 系统在 2.0pre84 版本被引入.

这个系统的核心是 *Option* 对象的概念. 这些对象根据它们的类型,要么存放单一值,要么存放值列表, 同时与待定选项相关的所有文档应该也会展示给用户. 选项对象是用下面的参数创建的: *OptionType(name, value=None, documentation=None, short_explanation=None, option_widget_keywords = None, default = None)*. *short_explanation* 参数当前还没有在默认控件中使用, 但是会在未来的版本中被使用. 选项对象被设计成可让用户从也可能是由 *choices* 参数创建的有限的选项中进行选择.

所有的选项类也都有 DEFAULT 和 WIDGET_TO_USE 类属性. 如果默认值还没被定义的话,前者会定义默认值. 第二个定义了让用户来调节待定选项的控件的类.

下面是当前版本定义的选项类: `OptionFreeText`, `OptionSingleChoice`, `OptionMultiChoice`, `OptionMultiFreeList`, `OptionBoolean`, `OptionFilename`, `OptionDate`, `OptionMultiFreeText`. 存到 option 对象的值都应该用 *set(value)* 方法设定, 用 *get()* 方法获取. 所有的选项类也都定义了一个可被重写的 *when_set* 方法, 而它会在值被修改之后调用. 允许用户从一系列的有限项作选择的选项类还有 *setChoices(choices)* 和 *getChoices* 方法.

选项列表可以使用 *OptionListDisplay* 控件来显示. 它接收选项列表当作其 *OptionListDisplay* 属性的值. 如果某个选项被选中, 一个给用户显示文档(如果有的话)的窗口会展示给用户并让用户改变它的值.

选项集合可以用一个 *OptionList* 对象合在一起. *OptionList* 类有一个 *options* 属性. 它只是一个列表, 选项对象可能被被加进来. 未来的版本可能会定义一个不一样的API. *OptionList* 对象的目的帮助保存和恢复选项集合到文件中的. 这些文件的格式是一个自定义的文本格式, 类似于标准的 Unix 文件, 但是可以存储和恢复字符串列表 (使用 tab[制表符] 作为分隔符). 这个格式还在演进,并可能未来的版本中被改变. 只有和默认值不同的值会被存下来.

*OptionList* 对象的创建可以带 *filename* 参数, 它有 *write_to_file(fn=None)* 和 *reload_from_file(fn=None)* 方法.

*SimpleOptionForm* 类是一个设计用来展示这些元素如何运作的窗口. *OptionListDisplay* 控件作为一个名为 *wOptionList* 的属性被创建.

示例 代码
************

下面简短的 demo 程序会在调用中存储选定的选项到文件 '/tmp/test' ::

	#!/usr/bin/env python
	# encoding: utf-8

	import npyscreen
	class TestApp(npyscreen.NPSApp):
	    def main(self):
	        Options = npyscreen.OptionList()

	        # 为了方便让我们不用不停的写 Options.options
	        options = Options.options

	        options.append(npyscreen.OptionFreeText('FreeText', value='', documentation="This is some documentation."))
	        options.append(npyscreen.OptionMultiChoice('Multichoice', choices=['Choice 1', 'Choice 2', 'Choice 3']))
	        options.append(npyscreen.OptionFilename('Filename', ))
	        options.append(npyscreen.OptionDate('Date', ))
	        options.append(npyscreen.OptionMultiFreeText('Multiline Text', value=''))
	        options.append(npyscreen.OptionMultiFreeList('Multiline List'))

			try:
	        	Options.reload_from_file('/tmp/test')
    		except FileNotFoundError:
				pass

	        F  = npyscreen.Form(name = "Welcome to Npyscreen",)

	        ms = F.add(npyscreen.OptionListDisplay, name="Option List",
	                values = options,
	                scroll_exit=True,
	                max_height=None)

	        F.edit()

	        Options.write_to_file('/tmp/test')

	if __name__ == "__main__":
	    App = TestApp()
	    App.run()
