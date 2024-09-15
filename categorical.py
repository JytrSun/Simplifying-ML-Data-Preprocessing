import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from data_description import DataDescription

class Categorical:
    # The Task associated with this class.
    tasks = [
        '\n1. Show Categorical Columns',
        '2. Performing Encoding for Nominal Data',
        '3. Performing Encoding for Ordinal Data',
        '4. Show the Dataset'
    ]

    def __init__(self, data):
        self.data = data

    # function to show all the categorical columns and number of unique values in them.
    def categoricalColumn(self):
        print('\n{0: <20}'.format("Categorical Column") + '{0: <5}'.format("Unique Values"))
        # select_dtypes selects the columns with object datatype(which could be further categorized)
        for column in self.data.select_dtypes(include="object"):
            print('{0: <20}'.format(column) + '{0: <5}'.format(self.data[column].nunique()))

    # function to encode any particular column
    def encoding(self, ordinal=False):
        if not ordinal:
            columns = [col for col in self.data.columns if self.data[col].dtype == 'object']
        else:
            columns = [col for col in self.data.columns if col in self.data.select_dtypes(exclude=['number']).columns]
        
        columns_str = ", ".join(columns)
        print(f"\nAvailable {'Nominal' if not ordinal else 'Ordinal'} Columns: {columns_str}")

        while True:
            column = input("\nWhich column would you like to encode? (Press -1 to go back): ").lower()
            if column == "-1":
                break

            if column in columns:
                if ordinal:
                    mapping = input("Enter the ordinal mappings for the categories in order (comma-separated): ")
                    mapping = mapping.split(",")
                    self.data[column] = pd.Categorical(self.data[column], categories=mapping, ordered=True)
                    self.data[column] = self.data[column].cat.codes
                else:
                    label_encoder = LabelEncoder()
                    self.data[column] = label_encoder.fit_transform(self.data[column])
                print("Encoding is done.......")
                self.categoricalColumn()
                break
            else:
                print("Wrong Column Name. Try Again...")

    # The main function of the Categorical class.
    def categoricalMain(self):
        while True:
            print("\nTasks")
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
                self.categoricalColumn()

            elif choice == 2:
                self.encoding()

            elif choice == 3:
                self.encoding(ordinal=True)

            elif choice == 4:
                DataDescription.showDataset(self)

            else:
                print("\nWrong Integer value!! Try again..")

        # return the data after modifying
        return self.data
