import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class FeatureScaling:
    def __init__(self, data):
        self.data = data

    def scale_features(self, columns_to_scale, scaling_method):
        if scaling_method not in ['standard', 'minmax']:
            print("Invalid scaling method. Please choose either 'standard' or 'minmax'.")
            return

        if columns_to_scale[0].strip().lower() == 'all':
            columns_to_scale = self.data.select_dtypes(include=['int', 'float']).columns.tolist()

        scaler = StandardScaler() if scaling_method == 'standard' else MinMaxScaler()

        for column in columns_to_scale:
            if column not in self.data.columns:
                print(f"Column '{column}' not found in the dataset.")
                continue

            if self.data[column].dtype not in ['int', 'float']:
                print(f"Column '{column}' is not numerical and cannot be scaled.")
                continue

            self.data[column] = scaler.fit_transform(self.data[[column]])

        return self.data

    @staticmethod
    def ask_columns_to_scale(data):
        print("Available columns for scaling:")
        for col in data.select_dtypes(include=['int', 'float']).columns:
            print(col)
        
        columns = input("Enter the names of the columns you want to scale (comma-separated), or enter 'all' to scale all numerical columns: ").split(',')
        return [col.strip() for col in columns]

    @staticmethod
    def ask_scaling_method():
        return input("Choose the scaling method (standard/minmax): ").strip().lower()
