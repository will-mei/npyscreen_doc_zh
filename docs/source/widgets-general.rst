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
    These versions of the Slider do not display a label.  (Similar to using the usual slider with *label=False*). New in Version 4.3.5

SliderPercent, TitleSliderPercent
    These versions of the Slider display a percentage in the label.  The number of decimal places can be set by setting the attribute *accuracy* or by passing in the keyword *accuracy* to the constructor.  Default is 2. New in Version 4.3.5.




Widgets: Grids
**************

SimpleGrid
    This offers a spreadsheet-like display.  The default is only intended to display information (in a grid of text-fields).  However, it is designed to be flexible and easy to customize to display a variety of different data.  Future versions may include new types of grids.  Note that you can control the look of the grid by specifying either *columns* or *column_width* at the time the widget is created.  It may be that in the future the other multi-line classes will be derived from this class.

    The cursor location is specified in the attribute *.edit_cell*.  Note that this follows the (odd) curses convention of specifying the row, then the column.

    *values* should be specified as a two-dimensional array.

    The convenience function *set_grid_values_from_flat_list(new_values, max_cols=None, reset_cursor=True)* takes a flat list and displays it on the grid.

    The following arguments can be passed to the constructor::

        columns = None
        column_width = None,
        col_margin=1,
        row_height = 1,
        values = None
        always_show_cursor = False
        select_whole_line = False (new in version 4.2)

    Classes derived from SimpleGrid may wish to modify the following class attributes::

        _contained_widgets    = textbox.Textfield
        default_column_number = 4  
        additional_y_offset   = 0  # additional offset to leave within the widget before the grid
        additional_x_offset   = 0  # additional offset to leave within the widget before the grid
        select_whole_line   # highlight the whole line that the cursor is on


GridColTitles
    Like the simple grid, but uses the first two lines of the display to display the column titles.  These can be provided as a *col_titles* argument at the time of construction, or by setting the *col_titles* attribute at any time.  In either case, provide a list of strings.


Customizing the appearance of individual grid cells
+++++++++++++++++++++++++++++++++++++++++++++++++++

New in version 4.8.2.

For some applications it may be desirable to customize the attributes of the contained grid widgets depending upon their content. Grid widgets call a method called `custom_print_cell(actual_cell, display_value)` after they have set the value of a cell and before the content of the cell is drawn to the screen.  The parameter `actual_cell` is the underlying widget object being used for display, while `display_value` is the object that has been set as the content of the cell (which is the output of the `display_value` method).

The following code demonstrates how to use this facility to adjust the color of the text displayed in a grid. My thanks are due to Johan Lundstrom for suggesting this feature::


    class MyGrid(npyscreen.GridColTitles):
        # You need to override custom_print_cell to manipulate how
        # a cell is printed. In this example we change the color of the
        # text depending on the string value of cell.
        def custom_print_cell(self, actual_cell, cell_display_value):
            if cell_display_value == 'FAIL':
               actual_cell.color = 'DANGER'
            elif cell_display_value == 'PASS':
               actual_cell.color = 'GOOD'
            else:
               actual_cell.color = 'DEFAULT'

    def myFunction(*args):
        # making an example Form
        F = npyscreen.Form(name='Example viewer')
        myFW = F.add(npyscreen.TitleText)
        gd = F.add(MyGrid)

        # Adding values to the Grid, this code just randomly
        # fills a 2 x 4 grid with random PASS/FAIL strings.
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



Widgets: Other Controls
***********************

Checkbox, RoundCheckBox
   These offer a single option - the label is generated from the attribute *name*, as for titled widgets.  The attribute *value* is either true or false.

   The function whenToggled(self) is called when the user toggles the state of the checkbox.  You can overload it.

CheckboxBare
    This has no label, and is only useful in special circumstances.  It was added at user request.

CheckBoxMultiline, RoundCheckBoxMultiline
    This widgets allow the label of the checkbox to be more than one line long.  The name of the widget should be specified as a
    list or tuple of strings.

    To use these widgets as part of a multiline widget, do the following::

        class MultiSelectWidgetOfSomeKind(npyscreen.MultiSelect):
            _contained_widgets = npyscreen.CheckBoxMultiline
            _contained_widget_height = 2

            def display_value(self, vl):
                # this function should return a list of strings.


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
