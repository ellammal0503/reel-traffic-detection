import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load CSV
data = pd.read_csv("sample_packets.csv")  # Replace with dataset
X = data.drop(columns=["label"])
y = data["label"]

# Train/Val Split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, shuffle=True, stratify=y)

# Train model
clf = GradientBoostingClassifier()
clf.fit(X_train, y_train)

# Evaluate
pred = clf.predict(X_val)
print(classification_report(y_val, pred))

# Save model
joblib.dump(clf, "video_classifier.pkl")
print("✅ Model saved at video_classifier.pkl")
