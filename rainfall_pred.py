import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

# Load dataset
df_path = "weatherAS.csv"

try:
    df = pd.read_csv(df_path)
except FileNotFoundError:
    messagebox.showerror("Error", f"File not found: {df_path}")
    raise SystemExit

# Replace Yes/No with 1/0
df = df.replace({'Yes': 1, 'No': 0})

essential_cols = ['Rainfall','Humidity9am','Humidity3pm','Pressure9am','Pressure3pm',
                  'Temp9am','Temp3pm','RainToday','RainTomorrow']
df = df[essential_cols].dropna()

X = df.drop('RainTomorrow', axis=1)
y = df['RainTomorrow']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# TRAIN BOTH MODELS

rf_model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
rf_model.fit(X_train, y_train)

dt_model = DecisionTreeClassifier(max_depth=8, random_state=42)
dt_model.fit(X_train, y_train)


# GUI
def rainfall_prediction_gui():
    root = tk.Tk()
    root.title("🌦️ Rainfall Predictor")
    root.geometry("550x750")
    root.configure(bg="#1c1f26")

    tk.Label(root, text="🌧️ Rainfall Predictor", font=("Poppins", 20, "bold"),
             bg="#1c1f26", fg="white").pack(pady=15)

    # Input labels
    input_labels = [
        "Rainfall (mm)", "Humidity 9am (%)", "Humidity 3pm (%)",
        "Pressure 9am (hPa)", "Pressure 3pm (hPa)",
        "Temp 9am (°C)", "Temp 3pm (°C)", "Rain Today"
    ]

    entries = []

    for lbl in input_labels:
        frame = tk.Frame(root, bg="#1c1f26")
        frame.pack(pady=5)
        tk.Label(frame, text=lbl, font=("Poppins", 12), bg="#1c1f26", fg="white").pack()
        if lbl == "Rain Today":
            var = tk.StringVar()
            var.set("No")
            tk.OptionMenu(frame, var, "Yes", "No").pack()
            entries.append(var)
        else:
            e = tk.Entry(frame, font=("Poppins", 12), justify="center")
            e.pack()
            entries.append(e)


    # MODEL SELECTION DROPDOWN
   
    tk.Label(root, text="Select Model", font=("Poppins", 12), bg="#1c1f26", fg="white").pack()
    selected_model = tk.StringVar()
    selected_model.set("Random Forest")
    tk.OptionMenu(root, selected_model, "Random Forest", "Decision Tree").pack(pady=5)

    result_label = tk.Label(root, text="", font=("Poppins", 14, "bold"),
                            bg="#1c1f26", fg="#00ff99")
    result_label.pack(pady=15)

    # Predict function
    def predict_rain():
        try:
            vals = []
            for i, e in enumerate(entries):
                if i == 7:  # Rain Today
                    val = 1 if e.get() == "Yes" else 0
                else:
                    val = float(e.get())
                vals.append(val)

            # Choose model
            if selected_model.get() == "Random Forest":
                model = rf_model
            else:
                model = dt_model

            prediction = model.predict([vals])[0]
            prob = model.predict_proba([vals])[0][1]

            if prediction == 1:
                result_label.config(text=f"🌧️ Rain expected tomorrow! Probability: {prob*100:.2f}%")
            else:
                result_label.config(text=f"☀️ No rain expected. Probability of rain: {prob*100:.2f}%")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    # Reset function
    def reset_inputs():
        for i, e in enumerate(entries):
            if i == 7:
                e.set("No")
            else:
                e.delete(0, tk.END)
        result_label.config(text="")

    # Feature importance (only for RF)
    def show_feature_importance():
        importances = rf_model.feature_importances_
        plt.figure(figsize=(8,6))
        plt.barh(X.columns, importances, color='teal')
        plt.xlabel("Feature Importance")
        plt.title("Random Forest Feature Importance")
        plt.show()
            # Decision Tree Feature Importance
    def show_dt_importance():
        importances = dt_model.feature_importances_
        plt.figure(figsize=(8,6))
        plt.barh(X.columns, importances)
        plt.xlabel("Feature Importance")
        plt.title("Decision Tree Feature Importance")
        plt.show()


    tk.Button(root, text="Predict", font=("Poppins", 12, "bold"), bg="#00adb5", fg="white",
              command=predict_rain, width=15).pack(pady=10)

    tk.Button(root, text="Reset", font=("Poppins", 12, "bold"), bg="#ff5722", fg="white",
              command=reset_inputs, width=15).pack(pady=5)

    tk.Button(root, text="Feature Importance", font=("Poppins", 12, "bold"), bg="#673ab7", fg="white",
              command=show_feature_importance, width=18).pack(pady=5)
    
    tk.Button(root, text="DT Feature Importance", font=("Poppins", 12, "bold"),
              bg="#9c27b0", fg="white", command=show_dt_importance, width=20).pack(pady=5)


    tk.Label(root, text="Model trained on Australian Rainfall dataset", font=("Poppins", 10),
             bg="#1c1f26", fg="#aaa").pack(side="bottom", pady=10)

    root.mainloop()

# Run GUI
rainfall_prediction_gui()
