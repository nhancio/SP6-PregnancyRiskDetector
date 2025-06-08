from flask import Flask, render_template, request, redirect, url_for, send_from_directory

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
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/submit", methods=["POST"])
def submit():
    # Handle form submission logic here
    abortions = request.form.get("abortions")
    gravida = request.form.get("gravida")
    time_of_birth = request.form.get("time_of_birth")
    mode_of_delivery = request.form.get("mode_of_delivery")
    place_of_delivery = request.form.get("place_of_delivery")
    conduct_by = request.form.get("conduct_by")
    del_complications = request.form.get("del_complications")
    indication_for_c_section = request.form.get("indication_for_c_section")
    weight_child = request.form.get("weight_child")
    weight_anc = request.form.get("weight_anc")
    hemoglobin = request.form.get("hemoglobin")
    blood_sugar = request.form.get("blood_sugar")
    height = request.form.get("height")
    age_preg = request.form.get("age_preg")
    death = request.form.get("death")
    blood_grp = request.form.get("blood_grp")
    district = request.form.get("district")
    asha_dtls = request.form.get("asha_dtls")
    facility_type = request.form.get("facility_type")
    facility_name = request.form.get("facility_name")
    # Process or store the data as needed
    return render_template("dashboard.html", message="Form submitted successfully!")

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
