import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_csv("/home/claude/project/data/students_cleaned.csv")

cat_cols = ["gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]
X = df[cat_cols]
y = df["average_score"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
])

model = Pipeline([
    ("prep", preprocessor),
    ("rf", RandomForestRegressor(n_estimators=200, max_depth=6, random_state=42))
])

model.fit(X_train, y_train)
preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)
print(f"MAE: {mae:.2f}")
print(f"R2 Score: {r2:.3f}")

# Feature importance (post one-hot)
ohe = model.named_steps["prep"].named_transformers_["cat"]
feature_names = ohe.get_feature_names_out(cat_cols)
importances = model.named_steps["rf"].feature_importances_
imp_df = pd.DataFrame({"feature": feature_names, "importance": importances}).sort_values("importance", ascending=False)
print("\nTop features:\n", imp_df.head(10).to_string(index=False))

joblib.dump(model, "/home/claude/project/app/model.pkl")
print("\nModel saved.")
