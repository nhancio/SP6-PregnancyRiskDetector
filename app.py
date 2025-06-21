from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import os

app = Flask(__name__, static_folder='static')

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
    # try:
    # Load label encoders and decision tree model directly from the static folder
    static_folder = os.path.join(app.root_path, 'static')
    print(f"[DEBUG] Static folder path: {static_folder}")
    try:
        with open(os.path.join(static_folder, "label_encoders.pkl"), "rb") as le_file:
            label_encoders = pickle.load(le_file)
        print("[DEBUG] Label encoders loaded successfully.")
        with open(os.path.join(static_folder, "preg_model.pkl"), "rb") as model_file:
            decision_tree_model = pickle.load(model_file)
        print("[DEBUG] Model loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to load model or encoders: {e}")
        return render_template("dashboard.html", error=f"File not found or load error: {e}")

    # List of input features
    input_features = ['DELIVERY_MODE_df5', 'BP_df5', 'DEL_COMPLICATIONS',
       'FACILITY_TYPE_df5', 'BLOOD_GRP_df5', 'ASHA_DTLS_df5', 'DOC_ANM_NAME', 'INDICATION_FOR_C_SECTION_df5',
       'DISTRICT_anc', 'DEATH_df5', 'HEIGHT_df5', 'FACILITY_NAME_df5', 'PLACE_OF_DELIVERY',
       'BLOOD_SUGAR_df5', 'MODE_OF_DELIVERY', 'AGE_preg', 'CONDUCT_BY',
       'WEIGHT_df2', 'HEMOGLOBIN_df5', 'WEIGHT_anc', 'GRAVIDA_df5', 'WEIGHT_child', 'GRAVIDA',
       'ABORTIONS_df5']

    # Collect form data
    form_data = {feature: request.form.get(feature) for feature in input_features}
    print(f"[DEBUG] Form data collected: {form_data}")
    form_data["GRAVIDA_df5"] = "G1"  # Hardcoded value for GRAVIDA_df5

    # Validate form data
    # for key, value in form_data.items():
    #     if value is None or value == "":
    #         print(f"[ERROR] Missing value for {key}")
    #         return render_template("dashboard.html", error=f"Missing value for {key}")

    # Encode form data using label encoders
    print("[DEBUG] Encoding form data...")
    encoded_data = []
    for feature in input_features:
        if feature in label_encoders and feature != "ASHA_DTLS_df5" and feature != "HEIGHT_df5" and feature != "WEIGHT_anc":
            try:
                encoded_value = label_encoders[feature].transform([form_data[feature]])[0]
                encoded_data.append(encoded_value)
                print(f"[DEBUG] Encoded {feature}: {form_data[feature]} -> {encoded_value}")
            except ValueError:
                print(f"[ERROR] Invalid value for {feature}: {form_data[feature]}")
                return f"<h1 style='color: red;'>Invalid value for {feature}</h1>"
        else:
            try:
                float_value = float(form_data[feature])
                encoded_data.append(float_value)
                print(f"[DEBUG] Used float for {feature}: {form_data[feature]} -> {float_value}")
            except ValueError:
                print(f"[ERROR] Invalid numeric value for {feature}: {form_data[feature]}")
                return f"<h1 style='color: red;'>Invalid numeric value for {feature}</h1>"

    # Convert encoded data to numpy array
    print("[DEBUG] Converting encoded data to numpy array...")
    input_array = np.array(encoded_data).reshape(1, -1)
    print("[DEBUG] Input array shape:", input_array.shape)
    print("[DEBUG] Input array:", input_array)

    # Predict using the decision tree model
    try:
        print("[DEBUG] Making prediction...")
        prediction = decision_tree_model.predict(input_array)
        print(f"[DEBUG] Prediction made: {prediction}")
    except Exception as e:
        print(f"[ERROR] Prediction error: {str(e)}")
        return f"<h1 style='color: red;'>Prediction error: {str(e)}</h1>"

    # Redirect to the results page with the prediction
    print(f"[DEBUG] Redirecting to results with prediction: {prediction[0]}")
    return redirect(url_for("results", prediction=prediction[0]))

if __name__ == "__main__":
    print("[DEBUG] Starting Flask app...")
    app.run(debug=False)
