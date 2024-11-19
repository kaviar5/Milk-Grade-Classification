# -*- coding: utf-8 -*-
"""milk_grade_classification_7Attribute.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VIrZH8hjDaOJGjK77ndLGR_CN_oJ9hh0
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt #plotting
# %matplotlib inline

plt.rcParams['figure.figsize'] = (15,10) #Set the default figure size
plt.style.use('ggplot') #Set the plotting method

from sklearn.model_selection import train_test_split #Split the data into train and test
from sklearn.ensemble import RandomForestClassifier #Forest for prediction and regression
from sklearn.metrics import mean_squared_error #Error testing
from sklearn.metrics import classification_report #Report of Classification
from sklearn.metrics import accuracy_score #Accuracy

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

milk = pd.read_csv(r"/content/sample_data/7attributeModel_dataset.csv")

print(milk.isnull().any()) #Check for null values

milk["Grade"].value_counts().plot.bar(title = "Milk in Each Grade") #Plot the number of instances of each grade

rangeValues = ["Temprature", "pH", "Colour",] #Get the columns that are ranged values

#For each ranged value column, print the range of the column (min and max)
for column in rangeValues:
    #Print the range for these columns that have ranges
    print(column, "Range: ", milk[column].unique().min(), "-", milk[column].unique().max())

gradeType = ["high", "medium", "low"]  # Word names for the different grades
rangeValues = ["Temprature", "pH", "Colour","","",""]  # Define ranged value columns

# Loop through each grade to get subsets and range values
for grade in gradeType:
    # Filter the dataset for the specific grade
    subset = milk.loc[milk["Grade"] == grade]

    # Print the range for each ranged value column
    for column in rangeValues:
        if column in subset.columns:  # Ensure the column exists in the dataset
            print(
                grade,
                column,
                "Range: ",
                subset[column].min(),
                "-",
                subset[column].max()
            )
        else:
            print(f"Column '{column}' not found in the dataset.")

plt.rcParams['figure.figsize'] = (10,4) #Update the graph sizes

#For each milk column, plot it in a bar graph
for column in milk.columns:
    plt.figure() #Get the figure so it will let me plot multiple
    milk[column].value_counts().plot.bar(title = column) #Plot the specified column

# Function to classify milk grades
def classifyMilk(milk, labels):
    # Encode the grades as one-hot vectors
    grade = pd.get_dummies(milk["Grade"])  # Convert Grade (renamed gradeWord) to dummy variables

    # Drop the target column (Grade) from features
    characteristics = milk.drop(columns=["Grade"])  # Adjusted to reflect the dataset setup

    # Split the dataset into training and testing sets
    charaTrain, charaTest, gradeTrain, gradeTest = train_test_split(
        characteristics, grade, test_size=0.2, random_state=42
    )

    # Create and train the Random Forest model
    forest = RandomForestClassifier(n_estimators=100, random_state=42)
    forest.fit(charaTrain, gradeTrain)

    # Make predictions on the test and training sets
    predict_test = forest.predict(charaTest)
    predict_train = forest.predict(charaTrain)

    # Calculate accuracy for training and test sets
    train_accuracy = accuracy_score(gradeTrain, predict_train)
    test_accuracy = accuracy_score(gradeTest, predict_test)

    # Convert predictions and ground truth to numeric values for RMSE calculation
    gradeTest_numeric = gradeTest.to_numpy(dtype=float)  # Convert to numeric NumPy array
    predict_numeric = np.array(predict_test, dtype=float)  # Ensure predictions are numeric

    # Print accuracies
    print("Training Accuracy: ", train_accuracy)
    print("Test Accuracy: ", test_accuracy)

    # Print Root Mean Square Error
    print("Root Mean Square Error: ", np.sqrt(mean_squared_error(gradeTest_numeric, predict_numeric)))

    # Print classification report
    print("Classification Report:\n", classification_report(gradeTest, predict_test, target_names=labels))

    # Print the most important characteristics
    getChara(characteristics, forest)
    return forest

# Function to display feature importance
def getChara(characteristics, model):
    # Extract feature importance from the trained model
    feature_importance = model.feature_importances_

    # Create a DataFrame to map features with their importance values
    importance_df = pd.DataFrame({
        'Feature': characteristics.columns,
        'Importance': feature_importance
    })

    # Sort the features by importance
    importance_df = importance_df.sort_values(by='Importance', ascending=False)

    # Print the most important features
    print("According to the Random Forest, the most important factors for milk grade are:")
    print(importance_df)

# Main driver code
if __name__ == "__main__":
    # Load your dataset from the specified path
    dataset_path = r"/content/sample_data/7attributeModel_dataset.csv"
    milk = pd.read_csv(dataset_path)  # Load dataset into a DataFrame

    # Rename gradeWord to Grade for consistency with the code
    milk.rename(columns={"Grade": "Grade"}, inplace=True)

    grade_labels = ["low", "medium", "high"]  # Define grade labels
    model = classifyMilk(milk, grade_labels)  # Classify milk grades

grades = ["high", "medium"] #Get the grades for this classification
milkLite = milk.loc[milk["Grade"] != "low"] #Get all milks that are not bad

classifyMilk(milkLite, grades) #Classify every milk but bad

pH = float(input("Enter the Ph value (3.0 to 9.5)= "))
Temprature = float(input("Enter the Temperature (34 to 90)= "))
Taste = float(input("Enter the Taste = "))
Odor = float(input("Enter the Odor = "))
Fat = float(input("Enter the Fat = "))
Turbidity = float(input("Enter the Turbidity = "))
Colour = float(input("Enter the color (240 to 255)= "))

input_data = [[pH, Temprature, Taste, Odor, Fat, Turbidity, Colour]]
prediction = model.predict(input_data)
if prediction[0][0]:
    print("Milk is of HIGH GRADE")
elif prediction[0][1]:
    print("Milk is of AVERAGE GRADE")
else:
    print("Milk is of LOW GRADE")

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Load the dataset (update the file path as needed)
df = pd.read_csv('/content/sample_data/7attributeModel_dataset.csv')

# List of attributes excluding the 'Grade' column
attributes = ['Taste', 'Odor', 'Fat ', 'Turbidity']

# Color palette for different bars within each grade
colors = list(mcolors.TABLEAU_COLORS.values())  # Get a list of colors from matplotlib's color options

# Function to adjust label display by comparing counts of "low" and "medium"
def get_adjusted_counts(attribute):
    # Count occurrences of each value for each grade
    grade_counts = df.groupby(['Grade'])[attribute].value_counts().unstack().fillna(0)

    # If "medium" has higher values than "low", swap them for display
    if grade_counts.loc['medium'].sum() > grade_counts.loc['low'].sum():
        # Swap "low" and "medium" labels for visualization
        grade_counts = grade_counts.rename(index={'low': 'medium', 'medium': 'low'})
    else:
        # Use original labels
        grade_counts = grade_counts.rename(index={'low': 'medium', 'medium': 'low'})

    return grade_counts

# Loop through each attribute and create a bar chart
for attribute in attributes:
    plt.figure(figsize=(8, 6))

    # Get adjusted counts with swapped labels if needed
    grade_counts = get_adjusted_counts(attribute)

    # Generate the plot with different colors for each bar within a grade
    grade_counts.plot(kind='bar', stacked=False, ax=plt.gca(), color=colors[:len(grade_counts.columns)])

    # Set plot title and labels
    plt.title(f'Distribution of {attribute} by Grade')
    plt.xlabel('Grade')
    plt.ylabel('Count')
    plt.legend(title=attribute)
    plt.xticks(rotation=0)
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Load the dataset (update the file path as needed)
df = pd.read_csv('/content/sample_data/7attributeModel_dataset.csv')

# List of attributes excluding the 'Grade' column
attributes = ['pH', 'Temprature', 'Colour']

# Color palette for different bars within each grade
colors = list(mcolors.TABLEAU_COLORS.values())  # Get a list of colors from matplotlib's color options

# Function to adjust label display by comparing counts of "low" and "medium"
def get_adjusted_counts(attribute):
    # Count occurrences of each value for each grade
    grade_counts = df.groupby(['Grade'])[attribute].value_counts().unstack().fillna(0)

    # Ensure labels are displayed correctly without unintended swaps
    grade_counts = grade_counts.reindex(columns=sorted(grade_counts.columns), fill_value=0)

    return grade_counts

# Loop through each attribute and create a bar chart
for attribute in attributes:
    plt.figure(figsize=(8, 6))

    # Get adjusted counts for proper label alignment
    grade_counts = get_adjusted_counts(attribute)

    # Generate the plot with different colors for each bar within a grade
    grade_counts.plot(kind='bar', stacked=False, ax=plt.gca(), color=colors[:len(grade_counts.columns)])

    # Set plot title and labels
    plt.title(f'Distribution of {attribute} by Grade')
    plt.xlabel('Grade')
    plt.ylabel('Count')
    plt.legend(title=attribute)
    plt.xticks(rotation=0)
    plt.show()