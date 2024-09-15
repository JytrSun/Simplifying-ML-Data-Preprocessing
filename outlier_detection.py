import pandas as pd
from data_description import DataDescription

class OutlierDetection:
    tasks = [
        '\n1. Detect Outliers using IQR',
        '2. Detect Outliers using Z-score',
        '3. Show the Dataset'
    ]

    def __init__(self, data):
        self.data = data

    def detect_outliers_iqr(self):
        numerical_columns = self.data.select_dtypes(include=['int', 'float']).columns
        outliers = pd.DataFrame()
        for column in numerical_columns:
            Q1 = self.data[column].quantile(0.25)
            Q3 = self.data[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            column_outliers = (self.data[column] < lower_bound) | (self.data[column] > upper_bound)
            outliers[column] = column_outliers
            if column_outliers.any():
                print(f"\nOutliers detected using IQR in column '{column}':")
                print(self.data[column][column_outliers])
        return outliers

    def detect_outliers_zscore(self):
        numerical_columns = self.data.select_dtypes(include=['int', 'float']).columns
        outliers = pd.DataFrame()
        for column in numerical_columns:
            z_scores = ((self.data[column] - self.data[column].mean()) / self.data[column].std()).abs()
            threshold = 3
            column_outliers = z_scores > threshold
            outliers[column] = column_outliers
            if column_outliers.any():
                print(f"\nOutliers detected using Z-score in column '{column}':")
                print(self.data[column][column_outliers])
        return outliers

    def handle_outliers(self, outliers):
        # Here you can choose how to handle outliers, e.g., remove them, replace with median, etc.
        # For simplicity, we will just remove them.
        self.data = self.data[~outliers.any(axis=1)]
        print("Outliers removed successfully.")

    def outlier_main(self):
        while True:
            print("\nTasks (Outlier Detection)\n")
            for i, task in enumerate(self.tasks):
                print(f"{i+1}. {task}")

            while True:
                try:
                    choice = int(input("\nWhat do you want to do? (Press -1 to go back): "))
                except ValueError:
                    print("Integer Value required. Try again...")
                    continue
                break

            if choice == -1:
                break

            elif choice == 1:
                outliers_iqr = self.detect_outliers_iqr()
                if outliers_iqr.any().any():
                    self.handle_outliers(outliers_iqr)
                else:
                    print("\nNo outliers detected using IQR.")

            elif choice == 2:
                outliers_zscore = self.detect_outliers_zscore()
                if outliers_zscore.any().any():
                    self.handle_outliers(outliers_zscore)
                else:
                    print("\nNo outliers detected using Z-score.")

            elif choice == 3:
                DataDescription.showDataset(self)

            else:
                print("\nWrong Integer value!! Try again..")

        return self.data
