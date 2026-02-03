import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
import io

API_KEY = "744718eab3d5ec3ceba70043ef45abcc"

def compare_cities():
    root = tk.Toplevel()
    root.title("🌍 Compare Two Cities")
    root.geometry("850x650")
    root.configure(bg="#0E0F1A")

    # Title
    tk.Label(root, text="🌎 Compare Two Cities", font=("Poppins", 22, "bold"),
             bg="#0E0F1A", fg="white").pack(pady=20)

    # Inputs
    input_frame = tk.Frame(root, bg="#0E0F1A")
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="City 1:", font=("Poppins", 13), bg="#0E0F1A", fg="white").grid(row=0, column=0, padx=10)
    city1_entry = tk.Entry(input_frame, font=("Poppins", 13), justify="center", width=18, relief="flat")
    city1_entry.grid(row=0, column=1)

    tk.Label(input_frame, text="City 2:", font=("Poppins", 13), bg="#0E0F1A", fg="white").grid(row=0, column=2, padx=10)
    city2_entry = tk.Entry(input_frame, font=("Poppins", 13), justify="center", width=18, relief="flat")
    city2_entry.grid(row=0, column=3)

    result_frame = tk.Frame(root, bg="#0E0F1A")
    result_frame.pack(pady=30)

    # City result labels
    left_panel = tk.Frame(result_frame, bg="#1A1C2B", bd=3, relief="ridge")
    left_panel.grid(row=0, column=0, padx=20)

    right_panel = tk.Frame(result_frame, bg="#1A1C2B", bd=3, relief="ridge")
    right_panel.grid(row=0, column=1, padx=20)

    city1_label = tk.Label(left_panel, text="", font=("Poppins", 14, "bold"), bg="#1A1C2B", fg="white")
    city1_label.pack(pady=5)
    city2_label = tk.Label(right_panel, text="", font=("Poppins", 14, "bold"), bg="#1A1C2B", fg="white")
    city2_label.pack(pady=5)

    city1_data = tk.Label(left_panel, text="", font=("Poppins", 12), bg="#1A1C2B", fg="#00ADB5", justify="left")
    city1_data.pack(pady=10)

    city2_data = tk.Label(right_panel, text="", font=("Poppins", 12), bg="#1A1C2B", fg="#00ADB5", justify="left")
    city2_data.pack(pady=10)

    best_label = tk.Label(root, text="", font=("Poppins", 16, "bold"), bg="#0E0F1A", fg="#00FF99")
    best_label.pack(pady=15)

    # Fetch data
    def fetch_weather(city):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            icon_code = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_data = requests.get(icon_url).content
            img = Image.open(io.BytesIO(icon_data))
            icon = ImageTk.PhotoImage(img)

            return {
                "city": city.title(),
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "condition": data["weather"][0]["description"].title(),
                "icon": icon
            }
        else:
            return None

    def compare():
        city1 = city1_entry.get().strip()
        city2 = city2_entry.get().strip()
        if not city1 or not city2:
            messagebox.showwarning("Warning", "Please enter both cities!")
            return

        w1 = fetch_weather(city1)
        w2 = fetch_weather(city2)
        if not w1 or not w2:
            messagebox.showerror("Error", "City not found or API issue.")
            return

        city1_label.config(text=w1['city'])
        city2_label.config(text=w2['city'])
        city1_data.config(text=f"🌡 {w1['temp']}°C\n💧 {w1['humidity']}%\n🌬 {w1['wind']} m/s\n☁ {w1['condition']}")
        city2_data.config(text=f"🌡 {w2['temp']}°C\n💧 {w2['humidity']}%\n🌬 {w2['wind']} m/s\n☁ {w2['condition']}")

        city1_label.image = w1['icon']
        city2_label.image = w2['icon']

        tk.Label(left_panel, image=w1['icon'], bg="#1A1C2B").pack()
        tk.Label(right_panel, image=w2['icon'], bg="#1A1C2B").pack()

        better_city = w1['city'] if w1['humidity'] < w2['humidity'] else w2['city']
        best_label.config(text=f"🏖️ Better to Visit Today: {better_city}")

        if better_city == w1['city']:
            left_panel.config(highlightthickness=3, highlightbackground="#00FF99")
            right_panel.config(highlightthickness=0)
        else:
            right_panel.config(highlightthickness=3, highlightbackground="#00FF99")
            left_panel.config(highlightthickness=0)

        # Comparison chart
        labels = ["Temperature (°C)", "Humidity (%)", "Wind Speed (m/s)"]
        city1_vals = [w1['temp'], w1['humidity'], w1['wind']]
        city2_vals = [w2['temp'], w2['humidity'], w2['wind']]

        x = np.arange(len(labels))
        width = 0.35

        plt.figure(figsize=(8,6))
        plt.bar(x - width/2, city1_vals, width, label=w1['city'], color='#00ADB5')
        plt.bar(x + width/2, city2_vals, width, label=w2['city'], color='#FF9800')
        plt.xticks(x, labels)
        plt.ylabel("Value")
        plt.title(f"Weather Comparison: {w1['city']} vs {w2['city']}")
        plt.legend()
        plt.tight_layout()
        plt.show()

    tk.Button(root, text="Compare", font=("Poppins", 14, "bold"),
              bg="#00ADB5", fg="white", activebackground="#393e46",
              activeforeground="white", relief="flat", width=15,
              command=compare).pack(pady=10)

    root.mainloop()
