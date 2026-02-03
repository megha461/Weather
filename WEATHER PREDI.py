import requests
from tkinter import *
from tkinter import messagebox

def mains():
    """
    Display an interactive weather dashboard using OpenWeatherMap API
    """
    def get_weather():
        city = city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name!")
            return

        api_key = "744718eab3d5ec3ceba70043ef45abcc"   
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric"}

        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            if data.get("cod") != 200:
                weather_label.config(
                    text=f"❌ {data.get('message', 'City not found').capitalize()}",
                    fg="red"
                )
                return

            
            weather = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            pressure = data["main"]["pressure"]
            country = data["sys"].get("country", "")
            icon_code = data["weather"][0]["icon"]

            # Update labels
            header_label.config(text=f"{city.title()}, {country}")
            temp_label.config(text=f"{temp:.1f}°C (Feels like {feels_like:.1f}°C)")
            weather_label.config(text=f"{weather}")
            details_label.config(
                text=f"💧 Humidity: {humidity}%   🌬 Wind: {wind} m/s   🔹 Pressure: {pressure} hPa"
            )

            
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            from urllib.request import urlopen
            from PIL import Image, ImageTk
            import io
            image_data = urlopen(icon_url).read()
            img = Image.open(io.BytesIO(image_data))
            img = img.resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            icon_label.config(image=photo)
            icon_label.image = photo

        except Exception as e:
            weather_label.config(text=f"⚠️ Error: {e}", fg="red")


    win = Toplevel()
    win.title("🌤 Live Weather Dashboard")
    win.geometry("500x500")
    win.configure(bg="#1e1e1e")

    Label(win, text="Enter City", font=("poppins", 14, "bold"), bg="#1e1e1e", fg="white").pack(pady=10)

    city_entry = Entry(win, font=("poppins", 14), justify="center", width=20)
    city_entry.pack(pady=5)

    Button(win, text="Get Weather", font=("poppins", 12, "bold"),
           bg="#00bfff", fg="white", command=get_weather).pack(pady=10)

    header_label = Label(win, text="", font=("poppins", 18, "bold"), bg="#1e1e1e", fg="white")
    header_label.pack(pady=10)

    icon_label = Label(win, bg="#1e1e1e")
    icon_label.pack()

    temp_label = Label(win, text="", font=("poppins", 24, "bold"), bg="#1e1e1e", fg="#ffcc00")
    temp_label.pack(pady=10)

    weather_label = Label(win, text="", font=("poppins", 16), bg="#1e1e1e", fg="#b0c4de")
    weather_label.pack(pady=5)

    details_label = Label(win, text="", font=("poppins", 12), bg="#1e1e1e", fg="#a0a0a0")
    details_label.pack(pady=10)

    win.mainloop()
