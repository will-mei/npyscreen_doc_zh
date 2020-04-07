控件：日期，滑块和组合控件
***********************************************

DateCombo, TitleDateCombo
    这些控件允许用户选择一个日期。日期的实际选择是由类MonthBox完成的，它在一个临时窗口中显示。构造函数可以被传递通过以下参数 - `allowPastDate=False` 和 `allowTodaysDate=False` - 这两者将影响用户被允许选择什么。构造函数也可以接受参数`allowClear=True`。

ComboBox, TitleCombo
    这个框看起来像一个文本框，但用户仅仅能够从选项列表中选择。如果用户想更改值，就在临时窗口中显示。就像MultiLine控件一样，属性 *value* 是列表 *values* 中一个选择的索引。通过重载 *display_value(self, vl)* 方法，ComboBox控件也可以被定制。

FilenameCombo, TitleFilenameCombo
    这展示了一个选择文件名的控件。以下参数可传递给构造函数::

        select_dir=False
        must_exist=False
        confirm_if_exists=False
        sort_by_extension=True

    这些也与控件中所示可以设置的属性相对应。


    该控件在版本 2.0pre81中被添加。



Slider, TitleSlider
   滑块表示一个水平滑动块。以下附加参数对构造函数是很有用的:

   out_of=100
      滑块的最大值。
   step=1
      用户增加或减少值得增量。
   lowest=0
      用户能选择的最小值。注意，滑块设计不允许用户选择负值。*lowest* 应当 >= 0
   label=True
      是否在滑块旁打印文本标签。如果这样，请参考 *translate_value* 方法。
   block_color = None
       显示滑块的水平块的颜色。默认情况下（None），与滑块本身颜色相同。

   所有这些选项设置了相同名称的属性，它们在控件中存在时可能随时被更改。

   在控件(如果 *label=True*)旁边显示的文本是由 *translate_value* 方法生成。它没有选项并返回一个字符串。把Slider对象划入子类并重载该方法是有意义的。确保生成固定长度的字符串可能是有意义的。因此默认代码如下::

      stri = "%s / %s" %(self.value, self.out_of)
      l = (len(str(self.out_of)))*2+4
      stri = stri.rjust(l)
      return stri

SliderNoLabel, TitleSliderNoLabel
    这些版本的滑块不显示标签。(类似于使用通常带 *label=False* 的滑块)。新版本4.3.5

SliderPercent, TitleSliderPercent
    这些版本的滑块在标签中显示百分比。通过设置属性 *accuracy* 或向构造函数传递关键字 *accuracy*，可以设置小数位数。默认是2。新版本4.3.5。




控件：网格
**************

SimpleGrid
    这提供了一种类似电子表格的显示方式。默认值仅仅用于显示信息（在文本字段的网格中）。但是，它是为了灵活且易于自定义显示各种不同数据而设计的。未来的版本可能包括新的网格类型。注意，你可以通过在创建控件时指定 *columns* 或 *column_width* 来控制网格的外观。将来可能从这个类派生出其他多行类。

    光标位置是由属性 *.edit_cell* 指定。注意，这遵循“先指定行，再指定列”的（奇数）curses约定。

    *values* 应被指定为一个二维数组。

    方便的函数 *set_grid_values_from_flat_list(new_values, max_cols=None, reset_cursor=True)* 采取一个简单列表并显示在网格中。

    以下参数可被传递给构造函数::

        columns = None
        column_width = None,
        col_margin=1,
        row_height = 1,
        values = None
        always_show_cursor = False
        select_whole_line = False (new in version 4.2)

    从SimpleGrid派生的类可能希望修改以下类属性::

        _contained_widgets    = textbox.Textfield
        default_column_number = 4  
        additional_y_offset   = 0  #在网格前留在控件内部的额外偏移量
        additional_x_offset   = 0  #在网格前留在控件内部的额外偏移量
        select_whole_line   #高亮显示游标所在的整行


GridColTitles
    像简单网格，但使用网格前两行来显示列标题。这些可在构造时作为 *col_titles* 参数提供，或者通过任意时间设置 *col_titles* 属性。在这两种情况下，提供一个字符串列表。


自定义单个网格单元的外观
+++++++++++++++++++++++++++++++++++++++++++++++++++

新版本4.8.2

对某些应用程序，最为理想的是自定义属性，那些包含依赖于他们内容的网格控件。网格控件在设置单元格的值之后，在单元格内容被绘制在屏幕上之前，调用一个名为 `custom_print_cell(actual_cell, display_value)` 的方法。参数 `actual_cell` 是用于显示底部控件对象，而 `display_value` 是被设置为单元格内容的对象（它是 `display_value` 方法的输出）。

