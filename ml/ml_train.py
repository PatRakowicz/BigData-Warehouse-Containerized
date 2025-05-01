import mysql.connector
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

conn = mysql.connector.connect(
    host="mysql",
    user="freduser",
    password="fredpass",
    database="fred_data"
)

query = '''
SELECT date, indicator, value
FROM fred_data
WHERE indicator IN (
    'GDP', 'CPIAUCSL', 'UNRATE', 'FEDFUNDS',
    'RSXFS', 'INDPRO', 'PI', 'USRECM'
)
ORDER BY date ASC
'''
data = pd.read_sql(query, conn)
print(f"Loaded {len(df)} rows from MySQL")
print("Available indicators:", df['indicator'].unique())
conn.close()

data_pivot = data.pivot(index="date", columns="indicator", values="value")
data_pivot.columns.name = None
data_pivot = data_pivot.dropna()

data_pivot["UNRATE_FUTURE"] = data_pivot["UNRATE"].astype(float).shift(-3)

data_pivot = data_pivot.dropna()

for col in data_pivot.columns:
    if col not in ["UNRATE", "UNRATE_FUTURE"]:
        data_pivot[f"{col}_lag1"] = data_pivot[col].shift(1)
        data_pivot[f"{col}_lag2"] = data_pivot[col].shift(2)

data_pivot = data_pivot.dropna()

X = data_pivot.drop(columns=["UNRATE", "UNRATE_FUTURE"])
y = data_pivot["UNRATE_FUTURE"]

X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("=== Unemployment Forecast (3-Month Ahead) ===")
mse = mean_squared_error(y_test, y_pred)
print(f"RMSE: {np.sqrt(mse):.3f}")
print(f"R² Score: {r2_score(y_test, y_pred):.3f}")
