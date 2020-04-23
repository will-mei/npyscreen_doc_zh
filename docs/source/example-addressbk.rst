示例程序:一个简单的通讯录
===========================================

一个通讯录程序需要一个数据库.为了方便,我们会用 sqlite. ::

    class AddressDatabase(object):
        def __init__(self, filename="example-addressbook.db"):
            self.dbfilename = filename
            db = sqlite3.connect(self.dbfilename)
            c = db.cursor()
            c.execute(
            "CREATE TABLE IF NOT EXISTS records\
                ( record_internal_id INTEGER PRIMARY KEY, \
                  last_name     TEXT, \
                  other_names   TEXT, \
                  email_address TEXT \
                  )" \
                )
            db.commit()
            c.close()

        def add_record(self, last_name = '', other_names='', email_address=''):
            db = sqlite3.connect(self.dbfilename)
            c = db.cursor()
            c.execute('INSERT INTO records(last_name, other_names, email_address) \
                        VALUES(?,?,?)', (last_name, other_names, email_address))
            db.commit()
            c.close()

        def update_record(self, record_id, last_name = '', other_names='', email_address=''):
            db = sqlite3.connect(self.dbfilename)
            c = db.cursor()
            c.execute('UPDATE records set last_name=?, other_names=?, email_address=? \
                        WHERE record_internal_id=?', (last_name, other_names, email_address, \
                                                            record_id))
            db.commit()
            c.close()

        def delete_record(self, record_id):
            db = sqlite3.connect(self.dbfilename)
            c = db.cursor()
            c.execute('DELETE FROM records where record_internal_id=?', (record_id,))
            db.commit()
            c.close()

        def list_all_records(self, ):
            db = sqlite3.connect(self.dbfilename)
            c = db.cursor()
            c.execute('SELECT * from records')
            records = c.fetchall()
            c.close()
            return records

        def get_record(self, record_id):
            db = sqlite3.connect(self.dbfilename)
            c = db.cursor()
            c.execute('SELECT * from records WHERE record_internal_id=?', (record_id,))
            records = c.fetchall()
            c.close()
            return records[0]

这个应用程序的主屏幕会是一个名字的列表. 当用户选择一个名字,我们会想要编辑它. 我们会子类化 MultiLineAction, 然后重写 `display value` 方法来改变每个记录是怎么展示的. 我们还会重写 `actionHighlighted` 方法以需要的时候转换到编辑窗. 最后,我们会添加两个新的按键 - 一个用来添加一个用来删除记录. 在切换到 EDITRECORDFM 之前, 我们要么会创建一个新窗口设置它的值为 None, 要么把它的值设置成我们希望编辑的记录的值. ::

    class RecordList(npyscreen.MultiLineAction):
        def __init__(self, *args, **keywords):
            super(RecordList, self).__init__(*args, **keywords)
            self.add_handlers({
                "^A": self.when_add_record,
                "^D": self.when_delete_record
            })

        def display_value(self, vl):
            return "%s, %s" % (vl[1], vl[2])

        def actionHighlighted(self, act_on_this, keypress):
            self.parent.parentApp.getForm('EDITRECORDFM').value =act_on_this[0]
            self.parent.parentApp.switchForm('EDITRECORDFM')

        def when_add_record(self, *args, **keywords):
            self.parent.parentApp.getForm('EDITRECORDFM').value = None
            self.parent.parentApp.switchForm('EDITRECORDFM')

        def when_delete_record(self, *args, **keywords):
            self.parent.parentApp.myDatabase.delete_record(self.values[self.cursor_line][0])
            self.parent.update_list()

实际上用来显示记录列表的窗口会是一个 FormMutt 子类. 我们会把 `MAIN_WIDGET_CLASS` 类变量改成我们自己的 RecordList 控件, 然后确保每一次窗口展示给用户的时候记录列表都是最新的. ::

    class RecordListDisplay(npyscreen.FormMutt):
        MAIN_WIDGET_CLASS = RecordList
        def beforeEditing(self):
            self.update_list()

        def update_list(self):
            self.wMain.values = self.parentApp.myDatabase.list_all_records()
            self.wMain.display()

用来编辑每个记录的窗口会是 ActionForm 的一个示例. 记录只会在用户选择了 'OK' 键之后才被修改. 在窗口展示给用户之前,每一个独立控件的值都会更新以匹配数据库的记录,或者被清空要是创建一个新的记录的话. ::

    class EditRecord(npyscreen.ActionForm):
        def create(self):
            self.value = None
            self.wgLastName   = self.add(npyscreen.TitleText, name = "Last Name:",)
            self.wgOtherNames = self.add(npyscreen.TitleText, name = "Other Names:")
            self.wgEmail      = self.add(npyscreen.TitleText, name = "Email:")

        def beforeEditing(self):
            if self.value:
                record = self.parentApp.myDatabase.get_record(self.value)
                self.name = "Record id : %s" % record[0]
                self.record_id          = record[0]
                self.wgLastName.value   = record[1]
                self.wgOtherNames.value = record[2]
                self.wgEmail.value      = record[3]
            else:
                self.name = "New Record"
                self.record_id          = ''
                self.wgLastName.value   = ''
                self.wgOtherNames.value = ''
                self.wgEmail.value      = ''

        def on_ok(self):
            if self.record_id: # We are editing an existing record
                self.parentApp.myDatabase.update_record(self.record_id,
                                                last_name=self.wgLastName.value,
                                                other_names = self.wgOtherNames.value,
                                                email_address = self.wgEmail.value,
                                                )
            else: # We are adding a new record.
                self.parentApp.myDatabase.add_record(last_name=self.wgLastName.value,
                other_names = self.wgOtherNames.value,
                email_address = self.wgEmail.value,
                )
            self.parentApp.switchFormPrevious()

        def on_cancel(self):
            self.parentApp.switchFormPrevious()

最后, 我们需要一个能管理两个窗口和数据库的应用对象::

    class AddressBookApplication(npyscreen.NPSAppManaged):
        def onStart(self):
            self.myDatabase = AddressDatabase()
            self.addForm("MAIN", RecordListDisplay)
            self.addForm("EDITRECORDFM", EditRecord)

    if __name__ == '__main__':
        myApp = AddressBookApplication()
        myApp.run()
