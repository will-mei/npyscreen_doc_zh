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
                # this function should return a list of strings.这个函数应返回字符串列表


    New in version 2.0pre83.


Button
   Functionally similar to the Checkbox widgets, but looking different.  The Button is usually used for OK and Cancel Buttons on Forms and similar things, though they should probably be replaced with the ButtonPress type.  The colour that the button is shown when selected is either an inverse of the colour of the button, or else selected by the attribute *cursor_color*.  This value can also be passed in to the constructor.  If this value is None, the inverse of the button colour will be used.

ButtonPress
    Not a toggle, but a control.  This widget has the method *whenPressed(self)*, which you should overload to do your own things.  

    From version 4.3.0 onwards, the constructor accepts an argument *when_pressed_function=None*.  If a callable is specified in this way, it will be called instead of the method *whenPressed*. NB.  The when_pressed_function functionality is potentially dangerous. It can set up a circular reference that the garbage collector will never free. If this is a risk for your program, it is best to subclass this object and override the *when_pressed_function* method instead.

FormControlCheckbox
   A common use of Checkbox is to offer the user the option to enter additional data.  For example "Enter Expiry Date".  In such a case, the Form needs to display additional fields in some cases, but not in others.  FormControlCheckbox makes this trivial.

   Two methods are defined:

   addVisibleWhenSelected(*wg*)
      *wg* should be a widget.  

      This method does not create a widget, but instead puts an existing widget under the control of the FormControlCheckbox.  If FormControlCheckbox is selected, the widget will be visible.  

      As many widgets as you wish can be added in this way.

   addInvisibleWhenSelected(*wg*)
      Widgets registered in this way are visible only when the FormControlCheckbox is not selected.

AnnotateTextboxBase, TreeLineAnnotated, TreeLineSelectableAnnotated
    The *AnnotateTextboxBase* class is mainly intended for use by the
    multiline listing widgets, for situations where each item displayed needs an
    annotation supplied to the left of the entry itself.  The API for these
    classes is slightly ugly, because these classes were originally intended for
    internal use only.  It is likely that more user-friendly versions will be
    supplied in a later release.  Classes derived from *AnnotateTextboxBase*
    should define the following:

    *ANNOTATE_WIDTH*
        This class attribute defines how much margin to leave before the
        text entry widget itself.  In the TreeLineAnnotated class the margin needed is calculated
        dynamically, and ANNOTATE_WIDTH is not needed.

    *getAnnotationAndColor*
        This function should return a tuple consisting of the string to
        display as the annotation and the name of the colour to use when displaying
        it.  The colour will be ignored on B/W displays, but should be provided in
        all cases, and the string should not be longer than *ANNOTATE_WIDTH*,
        although by default the class does not check this.

    *annotationColor*, *annotationNoColor*
        These methods draw the annotation on the screen.  If using strings
        only, these should not need overriding.  If one is altered, the other should
        be too, since npyscreen will use one if the display is configured for colour
        and the other if configured for black and white.
