import npyscreen


class SelectFileExample(npyscreen.Form):
    def create(self):
        key_of_choice = 'p'
        what_to_display = 'Press {} for popup \n Press escape key to quit'.format(key_of_choice)

        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        self.add_handlers({key_of_choice: self.spawn_file_dialog})
        self.add(npyscreen.FixedText, value=what_to_display)

    def spawn_file_dialog(self, code_of_key_pressed):
        the_selected_file = npyscreen.selectFile()
        npyscreen.notify_wait('That returned: {}'.format(the_selected_file), title= 'results')

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', SelectFileExample, name='To show off notify_wait')


if __name__ == '__main__':
    TestApp = MyApplication().run()