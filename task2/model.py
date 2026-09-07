# ==========================================
# ARTIFICIAL INTELLIGENCE - PROJECT 2
# DATA CLASSIFICATION PIPELINE
# ==========================================

# 1. IMPORT NECESSARY LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, f1_score

# 2. LOAD THE RAW MATERIAL
print("Loading Iris dataset...")
iris = load_iris()
X = iris.data  
y = iris.target 

# 3. STRUCTURAL INTEGRITY: THE SPLIT
# 80% training, 20% testing, shuffled
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

# 4. THE GATEKEEPER RULE: SCALING
print("Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==========================================
# PART A: TUNING THE ENGINE (THE ELBOW METHOD)
# ==========================================
print("Running the Elbow Method to find optimal K...")
error_rates = []
k_range = range(1, 21)

for i in k_range:
    knn_temp = KNeighborsClassifier(n_neighbors=i)
    knn_temp.fit(X_train_scaled, y_train)
    predictions_temp = knn_temp.predict(X_test_scaled)
    error = np.mean(predictions_temp != y_test)
    error_rates.append(error)

# Plotting the Elbow Curve
plt.figure(figsize=(10, 6))
plt.plot(k_range, error_rates, color='blue', linestyle='dashed', marker='o',
         markerfacecolor='red', markersize=8)
plt.title('Error Rate vs. K Value')
plt.xlabel('K Value')
plt.ylabel('Error Rate')
plt.xticks(k_range)
plt.grid(True)
plt.show()  # Close the graph window to continue running the script

# ==========================================
# PART B: THE FINAL WORKFLOW & VALIDATION
# ==========================================
# Change 'optimal_k' to the best number you saw on your graph!
optimal_k = 5 

print(f"\nTraining final model with K={optimal_k}...")
final_model = KNeighborsClassifier(n_neighbors=optimal_k)
final_model.fit(X_train_scaled, y_train)

# Predict on the unseen test data
final_predictions = final_model.predict(X_test_scaled)

# Evaluate the Output
print("\n--- OUTPUT VALIDATION ---")
conf_matrix = confusion_matrix(y_test, final_predictions)
print("Confusion Matrix:")
print(conf_matrix)

# F1 Score using 'macro' average for multi-class
f1 = f1_score(y_test, final_predictions, average='macro')
print(f"\nF1 Score: {f1:.2f}")
print("Pipeline Complete!")
