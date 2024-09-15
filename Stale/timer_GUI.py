import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time

from timerApp import TimeTracker

class PomodoroGUI:
    def __init__(self, root, tracker):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.tracker = tracker

        # Create widgets
        self.label = tk.Label(root, text="Pomodoro Timer", font=("Times New Roman", 24))
        self.label.pack(pady=20)

        # Display message
        self.time_label = tk.Label(root, text=self.tracker.time_formating(self.tracker.focus_duration), font=("Times New Roman", 48))
        self.time_label.pack()

        # Buttons

        # Start button
        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=20)

        # Stop button
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side=tk.RIGHT, padx=20)

        # Control variable
        self.is_running = False

    # Update the labels
    def update_label(self, text):
        self.label.config(text=text)
        self.label.update()

    def update_time_label(self, text):
        self.time_label.config(text=text)
        self.time_label.update()


    # Start the timer
    def start_timer(self):
        self.is_running = True
        timer_thread = Thread(target=self.run_timer)
        timer_thread.daemon = True
        timer_thread.start()

    # Stop the timer
    def stop_timer(self):
        self.is_running = False


    def run_timer(self):
        while self.tracker.completed_cycles < self.tracker.total_cycles and self.is_running:
            # Start focus session and update label
            self.update_label(f"Focus session: #{self.tracker.completed_cycles + 1}")
            self._countdown(self.tracker.focus_duration)

            if self.is_running or self.tracker.pressed_q:
                break
            if self.tracker.completed_cycles % self.tracker.cycles_to_long_break == 0:
                self.update_label("Long break")
                self._countdown(self.tracker.long_break, break_time=True)
            else:
                self.update_label("Short break")
                self._countdown(self.tracker.short_break, break_time=True)

    def _countdown(self, countdown_time, break_time=False):
        """Method to handle the countdown and update the GUI"""
        while countdown_time > 0 and self.is_running:
            timer = self.tracker.time_formating(countdown_time)
            self.update_time_label(timer)
            time.sleep(1)
            countdown_time -= 1

        # Here either:
        # 1. The countdown has finished
        # 2. The user has stopped the timer (self.is_running = False)

        if self.is_running:     # If the timer has finished
            if break_time:      # And it was a break
                self.update_label("Break time is over!")
            else:               # If it was a focus session
                self.update_label("Focus session is over!")
                self.tracker.completed_cycles += 1
            time.sleep(2)       # Pause to display message
            
        

# Run the application
if __name__ == "__main__":
    time_tracker = TimeTracker(focus_duration=0.2, short_break=0.05, long_break=0.1, total_cycles=5, cycles_to_long_break=2)
    root = tk.Tk()
    gui = PomodoroGUI(root, time_tracker)
    root.mainloop()