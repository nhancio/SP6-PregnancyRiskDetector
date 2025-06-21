from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import os
from flask import Flask
app = Flask(__name__, static_folder="../static", template_folder="../templates")
# Correct the static folder path
base_dir = os.path.dirname(os.path.dirname(__file__))  # One level up from /api
static_folder = os.path.join(base_dir, "static")

try:
    with open(os.path.join(static_folder, "label_encoders.pkl"), "rb") as le_file:
        label_encoders = pickle.load(le_file)
    print("[DEBUG] Label encoders loaded successfully.")

    with open(os.path.join(static_folder, "preg_model.pkl"), "rb") as model_file:
        decision_tree_model = pickle.load(model_file)
    print("[DEBUG] Model loaded successfully.")

except Exception as e:
    print(f"[ERROR] Failed to load model or encoders at startup: {e}")
    label_encoders = None
    decision_tree_model = None



# app = Flask(__name__, static_folder='static')
app.config['SERVER_NAME'] = 'predict.nhancio.com'

# Hardcoded credentials
USERNAME = "admin"
PASSWORD = "admin"

@app.route("/", methods=["GET", "POST"])
def login():
    print("[DEBUG] Entered login route, method:", request.method)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(f"[DEBUG] Login attempt with username: {username}")
        if username == USERNAME and password == PASSWORD:
            print("[DEBUG] Login successful, redirecting to dashboard.")
            return redirect(url_for("dashboard"))
            # return redirect(url_for("dashboard", _external=True, _scheme="https"))
        else:
            print("[DEBUG] Login failed. Invalid credentials.")
            return render_template("login.html", error="Invalid credentials. Please try again.")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    print("[DEBUG] Entered dashboard route.")
    return render_template("dashboard.html")

@app.route("/results")
def results():
    prediction = request.args.get("prediction")
    print(f"[DEBUG] Entered results route. Prediction: {prediction}")
    return render_template("results.html", prediction=prediction)

@app.route("/submit", methods=["POST"])
def submit():
    print("[DEBUG] Entered submit route.")
    
    if decision_tree_model is None or label_encoders is None:
        print("[ERROR] Model or encoders not loaded.")
        return "<h1 style='color:red;'>Model or encoders not loaded. Please check server setup.</h1>"

    # Input features expected from form
    input_features = ['DELIVERY_MODE_df5', 'BP_df5', 'DEL_COMPLICATIONS',
        'FACILITY_TYPE_df5', 'BLOOD_GRP_df5', 'ASHA_DTLS_df5', 'DOC_ANM_NAME',
        'INDICATION_FOR_C_SECTION_df5', 'DISTRICT_anc', 'DEATH_df5',
        'HEIGHT_df5', 'FACILITY_NAME_df5', 'PLACE_OF_DELIVERY',
        'BLOOD_SUGAR_df5', 'MODE_OF_DELIVERY', 'AGE_preg', 'CONDUCT_BY',
        'WEIGHT_df2', 'HEMOGLOBIN_df5', 'WEIGHT_anc', 'GRAVIDA_df5',
        'WEIGHT_child', 'GRAVIDA', 'ABORTIONS_df5']

    # Collect form data
    form_data = {feature: request.form.get(feature) for feature in input_features}
    print(f"[DEBUG] Form data received: {form_data}")

    # Check for missing fields
    missing = [field for field, value in form_data.items() if value in (None, '')]
    if missing:
        print(f"[ERROR] Missing fields: {missing}")
        return f"<h1 style='color:red;'>Missing required fields: {missing}</h1>"

    # Hardcode override if needed
    form_data["GRAVIDA_df5"] = "G1"  # can remove if unnecessary

    # Encode form data
    encoded_data = []
    print("[DEBUG] Starting encoding process...")
    for feature in input_features:
        value = form_data[feature]
        if feature in label_encoders and feature not in ["ASHA_DTLS_df5", "HEIGHT_df5", "WEIGHT_anc"]:
            try:
                encoded_value = label_encoders[feature].transform([value])[0]
                encoded_data.append(encoded_value)
                print(f"[DEBUG] Encoded {feature}: {value} -> {encoded_value}")
            except Exception as e:
                print(f"[ERROR] Failed to encode {feature}: {value} | Error: {e}")
                return f"<h1 style='color:red;'>Invalid value for {feature}: {value}</h1>"
        else:
            try:
                float_val = float(value)
                encoded_data.append(float_val)
                print(f"[DEBUG] Used float for {feature}: {value} -> {float_val}")
            except Exception as e:
                print(f"[ERROR] Invalid numeric value for {feature}: {value} | Error: {e}")
                return f"<h1 style='color:red;'>Invalid numeric value for {feature}: {value}</h1>"

    # Prepare input for model
    try:
        input_array = np.array(encoded_data).reshape(1, -1)
        print("[DEBUG] Input array:", input_array)
        prediction = decision_tree_model.predict(input_array)[0]
        print(f"[DEBUG] Prediction: {prediction}")
    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        return f"<h1 style='color:red;'>Prediction error: {str(e)}</h1>"

    return redirect(url_for("results", prediction=prediction))


@app.route("/test_model")
def test_model():
    if decision_tree_model is None or label_encoders is None:
        return "Model or encoders not loaded"
    return "Model and encoders loaded successfully"

# if __name__ == "__main__":
#     print("[DEBUG] Starting Flask app...")
#     app.run(debug=False)
