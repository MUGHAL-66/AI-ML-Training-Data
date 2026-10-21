# ============================================================
# KNN REGRESSION - KING COUNTY HOUSE PRICE DATASET
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ============================================================
# STEP 1: Load Dataset
# ============================================================

df = pd.read_csv("KC_House_Data.csv")

print("\n========================================")
print("DATASET LOADED")
print("========================================")

print("Dataset Shape:", df.shape)

print("\nFirst 5 Rows:")
print(df.head())


# ============================================================
# STEP 2: Dataset Information
# ============================================================

print("\n========================================")
print("DATASET INFORMATION")
print("========================================")

print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ============================================================
# STEP 3: Remove Duplicate Rows
# ============================================================

df = df.drop_duplicates()

print("\nShape after removing duplicates:")
print(df.shape)


# ============================================================
# STEP 4: Date Handling
# ============================================================

# Convert date column into datetime

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

# Extract useful information from date

df["sale_year"] = df["date"].dt.year
df["sale_month"] = df["date"].dt.month
df["sale_day"] = df["date"].dt.day

# Drop original date column

df = df.drop("date", axis=1)

print("\nDate converted successfully!")

print("\nNew date-related columns:")
print(df[["sale_year", "sale_month", "sale_day"]].head())


# ============================================================
# STEP 5: Remove ID Column
# ============================================================

# ID is only an identifier.
# It should not be used for prediction.

if "id" in df.columns:
    df = df.drop("id", axis=1)

print("\nID column removed.")


# ============================================================
# STEP 6: Target and Features
# ============================================================

# Target variable

y = df["price"]

# Features

X = df.drop("price", axis=1)


print("\n========================================")
print("FEATURES AND TARGET")
print("========================================")

print("X Shape:", X.shape)
print("y Shape:", y.shape)

print("\nFeatures:")
print(X.columns.tolist())

print("\nTarget: price")


# ============================================================
# STEP 7: Handle Zipcode
# ============================================================

# Zipcode is categorical.
# We convert it into dummy variables instead of treating
# zipcode as a continuous numerical value.

if "zipcode" in X.columns:

    X["zipcode"] = X["zipcode"].astype(str)

    X = pd.get_dummies(
        X,
        columns=["zipcode"],
        drop_first=True
    )

print("\nZipcode converted into dummy variables.")


# ============================================================
# STEP 8: Check Missing Values Again
# ============================================================

print("\nMissing values after preprocessing:")
print(X.isnull().sum().sum())


# ============================================================
# STEP 9: Train/Test Split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\n========================================")
print("TRAIN TEST SPLIT")
print("========================================")

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)


# ============================================================
# STEP 10: Feature Scaling / Normalization
# ============================================================

# KNN is distance-based.
# Therefore, scaling is very important.

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)

print("\nFeature scaling completed.")


# ============================================================
# STEP 11: Test Different K Values
# ============================================================

k_values = [1, 3, 5, 7, 9, 11, 15, 20]

rmse_scores = []
mae_scores = []
r2_scores = []


print("\n========================================")
print("TESTING DIFFERENT K VALUES")
print("========================================")

for k in k_values:

    knn = KNeighborsRegressor(
        n_neighbors=k,
        weights="uniform"
    )

    knn.fit(
        X_train_scaled,
        y_train
    )

    y_pred_k = knn.predict(
        X_test_scaled
    )

    mae = mean_absolute_error(
        y_test,
        y_pred_k
    )

    mse = mean_squared_error(
        y_test,
        y_pred_k
    )

    rmse = np.sqrt(mse)

    r2 = r2_score(
        y_test,
        y_pred_k
    )

    mae_scores.append(mae)
    rmse_scores.append(rmse)
    r2_scores.append(r2)

    print(
        f"K = {k:2d} | "
        f"MAE = {mae:,.2f} | "
        f"RMSE = {rmse:,.2f} | "
        f"R² = {r2:.4f}"
    )


# ============================================================
# STEP 12: Find Best K
# ============================================================

best_index = np.argmin(rmse_scores)

best_k = k_values[best_index]

best_rmse = rmse_scores[best_index]

print("\n========================================")
print("BEST K")
print("========================================")

