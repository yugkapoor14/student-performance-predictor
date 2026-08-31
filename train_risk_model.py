import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("/home/claude/project/data/students_cleaned.csv")

# Define "at-risk" as average_score < 60
df["at_risk"] = (df["average_score"] < 60).astype(int)
print("At-risk distribution:\n", df["at_risk"].value_counts())

cat_cols = ["gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]
X = df[cat_cols]
y = df["at_risk"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
])

model = Pipeline([
    ("prep", preprocessor),
    ("rf", RandomForestClassifier(n_estimators=300, max_depth=6, random_state=42, class_weight="balanced"))
])

model.fit(X_train, y_train)
preds = model.predict(X_test)

acc = accuracy_score(y_test, preds)
print(f"\nAccuracy: {acc:.3f}")
print("\nClassification report:\n", classification_report(y_test, preds))

ohe = model.named_steps["prep"].named_transformers_["cat"]
feature_names = ohe.get_feature_names_out(cat_cols)
importances = model.named_steps["rf"].feature_importances_
imp_df = pd.DataFrame({"feature": feature_names, "importance": importances}).sort_values("importance", ascending=False)
print("\nTop features:\n", imp_df.head(8).to_string(index=False))

joblib.dump(model, "/home/claude/project/app/risk_model.pkl")
print("\nModel saved as risk_model.pkl")
