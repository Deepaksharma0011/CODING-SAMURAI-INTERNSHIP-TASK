# 🎓 Coding Samurai - Data Science Internship
### Deepak Sharma | Data Science Intern

---

## 📌 About
This repository contains all Data Science projects completed as part of the **Coding Samurai Internship Program**.

---

## 🚀 Projects

---

### 📈 Project 1: TCS Stock Price Prediction using LSTM
**Level:** Advanced | **Domain:** Time Series Forecasting

**Description:**
Predicts TCS (Tata Consultancy Services) stock prices using a deep learning LSTM model. Historical data is fetched from Yahoo Finance and used to forecast the next 30 days.

**Tech Stack:**
`Python` `TensorFlow` `Keras` `LSTM` `yfinance` `Pandas` `Matplotlib` `Scikit-learn`

**Key Steps:**
- Fetched 5 years of real TCS stock data using yfinance
- Performed EDA — price trends, volume, moving averages
- Built 3-layer LSTM model with Dropout
- Evaluated using RMSE, MAE, R² Score
- Forecasted next 30 days of stock prices

📂 File: `TCS_Stock_Prediction_LSTM.ipynb`

---

### 🐦 Project 2: Twitter Sentiment Analysis using NLP
**Level:** Advanced | **Domain:** Natural Language Processing

**Description:**
Performs sentiment analysis on 74,000+ real Twitter tweets. Classifies tweets as Positive, Negative, or Neutral using TF-IDF vectorization and Logistic Regression.

**Tech Stack:**
`Python` `NLTK` `TextBlob` `TF-IDF` `Scikit-learn` `WordCloud` `Matplotlib` `Seaborn`

**Key Steps:**
- Loaded 74,682 real tweets from Twitter Entity Sentiment Dataset
- Performed EDA — sentiment distribution, topic analysis
- Cleaned text — removed URLs, mentions, hashtags, stopwords
- Generated WordCloud for Positive & Negative tweets
- Trained Logistic Regression classifier
- Compared with TextBlob rule-based approach
- Tested on custom tweets

📂 File: `Twitter_Sentiment_Analysis.ipynb`

> Dataset: [Kaggle - Twitter Entity Sentiment Analysis](https://www.kaggle.com/datasets/jp797498e/twitter-entity-sentiment-analysis)

---

## 🛠️ How to Run

```bash
# Install libraries
pip install yfinance pandas numpy matplotlib seaborn scikit-learn nltk textblob wordcloud tensorflow keras jupyter

# Launch Jupyter
jupyter notebook
```

---

## 🙋 Author
**Deepak Sharma**  
Data Science Intern @ Coding Samurai  
🔗 [https://www.linkedin.com/in/deepak-sharma-1875462ba/]  
📧 [ds6739820@@gmail.com]

---

*#CodingSamurai #DataScience #LSTM #NLP #Python #MachineLearning #Internship*
