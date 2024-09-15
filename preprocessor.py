# -*- coding: utf-8 -*-
from data_description import DataDescription
from data_input import DataInput
from imputation import Imputation
from download import Download
from categorical import Categorical
from outlier_detection import OutlierDetection
from data_visualization import DataVisualization
from feature_scaling import FeatureScaling

from colorama import init, Style
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Initialize colorama
init()

class Preprocessor:
    bold_start = Style.BRIGHT
    bold_end = Style.RESET_ALL
    
    # The Task associated with this class. This is also the main class of the project.
    tasks = [
        '1. Data Description',
        '2. Handling NULL Values',
        '3. Handling Outliers',
        '4. Encoding Categorical Values',
        '5. Visualize Distribution of a Column',
        '6. Feature Scaling',
        '7. Download the modified dataset'
    ]

    data = 0
    
    def __init__(self):
        self.data = DataInput().inputFunction()
        print("\n\n" + self.bold_start + "WELCOME TO THE MACHINE LEARNING PREPROCESSOR CLI!!!" + self.bold_end + "\n\n")
    
    def printData(self):
        print(self.data)

    # main function of the Preprocessor class.
    def preprocessorMain(self):

        print("Columns\n")
        for column in self.data.columns.values:
            print(column, end="  ")

        while True:
            print("\nTasks (Preprocessing)\n")
            for task in self.tasks:
                print(task)

            while True:
                try:
                    choice = int(input("\nWhat do you want to do? (Press -1 to exit):  "))
                except ValueError:
                    print("Integer Value required. Try again.....")
                    continue
                break

            if choice == -1:
                exit()

            # moves the control into the DataDescription class.
            elif choice==1:
                DataDescription(self.data).describe()

            # moves the control into the Imputation class.
            elif choice==2:
                self.data = Imputation(self.data).imputer()

            # moves the control into the OutlierDetection class.
            elif choice==3:
                self.data = OutlierDetection(self.data).outlier_main()

            # moves the control into the Categorical class.
            elif choice==4:
                self.data = Categorical(self.data).categoricalMain()

            # moves the control into the DataVisualization class for visualizing distribution.
            elif choice==5:
                DataVisualization(self.data).visualize_distribution()

            # moves the control into the FeatureScaling class.
            
            elif choice==6:
                columns_to_scale = FeatureScaling.ask_columns_to_scale(self.data)
                scaling_method = FeatureScaling.ask_scaling_method()
                FeatureScaling(self.data).scale_features(columns_to_scale, scaling_method)

            # moves the control into the Download class.
            elif choice==7:
                Download(self.data).download()
            
            else:
                print("\nWrong Integer value!! Try again..")

# obj is the object of our Preprocessor class(main class).
obj = Preprocessor()
# the object 'obj' calls the main function of our Preprocessor class.
obj.preprocessorMain()