以下代码演示如何使用这个工具来调整网格中显示的文本颜色。特别感谢Johan Lundstrom提出的这个特点::


    class MyGrid(npyscreen.GridColTitles):
        # 你需要覆盖custom_print_cell来操作如果打印单元格。在本例中，我们根据单元格的字符串值更改文本颜色
        def custom_print_cell(self, actual_cell, cell_display_value):
            if cell_display_value == 'FAIL':
               actual_cell.color = 'DANGER'
            elif cell_display_value == 'PASS':
               actual_cell.color = 'GOOD'
            else:
               actual_cell.color = 'DEFAULT'

    def myFunction(*args):
        # 制作一个实例表单
        F = npyscreen.Form(name='Example viewer')
        myFW = F.add(npyscreen.TitleText)
        gd = F.add(MyGrid)

        # 给网格添加值，这段代码只是通过任意PASS/FAIL字符串填充一个2 x 4网格
        gd.values = []
        for x in range(2):
            row = []
            for y in range(4):
                if bool(random.getrandbits(1)):
                    row.append("PASS")
                else:
                    row.append("FAIL")
            gd.values.append(row)
        F.edit()

    if __name__ == '__main__':
        npyscreen.wrapper_basic(myFunction)



控件：其他控件
***********************

Checkbox, RoundCheckBox
   这些提供一个单独选项 - 该标签是由属性 *name* 生成，作为标题控件。属性 *value* 为真或为假。

   当用户切换到复选框时，调用函数whenToggled(self)。你可以重载它。

CheckboxBare
    这没有标签，并且只有在特殊情况下才有用。它是根据用户请求添加得。

CheckBoxMultiline, RoundCheckBoxMultiline
    这控件允许复选框的标签超过一行。控件的名称应指定为字符串的列表或元组。

    把这些控件作为多行控件的一部分来使用，执行以下代码::

        class MultiSelectWidgetOfSomeKind(npyscreen.MultiSelect):
            _contained_widgets = npyscreen.CheckBoxMultiline
            _contained_widget_height = 2

            def display_value(self, vl):
                # 这个函数应返回字符串列表


    新版本2.0pre83。


Button
   功能上与复选框控件相似，但看起来不相同。 按钮通常用在表单和相似内容上的OK和Cancel按钮，尽管它们可能应被ButtonPress类型替代。按钮被选中时的颜色要么与按钮的颜色相反，要么通过属性 *cursor_color* 来选择。这个值也可传递给构造函数。如果这个值是None,将使用按钮颜色的相反值。

ButtonPress  
    不是一个触发器，仅仅一个控件。这个控件由方法 *whenPressed(self)*，该方法你应该重载来做你自己的事情。

    从版本4.3.0开始，该构造函数接受一个参数 *when_pressed_function=None*。如果以这个方式指定一个callable，它将被调用，而不是方法 *whenPressed*. NB. when_pressed_function功能上有潜在危险。它能设置一个循环引用，该垃圾收集器将永远不会释放。如果这对你的程序存在风险，最好把这个对象设置为子类，并且重载 *when_pressed_function*方法来替代。

FormControlCheckbox
   复选框的一般用法是为用户提供输入额外数据的选项。例如 "输入有效期"。在这种情况下，表单在某些情况下需要显示额外字段，但在其他情况下则不需要。FormControlCheckbox使这变得很简单。

   定义两种方法:

   addVisibleWhenSelected(*wg*)
      *wg* 应是一个控件

      这个方法不创建一个控件，而是将现有控件置于FormControlCheckbox的控制之下。如果已选择FormControlCheckbox，该控件就是可见的。

      通过这种方式按照你的意愿添加许多控件。

   addInvisibleWhenSelected(*wg*)
      只有在FormControlCheckbox没被选择时，以这种方式注册的控件才是可见的。

AnnotateTextboxBase, TreeLineAnnotated, TreeLineSelectableAnnotated
    *AnnotateTextboxBase* 类主要是为了给多行列表控件使用，用于显示的每一项都需要在选项本身左侧提供注释的情况。这些类的API有些难看，因为这些类最初只用于内部管理。在以后的本本中可能会提供更友好的版本。派生自 *AnnotateTextboxBase* 的类应定义以下内容:

    *ANNOTATE_WIDTH*
        这个类属性定义了在文本输入控件本身之前按需要留出多少边距。在TreeLineAnnotated类中，边距需要动态计算，且不需要ANNOTATE_WIDTH。

    *getAnnotationAndColor*
        这个函数应返回一个元组，该元组由作为注释显示的字符串和显示时使用颜色名字组成。在B/W显示器上，颜色会被忽略，但在所有情况下都应提供，并且字符串长度应不超过 *ANNOTATE_WIDTH*，尽管默认情况下该类不检查这个。

    *annotationColor*, *annotationNoColor*
        这些方法在屏幕上绘制注释。如果仅使用字符串，这些应不需要覆盖。如果其中一个被更改，另一个也应改变，因为npyscreen将使用一个的显示被配置为彩色，且另一个为黑白色。
