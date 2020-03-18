import npyscreen
import time


class BlankTerminalExample(npyscreen.Form):
    def create(self):
        key_of_choice = 'b'
        what_to_display = 'Press {} to blank screen \n Press escape key to quit'.format(key_of_choice)

        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        self.add_handlers({key_of_choice: self.initiate_blanking_sequence})
        self.add(npyscreen.FixedText, value=what_to_display)

    def initiate_blanking_sequence(self, code_of_key_pressed):
        npyscreen.blank_terminal()
        time.sleep(1.5)
        npyscreen.notify('..and we\'re back', title='Phew')
        time.sleep(0.75)

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', BlankTerminalExample, name='To show off blank_screen')


if __name__ == '__main__':
    TestApp = MyApplication().run()