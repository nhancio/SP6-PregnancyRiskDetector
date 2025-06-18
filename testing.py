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


# Check if the column exists in the encoders
column_name = "TIME_OF_BIRTH"

if column_name in label_encoders:
    encoder = label_encoders[column_name]

    if hasattr(encoder, 'classes_'):
        print(f"✅ Possible values for '{column_name}':")
        print(set(encoder.classes_))
    else:
        print(f"⚠️ Encoder for '{column_name}' does not have 'classes_' attribute.")
else:
    print(f"❌ No encoder found for column: '{column_name}'")
