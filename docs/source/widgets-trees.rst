控件：树和显示树
********************************


表示树的数据
++++++++++++++++++++++

TreeData
    类TreeData是被用于表示树对象。每一个树节点，包括根节点，是一个NPSTreeData实例。每个节点可能有它自己的内容，父节点或子节点。

    每个节点的内容不是在创建的时候设置，就是使用 *.set_content* 方法设置。

    *get_content()* 返回该内容。

    *get_content_for_display()* 是控件用于显示树，这些控件期望返回一个能够给用户显示内容的字符串。

    *new_child(content=...)* 创建一个新的子节点

    *selectable* 如果这个属性为真，则用户可以标记一个值为'selected'。这被MLTreeMultiSelect控件使用，并且默认值为True。

    *ignore_root* 这个属性控制着是否向用户展示树的根节点。

    *expanded* 这个属性控制着是否扩展树的分支，假设该节点有任何子节点。

    *sort* 这个属性控制是否对树进行排序。

    *sort_function* 如果树已排序，当树显示时，将使用此属性中命名的函数作为对树排序的键。

    *walk_tree(only_expanded=True, ignore_root=True, sort=None, sort_function=None)* 遍历树。你可以覆盖标准sort和sort函数，并决定是否只遍历那些被标记为展开的树节点。


Trees
+++++

MLTree, MLTreeAction
    这个类的 *values* 属性必须存储一个NPSTree实例。尽管如此，如果你希望覆盖类的 *convertToTree* 方法。这个方法应返回一个NPSTree实例。当 *values* 被赋值时，该函数自动被调用。

    默认情况下，这个类使用 *TreeLine* 控件来显示树的每一行树。在派生类中，你可以通过改变类属性 *_contained_widgets* 来更改它。类属性 `_contained_widget_height`  定义了每个给定的控件显示多少行。

MLTreeAnnotated, MLTreeAnnotatedAction
      在默认情况下，这个类使用 *TreeLineAnnotated* 控件来显示树的每一行。在派生类中，你可以通过改变类属性 *_contained_widgets* 来更改它。

MLTreeMultiSelect
    *New in version 2.0pre70*

    这个类允许你选择树的多个项。你可以通过设置NPSTreeData节点的 *selectable* 属性来选择用户能够选择的NPSTreeData节点。

    方法 *get_selected_objects(self, return_node=True,)* 返回一个列出被选中节点的生成器对象。如果return_node时True，则产生实际节点本身，否则会产生 *node.getContent()* 的值。

    *New in Version 2.0pre71* 如果属性 *select_cascades* 为True(可通过创建时传递参数 *select_cascades* 或者后续直接设置属性来设置)，则选择节点将自动选择已选中节点下任何可选节点。默认设置为True。

    所选节点的属性 *selected* 也被设置为True，因此，你可以遍历树来找到他们，如果你愿意的话。

    用于显示每一行的控件是 *TreeLineSelectable* 。

MLTreeMultiSelectAnnotated
    *New in version 2.0pre71*

    MLTreeMultiSelect类的一个版本，是使用 *TreeLineSelectableAnnotated* 作为显示控件。



弃用的Tree类
+++++++++++++++++++++++
NPSTreeData
    DEPRECATED in favour of the TreeData class.  The NPSTreeData class is used to represent tree objects.  Each node of the tree, including the root node, is an NPSTreeData instance.  Each node may have its own content, a parent or children.

    The content of each node is either set when it is created or using the *.setContent* method.

    *.getContent* returns the content.

    *.getContentForDisplay* is used by the widgets that display trees, which expect it to return a string that can be displayed to the user to represent the content.  You might want to overload this method.

    *newChild(content=...)* creates a new child node.

    *selectable* (new in version 2.0pre70) If this attribute is true the user can mark a value as 'selected'. This is used by MLTreeMultiSelect widget, and is True by default.



MultiLineTree, SelectOneTree, and MultiLineTree
    These widgets all work in a very similar way to the non-Tree versions,
    except that they expect to contain an NPSTree in their .values attribute.
    The other major difference is that their .value attribute does not contain
    the index of the selected value(s), but the selected value(s)
    itself/themselves.  However, these classes are DEPRECATED in favour of the
    much improved *MLTree* and *MLTreeAction* classes.


MultiLineTreeNew, MultiLineTreeNewAction
    *These classes are provided solely for compatibility with old code. New classes should use the MLTree and related classes*

    The *values* attribute of this class must store an NPSTree instance.
    However, if you wish you can override the method *convertToTree* of this
    class.  This method should return an NPSTree instance.  The function will be
    called automatically whenever *values* is assigned.


    By default this class uses *TreeLineAnnotated* widgets
    to display each line of the tree.  In derived classes You can change this by changing
    the class attribute *_contained_widgets*.

MutlilineTreeNewAnnotated, MultilineTreeNewAnnotatedAction
    *These classes are provided solely for compatibility with old code. New classes should use the MLTree and related classes*

    By default this class uses *TreeLineAnnotated* widgets
    to display each line of the tree.  In derived classes You can change this by changing
    the class attribute *_contained_widgets*.
