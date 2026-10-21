# ============================================================
# CELL 1: Import Libraries
# ============================================================

import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

print("Pandas version:", pd.__version__)
print("NumPy version:", np.__version__)


# ============================================================
# CELL 2: DataFrame from Dictionary
# ============================================================

df = pd.DataFrame({
    'Name': ['Ali', 'Sara', 'Ahmed', 'Ayesha', 'Bilal'],
    'Age': [25, 30, 28, 35, 22],
    'Salary': [50000, 70000, 60000, 90000, 45000],
    'Department': ['IT', 'HR', 'IT', 'Finance', 'HR']
})

print("\nDataFrame from Dictionary:")
print(df)


# ============================================================
# CELL 3: DataFrame from List of Lists
# ============================================================

df_list = pd.DataFrame(
    [
        ['Ali', 25, 50000],
        ['Sara', 30, 70000],
        ['Ahmed', 28, 60000]
    ],
    columns=['Name', 'Age', 'Salary']
)

print("\nDataFrame from List of Lists:")
print(df_list)


# ============================================================
# CELL 4: Pandas Series
# ============================================================

s = pd.Series(
    [10, 20, 30, 40, 50],
    name='Numbers'
)

print("\nPandas Series:")
print(s)


# ============================================================
# CELL 5: Reading Data Examples
# ============================================================

print("\nReading Data Examples:")

# CSV file read karne ke liye:
# csv_data = pd.read_csv('data.csv')
# print(csv_data)

# Excel file read karne ke liye:
# excel_data = pd.read_excel('data.xlsx')
# print(excel_data)

# JSON file read karne ke liye:
# json_data = pd.read_json('data.json')
# print(json_data)

# SQL data read karne ke liye:
# sql_data = pd.read_sql('SELECT * FROM customers', connection)
# print(sql_data)

# Clipboard se data read karne ke liye:
# clipboard_data = pd.read_clipboard()
# print(clipboard_data)

print("External file/database examples are commented.")
print("Required file available hone par comments remove kar sakte hain.")

# ============================================================
# CELL 6: Saving / Exporting Data
# ============================================================

# Save DataFrame to CSV
# df.to_csv('output.csv', index=False)

# Save DataFrame to Excel
# df.to_excel('output.xlsx', index=False)

# Save DataFrame to JSON
# df.to_json('output.json')

# Save DataFrame to SQL
# df.to_sql('customers', connection, if_exists='replace', index=False)

print("Export examples are commented so files are not overwritten accidentally.")


# ============================================================
# CELL 7: Understanding Your Data
# ============================================================

print("\n========== HEAD ==========")
print(df.head())

print("\n========== HEAD(3) ==========")
print(df.head(3))

print("\n========== TAIL ==========")
print(df.tail())

print("\n========== SHAPE ==========")
print("Rows and Columns:", df.shape)

print("\n========== COLUMNS ==========")
print(df.columns.tolist())

print("\n========== INDEX ==========")
print(df.index)

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== INFO ==========")
df.info()

print("\n========== DESCRIPTIVE STATISTICS ==========")
print(df.describe())

print("\n========== ALL COLUMN SUMMARY ==========")
print(df.describe(include='all'))

print("\n========== UNIQUE COUNTS ==========")
print(df.nunique())


# ============================================================
# CELL 8: Selecting Columns
# ============================================================

print("\n========== ONE COLUMN ==========")

# Select one column
print(df['Age'])

print("\n========== MULTIPLE COLUMNS ==========")

# Select multiple columns
print(df[['Name', 'Age', 'Salary']])

print("\n========== DOT NOTATION ==========")

# Dot notation
print(df.Age)


# ============================================================
# CELL 9: Selecting Rows with iloc and loc
# ============================================================

print("\n========== FIRST ROW ==========")

# Select first row by position
print(df.iloc[0])

print("\n========== FIRST FIVE ROWS ==========")

# Select first five rows
print(df.iloc[:5])

print("\n========== SPECIFIC ROWS ==========")

# Select rows 0, 2 and 4
print(df.iloc[[0, 2, 4]])

print("\n========== SPECIFIC CELL ==========")

# Row 0, Column 1
print("Cell at row 0, column 1:", df.iloc[0, 1])

print("\n========== LOC ==========")

# Select rows and columns by labels
print(df.loc[0:2, ['Name', 'Age']])


# ============================================================
# CELL 10: Filtering Data
# ============================================================

print("\n========== AGE > 25 ==========")

# Filter Age greater than 25
print(df[df['Age'] > 25])

print("\n========== SALARY > 50000 ==========")

# Filter Salary greater than 50,000
print(df[df['Salary'] > 50000])

print("\n========== AND CONDITION ==========")

# Both conditions must be true
print(
    df[
        (df['Age'] > 25) &
        (df['Salary'] > 50000)
    ]
)

print("\n========== OR CONDITION ==========")

# At least one condition must be true
print(
    df[
        (df['Age'] > 25) |
        (df['Salary'] > 50000)
    ]
)

print("\n========== NOT CONDITION ==========")

# NOT condition
print(
    df[
        ~(df['Age'] > 25)
    ]
)