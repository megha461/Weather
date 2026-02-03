import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# LOAD DATA
dataset = pd.read_csv('weatherHistory.csv')

dataset = dataset[['Temperature (C)', 'Apparent Temperature (C)', 'Humidity',
                   'Pressure (millibars)', 'Visibility (km)', 'Summary']]
dataset = dataset.dropna()

valid_conditions = ["Clear", "Cloudy", "Partly Cloudy", "Rain", "Foggy"]
dataset = dataset[dataset["Summary"].isin(valid_conditions)]
dataset["Summary"] = dataset["Summary"].astype(str)

dataset = pd.get_dummies(dataset, columns=["Summary"], drop_first=True)

X = dataset.drop("Temperature (C)", axis=1)
y = dataset["Temperature (C)"]
X_columns = X.columns

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# MODELS 
# Linear
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Random Forest
rf_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42
)
rf_model.fit(X_train, y_train)

# Polynomial Regression (degree 3)
poly_model = Pipeline([
    ("poly_features", PolynomialFeatures(degree=3, include_bias=False)),
    ("lin_reg", LinearRegression())
])
poly_model.fit(X_train, y_train)

# Decision Tree
dt_model = DecisionTreeRegressor(max_depth=10, random_state=42)
dt_model.fit(X_train, y_train)


# PRINT R2 AND MSE FOR ALL MODELS

print("\n================ MODEL PERFORMANCE ================\n")

# Linear Regression
y_pred_lr = lr_model.predict(X_test)
print("📌 Linear Regression")
print("R² Score:", r2_score(y_test, y_pred_lr))
print("MSE:", mean_squared_error(y_test, y_pred_lr), "\n")

# Random Forest
y_pred_rf = rf_model.predict(X_test)
print("📌 Random Forest")
print("R² Score:", r2_score(y_test, y_pred_rf))
print("MSE:", mean_squared_error(y_test, y_pred_rf), "\n")

# Polynomial Regression
y_pred_poly = poly_model.predict(X_test)
print("📌 Polynomial Regression")
print("R² Score:", r2_score(y_test, y_pred_poly))
print("MSE:", mean_squared_error(y_test, y_pred_poly), "\n")

# Decision Tree
y_pred_dt = dt_model.predict(X_test)
print("📌 Decision Tree")
print("R² Score:", r2_score(y_test, y_pred_dt))
print("MSE:", mean_squared_error(y_test, y_pred_dt), "\n")

def generate_recommendations(pred_temp, weather_summary, humidity):
    recommendations = []
    if pred_temp > 35:
        recommendations.append("🌞 It’s very hot today! Stay hydrated.")
    elif pred_temp < 10:
        recommendations.append("❄ It’s cold! Wear warm clothes.")
    else:
        recommendations.append("🌡 Moderate temperature. Enjoy your day!")

    if weather_summary.lower() in ["rain", "partly cloudy"]:
        recommendations.append("☔ Carry an umbrella.")
    if weather_summary.lower() == "foggy":
        recommendations.append("🌁 Drive carefully due to fog.")
    if humidity > 80:
        recommendations.append("💧 High humidity today.")

    return recommendations

def predict(model_type):

    if model_type == "linear":
        model = lr_model
    elif model_type == "rf":
        model = rf_model
    elif model_type == "poly":
        model = poly_model
    elif model_type == "dt":
        model = dt_model

    prediction_window = tk.Toplevel()
    prediction_window.title("🌡 Predict Temperature")
    prediction_window.geometry("550x700")
    prediction_window.configure(bg="#1c1f26")

    labels = ["Apparent Temperature (°C)", "Humidity", "Pressure (millibars)",
              "Visibility (km)", "Weather Summary"]

    entries = []
    tk.Label(prediction_window, text="🌡 Predict Temperature", font=("Poppins", 22, "bold"),
             bg="#1c1f26", fg="white").pack(pady=20)

    for lbl in labels:
        frame = tk.Frame(prediction_window, bg="#1c1f26")
        frame.pack(pady=8)

        tk.Label(frame, text=lbl, font=("Poppins", 13),
                 bg="#1c1f26", fg="white").pack()

        if lbl == "Weather Summary":
            entry = tk.StringVar()
            options = ["Clear", "Cloudy", "Partly Cloudy", "Rain", "Foggy"]
            entry.set(options[0])
            tk.OptionMenu(frame, entry, *options).pack()
            entries.append(entry)
        else:
            entry = tk.Entry(frame, font=("Poppins", 13), justify="center", width=18)
            entry.pack()
            entries.append(entry)

    result_label = tk.Label(prediction_window, text="", font=("Poppins", 16, "bold"),
                            bg="#1c1f26", fg="#00ff99")
    result_label.pack(pady=20)

    report_data = {}

    def do_predict():
        try:
            vals = [float(e.get()) if isinstance(e, tk.Entry) else e.get() for e in entries]
            numeric_vals = vals[:4]
            cond_val = vals[4]

            cond_features = {
                "Summary_Cloudy": 0,
                "Summary_Foggy": 0,
                "Summary_Partly Cloudy": 0,
                "Summary_Rain": 0
            }

            key = f"Summary_{cond_val}"
            if key in cond_features:
                cond_features[key] = 1

            input_dict = {
                "Apparent Temperature (C)": numeric_vals[0],
                "Humidity": numeric_vals[1],
                "Pressure (millibars)": numeric_vals[2],
                "Visibility (km)": numeric_vals[3],
                **cond_features
            }

            input_df = pd.DataFrame([input_dict])
            input_df = input_df.reindex(columns=X_columns, fill_value=0)
            scaled = scaler.transform(input_df)

            pred_temp = model.predict(scaled)[0]

            recs = generate_recommendations(pred_temp, cond_val, numeric_vals[1])

            result_label.config(text=f"Predicted Temperature: {pred_temp:.2f} °C\n" +
                                     "\n".join(recs))

            report_data.clear()
            report_data.update(input_dict)
            report_data["Predicted Temperature"] = round(pred_temp, 2)

        except Exception as e:
            messagebox.showerror("Error", f"Invalid Input: {e}")

    tk.Button(prediction_window, text="Predict",
              font=("Poppins", 14, "bold"), bg="#00adb5", fg="white",
              width=15, command=do_predict).pack(pady=10)


