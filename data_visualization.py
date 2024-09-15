import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualization:
    def __init__(self, data):
        self.data = data

    def visualize_distribution(self):
        print("Available columns for visualization:")
        for column in self.data.columns:
            print(column)
        
        column = input("\nEnter the name of the column you want to visualize: ")
        if column in self.data.columns:
            print(f"Data type of column '{column}': {self.data[column].dtype}")  # Debugging statement
            if self.data[column].dtype in ['int64', 'float64']:  # Check if the column is numeric
                try:
                    plt.figure(figsize=(8, 6))
                    sns.histplot(self.data[column], kde=True)
                    plt.title(f'Distribution of {column}')
                    plt.xlabel(column)
                    plt.ylabel('Frequency')
                    plt.show()
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print(f"The column '{column}' is not numeric and cannot be visualized.")
        else:
            print(f"The column '{column}' does not exist in the dataset.")

    def visualize_correlation(self):
        plt.figure(figsize=(10, 8))
        sns.heatmap(self.data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Heatmap')
        plt.show()

    def visualize_categorical(self, column):
        if self.data[column].dtype == 'object':  # Check if the column is categorical
            plt.figure(figsize=(8, 6))
            sns.countplot(x=column, data=self.data)
            plt.title(f'Count of each category in {column}')
            plt.xlabel(column)
            plt.ylabel('Count')
            plt.show()
        else:
            print(f"The column '{column}' is not categorical and cannot be visualized.")
