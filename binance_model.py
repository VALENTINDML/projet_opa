import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
from pathlib import Path

!where

# Charger les données Binance
# df = pd.read_csv("binance_trades_2025-07-05.csv")

today = datetime.datetime.now().strftime("%Y-%m-%d")
csv_path = Path(f"binance_trades_{today}.csv") # Mise en place d'un nouveau fichier charque jours si il existe

if csv_path.exist():
    df = pd.read_csv(csv_path)
    print(f"Le fichier {csv_path} à été chargé") # Condition pour entrainer le modele

# Nettoyage et conversion
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df.dropna(inplace=True)

# Créer la variable cible : le prix du prochain trade
df['next_price'] = df['price'].shift(-1)
df.dropna(inplace=True)

# Définir les features et la target
X = df[['price', 'quantity']]
y = df['next_price']

# Séparer les données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner un modèle de régression
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Évaluer le modèle
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("RMSE:", rmse)
print("R2 Score:", r2)

# Sauvegarder le modèle pour l'utiliser plus tard dans une API
joblib.dump(model, "model.pkl")
print("✅ Modèle enregistré sous model.pkl")

else :
    print(f"Aucun fichier trouvé le {"today"}") # Si aucun fichier ce jour
