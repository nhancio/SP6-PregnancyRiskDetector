# AI4TG App User Journey

## Overview
The AI4TG app is designed to predict outcomes based on user-provided data. It includes a login system, a dashboard for data submission, and a results page to display predictions.

## User Journey

1. **Login Page**:
   - The user accesses the app and is presented with the login page (`login.html`).
   - They enter their credentials (username and password).
   - If the credentials are correct, they are redirected to the dashboard. Otherwise, an error message is displayed.

2. **Dashboard**:
   - After logging in, the user is taken to the dashboard (`dashboard.html`).
   - The dashboard contains forms for submitting various data points related to delivery, health metrics, facility information, and additional medical details.
   - The user fills out the required fields and submits the form.

3. **Prediction Process**:
   - Upon form submission, the app processes the data using pre-trained models and label encoders stored in the `static` folder.
   - The data is validated and encoded before being passed to the prediction model.

4. **Results Page**:
   - After the prediction is made, the user is redirected to the results page (`results.html`).
   - The predicted outcome is displayed along with an option to return to the dashboard.

## Key Features
- **Secure Login**: Hardcoded credentials ensure basic access control.
- **Data Submission**: Intuitive forms for entering required data.
- **Prediction**: Machine learning models provide accurate predictions based on user input.
- **Results Display**: Clear and concise presentation of prediction results.

## Notes
- Ensure the `label_encoders.pkl` and `preg_model.pkl` files are present in the `static` folder for the app to function correctly.
- Use the `testing.py` script to verify the availability of required files.

## Running the App
1. Install dependencies listed in `requirements.txt`.
2. Run `app.py` using Python.
3. Access the app at `http://127.0.0.1:5000/`.

Enjoy using the AI4TG app!
