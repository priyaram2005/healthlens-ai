import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# -------------------------
# GENERATE SYNTHETIC DATA (ENHANCED)
# -------------------------
data = []

for _ in range(2000):
    hb = np.random.uniform(8, 16)                 # Hemoglobin
    glucose = np.random.uniform(70, 180)          # Sugar
    wbc = np.random.uniform(4000, 12000)          # WBC
    cholesterol = np.random.uniform(120, 300)     # Cholesterol
    platelets = np.random.uniform(150000, 450000) # Platelets

    # -------------------------
    # RISK LOGIC (REALISTIC RULES)
    # -------------------------
    score = 0

    if hb < 11:
        score += 2
    elif hb < 12:
        score += 1

    if glucose > 140:
        score += 2
    elif glucose > 110:
        score += 1

    if cholesterol > 240:
        score += 2
    elif cholesterol > 200:
        score += 1

    if wbc < 4000 or wbc > 11000:
        score += 1

    if platelets < 150000:
        score += 1

    # -------------------------
    # FINAL LABEL
    # -------------------------
    if score >= 4:
        risk = "High"
    elif score >= 2:
        risk = "Moderate"
    else:
        risk = "Low"

    data.append([hb, glucose, wbc, cholesterol, platelets, risk])

# -------------------------
# DATAFRAME
# -------------------------
df = pd.DataFrame(data, columns=[
    "hb", "glucose", "wbc", "cholesterol", "platelets", "risk"
])

# -------------------------
# FEATURES & LABEL
# -------------------------
X = df[["hb", "glucose", "wbc", "cholesterol", "platelets"]]
y = df["risk"]

# -------------------------
# TRAIN TEST SPLIT
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------
# MODEL TRAINING
# -------------------------
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# -------------------------
# SAVE MODEL
# -------------------------
joblib.dump(model, "model.pkl")

# -------------------------
# PRINT ACCURACY
# -------------------------
accuracy = model.score(X_test, y_test)
print(f"Model trained with accuracy: {accuracy:.2f}")