编写测试
=========

(4.7.0版本新增)

脚本化 npyscreen 应用的键盘输入用于测试目的是可行的.

npyscreen 模块导出下面包含了相关设置的字典::

    TEST_SETTINGS = {
        'TEST_INPUT': None,
        'TEST_INPUT_LOG': [],
        'CONTINUE_AFTER_TEST_INPUT': False,
        'INPUT_GENERATOR': False
        }

如果 'TEST_INPUT' 是 None, 应用照常进行. 如果它是一个数组, 按键动作会从数组的左边开始被加载, 然后送到应用程序获取键盘输入的地方. 注意,像 *curses.KEYDOWN* 这样的特殊字符也可以被处理,而控制字符可以用像 *"^X"* 这样的字符串来表示.

这种方式发送到应用程序的按键动作会自动的添加到 *'TEST_INPUT_LOG'* , 所以就能看到在处理输入的时候在哪里出现了错误.

如果 'CONTINUE_AFTER_TEST_INPUT' 为 True, 那么在指定自动输入之后, *'TEST_INPUT'* 就被设成 *None* 并且应用程序会正常继续. 如果它为 False, 那就会抛出  *ExhaustedTestInput* 异常. 这可以让单元测试来接着检测应用的状态.

'INPUT_GENERATOR' 可以设置为一个可迭代对象. 调用 `next(INPUT_GENERATOR)` 每一个按键都会被读取. 假如可迭代对象是线程安全的, 这就让用一个线程来提供测试用的输入变得容易了. 相对 TEST_INPUT 可以多用一下这个. 在 4.9 版本中按用户要求加入.



便捷函数 (4.8.5 版本新增)
--------------------------------------------

.. py:function:: npyscreen.add_test_input_from_iterable(iterable)

	将每个 `iterable` 项 加入 `TEST_SETTINGS['TEST_INPUT']`.

.. py:function:: npyscreen.add_test_input_ch(ch)

	添加 `ch` 到 `TEST_SETTINGS['TEST_INPUT']`.


防止编写单元测试产生分叉
----------------------------------------

为了避免底层 curses 模块的内存溢出, npyscreen 库有时会悬着在 fork 出的进程中运行应用程序代码. 处于一定的测试目的这可能不是我们想要的, 或许会想在你的应用程序中传递 `fork=False` 到 `run()` 方法来测试.




例子
-------

下面是个小例子::

    #!/usr/bin/python
    import curses
    import npyscreen

    npyscreen.TEST_SETTINGS['TEST_INPUT'] = [ch for ch in 'This is a test']
    npyscreen.TEST_SETTINGS['TEST_INPUT'].append(curses.KEY_DOWN)
    npyscreen.TEST_SETTINGS['CONTINUE_AFTER_TEST_INPUT'] = True

    class TestForm(npyscreen.Form):
        def create(self):
            self.myTitleText = self.add(npyscreen.TitleText, name="Events (Form Controlled):", editable=True)

    class TestApp(npyscreen.StandardApp):
        def onStart(self):
            self.addForm("MAIN", TestForm)


    if __name__ == '__main__':
        A = TestApp()
        A.run(fork=False)
        # 'This is a test' will appear in the first widget, as if typed by the user.
