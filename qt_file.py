import sys
from PyQt5.QtWidgets import QApplication, QDialog, QListView, QProgressBar
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class DataMaker:
    def data_sender(self):
        data = [['first', 10], ['second', 20, 2000],['third', 10],
                ['fourth', 30, 10000], ['fifth', 20], ['sixth', 10]]
        return data


class MyDialog(QDialog):
    total_percent = 0  

    def __init__(self):
        super().__init__()
        loadUi("Dialog.ui", self)

        self.buttonBox.accepted.connect(self.on_accepted)  
        self.buttonBox.rejected.connect(self.on_rejected)  
        self.listView = self.findChild(QListView, 'listView')
        self.progressBar = self.findChild(QProgressBar, 'progressBar')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_percent)

        # Import from DataMaker class
        self.data_maker_instance = DataMaker()

    def on_accepted(self):
        print("Accepted")

    def on_rejected(self):
        print("Rejected")

    def data_importer(self):
        self.data = self.data_maker_instance.data_sender()
        self.current_index = 0
        self.total_percent = 0  
        self.target_percent = 0 
        self.model = QStandardItemModel()
        self.set_timer_interval()

    def set_timer_interval(self):
        if self.current_index < len(self.data):
            item_data = self.data[self.current_index]
            if len(item_data) >= 2:
                self.target_percent += item_data[1]  
                if len(item_data) >= 3:
                    time_value = item_data[2] 
                    self.timer_interval = int(time_value / self.target_percent) 
                else:
                    self.timer_interval = 100 
                self.timer.start(self.timer_interval)
            else:
                self.timer.stop()

    def update_percent(self):
        if self.total_percent < self.target_percent:
            self.total_percent += 1
            self.progressBar.setValue(self.total_percent)
        else:
            self.timer.stop()
            self.display_next_item()

    def display_next_item(self):
        if self.current_index < len(self.data):
            item_data = self.data[self.current_index]

            item = QStandardItem(str(item_data[0]))
            self.model.appendRow(item)
            self.listView.setModel(self.model)
            self.current_index += 1
            self.set_timer_interval()  
        else:
            self.timer.stop()

    def main_gui():
        app = QApplication(sys.argv)
        dialog = MyDialog()
        dialog.show()
        dialog.data_importer()  # Start displaying items
        sys.exit(app.exec_())





