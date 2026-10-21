import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve
)


# ------------------------------------------------------------
# STEP 2: Define Column Names
# ------------------------------------------------------------

columns = [
    "id",
    "diagnosis",

    "radius_mean",
    "texture_mean",
    "perimeter_mean",
    "area_mean",
    "smoothness_mean",
    "compactness_mean",
    "concavity_mean",
    "concave_points_mean",
    "symmetry_mean",
    "fractal_dimension_mean",

    "radius_se",
    "texture_se",
    "perimeter_se",
    "area_se",
    "smoothness_se",
    "compactness_se",
    "concavity_se",
    "concave_points_se",
    "symmetry_se",
    "fractal_dimension_se",

    "radius_worst",
    "texture_worst",
    "perimeter_worst",
    "area_worst",
    "smoothness_worst",
    "compactness_worst",
    "concavity_worst",
    "concave_points_worst",
    "symmetry_worst",
    "fractal_dimension_worst"
]


# ------------------------------------------------------------
# STEP 3: Load Dataset
# ------------------------------------------------------------

df = pd.read_csv(
    "wdbc.data",
    header=None,
    names=columns
)

print("\nDataset loaded successfully!")
print("Shape:", df.shape)

print("\nFirst 5 rows:")
print(df.head())


# ------------------------------------------------------------
# STEP 4: Check Dataset Information
# ------------------------------------------------------------

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nDiagnosis Counts:")
print(df["diagnosis"].value_counts())


# ------------------------------------------------------------
# STEP 5: Remove ID Column
# ------------------------------------------------------------

X = df.drop(["id", "diagnosis"], axis=1)

y = df["diagnosis"]


# ------------------------------------------------------------
# STEP 6: Convert Target B/M into 0/1
# ------------------------------------------------------------

# B = Benign = 0
# M = Malignant = 1

y = y.map({
    "B": 0,
    "M": 1
})

print("\nTarget after conversion:")
print(y.value_counts())


# ------------------------------------------------------------
# STEP 7: Train/Test Split
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)


# ------------------------------------------------------------
# STEP 8: Feature Scaling
# ------------------------------------------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)


# ------------------------------------------------------------
# STEP 9: Create Logistic Regression Model
# ------------------------------------------------------------

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)


# ------------------------------------------------------------
# STEP 10: Train Model
# ------------------------------------------------------------

model.fit(X_train_scaled, y_train)

print("\nLogistic Regression model trained successfully!")


# ------------------------------------------------------------
# STEP 11: Make Predictions
# ------------------------------------------------------------

y_pred = model.predict(X_test_scaled)

# Probability of malignant class
y_probability = model.predict_proba(X_test_scaled)[:, 1]


# ------------------------------------------------------------
# STEP 12: Calculate Accuracy
# ------------------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n========================================")
print("MODEL PERFORMANCE")
print("========================================")

print(f"\nAccuracy: {accuracy:.4f}")
print(f"Accuracy Percentage: {accuracy * 100:.2f}%")


# ------------------------------------------------------------
# STEP 13: Classification Report
# ------------------------------------------------------------

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Benign", "Malignant"]
    )
)


# ------------------------------------------------------------
# STEP 14: Confusion Matrix
# ------------------------------------------------------------

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)


# ------------------------------------------------------------
# STEP 15: Confusion Matrix Graph
# ------------------------------------------------------------

plt.figure(figsize=(7, 5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Benign", "Malignant"],
    yticklabels=["Benign", "Malignant"]
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix - Logistic Regression")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# STEP 16: ROC-AUC Score
# ------------------------------------------------------------

roc_auc = roc_auc_score(
    y_test,
    y_probability
)

print(f"\nROC-AUC Score: {roc_auc:.4f}")


# ------------------------------------------------------------
# STEP 17: ROC Curve - 100% Reference
# ------------------------------------------------------------

fpr, tpr, thresholds = roc_curve(
    y_test,
    y_probability
)

plt.figure(figsize=(8, 6))

# ROC Curve
plt.plot(
    fpr,
    tpr,
    linewidth=2,
    label=f"Logistic Regression (AUC = {roc_auc:.4f})"
)

# 100% reference line
plt.axhline(
    y=1.0,
    linestyle="--",
    linewidth=2,
    label="100% TPR Reference"
)

# Random classifier reference
plt.plot(
    [0, 1],
    [0, 1],
    linestyle=":",
    label="Random Classifier"
)

plt.xlim(0, 1)
plt.ylim(0, 1.05)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Logistic Regression")

plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# STEP 18: Actual vs Predicted
# ------------------------------------------------------------

results = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": y_pred,
    "Malignant_Probability": y_probability
})


# Convert 0/1 back to readable labels

results["Actual"] = results["Actual"].map({
    0: "Benign",
    1: "Malignant"
})

results["Predicted"] = results["Predicted"].map({
    0: "Benign",
    1: "Malignant"
})


print("\n========================================")
print("ACTUAL VS PREDICTED")
print("========================================")

print(results.head(20))


# ------------------------------------------------------------
# STEP 19: Actual vs Predicted Class Distribution
# ------------------------------------------------------------

print("\n========================================")
print("ACTUAL VS PREDICTED CLASS DISTRIBUTION")
print("========================================")

comparison = pd.DataFrame({
    "Actual": pd.Series(y_test).value_counts().sort_index(),
    "Predicted": pd.Series(y_pred).value_counts().sort_index()
})

comparison.index = ["Benign", "Malignant"]

print(comparison)


# ------------------------------------------------------------
# STEP 20: Actual vs Predicted Class Distribution Graph
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

comparison.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.xlabel("Diagnosis")
plt.ylabel("Number of Samples")
plt.title("Actual vs Predicted Class Distribution")

plt.xticks(rotation=0)

plt.legend(
    title="Type"
)

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# STEP 21: Save Predictions to CSV
# ------------------------------------------------------------

results.to_csv(
    "actual_vs_predicted.csv",
    index=False
)

print("\nActual vs Predicted results saved as:")
print("actual_vs_predicted.csv")


# ------------------------------------------------------------
# STEP 22: Final Message
# ------------------------------------------------------------

print("\n========================================")
print("LOGISTIC REGRESSION COMPLETED")
print("========================================")