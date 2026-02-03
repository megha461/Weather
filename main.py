import tkinter as tk

def answer(event=None):
    choice = textField.get()
    if choice == '1':
        import Api
        Api.mains()
    elif choice == '2':
        import rainfall_pred
        rainfall_pred.possible_rain()
    elif choice == '3':
        import rainfall_pred
        rainfall_pred.analyze()

if __name__ == "__main__":
    canvas = tk.Tk()
    canvas.title("Weather App")
    canvas.configure(bg='#6b8e23')

    f = ("poppins", 15, "bold")
    t = ("poppins", 25, "bold")

    label1 = tk.Label(canvas, text="\nWeather Report Menu\n", font=t, bg="#6b8e23", fg="white")
    label1.pack()

    menu_text = "1: Current Weather Report\n2: Predict Rainfall Tomorrow\n3: Analyze Average Rainfall (India)"
    label2 = tk.Label(canvas, text=menu_text, font=f, bg="#6b8e23", fg="white")
    label2.pack(pady=10)

    textField = tk.Entry(canvas, justify='center', width=10, font=t, fg="red", bg="#C04000")
    textField.pack(pady=20)
    textField.focus()
    textField.bind('<Return>', answer)

    canvas.mainloop()

