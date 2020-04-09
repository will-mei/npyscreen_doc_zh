控件：带标题的控件
***********************

大多数标准控件版本有两种形式 - 一个基础版本和一个相应版本，后者也打印一个带控件名称的标签。例如，Textfield和TitleText。

标题版本实际上是一个包含控件的装饰器，而不是成为一个对它们本身合适的控件，并且会在修改它们行为时造成混乱。

In general, to create your own version of these widgets, you should first create the contained widget, and then create a titled version.
通常情况下，为了创建自己的这些控件版本，你首先应该创建包含控件，然后创建一个标题版本。

例如::

	class NewTextWidget(textbox.Textfield):
		# 这个类的所有自定义代码
		# 应在这里


	class TitleProductSearch(TitleText):
		_entry_type = NewTextWidget

你可以通过将参数 *begin_entry_at* 传递给构造函数来调整子控件在屏幕上的位置。默认值是16。你也可以通过在创建控件时传递参数 *use_two_lines=True|False* 来覆盖是否使用单独行做标题的控件。默认的 *use_two_lines=None* 将保持标题和包含控件在同一行，除非标签太长。

你可以在创建时使用参数 *labelColor='LABEL'* 来改变标签颜色。你可以从你正在使用的主题中指定任何颜色名称。

创建之后，由TitleWidget管理的两个控件可以通过对象的 *label_widget* 和 *entry_widget* 属性来访问。


带标题的多行控件
++++++++++++++++++++++++

如果你正在创建带标题的多行控件版本，你将发现最好的方法是从类 `TitleMultiLine` 继承，它封装了更多的多行功能


控件：框控件
********************

这些控件以一种与带标题的控件版本类似的方式工作。box控件包括另一个类的控件。


BoxBasic
	 BoxBasic 在屏幕上打印一个带可选名称和页脚的框。它是为了作为一个深一层控件的基类，不是直接使用。

BoxTitle
		BoxTitle是Title控件和多行控件的混合物。此外，它的主要目的是作为更复杂布局的基类。这个类有一个 `_contained_widget` 属性，它在创建时将控件放入框中。在Boxtitle类，这是一个多行控件。控件的标题可以传递给参数 `name=....` 的 `__init__`。另一个周长 `footer=...` 给页脚框的文本。这些对应的属性命名为 `name` 和 `footer`，可以随时更改。

		属性 `entry_widget` 提供对包含控件的直接访问。

		属性 `editable`、`values` 和 `value` 提供对 `entry_widget` 属性的直接访问。

	这个控件的构造函数可以传递给参数 `contained_widget_arguments`。这个应是一个参数字典，在entry_widget创建时将被传递。注意，此时没有对该字典进行完整性检查。（4.8.0版本新增）

你可以用与新的标题控件相同的方式来创建这些控件自己的版本。首先创建包含控件，然后创建box类封装类::

	class NewMultiLineClass
		# 在这里做巧妙的事情！
		# ....

	 class BoxTitle(BoxBasic):
	     _contained_widget = NewMultiLineClass
