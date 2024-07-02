import tkinter as tk
from tkinter import ttk

class JungleTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.root.geometry("115x40+430+840")  # Width x Height + 
        self.root.attributes("-topmost", True)  # Keep the window on top of other windows

        self.style = ttk.Style()
        self.style.configure("LightGreen.TButton", foreground="#90EE90")  # Light green
        self.style.configure("LightBlue.TButton", foreground="lightblue")
        self.style.configure("Orange.TButton", foreground="orange")
        self.style.configure("Red.TButton", foreground="#fff333")
        self.style.configure("White.TButton", foreground="white")

        self.create_widgets()

    def create_widgets(self):
        # Define the timers with labels and durations
        self.timers = [
            {"label": "", "duration": 2, "running": False, "initial_duration": 2*60+15},
        ]

        self.timer_vars = []  # List to store StringVars for timer text
        self.timer_buttons = []  # List to store button references

        # Create the UI for each timer
        for idx, timer in enumerate(self.timers):
            frame = ttk.Frame(self.root, padding="5")
            frame.grid(row=0, column=idx, sticky=(tk.W, tk.E))  # Place frames in a single row and multiple columns

            time_var = tk.StringVar()
            time_var.set(self.format_time(timer["duration"]))  # Set initial timer text
            self.timer_vars.append(time_var)
            
            # Create a button that includes the label and timer display
            timer_button = ttk.Button(frame, text=f"{timer['label']} {self.format_time(timer['duration'])}", style="Black.TButton")
            timer_button.config(command=lambda t=timer, v=time_var, b=timer_button: self.start_timer(t, v, b))
            timer_button.pack(fill='x', padx=(5, 5), pady=(5, 5))  # Adjust padding for smaller margins

            self.timer_buttons.append(timer_button)

    def start_timer(self, timer, time_var, timer_button):
        if not timer["running"]:
            timer["running"] = True  # Set timer as running
            self.update_color(timer_button, timer["duration"])  # Update color initially
            self.countdown(timer, timer["duration"], time_var, timer_button)  # Start countdown

    def countdown(self, timer, remaining_time, time_var, timer_button):
        if remaining_time >= 0:
            time_var.set(self.format_time(remaining_time))  # Update the displayed time
            timer_button.config(text=f"{timer['label']} {self.format_time(remaining_time)}")  # Update button text
            self.update_color(timer_button, remaining_time)  # Update the color based on remaining time
            self.root.after(1000, self.countdown, timer, remaining_time-1, time_var, timer_button)  # Call countdown again after 1 second
        else:
            timer["running"] = False  # Timer has finished
            timer_button.config(style="Black.TButton")  # Reset color
            # Reset timer to initial duration
            timer["duration"] = timer["initial_duration"]
            time_var.set(self.format_time(timer["initial_duration"]))
            timer_button.config(text=f"{timer['label']} {self.format_time(timer['initial_duration'])}")

    def format_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02}"  # Format time as MM:SS

    def update_color(self, timer_button, remaining_time):
        # Change the color of the timer text based on the remaining time
        if remaining_time > 2*60:
            timer_button.config(style="LightGreen.TButton")  # Changed to light green
        elif remaining_time > 60:
            timer_button.config(style="LightBlue.TButton")  # Changed to light blue
        elif remaining_time > 10:
            timer_button.config(style="Orange.TButton")
        else:
            timer_button.config(style="Red.TButton")

if __name__ == "__main__":
    root = tk.Tk()
    app = JungleTimerApp(root)
    root.mainloop()