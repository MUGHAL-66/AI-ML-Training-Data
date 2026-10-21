# Matplotlib.ipynb — all code cells
# Copy/paste this file into VS Code and run ONE CELL BLOCK at a time.
# The original notebook code is preserved; only cell separator comments were added.


##############################################################################
# CODE CELL 1
# ########################################################################
# Install if needed:
# !pip install matplotlib pandas numpy scikit-learn

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("Matplotlib version:", plt.matplotlib.__version__)

##############################################################################
# CODE CELL 2
# ########################################################################
x = [1, 2, 3, 4, 5]
y = [10, 15, 13, 20, 25]

plt.plot(x, y)
plt.show()

##############################################################################
# CODE CELL 3
# ########################################################################
plt.plot(x, y)

plt.title("Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True)

plt.show()

##############################################################################
# CODE CELL 4
# ########################################################################
plt.plot(
    x, y,
    marker="o",
    linestyle="--",
    linewidth=2,
    label="Sales"
)

plt.title("Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.legend()
plt.grid(True)
plt.show()

##############################################################################
# CODE CELL 5
# ########################################################################
months = [1, 2, 3, 4, 5]
sales_a = [10, 15, 13, 20, 25]
sales_b = [8, 12, 16, 18, 23]

plt.plot(months, sales_a, marker="o", label="Product A")
plt.plot(months, sales_b, marker="s", label="Product B")

plt.title("Product Sales Comparison")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.legend()
plt.grid(True)
plt.show()

##############################################################################
# CODE CELL 6
# ########################################################################
departments = ["IT", "HR", "Finance", "Sales"]
employees = [40, 20, 25, 35]

plt.bar(departments, employees)

plt.title("Employees by Department")
plt.xlabel("Department")
plt.ylabel("Employees")
plt.show()

##############################################################################
# CODE CELL 7
# ########################################################################
plt.barh(departments, employees)

plt.title("Employees by Department")
plt.xlabel("Employees")
plt.ylabel("Department")
plt.show()

##############################################################################
# CODE CELL 8
# ########################################################################
departments = ["IT", "HR", "Finance"]
male = [25, 10, 15]
female = [15, 20, 10]

pos = np.arange(len(departments))
width = 0.35

plt.bar(pos - width/2, male, width, label="Male")
plt.bar(pos + width/2, female, width, label="Female")

plt.xticks(pos, departments)
plt.ylabel("Employees")
plt.title("Employees by Department and Gender")
plt.legend()
plt.show()

##############################################################################
# CODE CELL 9
# ########################################################################
age = np.array([20, 22, 25, 28, 30, 35, 40, 45])
salary = np.array([35, 38, 45, 50, 55, 65, 75, 90])

plt.scatter(age, salary)

plt.title("Age vs Salary")
plt.xlabel("Age")
plt.ylabel("Salary")
plt.grid(True)
plt.show()

##############################################################################
# CODE CELL 10
# ########################################################################
rng = np.random.default_rng(42)
salary = rng.normal(60000, 12000, 500)

plt.hist(salary, bins=20)

plt.title("Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Frequency")
plt.show()

##############################################################################
# CODE CELL 11
# ########################################################################
plt.hist(salary, bins=20, density=True)

plt.title("Salary Distribution Density")
plt.xlabel("Salary")
plt.ylabel("Density")
plt.show()

##############################################################################
# CODE CELL 12
# ########################################################################
data = [45, 50, 52, 55, 58, 60, 62, 65, 100]

plt.boxplot(data)

plt.title("Box Plot")
plt.ylabel("Value")
plt.show()

##############################################################################
# CODE CELL 13
# ########################################################################
labels = ["IT", "HR", "Finance", "Sales"]
values = [40, 20, 25, 35]

plt.pie(
    values,
    labels=labels,
    autopct="%1.1f%%"
)

plt.title("Department Distribution")
plt.show()

##############################################################################
# CODE CELL 14
# ########################################################################
fig, ax = plt.subplots()

ax.plot(x, y, marker="o")
ax.set_title("Sales")
ax.set_xlabel("Month")
ax.set_ylabel("Sales")
ax.grid(True)

plt.show()

##############################################################################
# CODE CELL 15
# ########################################################################
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].plot(x, y, marker="o")
axes[0].set_title("Line Plot")

axes[1].bar(departments, employees)
axes[1].set_title("Bar Plot")

plt.tight_layout()
plt.show()

##############################################################################
# CODE CELL 16
# ########################################################################
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0, 0].plot(x, y)
axes[0, 0].set_title("Line")

axes[0, 1].bar(departments, employees)
axes[0, 1].set_title("Bar")

