import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, QTextEdit, QFileDialog, QMessageBox, QDialog, QInputDialog
from PyQt5.QtGui import QFont
from os import path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Importing custom modules
from data_description import DataDescription
from categorical import Categorical
from imputation import Imputation
from data_visualization import DataVisualization
from outlier_detection import OutlierDetection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Analysis Application")
        self.setGeometry(100, 100, 800, 600)  # Initial window size

        # Create a central widget and set layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create tabs for different modules
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # Add tabs for each module
        self.add_data_description_tab()
        self.add_data_preprocessing_tab()
        self.add_data_visualization_tab()
        self.add_outlier_detection_tab()

    def add_data_description_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Data Description Module")
        label.setFont(QFont('Arial', 12))
        layout.addWidget(label)

        btn_show_dataset = QPushButton("Show Dataset")
        btn_show_dataset.clicked.connect(self.show_dataset)

        btn_describe_column = QPushButton("Describe a Specific Column")
        btn_describe_column.clicked.connect(self.describe_column)

        btn_show_properties = QPushButton("Show Properties of Each Column")
        btn_show_properties.clicked.connect(self.show_properties)

        layout.addWidget(btn_show_dataset)
        layout.addWidget(btn_describe_column)
        layout.addWidget(btn_show_properties)

        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Data Description")

    def add_data_preprocessing_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Data Preprocessing Module")
        label.setFont(QFont('Arial', 12))
        layout.addWidget(label)

        btn_input_data = QPushButton("Input Data")
        btn_input_data.clicked.connect(self.input_data)

        btn_change_to_lowercase = QPushButton("Change Column Names to Lowercase")
        btn_change_to_lowercase.clicked.connect(self.change_to_lowercase)

        btn_handle_missing_values = QPushButton("Handle Missing Values")
        btn_handle_missing_values.clicked.connect(self.handle_missing_values)

        btn_encode_categorical = QPushButton("Encode Categorical Data")
        btn_encode_categorical.clicked.connect(self.encode_categorical)

        layout.addWidget(btn_input_data)
        layout.addWidget(btn_change_to_lowercase)
        layout.addWidget(btn_handle_missing_values)
        layout.addWidget(btn_encode_categorical)

        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Data Preprocessing")

    def add_data_visualization_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Data Visualization Module")
        label.setFont(QFont('Arial', 12))
        layout.addWidget(label)

        btn_visualize_distribution = QPushButton("Visualize Distribution")
        btn_visualize_distribution.clicked.connect(self.visualize_distribution)

        btn_visualize_correlation = QPushButton("Visualize Correlation")
        btn_visualize_correlation.clicked.connect(self.visualize_correlation)

        btn_visualize_categorical = QPushButton("Visualize Categorical Data")
        btn_visualize_categorical.clicked.connect(self.visualize_categorical)

        layout.addWidget(btn_visualize_distribution)
        layout.addWidget(btn_visualize_correlation)
        layout.addWidget(btn_visualize_categorical)

        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Data Visualization")

    def add_outlier_detection_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Outlier Detection Module")
        label.setFont(QFont('Arial', 12))
        layout.addWidget(label)

        btn_detect_outliers_iqr = QPushButton("Detect Outliers using IQR")
        btn_detect_outliers_iqr.clicked.connect(self.detect_outliers_iqr)

        btn_detect_outliers_zscore = QPushButton("Detect Outliers using Z-score")
        btn_detect_outliers_zscore.clicked.connect(self.detect_outliers_zscore)

        layout.addWidget(btn_detect_outliers_iqr)
        layout.addWidget(btn_detect_outliers_zscore)

        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Outlier Detection")

    def show_dataset(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
            if filename:
                data = pd.read_csv(filename)
                self.display_data(data)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def display_data(self, data):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dataset")
        dialog.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setPlainText(data.to_string())
        layout.addWidget(text_edit)

        dialog.setLayout(layout)
        dialog.exec_()

    def describe_column(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
            if filename:
                data = pd.read_csv(filename)
                column_name, ok_pressed = QInputDialog.getText(self, "Column Description", "Enter column name:")
                if ok_pressed:
                    if column_name in data.columns:
                        dialog = QDialog(self)
                        dialog.setWindowTitle(f"Description of Column '{column_name}'")
                        dialog.setGeometry(100, 100, 400, 300)

                        layout = QVBoxLayout()
                        text_edit = QTextEdit()
                        text_edit.setPlainText(str(data[column_name].describe()))
                        layout.addWidget(text_edit)

                        dialog.setLayout(layout)
                        dialog.exec_()
                    else:
                        QMessageBox.warning(self, "Warning", f"Column '{column_name}' not found in the dataset.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_properties(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
            if filename:
                data = pd.read_csv(filename)
                properties = data.info()
                QMessageBox.information(self, "Properties of Each Column", properties)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def input_data(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
            if filename:
                data = pd.read_csv(filename)
                QMessageBox.information(self, "Success", "Data loaded successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def change_to_lowercase(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
            if filename:
                data = pd.read_csv(filename)
                data.columns = map(str.lower, data.columns)
                QMessageBox.information(self, "Success", "Column names changed to lowercase.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def handle_missing_values(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
            if filename:
                data = pd.read_csv(filename)
                data.dropna(inplace=True)
                QMessageBox.information(self, "Success", "Missing values handled successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def encode_categorical(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
            if filename:
                data = pd.read_csv(filename)
                categorical_columns = data.select_dtypes(include=['object']).columns
                for column in categorical_columns:
                    label_encoder = LabelEncoder()
                    data[column] = label_encoder.fit_transform(data[column])
                QMessageBox.information(self, "Success", "Categorical data encoded successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def visualize_distribution(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
            if filename:
                data = pd.read_csv(filename)
                numerical_columns = data.select_dtypes(include=['int', 'float']).columns
                for column in numerical_columns:
                    plt.figure(figsize=(8, 6))
                    sns.histplot(data[column], kde=True)
                    plt.title(f'Distribution of {column}')
                    plt.xlabel(column)
                    plt.ylabel('Frequency')
                    plt.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def visualize_correlation(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
            if filename:
                data = pd.read_csv(filename)
                plt.figure(figsize=(10, 8))
                sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
                plt.title('Correlation Heatmap')
                plt.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def visualize_categorical(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
            if filename:
                data = pd.read_csv(filename)
                categorical_columns = data.select_dtypes(include=['object']).columns
                for column in categorical_columns:
                    plt.figure(figsize=(8, 6))
                    sns.countplot(x=column, data=data)
                    plt.title(f'Count of each category in {column}')
                    plt.xlabel(column)
                    plt.ylabel('Count')
                    plt.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def detect_outliers_iqr(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
            if filename:
                data = pd.read_csv(filename)
                numerical_columns = data.select_dtypes(include=['int', 'float']).columns
                for column in numerical_columns:
                    Q1 = data[column].quantile(0.25)
                    Q3 = data[column].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    column_outliers = (data[column] < lower_bound) | (data[column] > upper_bound)
                    if column_outliers.any():
                        QMessageBox.information(self, "Outliers Detected", f"Outliers detected using IQR in column '{column}':\n{data[column][column_outliers]}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def detect_outliers_zscore(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
            if filename:
                data = pd.read_csv(filename)
                numerical_columns = data.select_dtypes(include=['int', 'float']).columns
                for column in numerical_columns:
                    z_scores = ((data[column] - data[column].mean()) / data[column].std()).abs()
                    threshold = 3
                    column_outliers = z_scores > threshold
                    if column_outliers.any():
                        QMessageBox.information(self, "Outliers Detected", f"Outliers detected using Z-score in column '{column}':\n{data[column][column_outliers]}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
