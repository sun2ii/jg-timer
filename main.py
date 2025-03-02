import tkinter as tk
from tkinter import ttk

class JungleTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.root.geometry("105x40+430+840")  # Width x Height + Right + Top
        self.root.attributes("-topmost", True)  # Keep the window on top of other windows

        self.style = ttk.Style()

        self.style.configure("LightGreen.TButton", foreground="#90EE90") 
        self.style.configure("LightBlue.TButton", foreground="lightblue")
        self.style.configure("Orange.TButton", foreground="orange")
        self.style.configure("Red.TButton", foreground="#ff0000")
        self.style.configure("White.TButton", foreground="white")

        self.create_widgets()

    def create_widgets(self):
        # Define the timers with labels and durations
        self.timers = [
            {"label": "", "duration": 135, "running": False, "initial_duration": 135, "timer_id": None, "press_count": 0, "count_up": False},
        ]

        self.timer_vars = []  # List to store StringVars for timer text
        self.timer_buttons = []  # List to store button references

        # Create the UI for each timer
        for idx, timer in enumerate(self.timers):
            frame = ttk.Frame(self.root, padding="2")
            frame.grid(row=0, column=idx, sticky=(tk.W, tk.E))  # Place frames in a single row and multiple columns

            time_var = tk.StringVar()
            time_var.set(self.format_time(timer["duration"]))  # Set initial timer text
            self.timer_vars.append(time_var)
            
            # Create a button that includes the label and timer display
            timer_button = ttk.Button(frame, text=f"({timer['press_count']}) {self.format_time(timer['duration'])}", style="White.TButton")
            timer_button.config(command=lambda t=timer, v=time_var, b=timer_button: self.start_timer(t, v, b))
            timer_button.pack(fill='x', padx=(3, 3), pady=(3, 3))  # Adjust padding for smaller margins

            self.timer_buttons.append(timer_button)

    def start_timer(self, timer, time_var, timer_button):
        # Cancel any existing countdown
        if timer["timer_id"] is not None:
            self.root.after_cancel(timer["timer_id"])
        
        timer["press_count"] += 1  # Increment the press count
        timer["running"] = True  # Set timer as running
        timer["count_up"] = False  # Reset count up state
        timer["duration"] = timer["initial_duration"]  # Reset timer to initial duration
        time_var.set(self.format_time(timer["duration"]))  # Set initial timer text
        timer_button.config(text=f"({timer['press_count']}) {self.format_time(timer['duration'])}")  # Update button text
        self.update_color(timer_button, timer["duration"])  # Update color initially
        
        # Start a new countdown and save the after callback ID
        timer["timer_id"] = self.root.after(1000, self.countdown, timer, timer["duration"] - 1, time_var, timer_button)

    def countdown(self, timer, remaining_time, time_var, timer_button):
        if remaining_time >= 0 and not timer["count_up"]:
            time_var.set(self.format_time(remaining_time))  # Update the displayed time
            timer_button.config(text=f"({timer['press_count']}) {self.format_time(remaining_time)}")  # Update button text
            self.update_color(timer_button, remaining_time)  # Update the color based on remaining time
            # Schedule the next countdown and save the after callback ID
            timer["timer_id"] = self.root.after(1000, self.countdown, timer, remaining_time - 1, time_var, timer_button)
        else:
            timer["count_up"] = True
            remaining_time += 1  # Start counting up
            time_var.set(f"+{self.format_time(remaining_time)}")
            timer_button.config(text=f"({timer['press_count']}) +{self.format_time(remaining_time)}")
            # Schedule the next count up and save the after callback ID
            timer["timer_id"] = self.root.after(1000, self.countdown, timer, remaining_time, time_var, timer_button)

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
        elif remaining_time > 33:
            timer_button.config(style="Orange.TButton")
        else:
            timer_button.config(style="Red.TButton")

if __name__ == "__main__":
    root = tk.Tk()
    app = JungleTimerApp(root)
    root.mainloop()