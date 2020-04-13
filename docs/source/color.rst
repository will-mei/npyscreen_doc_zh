对颜色的支持
==================

.. _color_reference:

设置颜色
*****************

所有的标准控件完全可以在黑白终端上显示。然而，目前这是一个多彩的世界，npyscreen让你显示你的控件，当然，如果不是Technicolor(TM)，并且尽可能允许接近curses。

颜色由ThemeManager类来处理。一般来说，你的应用程序应坚持使用ThemeManager，你应使用 *setTheme(ThemeManager)* 函数来设置它。所以举个例子::

    npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)

任何由npyscreen定义的默认主题将通过npyscreen.Themes访问。

一个基础主题看起来像这样::

    class DefaultTheme(npyscreen.ThemeManager):
        default_colors = {
        'DEFAULT'     : 'WHITE_BLACK',
        'FORMDEFAULT' : 'WHITE_BLACK',
        'NO_EDIT'     : 'BLUE_BLACK',
        'STANDOUT'    : 'CYAN_BLACK',
        'CURSOR'      : 'WHITE_BLACK',
        'CURSOR_INVERSE': 'BLACK_WHITE',
        'LABEL'       : 'GREEN_BLACK',
        'LABELBOLD'   : 'WHITE_BLACK',
        'CONTROL'     : 'YELLOW_BLACK',
        'IMPORTANT'   : 'GREEN_BLACK',
        'SAFE'        : 'GREEN_BLACK',
        'WARNING'     : 'YELLOW_BLACK',
        'DANGER'      : 'RED_BLACK',
        'CRITICAL'    : 'BLACK_RED',
        'GOOD'        : 'GREEN_BLACK',
        'GOODHL'      : 'GREEN_BLACK',
        'VERYGOOD'    : 'BLACK_GREEN',
        'CAUTION'     : 'YELLOW_BLACK',
        'CAUTIONHL'   : 'BLACK_YELLOW',
        }

颜色 - 例如WHITE_BLACK("黑底白字") - 是在ThemeManager类的 *initialize_pairs* 方法中定义的::

    ('BLACK_WHITE',      curses.COLOR_BLACK,      curses.COLOR_WHITE),
     ('BLUE_BLACK',       curses.COLOR_BLUE,       curses.COLOR_BLACK),
     ('CYAN_BLACK',       curses.COLOR_CYAN,       curses.COLOR_BLACK),
     ('GREEN_BLACK',      curses.COLOR_GREEN,      curses.COLOR_BLACK),
     ('MAGENTA_BLACK',    curses.COLOR_MAGENTA,    curses.COLOR_BLACK),
     ('RED_BLACK',        curses.COLOR_RED,        curses.COLOR_BLACK),
     ('YELLOW_BLACK',     curses.COLOR_YELLOW,     curses.COLOR_BLACK),
    )

('WHITE_BLACK' 总是明确的。)    

如果你发现你需要更多类，把ThemeManager归为子类并且改变类属性 *_colours_to_define*。你可以使用除了标准curses颜色的其他颜色，但由于不是所有终端都支持这样做，npyscreen不默认这样。

如果你想禁用应用程序中的所有颜色，npyscreen定义了两个方便的函数: *disableColor()* 和 *enableColor()*。


How Widgets use colour
**********************

When a widget is being drawn, it asks the active ThemeManager to tell it appropriate colours.  'LABEL', for example, is a label given to colours that will be used for the labels of widgets.  The Theme manager looks up the relevant name in its *default_colors* dictionary and returns the appropriate colour-pair as an curses attribute that is then used to draw the widget on the screen.

Individual widgets often have *color* attribute of their own (which may be set by the constructor).  This is usually set to 'DEFAULT', but could be changed to any other defined name.  This mechanism typically only allows individual widgets to have one particular part of their colour-scheme changed.

Title... versions of widgets also define the attribute *labelColor*, which can be used to change the colour of their label colour.


Defining custom colours (strongly discouraged)
***********************************************

On some terminals, it is possible to define custom colour values.  rxvt/urxvt is one such terminal.  From version 4.8.4 onwards, support for this is built in
to theme manager classes.  

The class variable color_values will be used when the class is initialized to redefine custom colour values::

	_color_values = (
			# redefining a standard color
	        (curses.COLOR_GREEN, (150,250,100)),
			# defining another color
			(70, (150,250,100)),
	    )

NB. Current versions of npyscreen make no effort to reset these values when the application exits.

Use of this facility is discouraged, because it is impossible to tell reliably whether or not a terminal actually supports custom colours.  This feature was added at user request to support a custom application.
