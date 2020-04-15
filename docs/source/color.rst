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


控件如何使用颜色
**********************

当一个控件被绘制时，它要求有效的ThemeManager去告诉它适当的颜色。例如，'LABEL'，是一个给予颜色的标签，将用于控件的标签。主题管理器在它的 *default_colors* 字典中查找相关名称，并且返回合适的colour-pair作为curses属性，该属性随后用于在屏幕上绘制控件。

单个控件往往有自己的 *color* 属性（可能由构造函数设置）。这是通常设置为 'DEFAULT'，但可以更改为任何其他定义的名称。这种机制很典型地仅仅允许单个控件更改其颜色方案的某个特定部分。

标题... 控件版本也定义了属性 *labelColor*，它可以用于改变他们标签颜色的风格


自定义颜色（强烈反对）
***********************************************

在某些终端上，可以自定义颜色值。txvt/urxvt是这样一种终端。从版本4.8.4开始，theme manager类内置了对此的支持。  

类变量 color_values 将在类被初始化来重新自定义颜色值时被使用::

	_color_values = (
			# 重新定义一种标准颜色
	        (curses.COLOR_GREEN, (150,250,100)),
			# 定义另一种颜色
			(70, (150,250,100)),
	    )

NB. 当前的npyscreen版本在应用程序退出时没有尝试重置这些值

使用这些设备是被阻止的，因为准确地判断一个终端是否确实支持自定义颜色是不可能的。该功能是根据用户请求添加的，为了支持定制的应用程序。
