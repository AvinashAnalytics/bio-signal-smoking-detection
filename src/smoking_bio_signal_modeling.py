# Import necessary libraries
import pandas as pd
import joblib  # For saving models
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

# Load the dataset
df = pd.read_csv('smoking.csv')

# Data cleaning and preparation
df = df.drop(columns=['ID', 'oral'])  # Drop irrelevant columns
df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})  # Encoding categorical variables

# Selecting features and target variable
x = df[['gender', 'Gtp', 'hemoglobin', 'triglyceride', 'height(cm)', 'age', 'waist(cm)', 'weight(kg)', 'HDL', 'fasting blood sugar', 'LDL', 'systolic', 'ALT', 'relaxation', 'serum creatinine']]
y = df['smoking']

# Split into train and test sets (80% train, 20% test)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Standardizing the features
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

# Train Logistic Regression model
lr = LogisticRegression()

# Cross-validation to get a better estimate of the performance
cv_scores = cross_val_score(lr, x_train, y_train, cv=5, scoring='accuracy')
print(f"Logistic Regression CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# Fit the Logistic Regression model
lr.fit(x_train, y_train)
y_pred = lr.predict(x_test)

# Print Logistic Regression results
print(f"Logistic Regression Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save the trained Logistic Regression model
joblib.dump(lr, 'logistic_regression_model.pkl')

# Hyperparameter tuning for Decision Tree using GridSearchCV
dt = DecisionTreeClassifier()

param_grid = {
    'max_depth': [3, 5, 7, 10, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# GridSearchCV for Decision Tree
grid_search = GridSearchCV(dt, param_grid, cv=5, n_jobs=-1, scoring='accuracy')
grid_search.fit(x_train, y_train)

print(f"Best Hyperparameters for Decision Tree: {grid_search.best_params_}")

# Train Decision Tree with the best hyperparameters
best_dt = grid_search.best_estimator_

# Fit the best Decision Tree model and evaluate
best_dt.fit(x_train, y_train)
y_pred = best_dt.predict(x_test)

print(f"Decision Tree Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save the best Decision Tree model
joblib.dump(best_dt, 'decision_tree_model.pkl')

# Bagging Classifier for better performance (Boosting the model using ensemble)
bagging_clf = BaggingClassifier(DecisionTreeClassifier(), n_estimators=1000)

# Train the Bagging model
bagging_clf.fit(x_train, y_train)

# Evaluate performance
y_pred = bagging_clf.predict(x_test)

print(f"Bagging Classifier Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save the Bagging Classifier model
joblib.dump(bagging_clf, 'bagging_classifier_model.pkl')
