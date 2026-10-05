from flask import Flask, render_template, request
import joblib
import numpy as np
from pathlib import Path


app = Flask(__name__)


model_path = Path(__file__).parent / "model" / "house_price_model.pkl"
model = joblib.load(model_path)


FEATURE_RANGES = {
    "MedInc": (0.0, 20.0),
    "HouseAge": (0.0, 60.0),
    "AveRooms": (0.0, 150.0),
    "AveBedrms": (0.0, 40.0),
    "Population": (0.0, 40000.0),
    "AveOccup": (0.0, 1500.0),
    "Latitude": (30.0, 45.0),
    "Longitude": (-130.0, -110.0)
}


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    error = None

    if request.method == "POST":

        try:

            features = {}

            for feature in FEATURE_RANGES:

                value = float(request.form[feature])

                minimum, maximum = FEATURE_RANGES[feature]

                if not minimum <= value <= maximum:
                    raise ValueError(
                        f"{feature} must be between {minimum} and {maximum}."
                    )

                features[feature] = value


            input_data = np.array([
                features["MedInc"],
                features["HouseAge"],
                features["AveRooms"],
                features["AveBedrms"],
                features["Population"],
                features["AveOccup"],
                features["Latitude"],
                features["Longitude"]
            ]).reshape(1, -1)


            
            prediction = model.predict(input_data)[0]


        except (ValueError, KeyError):

            error = (
                "Please enter valid values within the allowed ranges."
            )


    return render_template(
        "index.html",
        prediction=prediction,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)