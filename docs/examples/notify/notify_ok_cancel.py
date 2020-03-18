import npyscreen


class NotifyOkCancelExample(npyscreen.Form):
    def create(self):
        key_of_choice = 'p'
        what_to_display = 'Press {} for popup \n Press escape key to quit'.format(key_of_choice)

        self.add_handlers({key_of_choice: self.spawn_notify_popup})
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        self.add(npyscreen.FixedText, value=what_to_display)

    def spawn_notify_popup(self, code_of_key_pressed):
        message_to_display = 'You have a choice, to Cancel and return false, or Ok and return true.'
        notify_result = npyscreen.notify_ok_cancel(message_to_display, title= 'popup')
        npyscreen.notify_wait('That returned: {}'.format(notify_result), title= 'results')

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', NotifyOkCancelExample, name='To show off notify_ok_cancel')


if __name__ == '__main__':
    TestApp = MyApplication().run()