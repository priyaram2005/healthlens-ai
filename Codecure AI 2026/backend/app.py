from flask import Flask, request, jsonify
import re
import joblib

app = Flask(__name__)

# -------------------------
# LOAD MODEL
# -------------------------
model = joblib.load("model.pkl")

# -------------------------
# NORMAL RANGES
# -------------------------
ranges = {
    "hemoglobin": (12, 16),
    "glucose": (70, 110),
    "wbc": (4000, 11000),
    "cholesterol": (125, 200),
    "platelets": (150000, 450000),
    "vitamin_d": (20, 50)
}

# -------------------------
# PARAMETER EXTRACTION
# -------------------------
def extract_parameters(text):
    patterns = {
        "hemoglobin": r"(hemoglobin|hb)[^\d]*(\d+\.?\d*)",
        "glucose": r"(glucose|blood sugar)[^\d]*(\d+\.?\d*)",
        "wbc": r"(wbc|white blood cells)[^\d]*(\d+)",
        "cholesterol": r"(cholesterol)[^\d]*(\d+)",
        "platelets": r"(platelets)[^\d]*(\d+)",
        "vitamin_d": r"(vitamin\s*d)[^\d]*(\d+\.?\d*)"
    }

    values = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            values[key] = float(match.group(2))

    return values

# -------------------------
# RULE-BASED ANALYSIS
# -------------------------
def analyze(values):
    analysis = {}

    for k, v in values.items():
        if k in ranges:
            low, high = ranges[k]

            if v < low:
                analysis[k] = "Low"
            elif v > high:
                analysis[k] = "High"
            else:
                analysis[k] = "Normal"

    return analysis

# -------------------------
# RECOMMENDATIONS ENGINE
# -------------------------
def get_recommendations(analysis):
    rec = []

    if analysis.get("hemoglobin") == "Low":
        rec.append("Increase iron-rich foods")

    if analysis.get("glucose") == "High":
        rec.append("Reduce sugar intake")

    if analysis.get("cholesterol") == "High":
        rec.append("Avoid oily/fatty foods")

    if analysis.get("vitamin_d") == "Low":
        rec.append("Get more sunlight / Vitamin D supplements")

    return rec

# -------------------------
# ML INPUT PREPARATION
# -------------------------
def prepare_ml_input(values):
    return [
        values.get("hemoglobin", 12),
        values.get("glucose", 90),
        values.get("wbc", 8000),
        values.get("cholesterol", 180),
        values.get("platelets", 250000)
    ]

# -------------------------
# MAIN API
# -------------------------
@app.route("/analyze", methods=["POST"])
def analyze_report():
    data = request.json
    text = data.get("report_text", "")

    # Step 1: Extract
    values = extract_parameters(text)

    # Step 2: Rule analysis
    analysis = analyze(values)

    # Step 3: ML prediction
    features = prepare_ml_input(values)
    risk = model.predict([features])[0]

    # Step 4: Recommendations
    recommendations = get_recommendations(analysis)

    return jsonify({
        "parameters": values,
        "analysis": analysis,
        "risk": risk,
        "recommendations": recommendations
    })

# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)