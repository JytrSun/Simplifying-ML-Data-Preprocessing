import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QLabel, QComboBox

# Importing modules
from data_description import DataDescription
from feature_scaling import FeatureScaling
from categorical import Categorical
from outlier_detection import OutlierDetection
from data_visualization import DataVisualization
from imputation import Imputation


class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Data Analysis Application")
        self.setGeometry(100, 100, 600, 400)

        self.data = None
        self.file_path = None

        self.upload_button = QPushButton("Upload CSV", self)
        self.upload_button.setGeometry(50, 50, 150, 30)
        self.upload_button.clicked.connect(self.upload_csv)

        self.label = QLabel(self)
        self.label.setGeometry(220, 50, 350, 30)

        self.create_module_buttons()

    def create_module_buttons(self):
        # Create buttons for each module
        modules = {
            "Data Description": DataDescription,
            "Feature Scaling": FeatureScaling,
            "Categorical Handling": Categorical,
            "Outlier Detection": OutlierDetection,
            "Data Visualization": DataVisualization,
            "Imputation": Imputation
        }

        y_offset = 100
        for module_name, module_class in modules.items():
            button = QPushButton(module_name, self)
            button.setGeometry(50, y_offset, 150, 30)
            button.clicked.connect(lambda _, mod=module_class: self.open_module_window(mod))
            y_offset += 40

    def open_module_window(self, module_class):
        if self.data is None:
            QMessageBox.warning(self, "Warning", "Please upload a CSV file first.")
            return

        self.module_window = ModuleWindow(module_class, self.data)
        self.module_window.show()

    def upload_csv(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("CSV files (*.csv)")
        file_dialog.setViewMode(QFileDialog.Detail)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.label.setText(file_path)
            try:
                self.data = pd.read_csv(file_path)
                QMessageBox.information(self, "Success", "CSV file uploaded successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error occurred: {str(e)}")


class ModuleWindow(QMainWindow):
    def __init__(self, module_class, data):
        super().__init__()
        self.module = module_class(data)
        self.setWindowTitle(module_class.__name__)
        self.setGeometry(200, 200, 600, 400)

        self.create_buttons()

    def create_buttons(self):
        tasks = self.module.tasks
        y_offset = 50
        for task in tasks:
            label = QLabel(task, self)
            label.setGeometry(50, y_offset, 300, 30)

            functions = task.split("\n")[1:]  # Exclude the task name
            for function in functions:
                combo_box = QComboBox(self)
                combo_box.setGeometry(350, y_offset, 200, 30)
                combo_box.addItem("Select Function")
                combo_box.addItem(function)
                y_offset += 40

                combo_box.currentIndexChanged.connect(lambda _, combo_box=combo_box, function=function: self.execute_function(combo_box.currentText(), function))

    def execute_function(self, selected_function, function_name):
        if selected_function != "Select Function":
            getattr(self.module, function_name.split(". ")[1].replace(" ", "_").lower())()

    # Remaining code...


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalysisApp()
    window.show()
    sys.exit(app.exec_())
