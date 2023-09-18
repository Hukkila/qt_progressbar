import sys
import time
from PyQt5.QtWidgets import QApplication, QDialog, QListView, QProgressBar
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from sub import DataMaker

class MyDialog(QDialog):
    total_percent = 0  # Class attribute to accumulate total percentage

    def __init__(self):
        super().__init__()

        # Load the .ui file dynamically
        loadUi("Dialog.ui", self)

        # Access UI elements
        self.buttonBox.accepted.connect(self.on_accepted)  # Connect accepted signal
        self.buttonBox.rejected.connect(self.on_rejected)  # Connect rejected signal
        self.listView = self.findChild(QListView, 'listView')
        self.progressBar = self.findChild(QProgressBar, 'progressBar')

        # Create an instance of DataMaker
        self.data_maker_instance = DataMaker()

        # Initialize a timer for displaying items one at a time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_percent)

    def on_accepted(self):
        # Define the action to perform when the "Ok" button is clicked
        print("Accepted")

    def on_rejected(self):
        # Define the action to perform when the "Cancel" button is clicked
        print("Rejected")

    def data_importer(self):
        self.data = self.data_maker_instance.data_sender()
        self.current_index = 0
        self.total_percent = 0  # Reset the total percent to 0 for each run
        self.target_percent = 0  # Reset the target percent to 0 for each run

        # Create a QStandardItemModel to hold the data
        self.model = QStandardItemModel()

        # Start the timer with the interval from the third value in the data
        self.set_timer_interval()

    def set_timer_interval(self):
        if self.current_index < len(self.data):
            item_data = self.data[self.current_index]
            if len(item_data) >= 2:
                self.target_percent += item_data[1]  # Accumulate target percent across items
                if len(item_data) >= 3:
                    time_value = item_data[2]  # Third value in the list (time in ms)
                    self.timer_interval = int(time_value / self.target_percent)  # Convert to integer
                else:
                    self.timer_interval = 1000  # Default to 1 second if no time is specified
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

            item = QStandardItem(str(item_data))
            self.model.appendRow(item)
            self.listView.setModel(self.model)
            self.current_index += 1
            self.set_timer_interval()  # Set timer interval for the next item
        else:
            # Stop the timer when all items have been displayed
            self.timer.stop()

def main():
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    dialog.data_importer()  # Start displaying items
    sys.exit(app.exec_())





