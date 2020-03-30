控件: 显示文本
***************

Textfield, TitleText
    一个单行的文本,不过长度是任意的 - 是最基本的输入控件. 注意,一些在更正中的文档版本指的会是 'textbox' [文本框]控件.

FixedText, TitleFixedText
    单行的文本, 但其文本框的编辑功能被移除了.

PasswordEntry, TitlePassword
    一个文本框, 但被修改了, 以便刚好 *.value* 的字母不显示出来.

Autocomplete
    这是一个带有附加功能的文本框 - 我们的想法是如果用户按下了 TAB键 控件会尝试 '补全' 用户正在输入的内容,适当给出可选择的选项. 其调用的方法是 `auto_complete(inputch)`.

    当然,上下文就是一切. *Autocomplete* 也因此没那么有用,但其用意是做为你可以子类化的东西. 参见 Filename 和 TitleFilename 这两个类作为例子.

Filename, TitleFilename
    一个会尝试 '补全' 用户输入的文件名或者路径的文本框.

    这是个 *Autocomplete* 控件的示例.

FilenameCombo, TitleFilenameCombo
    这是更高级的选择文件的方法. 2.0pre82 版本新添.


MultiLineEdit
    该控件可允许用户编辑若干行的文本.

Pager, TitlePager
    该[页面]控件会显示多行文本, 并允许用户来回滚动, 但不能编辑. 要显示的文本存放在 `.values` 属性中.


细节
+++++

.. py:class:: Textbox

    .. py:method:: display_value(vl)

        控制 `.value` 属性的值如何显示. 由于各自版本的文本控件都要用在其他混合控件里(比如大多数的多行控件类), 该方法通常会被重写.

    .. py:method:: show_brief_message

        发出蜂鸣并显示一个简短的信息给用户. 通常来说会有更好的方式来做这个, 但这个有时候也会有用, 比如在 Autocomplete 类显示错误的时候.
