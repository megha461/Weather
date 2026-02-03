🌦️ Weather Prediction System using Machine Learning
📌 Project Overview

This project implements an **AI/ML-based Weather Prediction System** that forecasts **rainfall and temperature** using historical meteorological data. The goal is to analyze weather patterns, compare multiple machine learning models, and identify the most accurate approach for weather forecasting.

The project focuses on real-world data preprocessing, model comparison, and result visualization, making it suitable for academic, research, and portfolio purposes.

 🎯 Objectives

* Predict **rainfall and temperature** using historical weather data
* Perform **data preprocessing and feature engineering**
* Analyze seasonal trends using **Exploratory Data Analysis (EDA)**
* Implement and compare multiple **Machine Learning models**
* Visualize predictions and model performance using graphs

 🗂️ Dataset Description

The project uses multiple CSV datasets containing weather information such as:

* Temperature (minimum, maximum, average)
* Rainfall
* Humidity
* Wind speed
* Atmospheric pressure

Example datasets used:

* Weather Data in India (1901–2017)
* Historical city-wise weather data
* Sub-sampled datasets for faster experimentation


 🛠️ Technologies & Tools

**Programming Language:**

* Python

**Libraries & Frameworks:**

* NumPy
* Pandas
* Matplotlib
* Scikit-learn
* XGBoost

**Development Tools:**

* VS Code
* Git & GitHub

🤖 Machine Learning Models Used

* Linear Regression
* Decision Tree
* Random Forest
* XGBoost

Each model is trained and evaluated to compare prediction accuracy for rainfall and temperature.

 📊 Evaluation Metrics

Model performance is evaluated using:

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* R² Score

Results are visualized using:

* Actual vs Predicted graphs
* Error distribution plots
* Model comparison charts

📁 Project Structure

```
Weather/
│
├── Api.py
├── main.py
├── project.py
├── rainfall_pred.py
├── temp_model.py
├── compare_cities.py
├── grid.py
│
├── data files (.csv)
├── Temperature_Report.pdf
├── .gitignore
└── README.md
```

 🚀 How to Run the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/megha461/Weather.git
   ```
2. Navigate to the project directory:

   ```bash
   cd Weather
   ```
3. Install required libraries:

   ```bash
   pip install -r requirements.txt
   ```
4. Run the main script:

   ```bash
   python main.py
   ```

---

## 📈 Results & Insights

* Tree-based models like **Random Forest and XGBoost** performed better for rainfall prediction due to non-linear data patterns.
* Temperature prediction achieved higher accuracy compared to rainfall forecasting.
* Visual analysis revealed strong seasonal and yearly weather trends.



 🔮 Future Enhancements

* Integrate real-time weather data using APIs
* Deploy the model using Flask/FastAPI
* Add deep learning models (LSTM) for time-series forecasting
* Create an interactive dashboard for visualization



**Megha**
GitHub: [https://github.com/megha461](https://github.com/megha461)


