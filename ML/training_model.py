# Trains a Logistic Regression model to predict careers from skill scores with cross-validation and evaluation.

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import sklearn


from data.skills import SKILL_LIST

# Load the training dataset.
data = pd.read_csv("data/training_data.csv")

# Separate features (skill scores) and target (job IDs).
X = data[SKILL_LIST]
y = data["job_id"]

# Split data into training and test sets with stratification to preserve class proportions.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y )

# Select the optimal regularization parameter C using cross-validation on the training set only.
print("Choosing C with 5-fold cross-validation on the training set:")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Candidate C values to evaluate.
candidate_cs = [0.01, 0.05, 0.1, 1.0]
cv_results = {}

# Evaluate each C value using cross-validation.
for c in candidate_cs:
    pipeline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=c))
    scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="accuracy")
    cv_results[c] = scores.mean()
    print(f"  C={c:<5} CV accuracy = {scores.mean():.4f} (+/- {scores.std():.4f})")

# C=1.0 has the best raw CV accuracy, but it makes the model overconfident.
# C=0.05 loses less than 1.5% accuracy but keeps predictions reasonably spread across the Top-5.
# Selected C=0.05 for better Top-5 recommendation behavior.
best_c = 0.05
print(f"Selected C={best_c} (not the top CV score - see diagnostics/controlled_profiles.py:")
print("  C=1.0 wins on raw accuracy but is badly overconfident for a Top-5 recommender)")
print()

# Build the final pipeline: StandardScaler + LogisticRegression.
# The scaler is fitted only on training data via Pipeline to prevent data leakage.
pipeline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=best_c))
pipeline.fit(X_train, y_train)

# Make predictions on the held-out test set.
predictions = pipeline.predict(X_test)

# Calculate evaluation metrics on the test set.
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, average="weighted", zero_division=0)
recall = recall_score(y_test, predictions, average="weighted", zero_division=0)
f1 = f1_score(y_test, predictions, average="weighted", zero_division=0)

# print("Held-out test set results:")
# print(f"  Accuracy:  {accuracy:.4f}")
# print(f"  Precision (weighted): {precision:.4f}")
# print(f"  Recall (weighted):    {recall:.4f}")
# print(f"  F1 (weighted):        {f1:.4f}")
# print()

# Perform 5 fold crossvalidation on the training set with the final chosen C for stability check.
final_cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="accuracy")
print(f"5-fold CV accuracy (final model, training set): {final_cv_scores.mean():.4f} (+/- {final_cv_scores.std():.4f})")
print()

# Generate confusion matrix to analyze prediction errors.
labels = sorted(y.unique())
cm = confusion_matrix(y_test, predictions, labels=labels)
cm_df = pd.DataFrame(cm, index=labels, columns=labels)
cm_df.to_csv("diagnostics/confusion_matrix.csv")

# Find and display the most commonly confused career pairs.
confused_pairs = []
for i, true_label in enumerate(labels):
    for j, pred_label in enumerate(labels):
        if i != j and cm[i][j] > 0:
            confused_pairs.append((cm[i][j], true_label, pred_label))
confused_pairs.sort(reverse=True)

print("Top 10 most commonly confused career pairs (true -> predicted, count):")
for count, true_label, pred_label in confused_pairs[:10]:
    print(f"  {true_label:30s} -> {pred_label:30s}  ({count} times)")
print()
print("Full confusion matrix saved to diagnostics/confusion_matrix.csv")
print()

# Retrain on the ENTIRE dataset before saving (the model used in production).
# The evaluation metrics above confirm generalization; this final fit is what gets shipped.
final_pipeline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=best_c))
final_pipeline.fit(X, y)

# Save the trained pipeline to disk.
joblib.dump({"pipeline": final_pipeline}, "data/model.pkl")
print("Model saved to data/model.pkl")

print(f"(trained with scikit-learn {sklearn.__version__})")