import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("CreditScore.csv")

print(df.shape)
print(df.head())
print(df.info())


#Missing Values..............#

missing = df.isnull().sum()

print(missing)
print((missing / len(df) * 100).round(2))

#  4. Duplicate Records........................

print("Duplicate rows:", df.duplicated().sum())

#.......5. Check Data Types

print(df.dtypes)


#.....  Categorical Values....
categorical_cols = df.select_dtypes(include="object").columns
numerical_cols = df.select_dtypes(include=np.number).columns

print("Categorical:", categorical_cols)
print("Numerical:", numerical_cols)

#...Target Variable Distribution

print(df["SeriousDlqin2yrs"].value_counts())

sns.countplot(data=df, x="SeriousDlqin2yrs")
plt.title("Distribution of Serious Delinquency")
plt.show()


#.......Percentage of Serious Delinquency

print(df["SeriousDlqin2yrs"].value_counts(normalize=True) * 100)

#......Univariate Analysis of Numerical Features

sns.histplot(df["Age"], bins=30, kde=True)
plt.title("Age Distribution")
plt.show()

#...............Boxplot

sns.boxplot(x=df["Age"])
plt.title("Age Boxplot")
plt.show()


print(df[df["Age"] <= 0])
print(df[df["Age"] > 100])

#.........8. Monthly Income

sns.histplot(df["MonthlyIncome"], bins=50, kde=True)
plt.title("Monthly Income Distribution")
plt.show()

sns.boxplot(x=df["MonthlyIncome"])
plt.show()

#.............9. Debt Ratio

sns.histplot(df["DebtRatio"], bins=50, kde=True)
plt.title("Debt Ratio Distribution")
plt.show()

sns.boxplot(x=df["DebtRatio"])
plt.show()


#...............10. Revolving Utilization

sns.histplot(df["RevolvingUtilizationOfUnsecuredLines"], bins=50)
plt.show()

sns.boxplot(x=df["RevolvingUtilizationOfUnsecuredLines"])
plt.show()


#.........11. Categorical Variable — Gender

print(df["Gender"].value_counts(dropna=False))

sns.countplot(data=df, x="Gender")
plt.title("Gender Distribution")
plt.show()


#.............. Age vs SeriousDlqin2yrs

sns.boxplot(data=df, x="SeriousDlqin2yrs", y="Age")
plt.title("Age vs SeriousDlqin2yrs")
plt.show()

#.............MonthlyIncome vs SeriousDlqin2yrs

sns.boxplot(
    data=df,
    x="SeriousDlqin2yrs",
    y="MonthlyIncome"
)

plt.ylim(0, df["MonthlyIncome"].quantile(0.99))
plt.title("Monthly Income vs SeriousDlqin2yrs")
plt.show()

#............. DebtRatio vs SeriousDlqin2yrs

sns.boxplot(
    data=df,
    x="SeriousDlqin2yrs",
    y="DebtRatio"
)

plt.ylim(0, df["DebtRatio"].quantile(0.99))
plt.title("DebtRatio vs SeriousDlqin2yrs")
plt.show()

#.........13. Correlation Matrix

corr = df.select_dtypes(include=np.number).corr()

plt.figure(figsize=(12, 8))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix")
plt.show()

#...............15. Cleaning Decisions

df_clean = df.copy()

df_clean["MonthlyIncome"] = df_clean["MonthlyIncome"].fillna(
    df_clean["MonthlyIncome"].median()
)

#................NumberOfDependents

df_clean["NumberOfDependents"] = df_clean["NumberOfDependents"].fillna(
    df_clean["NumberOfDependents"].median()
)

#.............Gender

df_clean = df_clean.drop(columns=["Gender"])

#.............16. Age Cleaning

df_clean.loc[df_clean["Age"] <= 0, "Age"] = np.nan
df_clean["Age"] = df_clean["Age"].fillna(df_clean["Age"].median())

