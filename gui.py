import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time

from timerApp import TimeTracker

class Sharptiming:
	
	def __init__(self, root, focus_duration=25, short_break=5, long_break=15, cycles_to_long_break=4):
		self.root = root
		self.root.title("Sharptiming")
		
		# Pomodoro variables
		# Convert minutes to seconds
		self.focus_duration = focus_duration * 60
		self.short_break = short_break * 60
		self.long_break = long_break * 60

		# Number of focus sessions before a long break
		self.cycles_to_long_break = cycles_to_long_break

		# Create widgets
		self.label = tk.Label(root, text="Sharptiming", font=("Times New Roman", 24))
		self.label.pack(padx=0, pady=20)

		# Display message

		self.timer_type = self.focus_timer()

		self.time_label = tk.Label(root, text=self.time_formating(self.focus_duration), font=("Times New Roman", 48))
		self.time_label.pack()

		# Buttons
		# Start button
		self.start_button = tk.Button(root, text="Start", command=self.start_timer)
		self.start_button.pack(side=tk.LEFT, padx=20)

		# Stop button
		self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer)
		self.stop_button.pack(side=tk.RIGHT, padx=20)

		# Focus button
		self.focus_button = tk.Button(root, text="Focus", command=self.focus_timer)
		self.focus_button.pack(side=tk.LEFT, padx=40)

		# Short break button
		self.short_break_button = tk.Button(root, text="Short Break", command=self.short_break_timer)
		self.short_break_button.pack(side=tk.LEFT, padx=40)

		# Long break button
		self.long_break_button = tk.Button(root, text="Long Break", command=self.long_break_timer)
		self.long_break_button.pack(side=tk.LEFT, padx=40)


	def time_formating(self, time_seconds, show_hours=False):
		mins, secs = divmod(time_seconds, 60)
		if show_hours:
			hours, mins = divmod(mins, 60)
			return f"{hours:02d}:{mins:02d}:{secs:02d}"
		return f"{mins:02d}:{secs:02d}"
	
	def start_timer(self):
		print("Timer started.")

	def stop_timer(self):
		print("Timer stopped.")

	def focus_timer(self):
		print("Focus timer.")
		return tk.Label(self.root, text="Pomodoro", font=("Times New Roman", 48))

	def short_break_timer(self):
		print("Short break timer.")
		return tk.Label(self.root, text="Short Break", font=("Times New Roman", 48))

	def long_break_timer(self):
		print("Long break timer.")
		return tk.Label(self.root, text="Long Break", font=("Times New Roman", 48))


# Run app
if __name__ == "__main__":
	root = tk.Tk()
	tracker = TimeTracker()
	app = Sharptiming(root)
	root.mainloop()