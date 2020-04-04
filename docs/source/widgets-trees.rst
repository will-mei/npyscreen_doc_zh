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
		不赞同使用的TreeData类。NPSTreedata类是用于表示tree对象。每一个树节点，包括根节点，是一个NPRSTreeData实例。每个节点会有自己的内容，父节点或子节点。

		每个节点的内容不是在创建的时候设置，就是使用 *.set_Content* 方法设置。

		*.getContent* 返回内容。

		*.getContentForDisplay* 是控件用于显示树，这些控件期望返回一个能够给用户显示内容的字符串。你可能想重载该方法。

		*newChild(content=...)* 创建一个子节点。

		*selectable* (new in version 2.0pre70) 如果该属性为真用户可标价一个值为'selected'。这是被MLTreeMultiSelect控件使用，且默认值为True。



MultiLineTree, SelectOneTree, and MultiLineTree
		这些控件以一种和无树版本非常相似的方式来工作，除非他们希望在.values属性中包含一个NPSTree。其他主要不同点是他们的.value属性不包括所选值的索引，不过所选值索引本身。然而，这些类是弃用的，支持使用更多改进的 *MLTree* 和 *MLTreeAction* 类。


MultiLineTreeNew, MultiLineTreeNewAction
		*提供这些类仅仅是为了与旧版本兼容。新类应该使用MLTree和相关类*


		这个类的 *values* 属性必须存储一个NPSTree实例。不管怎样，如果你想，你可以重载这个类的 *convertToTree* 方法。这个方法将返回一个NPSTree实例。当 *values* 被赋值时，该函数自动被调用。


		默认情况下，这个类使用 *TreeLineAnnotated* 控件来显示树的每一行树。在派生类中，你可以通过改变类属性 *_contained_widgets* 来更改它。

MutlilineTreeNewAnnotated, MultilineTreeNewAnnotatedAction
		*提供这些类仅仅是为了与旧版本兼容。新类应该使用MLTree和相关类*

		默认情况下，这个类使用 *TreeLineAnnotated* 控件来显示树的每一行树。在派生类中，你可以通过改变类属性 *_contained_widgets* 来更改它。
