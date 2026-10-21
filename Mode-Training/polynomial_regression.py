import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error
)

# 1. Load dataset
df = pd.read_csv("sat_gpa.csv")

print("First 5 rows:")
print(df.head())

print("\nDataset shape:", df.shape)

# 2. Define input and target
X = df[["SAT"]]
y = df["GPA"]

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Compare polynomial degrees
degrees = [1, 2, 3]
comparison = []

for degree in degrees:

    if degree == 1:
        model_poly = LinearRegression()
    else:
        model_poly = Pipeline([
            ("poly", PolynomialFeatures(degree=degree)),
            ("linear", LinearRegression())
        ])

    # Train model
    model_poly.fit(X_train, y_train)

    # Predictions
    train_pred = model_poly.predict(X_train)
    test_pred = model_poly.predict(X_test)

    # R²
    train_r2 = r2_score(y_train, train_pred)
    test_r2 = r2_score(y_test, test_pred)

    # RMSE
    train_rmse = np.sqrt(
        mean_squared_error(y_train, train_pred)
    )
    test_rmse = np.sqrt(
        mean_squared_error(y_test, test_pred)
    )

    # MAE
    train_mae = mean_absolute_error(y_train, train_pred)
    test_mae = mean_absolute_error(y_test, test_pred)

    comparison.append({
        "Degree": degree,
        "Training R2": train_r2,
        "Testing R2": test_r2,
        "Training RMSE": train_rmse,
        "Testing RMSE": test_rmse,
        "Training MAE": train_mae,
        "Testing MAE": test_mae
    })

# 5. Display comparison
comparison_df = pd.DataFrame(comparison)

print("\nPolynomial Regression Comparison:")
print(comparison_df.round(4).to_string(index=False))


# 6. Best model based on Testing R²
best_degree = comparison_df.loc[
    comparison_df["Testing R2"].idxmax(),
    "Degree"
]

best_r2 = comparison_df["Testing R2"].max()

print("\nBest Degree:", int(best_degree))
print("Best Testing R²:", round(best_r2, 4))


# 7. Train Degree 1 model for Actual vs Predicted graph
best_model = LinearRegression()
best_model.fit(X_train, y_train)

test_pred = best_model.predict(X_test)

# Calculate R² for graph
r2 = r2_score(y_test, test_pred)

print("Degree 1 Testing R²:", round(r2, 4))


# 8. Actual vs Predicted GPA
import matplotlib.pyplot as plt

plt.scatter(y_test, test_pred)

plt.xlabel("Actual GPA")
plt.ylabel("Predicted GPA")
plt.title(f"Actual vs Predicted GPA - R² = {r2:.4f}")

plt.grid(True)
plt.show()