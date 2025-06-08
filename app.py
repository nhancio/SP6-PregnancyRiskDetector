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
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials. Please try again.")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/results")
def results():
    prediction = request.args.get("prediction")
    return render_template("results.html", prediction=prediction)

@app.route("/submit", methods=["POST"])
def submit():
    # try:
    # Load label encoders and decision tree model directly from the static folder
    static_folder = os.path.join(app.root_path, 'static')
    with open(os.path.join(static_folder, "label_encoders.pkl"), "rb") as le_file:
        label_encoders = pickle.load(le_file)
    with open(os.path.join(static_folder, "preg_model.pkl"), "rb") as model_file:
        decision_tree_model = pickle.load(model_file)
    # except FileNotFoundError as e:
    # return render_template("dashboard.html", error=f"File not found: {e.filename}")

    # List of input features
    input_features = ['DELIVERY_MODE_df5', 'BP_df5', 'DEL_COMPLICATIONS',
       'FACILITY_TYPE_df5', 'BLOOD_GRP_df5', 'ASHA_DTLS_df5', 'DOC_ANM_NAME', 'INDICATION_FOR_C_SECTION_df5',
       'DISTRICT_anc', 'DEATH_df5', 'HEIGHT_df5', 'FACILITY_NAME_df5', 'PLACE_OF_DELIVERY',
       'BLOOD_SUGAR_df5', 'MODE_OF_DELIVERY', 'AGE_preg', 'CONDUCT_BY',
       'WEIGHT_df2', 'HEMOGLOBIN_df5', 'WEIGHT_anc', 'GRAVIDA_df5', 'WEIGHT_child', 'GRAVIDA',
       'ABORTIONS_df5']

    # Collect form data
    form_data = {feature: request.form.get(feature) for feature in input_features}
    form_data["GRAVIDA_df5"] = "G1"  # Hardcoded value for GRAVIDA_df5

    # Validate form data
    # for key, value in form_data.items():
    #     if value is None or value == "":
    #         return render_template("dashboard.html", error=f"Missing value for {key}")

    # Encode form data using label encoders
    encoded_data = []
    for feature in input_features:
        if feature in label_encoders:
            try:
                encoded_data.append(label_encoders[feature].transform([form_data[feature]])[0])
            except ValueError:
                return f"<h1 style='color: red;'>Invalid value for {feature}</h1>"
        else:
            try:
                encoded_data.append(float(form_data[feature]))
            except ValueError:
                return f"<h1 style='color: red;'>Invalid numeric value for {feature}</h1>"

    # Convert encoded data to numpy array
    input_array = np.array(encoded_data).reshape(1, -1)

    # Predict using the decision tree model
    try:
        prediction = decision_tree_model.predict(input_array)
    except Exception as e:
        return f"<h1 style='color: red;'>Prediction error: {str(e)}</h1>"

    # Redirect to the results page with the prediction
    return redirect(url_for("results", prediction=prediction[0]))

if __name__ == "__main__":
    app.run(debug=True)
