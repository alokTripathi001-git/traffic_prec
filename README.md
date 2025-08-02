# 🚦 Traffic Prediction Web App

A real-time traffic prediction web application built using **Flask**, **KNN ML model**, **TomTom API**, and **OpenRouteService**.  
It predicts the traffic condition between a given **origin and destination** based on user input and real-time data.

---

## 📂 Dataset

- **Source:** [Kaggle - Traffic Prediction Dataset](https://www.kaggle.com/datasets/hasibullahaman/traffic-prediction-dataset)
- **Used For:** Training KNN model with 90% accuracy.

---

## 🛠️ Tech Stack

| Component         | Technology Used             |
|-------------------|------------------------------|
| Backend           | Python (Flask)              |
| Frontend          | HTML, CSS                   |
| ML Model          | K-Nearest Neighbors (KNN)   |
| APIs              | TomTom API, OpenRouteService |
| Libraries         | pandas, scikit-learn, requests |

---

## 🔥 Features

- Origin-Destination input by user.
- Live route map using OpenRouteService.
- Real-time traffic prediction using KNN model.
- 90% accuracy achieved on dataset.
- Simple UI with clear output.

---

## 🏗️ Architecture

```
User Input → Flask App → TomTom & OpenRouteService APIs
                        ↓
                  Feature Extraction
                        ↓
               KNN ML Model Prediction
                        ↓
               Traffic Condition Output
```

---

## 🧪 ML Model Details

- **Algorithm:** K-Nearest Neighbors (KNN)
- **Trained on:** Kaggle dataset (link above)
- **Accuracy:** 90%
- **Output:** Predicted traffic level (Low / Medium / High)

> Saved model: `model/knn_model.pkl`

---

## 🚀 How to Run Locally

### 1️⃣ Clone the Project

```bash
git clone https://github.com/your-username/traffic-prediction-app.git
cd traffic-prediction-app
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set API Keys

Create a file named `.env` or `config.py` and add:

```python
TOMTOM_API_KEY = "your_tomtom_key"
ORS_API_KEY = "your_openrouteservice_key"
```

### 5️⃣ Run the App

```bash
python app.py
```

Open browser and go to:  
👉 `http://127.0.0.1:5000/`

---

## 🌍 APIs Used

### ✅ TomTom API
- Used to get real-time traffic data
- Free key available at [https://developer.tomtom.com](https://developer.tomtom.com)

### ✅ OpenRouteService
- Used for map rendering and route calculations
- Get API key at [https://openrouteservice.org](https://openrouteservice.org)

---

## 🧾 Example Input/Output

| Input                | Value                          |
|---------------------|--------------------------------|
| Origin              | Kanpur, Uttar Pradesh          |
| Destination         | Lucknow, Uttar Pradesh         |
| Predicted Traffic   | High                           |

---

## 📁 Folder Structure

```
traffic-prediction-app/
│
├── app.py                   # Flask app
├── model/
│   └── knn_model.pkl        # Trained ML model
├── templates/
│   └── index.html           # Frontend HTML
├── static/
│   └── style.css            # CSS Styling
├── utils/
│   └── api_helpers.py       # API functions
├── requirements.txt
└── README.md
```

---

## ❗ Troubleshooting

- **Model Not Loading?**  
  Make sure `knn_model.pkl` is placed inside the `model/` folder.

- **API Key Errors?**  
  Verify your TomTom or ORS API key is valid and not expired.

- **CORS Issues?**  
  Use Flask-CORS or switch browser.

---

## 📜 License

This project is made for **learning and demonstration purposes only** under the MIT License.

---

## 🙌 Acknowledgements

- TomTom Maps API  
- OpenRouteService  
- Hasibullah Aman for Kaggle Dataset  
- scikit-learn and Flask contributors

---

## ✉️ Contact

For any query or collaboration:  
📧aloktripathi070@gmail.com



