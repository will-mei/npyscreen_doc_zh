控件: 选取选项
***************

MultiLine
    向用户给出一个选项列表.(该控件可能应该可以有一个更好的名字,但是我们现在先这样吧)

    选项应该以列表形式被存在 *values* 属性中. *value* 属性保存了用户所选项目的索引. 如果你想返回实际选择的值而不是某个索引,请使用 *get_selected_objects()* 方法.

    MultiLine 及其衍生控件类的最重要的特性之一就是, 它们可以很容易的被适配用来让用户选择不同类型的对象. 要这么做,请重写 *display_value(self, vl)* 方法. 其中 *vl* 参数会是被显示的对象, 函数应该会返回一个能被显示到屏幕上的字符串.

    换句话说,你可以传入一个任意类型对象的列表. 默认,他们会被用 *str()* 来显示,但是通过重写 *display_value* 你能用任何你认为合适的方式展示它们.

    MultiLine 也会允许用户 '过滤' 条目. (绑定的按键 I, L, n, p 默认是 过滤器, 清除过虑器, 下一个和上一个). 当前的实现会高亮显示屏幕上匹配的行. 未来的版本可能会隐藏其他的行或者会给出一个选项. 你可以通过重写 filter_value 方法来控制过滤器如何进行操作. 它要接收一个索引作为参数 (用来在 .values 列表中找到某一行) 并且匹配则返回 True, 否则返回 False. 从 2.0pre74 版本开始,整个过滤系统可以通过设置 *.allow_filtering* 为 False 来禁用. 这也可以作为参数传递到构造函数中.

    MultiLine 控件是一个容器控件, 然后容纳一系列的处理各个显示部分的其他控件. 所有的多行控件类都会有一个 `_contained_widget` 类属性. 它控制控件如何被构建. 其 `_contained_widget_height` 类属性指定了给每个控件多少屏幕里的行.


TitleMultiLine
   A titled version of the MultiLine widget.

   If creating your own subclasses of MultiLine, you can create Title versions by subclassing this object and changing the *_entry_type* class variable.

MultiSelect, TitleMultiSelect,
    Offer the User a list of options, allow him or her to select more than one of them.

    The *value* attribute is a list of the indexes user's choices.  As with the MultiLine widget, the list of choices is stored in the attribue *values*.

SelectOne, TitleSelectOne
    Functionally, these are like the Multiline versions, but with a display similar to the MultiSelect widget.

MultiSelectFixed, TitleMultiSelectFixed
    These special versions of MultiSelect are intended to display data, but like Textfixed do not allow the user to actually edit it.

MultiLineAction
    A common use case for this sort of widget is to perform an action on the currently highlighted item when the user pushes Return, Space etc.  Override the method *actionHighlighted(self, act_on_this, key_press)* of this class to provide this sort of widget.  That method will be called when the user 'selects' an item (though in this case .value will not actually be set) and will be passed the item highlighted and the key the user actually pressed.

MultiSelectAction
    This is similar to the MultiLineAction widget above, except that it also provides the method *actionSelected(self, act_on_these, keypress)*.  This can be overridden, and will be called if the user pressed ';'.  The method will be passed a list of the objects selected and the keypress.  You probably want to adjust the default keybindings to make this widget useful.

BufferPager, TitleBufferPager *New in Version 2.0pre90*
    The `BufferPager` class is a subclass of the *Pager* class.  It is designed to display text to the user in much the way that `tail -f` does under \*nix.  By default, the .values attribute is set to an instance of the `collections.deque` class.  You can pass a `maxlen=` value to the constructor.  If not, the maxlen for the deque object will be taken from the class attribute `DEFAULT_MAXLEN`, which is None by default.

    .. py:method:: BufferPager.clearBuffer()

        Clear the buffer.

    .. py:method:: BufferPager.buffer(lines, scroll_end=True, scroll_if_editing=False)

        Add `lines` to the contained deque object.  If `scroll_end` is True, scroll to the end of the buffer.  If `scroll_if_editing` is True, then scroll to the end even if the user is currently editing the Pager.  If the contained deque object was created with a maximum length, then new data may cause older data to be forgotten.

MultiLineEditable
    A list of items that the user can edit, based on the multiline classes.  New in version 3.9

    .. py:method:: get_new_value()

        This method should return a 'blank' object that can be used to initialize a new item on the list.  By default it returns an
        empty string.


    .. py:method:: check_line_value(vl)

        This method should say whether vl is a valid object that can be added to the list, returning True or False.  By default, this
        method rejects empty strings.

MultiLineEditableTitle
    A titled version of MultiLineEditable. The class attribute *_entry_type* controls the type of contained widget.

MultiLineEditableBoxed
    A boxed version of MultiLineEditable. The class attribute **_entry_type** controls the type of contained widget.


Custom Multiselect Widgets
++++++++++++++++++++++++++

Multiline widgets are a container widget that then holds a series of other widgets that handle various parts of the display.  All multiline classes have a `_contained_widget` class attribute. This controls how the widget is constructed.  The class attribute `_contained_widget_height` specifies how many lines of the screen each widget should be given.

From version 3.4 onwards, contained widgets that have a `.selected` attribute are handled differently: widgets will have their `.selected` attribute set to `True` if the line is selected and `False` otherwise.  Widgets may also have their `.important` attribute set to True or False, depending on if they are included in a current filter (see above).

Widgets that do not have a `selected` attribute have the value for each line put in their `name` attribute, and whether the line is selected or not put in their `value` attribute.  This is a legacy of the fact that the standard multiselect widgets use checkboxes to display each line.

From version 4.8.7 onwards, multiline widgets use the methods `set_is_line_important`, `set_is_line_bold` and `set_is_line_cursor` to control the display of each line.  These methods are passed the widget object in question and a Boolean value.  They are intended to be overridden.
