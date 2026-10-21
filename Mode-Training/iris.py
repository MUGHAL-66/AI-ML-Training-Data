import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. Load Dataset
df = pd.read_csv("iris_binary_class.csv")

print("First 5 rows:")
print(df.head())

# 2. Check Dataset
print("\nDataset Shape:")
print(df.shape)

print("\nClass Distribution:")
print(df["species"].value_counts())

# 3. Separate Features and Target
X = df[[
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width"
]]

y = df["species"]

# 4. Convert Target into 0 and 1
y = y.map({
    "setosa": 0,
    "versicolor": 1
})

# 5. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Data:", X_train.shape)
print("Testing Data:", X_test.shape)

# 6. Feature Scaling
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 7. Create Logistic Regression Model
model = LogisticRegression()

# 8. Train Model
model.fit(X_train_scaled, y_train)

# 9. Prediction
y_pred = model.predict(X_test_scaled)

# 10. Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)
print("Accuracy (%):", accuracy * 100)

# 11. Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

# 12. Classification Report
print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["setosa", "versicolor"]
))

# 13. Actual vs Predicted
result = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": y_pred
})

result["Actual"] = result["Actual"].map({
    0: "setosa",
    1: "versicolor"
})

result["Predicted"] = result["Predicted"].map({
    0: "setosa",
    1: "versicolor"
})

print("\nActual vs Predicted:")
print(result)