# ORIGINAL VS PREDICTED GRAPH 
def original(model_type):

    if model_type == "linear":
        model = lr_model
    elif model_type == "rf":
        model = rf_model
    elif model_type == "poly":
        model = poly_model
    elif model_type == "dt":
        model = dt_model

    y_pred = model.predict(X_scaled)

    plt.figure(figsize=(8, 6))
    plt.scatter(y, y_pred, alpha=0.6, edgecolor='black')
    line = np.linspace(y.min(), y.max(), 100)
    plt.plot(line, line, "r--")

    plt.title(f"Original vs Predicted ({model_type.upper()})")
    plt.xlabel("Actual Temperature")
    plt.ylabel("Predicted Temperature")

    plt.grid(True)
    plt.show()


# RESIDUAL PLOT 
def residual_plot(model_type):

    if model_type == "linear":
        model = lr_model
    elif model_type == "rf":
        model = rf_model
    elif model_type == "poly":
        model = poly_model
    elif model_type == "dt":
        model = dt_model

    y_pred = model.predict(X_scaled)
    residuals = y - y_pred

    plt.figure(figsize=(8, 6))
    plt.scatter(y_pred, residuals, alpha=0.6, edgecolor='black')
    plt.axhline(0, color="red", linestyle="--")

    plt.title(f"Residual Plot ({model_type.upper()})")
    plt.xlabel("Predicted")
    plt.ylabel("Residuals")
    plt.grid(True)
    plt.show()

root = tk.Tk()
root.title("🌤 Weather Temperature Predictor")
root.geometry("450x700")
root.configure(bg="#1c1f26")

tk.Label(root, text="🌤 Weather Temperature Predictor",
         font=("Poppins", 18, "bold"), bg="#1c1f26", fg="white").pack(pady=20)

# PREDICT BUTTONS
tk.Button(root, text="Predict (Linear Regression)", font=("Poppins", 14, "bold"),
          bg="#00adb5", fg="white", command=lambda: predict("linear")).pack(pady=8)

tk.Button(root, text="Predict (Random Forest)", font=("Poppins", 14, "bold"),
          bg="#2196F3", fg="white", command=lambda: predict("rf")).pack(pady=8)

tk.Button(root, text="Predict (Polynomial Regression)", font=("Poppins", 14, "bold"),
          bg="#8BC34A", fg="white", command=lambda: predict("poly")).pack(pady=8)

tk.Button(root, text="Predict (Decision Tree)", font=("Poppins", 14, "bold"),
          bg="#9C27B0", fg="white", command=lambda: predict("dt")).pack(pady=8)

# ORIGINAL VS PREDICTED
tk.Button(root, text="Original vs Predicted (Linear)", font=("Poppins", 14, "bold"),
          bg="#ff5722", fg="white", command=lambda: original("linear")).pack(pady=8)

tk.Button(root, text="Original vs Predicted (Random Forest)", font=("Poppins", 14, "bold"),
          bg="#FF9800", fg="white", command=lambda: original("rf")).pack(pady=8)

tk.Button(root, text="Original vs Predicted (Polynomial)", font=("Poppins", 14, "bold"),
          bg="#4CAF50", fg="white", command=lambda: original("poly")).pack(pady=8)

tk.Button(root, text="Original vs Predicted (Decision Tree)", font=("Poppins", 14, "bold"),
          bg="#673AB7", fg="white", command=lambda: original("dt")).pack(pady=8)

# RESIDUAL PLOTS
tk.Button(root, text="Residual Plot (Linear)", font=("Poppins", 14, "bold"),
          bg="#673ab7", fg="white", command=lambda: residual_plot("linear")).pack(pady=8)

tk.Button(root, text="Residual Plot (Random Forest)", font=("Poppins", 14, "bold"),
          bg="#9c27b0", fg="white", command=lambda: residual_plot("rf")).pack(pady=8)

tk.Button(root, text="Residual Plot (Polynomial)", font=("Poppins", 14, "bold"),
          bg="#009688", fg="white", command=lambda: residual_plot("poly")).pack(pady=8)

tk.Button(root, text="Residual Plot (Decision Tree)", font=("Poppins", 14, "bold"),
          bg="#E91E63", fg="white", command=lambda: residual_plot("dt")).pack(pady=8)

root.mainloop()





