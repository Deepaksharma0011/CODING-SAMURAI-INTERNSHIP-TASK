# 📈 TCS Stock Price Prediction using LSTM
### Coding Samurai Data Science Internship - Level 3 Project

---

## 📌 Project Overview
This project predicts **TCS (Tata Consultancy Services)** stock prices using a **Long Short-Term Memory (LSTM)** deep learning model. Historical stock data is fetched from Yahoo Finance and used to forecast the next 30 days of stock prices.

---

## 🛠️ Technologies Used
| Tool | Purpose |
|------|---------|
| Python | Programming Language |
| Jupyter Notebook | Development Environment |
| yfinance | Fetching Stock Data |
| Pandas & NumPy | Data Manipulation |
| Matplotlib | Data Visualization |
| Scikit-learn | Preprocessing & Metrics |
| TensorFlow / Keras | Building LSTM Model |

---

## 📊 Project Workflow

1. **Data Collection** — TCS stock data (2019–2024) via yfinance
2. **EDA** — Price trends, volume analysis, moving averages (50-day, 200-day)
3. **Preprocessing** — MinMaxScaler normalization, sequence creation (60-day look-back)
4. **Model Building** — 3-layer LSTM with Dropout layers
5. **Training** — 50 epochs with Early Stopping
6. **Evaluation** — RMSE, MAE, R² Score
7. **Forecasting** — Next 30 days predicted

---

## 📁 Project Structure
```
CODING-SAMURAI-INTERNSHIP-TASK/
│
├── TCS_Stock_Prediction_LSTM.ipynb   # Main Jupyter Notebook
└── README.md                          # Project Description
```

---

## 📈 Results
- **Model:** LSTM (3 layers)
- **Stock:** TCS.NS (NSE India)
- **Data:** 5 Years (2019–2024)
- **Look-back Window:** 60 Days
- **Forecast:** 30 Days into future

---

## ▶️ How to Run

```bash
# Install required libraries
pip install yfinance pandas numpy matplotlib scikit-learn tensorflow keras jupyter

# Launch Jupyter Notebook
jupyter notebook

# Open TCS_Stock_Prediction_LSTM.ipynb and Run All cells
```

---

## ⚠️ Disclaimer
This project is built for **educational purposes only** as part of the Coding Samurai Internship. Stock price predictions are not financial advice.

---

## 🙋 Author
**[Your Name]**  
Data Science Intern @ Coding Samurai  
📧 [your.email@gmail.com]  
🔗 [LinkedIn Profile Link]

---

*#CodingSamurai #DataScience #LSTM #StockPrediction #Python*