print("Best K:", best_k)
print(f"Best RMSE: {best_rmse:,.2f}")


# ============================================================
# STEP 13: Plot K vs RMSE
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    k_values,
    rmse_scores,
    marker="o"
)

plt.xlabel("Number of Neighbors (K)")
plt.ylabel("RMSE")
plt.title("KNN Regression - K Value vs RMSE")

plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()


# ============================================================
# STEP 14: Train Final KNN Model
# ============================================================

final_model = KNeighborsRegressor(
    n_neighbors=best_k,
    weights="uniform"
)

final_model.fit(
    X_train_scaled,
    y_train
)

print("\nFinal KNN model trained successfully!")


# ============================================================
# STEP 15: Make Final Predictions
# ============================================================

y_pred = final_model.predict(
    X_test_scaled
)


# ============================================================
# STEP 16: Calculate Evaluation Metrics
# ============================================================

mae = mean_absolute_error(
    y_test,
    y_pred
)

mse = mean_squared_error(
    y_test,
    y_pred
)

rmse = np.sqrt(mse)

r2 = r2_score(
    y_test,
    y_pred
)


# ============================================================
# STEP 17: Display Model Performance
# ============================================================

print("\n========================================")
print("FINAL KNN REGRESSION PERFORMANCE")
print("========================================")

print(f"\nBest K: {best_k}")

print(f"MAE  : {mae:,.2f}")

print(f"MSE  : {mse:,.2f}")

print(f"RMSE : {rmse:,.2f}")

print(f"R²   : {r2:.4f}")

print(f"R² Percentage: {r2 * 100:.2f}%")


# ============================================================
# STEP 18: Actual vs Predicted DataFrame
# ============================================================

results = pd.DataFrame({
    "Actual_Price": y_test.values,
    "Predicted_Price": y_pred
})

results["Prediction_Error"] = (
    results["Actual_Price"]
    - results["Predicted_Price"]
)

print("\n========================================")
print("ACTUAL VS PREDICTED")
print("========================================")

print(results.head(20))


# ============================================================
# STEP 19: Actual vs Predicted Graph
# ============================================================

plt.figure(figsize=(8, 6))

plt.scatter(
    y_test,
    y_pred,
    alpha=0.5
)

# Perfect prediction line

min_value = min(
    y_test.min(),
    y_pred.min()
)

max_value = max(
    y_test.max(),
    y_pred.max()
)

plt.plot(
    [min_value, max_value],
    [min_value, max_value],
    linestyle="--",
    linewidth=2
)

plt.xlabel("Actual House Price")
plt.ylabel("Predicted House Price")

plt.title(
    f"Actual vs Predicted House Prices (K={best_k})"
)

plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()


# ============================================================
# STEP 20: Prediction Error / Residual
# ============================================================

residuals = (
    y_test.values
    - y_pred
)

plt.figure(figsize=(8, 6))

plt.scatter(
    y_pred,
    residuals,
    alpha=0.5
)

# Zero error reference line

plt.axhline(
    y=0,
    linestyle="--",
    linewidth=2
)

plt.xlabel("Predicted House Price")
plt.ylabel("Prediction Error")

plt.title(
    f"Prediction Error / Residual Plot (K={best_k})"
)

plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()


# ============================================================
# STEP 21: Error Distribution
# ============================================================

plt.figure(figsize=(8, 5))

sns.histplot(
    residuals,
    kde=True
)

plt.xlabel("Prediction Error")
plt.ylabel("Frequency")

plt.title("Distribution of Prediction Errors")

plt.tight_layout()
plt.show()


# ============================================================
# STEP 22: Save Results
# ============================================================

results.to_csv(
    "KNN_house_price_predictions.csv",
    index=False
)

print("\nPrediction results saved as:")
print("KNN_house_price_predictions.csv")


# ============================================================
# STEP 23: Final Message
# ============================================================

print("\n========================================")
print("KNN REGRESSION COMPLETED")
print("========================================")

print(f"Best K       : {best_k}")
print(f"MAE          : {mae:,.2f}")
print(f"MSE          : {mse:,.2f}")
print(f"RMSE         : {rmse:,.2f}")
print(f"R²           : {r2:.4f}")
print(f"R² Percentage: {r2 * 100:.2f}%")