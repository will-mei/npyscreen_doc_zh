编写更复杂的表单
==========================

终端应用程序的一个非常典型的编程风格是有一个带命令行的屏幕，通常显示在屏幕底部，然后一些列表控件或其他显示占用了大部分屏幕顶部的标题栏和状态栏上方的命令行。在这个模式上的变化在像Mutt、less、Vim、irssi等应用程序中可以找到。

为了让编写这些类型的表单更容易，npyscreen提供一系列能够协同工作的类。

FormMuttActive, FormMuttActiveWithMenus, FormMuttActiveTraditional, FormMuttActiveTraditionalWithMenus
    这些类定义了基本表单。以下 *class attribute* 明确指定了表单如何工作::

            MAIN_WIDGET_CLASS   = wgmultiline.MultiLine
            MAIN_WIDGET_CLASS_START_LINE = 1
            STATUS_WIDGET_CLASS = wgtextbox.Textfield
            STATUS_WIDGET_X_OFFSET = 0
            COMMAND_WIDGET_CLASS= wgtextbox.Textfield
            COMMAND_WIDGET_NAME = None
            COMMAND_WIDGET_BEGIN_ENTRY_AT = None
            COMMAND_ALLOW_OVERRIDE_BEGIN_ENTRY_AT = True

            DATA_CONTROLER    = npysNPSFilteredData.NPSFilteredDataList

            ACTION_CONTROLLER  = ActionControllerSimple

    默认定义使以下实例属性在初始化后可用::

            # Widgets -
            self.wStatus1 # by default a title bar
            self.wStatus2 # just above the command line
            self.wMain    # the main area of the form - by default a MultiLine object
            self.wCommand # the command widget

            self.action_controller # not a widget. See below.

    表单的 *.value* 属性设置为一个指定对象实例DATA_CONTROLLER

    通常，应用程序希望定义属于自己的DATA_CONTROLLER和ACTION_CONTROLLER。

    传统和非传统的表单之间的区别是，传统表单的重点总是停留在命令行控件，尽管一些按键将传递到MAIN_WIDGET_CLASS - 所以，从用户角度看，看起来像他们同时在交互。

TextCommandBox
    TextCommandBox是像一个普通的文本框，只是将用户输入传递给了action_controller。另外，它可以保持命令输入历史记录。请参阅ActionControllerSimple文档，获取更多细节。

TextCommandBoxTraditional
    这个与TextCommandBox相同，不同点在于它将特定的按键传递给由 *self.linked_widget* 指定的控件。在默认情况下，任何与TextCommanBoxTraditional中处理程序不匹配的按键都将被传递给链接控件。除此之外，列表 *self.always_pass_to_linked_widget* 列出的任何按键将被链接控件处理。但是，如果当前命令行是以类属性 *BEGINNING_OF_COMMAND_LINE_CHARS* 列表中的任意字母开头，用户输入将由该类处理，而不是链接控件。

    这相当复杂，但举个例子可能会更清晰。默认的BEGINNING_OF_COMMAND_LINE_CHARS明确':'或'/'标志着命令行的开始。在那之后，按键由这个控件处理，而不是链接控件，因此向上和向下的箭头开始导航命令历史记录。但是，如果当前命令行是空的，这些键将导航到链接控件。

    与TextCommandBox控件一样，命令行的值传递给父窗体的action_controller对象。

ActionControllerSimple
    这个对象接受命令行并且执行call-back函数。

    它可识别两种类型的命令行 - 一个"live"命令行，指命令行每次更新都会执行一个动作，并且在按下返回键时执行一条命令。

    使用 *add_action(ident, function, live)* 方法添加回调。'ident'是一个正则表达式，它将与命令行相匹配，*function* 是回调本身，*live* 为真或为假，用于指定是否应该在每次按键时执行回调（假设"ident"匹配）。
    
    匹配正则表达式'ident'的命令行导致回调函数去调用以下参数：*call_back(command_line, control_widget_proxy, live=True)*。这里 *command_line* 是命令行的字符串，*control_widget_proxy* 是对命令行控件的弱引用，live指定这个函数将调用'live'还是作为一个返回结果。

    方法 *create()* 可被覆盖。当创建对象是调用它。默认不做任何事。你可能想使用它来调用 *self.add_action*。

NPSFilteredDataBase
    默认 *NPSFilteredDataBase* 类建议如何管理代码的显示可能被分隔成一个单独的对象。精确的方法将非常依赖于应用程序。这不是此类型应用程序最重要的部分，但这是把数据库访问逻辑从用户接口逻分离出来最好的实践。



Example Code示例代码
************

以下示例展示该模块如果工作。应用程序创建一个由搜索功能的ActionController。该功能调用了用户自定义函数 set_search，它与表单的父类进行通信。值（实际是NPSFilteredDataBase类）然后它使用这个类去设置wMain.values并且调用wMain.display()来更新显示。

FmSearchActive是一个简单的FormMuttActiveTraditional类，它有一个类属性，指定表单应使用我们的功能控制器::

    class ActionControllerSearch(npyscreen.ActionControllerSimple):
        def create(self):
            self.add_action('^/.*', self.set_search, True)

        def set_search(self, command_line, widget_proxy, live):
            self.parent.value.set_filter(command_line[1:])
            self.parent.wMain.values = self.parent.value.get()
            self.parent.wMain.display()


    class FmSearchActive(npyscreen.FormMuttActiveTraditional):
        ACTION_CONTROLLER = ActionControllerSearch

    class TestApp(npyscreen.NPSApp):
        def main(self):
            F = FmSearchActive()
            F.wStatus1.value = "Status Line "
            F.wStatus2.value = "Second Status Line "
            F.value.set_values([str(x) for x in range(500)])
            F.wMain.values = F.value.get()

            F.edit()


    if __name__ == "__main__":
        App = TestApp()
        App.run()
