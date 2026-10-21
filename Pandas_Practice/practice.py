# Import the main libraries used throughout this notebook
import pandas as pd
import numpy as np

# Optional: display more columns when working with wider DataFrames
pd.set_option('display.max_columns', None)

print("Pandas version:", pd.__version__)
print("NumPy version:", np.__version__)

# Create a DataFrame from a dictionary
df = pd.DataFrame({
    'Name': ['Ali', 'Sara', 'Ahmed', 'Ayesha', 'Bilal'],
    'Age': [25, 30, 28, 35, 22],
    'Salary': [50000, 70000, 60000, 90000, 45000],
    'Department': ['IT', 'HR', 'IT', 'Finance', 'HR']
})

df