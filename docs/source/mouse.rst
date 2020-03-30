增强鼠标支持
==============
想要更细致的处理鼠标事件的控件需要重写 *.handle_mouse_event(self, mouse_event)* 方法. 注意 *mouse_event* 是一个元组::

    def handle_mouse_event(self, mouse_event):
        mouse_id, x, y, z, bstate = mouse_event # 参阅下面的提示.
        # 这里处理后续任务 ....

这个通常很有用,但是 x 和 y 都是绝对位置,而不是相对位置. 因为这个原因, 你应该利用已经提供好的便利功能来把这些值转换成与相对于控件的坐标. 这样的话,大多的鼠标处理函数都会看起来像这样::

    def handle_mouse_event(self, mouse_event):
        mouse_id, rel_x, rel_y, z, bstate = self.interpret_mouse_event(mouse_event)
        # Do things here.....

鼠标控制器只会在控件是 "可编辑" 的条件下被调用. 只有很少见的情况下,你可能会想用一个不可编辑的控件来响应鼠标事件. 那种情况下, 你可以把控件的 *.self.interested_in_mouse_even_when_not_editable* 属性设为 True.

关于鼠标事件的更多细节参见 python 标准库的 curses 模块文档.