axes[1, 0].scatter(age, salary)
axes[1, 0].set_title("Scatter")

axes[1, 1].hist(salary, bins=15)
axes[1, 1].set_title("Histogram")

plt.tight_layout()
plt.show()

##############################################################################
# CODE CELL 17
# ########################################################################
x = np.array([1,2,3,4,5])
y = np.array([10,15,13,20,25])

plt.plot(x, y, marker="o")

plt.annotate(
    "Highest",
    xy=(5, 25),
    xytext=(3.5, 22),
    arrowprops={"arrowstyle": "->"}
)

plt.show()

##############################################################################
# CODE CELL 18
# ########################################################################
plt.plot(x, y)

plt.xlim(1, 5)
plt.ylim(0, 30)

plt.title("Controlled Axis Range")
plt.show()

##############################################################################
# CODE CELL 19
# ########################################################################
months = np.arange(1, 7)
sales = [20, 25, 30, 35, 40, 45]
profit = [2, 3, 4, 5, 6, 8]

fig, ax1 = plt.subplots()

ax1.plot(months, sales, marker="o")
ax1.set_xlabel("Month")
ax1.set_ylabel("Sales")

ax2 = ax1.twinx()
ax2.plot(months, profit, marker="s", linestyle="--")
ax2.set_ylabel("Profit")

plt.title("Sales and Profit")
plt.show()

##############################################################################
# CODE CELL 20
# ########################################################################
data = np.array([
    [1.0, 0.8, 0.2],
    [0.8, 1.0, 0.4],
    [0.2, 0.4, 1.0]
])

plt.imshow(data, aspect="auto")
plt.colorbar()

plt.xticks(range(3), ["Age", "Salary", "Experience"])
plt.yticks(range(3), ["Age", "Salary", "Experience"])

plt.title("Correlation Matrix")
plt.show()

##############################################################################
# CODE CELL 21
# ########################################################################
actual = np.array([100, 120, 130, 150, 170])
predicted = np.array([105, 115, 128, 145, 175])

plt.scatter(actual, predicted)

# Ideal prediction line
minimum = min(actual.min(), predicted.min())
maximum = max(actual.max(), predicted.max())

plt.plot([minimum, maximum], [minimum, maximum], linestyle="--")

plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("Actual vs Predicted")
plt.grid(True)
plt.show()

##############################################################################
# CODE CELL 22
# ########################################################################
residuals = actual - predicted

plt.scatter(predicted, residuals)
plt.axhline(0, linestyle="--")

plt.xlabel("Predicted")
plt.ylabel("Residual")
plt.title("Residual Plot")
plt.grid(True)
plt.show()

##############################################################################
# CODE CELL 23
# ########################################################################
from sklearn.metrics import confusion_matrix

y_true = [0, 0, 0, 1, 1, 1, 1, 0]
y_pred = [0, 1, 0, 1, 1, 0, 1, 0]

cm = confusion_matrix(y_true, y_pred)

plt.imshow(cm)
plt.colorbar()

plt.xticks([0, 1], ["Pred 0", "Pred 1"])
plt.yticks([0, 1], ["Actual 0", "Actual 1"])

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, cm[i, j], ha="center", va="center")

plt.title("Confusion Matrix")
plt.show()

##############################################################################
# CODE CELL 24
# ########################################################################
epochs = np.arange(1, 11)
train_loss = [0.90, 0.70, 0.55, 0.45, 0.37, 0.31, 0.27, 0.24, 0.22, 0.20]
val_loss = [0.95, 0.76, 0.62, 0.54, 0.49, 0.47, 0.48, 0.50, 0.53, 0.56]

plt.plot(epochs, train_loss, marker="o", label="Training Loss")
plt.plot(epochs, val_loss, marker="s", label="Validation Loss")

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training vs Validation Loss")
plt.legend()
plt.grid(True)
plt.show()

##############################################################################
# CODE CELL 25
# ########################################################################
features = ["Age", "Income", "Experience", "Education"]
importance = [0.15, 0.45, 0.30, 0.10]

plt.barh(features, importance)

plt.xlabel("Importance")
plt.title("Feature Importance")
plt.show()

##############################################################################
# CODE CELL 26
# ########################################################################
plt.plot(x, y, marker="o")
plt.title("Sales Trend")

# Save as PNG
plt.savefig("sales_trend.png", dpi=300, bbox_inches="tight")

plt.show()

##############################################################################
# CODE CELL 27
# ########################################################################
fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(
    x, y,
    marker="o",
    linewidth=2,
    alpha=0.8,
    label="Sales"
)

ax.set_title("Professional-Style Sales Plot")
ax.set_xlabel("Month")
ax.set_ylabel("Sales")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
