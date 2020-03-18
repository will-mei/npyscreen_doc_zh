创建npyscreen应用程序
=====================

对象概览
--------

Npyscreen 应用程序是由3种主要类型的对象构建出来的.

Form Objects 窗口
    窗体对象(通常是整个终端的大小,但有时大一些或者 -用于菜单之类的时候会小一些)可以提供出一个区域容纳其他控件.它们可能提供一些额外功能,比如菜单的控制系统,或是在当用户选择"ok"按钮时启动的协程.它们可能还会定义一些在用户按键间隙,或是用户在窗口中移动时要进行的操作.

Widget Objects 控件
    这些是窗体上独立的控制部件, -文本框,标签,滚动条等等.

Application Objects 应用
    这些对象提供一种更方便的管理你的应用程序运行的方式. 虽然有时也能不用应用对象来写一些简单的应用,但不建议这样. 讲道理,应用对象在多屏幕应用的管理上更不容易出错(在那些随时让应用崩溃的bug上). 另外,使用这些对象让你能利用 npyscreen 开发好的高级特性.

给急性子的程序结构
-------------------

大多数新应用程序看起来都像下面这样::

    import npyscreen

    # 这里应用充当了 curses 初始化封装器的角色
    # 同时也管理着应用的实际形态.

    class MyTestApp(npyscreen.NPSAppManaged):
        def onStart(self):
            self.registerForm("MAIN", MainForm())

    # 这个窗口类定义了展示给用户的显示内容.

    class MainForm(npyscreen.Form):
        def create(self):
            self.add(npyscreen.TitleText, name = "Text:", value= "Hellow World!" )

        def afterEditing(self):
            self.parentApp.setNextForm(None)

    if __name__ == '__main__':
        TA = MyTestApp()
        TA.run()


应用程序结构细节(教程)
----------------------

第一次使用的用户可能会对上面的代码比较困惑. 要是这样,下面的教程就来详细解释一个npyscreen程序的结构.哪怕你很不了解底层的curses系统,你也应该可以跟上我们的节奏.

窗体, 控件和应用
****************

使用封装器
+++++++++++
切换到和切出 curses 环境是个非常枯燥的任务. python 的 curses 模块提供了一个封装器来完成这些. 这在 npyscreen 中以 wrapper_basic 向外暴露. 一个很简单的应用程序的基本框架看起来应该是这样的::

    import npyscreen

    def myFunction(*args):
        pass

    if __name__ == '__main__':
        npyscreen.wrapper_basic(myFunction)
        print( "Blink and you missed it!" )


没啥复杂的. curses 环境启动并且啥也没干就退出了.但这只是一个开始.

注意, npyscreen 还提供其他封装器来完成一些稍有不同的东西.


使用窗体
++++++++

现在我们来放点东西到屏幕上.为此我们需要一个 *Form* 实例::

    F = npyscreen.Form(name='My Test Application')

这应该就够了,让我们把他放到封装器里面::

    import npyscreen

    def myFunction(*args):
        F = npyscreen.Form(name='My Test Application')

    if __name__ == '__main__':
        npyscreen.wrapper_basic(myFunction)
        print( "Blink and you missed it!" )

这看起来好像还是啥也没干 -- 因为我们实际还没有把窗体显示出来.  *F.display()* 可以把它放到屏幕上, 但是我们实际上是希望用户可以玩一下, 所以让我们用 F.edit() 换掉它::

    import npyscreen

    def myFunction(*args):
        F = npyscreen.Form(name='My Test Application')
        F.edit()

    if __name__ == '__main__':
        npyscreen.wrapper_basic(myFunction)
        print( "Blink and you missed it!" )


但还是没运行, 因为当你想要尝试编辑窗体的时候 npyscreen 会发现没有控件可编辑. 我们把它改正过来.

添加第一个控件
++++++++++++++

我们把一个带标题的文本框放到里面. 我们用下面的代码来做到这点::

    F.add(npyscreen.TitleText, name="First Widget")

The full code is::

    import npyscreen

    def myFunction(*args):
        F = npyscreen.Form(name='My Test Application')
        F.add(npyscreen.TitleText, name="First Widget")
        F.edit()

    if __name__ == '__main__':
        npyscreen.wrapper_basic(myFunction)
        print( "Blink and you missed it!" )

好多了! 这样我们就有了一个有应用样子的东西了. 加上3点小调整我们就可以把关闭显示的信息改成用户输的随便什么内容::

    import npyscreen

    def myFunction(*args):
        F = npyscreen.Form(name='My Test Application')
        myFW = F.add(npyscreen.TitleText, name="First Widget")   # <------- Change 1
        F.edit()
        return myFW.value   # <------- Change 2

    if __name__ == '__main__':
        print( npyscreen.wrapper_basic(myFunction) ) # <---- and change 3

让我们更加面向对象一点
+++++++++++++++++++++++

我们现在用的这个方法在简单程序上还可以. 一旦我们开始在窗体上创建大量控件,还是把那些代码收进对象里面更好.
不再过程化的用基础的 Form() 类, 让我们创建一个自己的窗口类. 我们会重写 Form 类的 *create()* 方法, 只要窗口被创建都会调用它::

    class myEmployeeForm(npyscreen.Form):
        def create(self):
            super(myEmployeeForm, self).create()  # This line is not strictly necessary: the API promises that the create method does nothing by default.
                                                  # I've ommitted it from later example code.
            self.myName        = self.add(npyscreen.TitleText, name='Name')
            self.myDepartment  = self.add(npyscreen.TitleText, name='Department')
            self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')

