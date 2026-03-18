from flask_cors import CORS
from flask import Flask, request, jsonify
from model import predict_price, get_locations
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# ── Health Check ────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def health():
    return jsonify(
        {"status": "ok", "message": "Bangalore House Price Prediction API is running"}
    )


# ── Get All Locations ────────────────────────────────────────────────────────
@app.route("/locations", methods=["GET"])
def locations():
    """Returns the full list of supported location names."""
    return jsonify({"locations": get_locations(), "total": len(get_locations())})


# ── Single Prediction ────────────────────────────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    """
    Predicts house price in Lakhs (INR).

    Expected JSON body:
    {
        "location": "indira nagar",
        "total_sqft": 1200,
        "bath": 2,
        "bhk": 3
    }
    """
    try:
        data = request.get_json()

        # ── Validate required fields ──
        required = ["location", "total_sqft", "bath", "bhk"]
        missing = [field for field in required if field not in data]
        if missing:
            return jsonify({"error": f"Missing required fields: {missing}"}), 400

        location = data["location"]
        total_sqft = float(data["total_sqft"])
        bath = int(data["bath"])
        bhk = int(data["bhk"])

        # ── Basic sanity checks ──
        if total_sqft <= 0:
            return jsonify({"error": "total_sqft must be greater than 0"}), 400
        if bath <= 0 or bhk <= 0:
            return jsonify({"error": "bath and bhk must be positive integers"}), 400
        if bath > bhk + 2:
            return jsonify({"error": "bath count seems unrealistic for given BHK"}), 400

        price = predict_price(location, total_sqft, bath, bhk)

        return (
            jsonify(
                {
                    "input": {
                        "location": location,
                        "total_sqft": total_sqft,
                        "bath": bath,
                        "bhk": bhk,
                    },
                    "predicted_price_lakhs": price,
                    "predicted_price_inr": f"₹ {price:.2f} Lakhs",
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


# ── Batch Prediction ─────────────────────────────────────────────────────────
@app.route("/predict/batch", methods=["POST"])
def batch_predict():
    """
    Predicts prices for multiple houses in one request.

    Expected JSON body:
    {
        "instances": [
            {"location": "indira nagar", "total_sqft": 1200, "bath": 2, "bhk": 3},
            {"location": "whitefield",   "total_sqft": 1500, "bath": 3, "bhk": 4}
        ]
    }
    """
    try:
        data = request.get_json()

        if not data or "instances" not in data:
            return jsonify({"error": "Missing 'instances' key in request body"}), 400

        instances = data["instances"]

        if not isinstance(instances, list) or len(instances) == 0:
            return jsonify({"error": "'instances' must be a non-empty list"}), 400

        results = []
        for i, instance in enumerate(instances):
            try:
                price = predict_price(
                    instance["location"],
                    float(instance["total_sqft"]),
                    int(instance["bath"]),
                    int(instance["bhk"]),
                )
                results.append(
                    {
                        "index": i,
                        "input": instance,
                        "predicted_price_lakhs": price,
                        "predicted_price_inr": f"₹ {price:.2f} Lakhs",
                    }
                )
            except Exception as e:
                results.append({"index": i, "input": instance, "error": str(e)})

        return jsonify({"total": len(results), "predictions": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
