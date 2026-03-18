#  Bangalore House Price Predictor

A complete end-to-end Machine Learning web application that predicts house prices in Bangalore, India based on location, area, number of bedrooms and bathrooms.

**Live Demo:** [neostrong.github.io/bangalore-house-price](https://neostrong.github.io/bangalore-house-price)  
**API:** [neostrong.pythonanywhere.com](https://neostrong.pythonanywhere.com)

---

##  Project Overview

This project covers the full ML pipeline — from raw data to a deployed web application:

- Data cleaning and feature engineering on 13,000+ Bangalore property listings
- Outlier removal using domain knowledge (price per sqft, BHK logic)
- Model selection using GridSearchCV across Linear Regression, Lasso, and Decision Tree
- REST API built with Flask and deployed on PythonAnywhere
- Responsive frontend built with HTML, CSS and JavaScript, hosted on GitHub Pages

---

##  Tech Stack

| Layer | Technology |
|---|---|
| Data Processing | Python, Pandas, NumPy |
| Model Training | scikit-learn, Linear Regression |
| API | Flask, Flask-CORS |
| Frontend | HTML, CSS, JavaScript |
| Deployment (API) | PythonAnywhere |
| Deployment (Frontend) | GitHub Pages |

---

##  Project Structure

```
bangalore-house-price/
├── house_prediction.ipynb             # Data cleaning, EDA, model training
├── banglore_home_prices_model.pickle  # Saved trained model
├── columns.json                       # Feature column names
├── server.py                          # Flask API server
├── model.py                           # Model loading and prediction logic
├── index.html                         # Frontend UI
├── style.css                          # Styling
└── app.js                             # Frontend logic and API calls
```

---

##  API Endpoints

### Health Check
```
GET /
```

### Get All Locations
```
GET /locations
```

### Predict Price
```
POST /predict
Content-Type: application/json

{
    "location": "indira nagar",
    "total_sqft": 1200,
    "bath": 2,
    "bhk": 3
}
```

**Response:**
```json
{
    "predicted_price_lakhs": 195.39,
    "predicted_price_inr": "Rs. 195.39 Lakhs"
}
```

---

##  Run Locally

**1. Clone the repository:**
```bash
git clone https://github.com/neostrong/bangalore-house-price.git
cd bangalore-house-price
```

**2. Install dependencies:**
```bash
pip install flask flask-cors scikit-learn numpy
```

**3. Run the server:**
```bash
python server.py
```

**4. Open the frontend:**
```bash
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser.

---

##  Model Performance

| Model | Best CV Score |
|---|---|
| Linear Regression | ~0.86 |
| Lasso | ~0.73 |
| Decision Tree | ~0.72 |

Linear Regression was selected as the best model based on cross-validation scores.

---

## 📬 Contact

**Ezekiel** — [GitHub](https://github.com/neostrong)