我们可以用前面的封装器的代码来利用这个特性::

    import npyscreen

    class myEmployeeForm(npyscreen.Form):
        def create(self):
            self.myName        = self.add(npyscreen.TitleText, name='Name')
            self.myDepartment  = self.add(npyscreen.TitleText, name='Department')
            self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')

    def myFunction(*args):
        F = myEmployeeForm(name = "New Employee")
        F.edit()
        return "Created record for " + F.myName.value

    if __name__ == '__main__':
        print( npyscreen.wrapper_basic(myFunction) )



提供选项
++++++++

实际上,我们可能就是不太想要任何旧部门名称输进来 - 我们希望给出一列选项. 让我们来用 TitleSelectOne 控件. 这是一个多行控件, 我们需要注意,让它只占用屏幕的几行就好(如果让它自己定,它会占用屏幕上剩余的所有空间)::

    self.myDepartment = self.add(npyscreen.TitleSelectOne, max_height=3,
                                    name='Department',
                                    values = ['Department 1', 'Department 2', 'Department 3'],
                                    scroll_exit = True  # 让用户移通过按下下方向键而不是 tab 来移出控件.
                                                        # 可以试试看看它们的不同.
                                    )

Putting that in context::

        import npyscreen

        class myEmployeeForm(npyscreen.Form):
            def create(self):
                self.myName        = self.add(npyscreen.TitleText, name='Name')
                self.myDepartment = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name='Department', values = ['Department 1', 'Department 2', 'Department 3'])
                self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')

        def myFunction(*args):
            F = myEmployeeForm(name = "New Employee")
            F.edit()
            return "Created record for " + F.myName.value

        if __name__ == '__main__':
            print( npyscreen.wrapper_basic(myFunction) )



更彻底面相对象一点
++++++++++++++++++

到现在我们都做得还不错,但还是比较糙. 我们还是手动调用 F.edit() 方法, 这对单窗体的应用还过得去,但是以后有递归深度的时候,一不小心就会有问题. 这也让一些这个库本身的更巧妙的特性无法操作了. 更好的办法是使用 *NPSAppManaged* 类来管理你的应用程序.

我们还是放弃这个支持我们这么久的旧框架,然后以另一个基础开始我们的应用程序吧::

    import npyscreen

    class MyApplication(npyscreen.NPSAppManaged):
        pass

    if __name__ == '__main__':
        TestApp = MyApplication().run()
        print( "All objects, baby." )

这样其实会异常退出, 因为你没有一个 'MAIN' 窗口, 这是 NPSAppManaged 程序的起始点.

我们把它改过来. 我们会用一下前面的窗口类::

    import npyscreen

    class myEmployeeForm(npyscreen.Form):
        def create(self):
           self.myName        = self.add(npyscreen.TitleText, name='Name')
           self.myDepartment = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name='Department', values = ['Department 1', 'Department 2', 'Department 3'])
           self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')

    class MyApplication(npyscreen.NPSAppManaged):
        def onStart(self):
           self.addForm('MAIN', myEmployeeForm, name='New Employee')

    if __name__ == '__main__':
        TestApp = MyApplication().run()
        print( "All objects, baby." )


如果你运行上面的代码,你可能觉得自己有点挫败, 因为这个程序会一直显示那个要你编辑的窗口,然后你不得不按下 "^C"(Control C) 来退出.

这是因为 NPSAppManaged 类一直会显示任何以它的 NEXT_ACTIVE_FORM 属性(这个例子里, 默认是 -- 'MAIN')命名的窗口. 旧版的教程会建议直接去设定它,但是你得用 setNextForm(formid) 方法.

让我们改一下 myEmployeeForm 来告诉它, 在 NPSAppManaged 上下文中运行之后,它应该通知它的父对象 NPSAppManaged 停止显示窗口. 我们通过创建一个叫做 *afterEditing* 的特殊方法来实现::

    class myEmployeeForm(npyscreen.Form):
        def afterEditing(self):
            self.parentApp.setNextForm(None)

        def create(self):
            self.myName        = self.add(npyscreen.TitleText, name='Name')
            self.myDepartment  = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name='Department', values = ['Department 1', 'Department 2', 'Department 3'])
            self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')



如果喜欢的话,我们还可以通过在 MyApplication 类中定义一个特殊的 *onInMainLoop* 方法来实现同样的结果 -- 这个方法会在每个窗口被编辑完之后被调用.

我们的代码现在看起来是这样的::

    import npyscreen

    class myEmployeeForm(npyscreen.Form):
        def afterEditing(self):
            self.parentApp.setNextForm(None)

        def create(self):
            self.myName        = self.add(npyscreen.TitleText, name='Name')
            self.myDepartment = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name='Department', values = ['Department 1', 'Department 2', 'Department 3'])
            self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')

    class MyApplication(npyscreen.NPSAppManaged):
        def onStart(self):
            self.addForm('MAIN', myEmployeeForm, name='New Employee')
            # A real application might define more forms here.......

    if __name__ == '__main__':
        TestApp = MyApplication().run()


处理方式的选择
++++++++++++++

上面最后一个例子,对于只是写个很简单的小应用可能有点杀鸡焉用牛刀了. 但是这样能提供一个健壮的多的可以构建更大型的应用程序框架, 比我们在教程一开始用的那个也就只多写了几行而已. 如果你要显示不止一个屏幕,或者一直运行一个应用的话,这就是你该用的处理方法.
