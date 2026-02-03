from tkinter import *
import speech_recognition as sr
import pyttsx3

def weather():
    import Api
    Api.mains()

def analyze():
    import rainfall_pred
    rainfall_pred.analyzge()

def pred():
    import temp_model
    temp_model.predict()

def ori():
    import temp_model
    temp_model.original()

def compare():
    import compare_cities
    compare_cities.compare_cities()

def main():    
    root = Tk()
    root.geometry("1000x900")
    root.title("Weather App")
    root.configure(bg='#2C3539')

    f = ("poppins", 15, "bold")
    t = ("poppins", 35, "bold")

    title = Label(root, text="\nWEATHER REPORT\n", font=t, bg="#837E7C", fg="white", width=30)
    title.pack(pady=10)

    result_label = Label(root, text="", font=("poppins", 20, "bold"), bg="#2C3539", fg="white")
    result_label.pack(pady=20)

    def tomorrow():
        import rainfall_pred
        rainfall_pred.possible_rain()  

        result_text = rainfall_pred.predict_custom_gui() 
        if "rain" in result_text.lower():
            result_label.config(text=f"🌧 {result_text}", fg="skyblue")
        else:
            result_label.config(text=f"☀️ {result_text}", fg="gold")

    Button(root, text='Analyze average rainfall (India)',
           fg='green', command=analyze, font=f, bg='#0C090A').pack(pady=10)
    
    Button(root, text='Current weather report for specific city',
           command=weather, fg='red', font=f, bg='#0C090A').pack(pady=10)
    
    Button(root, text='Predict rainfall tomorrow?',
           fg='blue', command=tomorrow, font=f, bg='#0C090A').pack(pady=10)
    
    
    Button(root, text='Predict temperature for year',
           fg='pink', command=pred, font=f, bg='#0C090A').pack(pady=10)
    
    Button(root, text='Original vs Predicted temperature',
           fg='yellow', command=ori, font=f, bg='#0C090A').pack(pady=10)
    
    Button(root, text='Compare Two Cities 🌍', fg='white', bg='#0C090A', 
       font=f, command=compare).pack(pady=10)


    root.mainloop()


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

engine.say("Hi, I am Alexa. Do you want to use voice mode?")
engine.runAndWait()


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take():
    try:
        with sr.Microphone() as source:
            print("🎧 Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print("You said:", command)
    except Exception as e:
        print("⚠️ Voice error:", e)
        command = 'please say correctly'
    return command


def run_alexa():
    talk("Say your query. For example, city, tomorrow, analyze, predict, or original.")
    command = take()

    if 'city' in command:
        weather()
    elif 'tomorrow' in command:
        import rainfall_pred
        rainfall_pred.possible_rain()
        rainfall_pred.predict_custom()
    elif 'analyze' in command:
        analyze()
    elif 'predict' in command:
        pred()
    elif 'original' in command:
        ori()
    else:
        main()


if __name__ == "__main__":
    run_alexa()
