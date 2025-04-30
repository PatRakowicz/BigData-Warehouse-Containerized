import mysql.connector
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Connect to MySQL
conn = mysql.connector.connect(
    host="mysql",
    user="freduser",
    password="fredpass",
    database="fred_data"
)

# Fetch all data
query = """
SELECT date, indicator, value
FROM fred_data
WHERE indicator IN ('GDP', 'CPI', 'UNRATE', 'FEDFUNDS', 'RSXFS', 'INDPRO', 'PI', 'RECESSION')
ORDER BY date ASC
"""
df = pd.read_sql(query, conn)
conn.close()

# Pivot: rows = dates, columns = indicators
df_pivot = df.pivot(index="date", columns="indicator", values="value").dropna()

# Make sure RECESSION is binary (just in case)
df_pivot["RECESSION"] = df_pivot["RECESSION"].apply(lambda x: int(float(x)))

# Optional: Add lag features
for col in df_pivot.columns:
    if col != "RECESSION":
        df_pivot[f"{col}_lag1"] = df_pivot[col].shift(1)

df_pivot = df_pivot.dropna()

# Split
X = df_pivot.drop("RECESSION", axis=1)
y = df_pivot["RECESSION"]
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Output results
print("=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred))
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, digits=3))
