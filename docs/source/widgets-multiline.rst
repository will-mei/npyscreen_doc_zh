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
   一个带标题版的 MultiLine.

   如果要创建自己的 MultiLine 的子类, 你可以子类化该对象然后修改类的 *_entry_type* 变量就能创出一个带标题的版本了.

MultiSelect, TitleMultiSelect,
    向用户给出一个选项的列表, 允许他/她选择其中的多个.

    其 *value* 属性是一个用户所选项的索引的列表. 与 MultiLine 控件一样,选项的列表存放在 *values* 属性中.

SelectOne, TitleSelectOne
    功能上,这些类跟 MultiLine 版本的差不多,但是显示的跟 MultiSelect 控件更相似.

MultiSelectFixed, TitleMultiSelectFixed
    这些 MultiSelect 特殊版本其实是用来显示数据的, 但是像 Textfixed 一样,不允许用户去实际编辑它们.

MultiLineAction
    这种控件的一个常见的使用场景就是, 在用户按下回车,空格等键时, 对当前高亮的条目执行一个动作. 重写该类的  *actionHighlighted(self, act_on_this, key_press)* 方法即可做出这种控件. 此方法会在用户 '选中' 一个条目时被调用(虽然这种情况下 .value 还没被实际设定),并且被传进来高亮条目以及用户实际按下的键.

MultiSelectAction
    这个跟上面的 MultiLineAction 控件类似, 不过它还提供 *actionSelected(self, act_on_these, keypress)* 方法. 这个可以被重写, 且如果用户按下';'(分号)键它会被调用. 这个函数会收到被选择的对象的列表和按下的键. 你或许会想调整它默认的按键绑定让它更好用.

BufferPager, TitleBufferPager *2.0pre90 版本新增*
    `BufferPager` 类似是 *Pager* 类的一个子类. 它被设计用来把文本以非常类似于在 \*nix 环境下 tail -f 的方式显示给用户. 默认 .value 属性被设为一个 `collections.deque` [双向队列]类的实例. 你可以传递 `maxlen=` 到其构造函数. 否则, deque 对象的 maxlen[最大长度] 会从 `DEFAULT_MAXLEN` 类属性中获取, 而它默认是 None.

    .. py:method:: BufferPager.clearBuffer()

        清空缓存.

    .. py:method:: BufferPager.buffer(lines, scroll_end=True, scroll_if_editing=False)

        将 `lines` 添加到所包含的双向队列对象中. 如果 `scroll_end` 为 True, 则滚动到缓冲区的结尾. 如果 `scroll_if_editing` 为 True, 那么即使用户当前正在编辑页面控件也会滚动到末尾. 如果包含的双向队列对象在创建时被指定了最大长度, 那么新数据可能会导致较旧数据被遗忘.

MultiLineEditable
    一个用户可以编辑的选项列表,基于多行控件类. 3.9 版本新增.

    .. py:method:: get_new_value()

        这个方法会返回一个'空白'对象, 它可以用来初始化列表中的新选项. 默认它返回一个空字符串.


    .. py:method:: check_line_value(vl)

        这个方法会说明 vl 是否是一个可以被添加到列表的有效对象, 返回 True 或 False. 默认该方法拒绝空字符串.

MultiLineEditableTitle
    标题版的 MultiLineEditable. 其 *_entry_type* 类属性控制着容纳的控件的类型.

MultiLineEditableBoxed
    带框版的 MultiLineEditable. 其 *_entry_type* 类属性控制着容纳的控件的类型.


自定义多选控件
++++++++++++++++++++++++++

多行控件是一个容器控件,它容纳一系列用于处理各显示部分的其他控件. 所有的多行控件类都有一个 `_contained_widget` 类属性. 这个控制控件如何被构造. `_contained_widget_height` 指定了应该给各个控件多少屏幕上的行.

从 3.4 版本以后, 内含的带有 `.selected` 属性的控件的处理有些不同了: 若行被选中,则把它们的 `.selected` 属性设置为 `True` ,否则为 `False`. 控件的 `.important` 属性可能也会被设置为 True 或 False, 取决于他们是否被当前的 filter 所包含(参见上面).

没有 `selected` 属性的控件,每一行的值都会被放到 `name` 属性中, 且不论行是否被选中都放到它们的 `value` 属性中. 这是个遗留问题, 因为实际上标准的多选控件是用多个选框[checkboxes]来显示每一行的.

从 4.8.7 版本以后,多行控件都开始使用 `set_is_line_important`, `set_is_line_bold` 和 `set_is_line_cursor` 方法来控制每行的显示. 这些方法会被传递进待选择的控件对象和一个布尔值. 它们都是用来被重写的.
