import pandas as pd

df = pd.read_csv("/home/claude/project/data/students_performance.csv")
df.columns = [c.strip().lower().replace(" ", "_").replace("/", "_") for c in df.columns]
df["average_score"] = df[["math_score", "reading_score", "writing_score"]].mean(axis=1)

print("Shape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nMissing values:\n", df.isnull().sum())

print("\n--- Average score by test prep course ---")
print(df.groupby("test_preparation_course")["average_score"].mean().round(2))

print("\n--- Average score by parental education ---")
print(df.groupby("parental_level_of_education")["average_score"].mean().sort_values(ascending=False).round(2))

print("\n--- Average score by lunch type ---")
print(df.groupby("lunch")["average_score"].mean().round(2))

print("\n--- Average score by gender ---")
print(df.groupby("gender")["average_score"].mean().round(2))

print("\n--- Average score by race/ethnicity group ---")
print(df.groupby("race_ethnicity")["average_score"].mean().sort_values(ascending=False).round(2))

df.to_csv("/home/claude/project/data/students_cleaned.csv", index=False)
print("\nSaved cleaned dataset.")
