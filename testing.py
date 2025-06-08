import pickle
import os

static_folder = os.path.join(os.path.dirname(__file__), "static")
le_path = os.path.join(static_folder, "label_encoders.pkl")
model_path = os.path.join(static_folder, "preg_model.pkl")

print("Label Encoders Path:", le_path)
print("Model Path:", model_path)

# Load and test
with open(le_path, "rb") as le_file:
    label_encoders = pickle.load(le_file)
    print("✅ Label encoders loaded")

with open(model_path, "rb") as model_file:
    model = pickle.load(model_file)
    print("✅ Model loaded")
