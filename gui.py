import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time

from timerApp import TimeTracker

class Sharptiming:
	
	def __init__(self, root, focus_duration=0.2, short_break=0.05, long_break=0.1, cycles_to_long_break=4):

		# Root window and title
		self.root = root
		self.root.title("Sharptiming")
		
		# Pomodoro variables
		# Convert minutes to seconds
		self.focus_duration = int(focus_duration * 60)
		self.short_break = int(short_break * 60)
		self.long_break = int(long_break * 60)

		self.is_focus_ = True
		self.is_long_ = False

		# Number of focus sessions before a long break
		self.cycles_to_long_break = cycles_to_long_break
		self.completed_cycles = 0

		# Initialize stat variables
		self.time_focused = 0
		self.time_break = 0

		self.elapsed_focus_time = 0
		self.elapsed_break_time = 0

		self.is_running = False


		# Create widgets

		# Type of timer label (Focus, Short Break, Long Break)
		self.label = tk.Label(root, text="Sharptiming", font=("Times New Roman", 24))
		self.label.pack(padx=0, pady=20)

		# Display message

	
		# Display time label
		self.time_label = tk.Label(root, text=self.time_formating(self.focus_duration), font=("Times New Roman", 48))
		self.time_label.pack()

		self.focus_timer()

		
		# Buttons
		# Start button
		self.start_button = tk.Button(root, text="Start", command=self.start_timer)
		self.start_button.pack(side=tk.LEFT, padx=20)

		# Stop button
		self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer)
		self.stop_button.pack(side=tk.LEFT, padx=20)

		# Focus button
		self.focus_button = tk.Button(root, text="Focus", command=self.focus_timer)
		self.focus_button.pack(side=tk.LEFT, padx=40)

		# Short break button
		self.short_break_button = tk.Button(root, text="Short Break", command=self.short_break_timer)
		self.short_break_button.pack(side=tk.LEFT, padx=40)

		# Long break button
		self.long_break_button = tk.Button(root, text="Long Break", command=self.long_break_timer)
		self.long_break_button.pack(side=tk.LEFT, padx=40)

		# Stats button
		self.stats_button = tk.Button(root, text="Stats", command=self.show_stats)
		self.stats_button.pack(side=tk.LEFT, padx=40)


	def time_formating(self, time_seconds, show_hours=False):
		mins, secs = divmod(time_seconds, 60)
		if show_hours:
			hours, mins = divmod(mins, 60)
			return f"{hours:02d}:{mins:02d}:{secs:02d}"
		return f"{mins:02d}:{secs:02d}"
	
	def start_timer(self):
		self.is_running = True
		print("Timer started.")
		self._countdown()

	def stop_timer(self):
		self.is_running = False
		print("Timer stopped.")


	def show_stats(self):
		self.is_running = False
		self.time_focused += self.elapsed_focus_time
		self.time_break += self.elapsed_break_time
		
		ft_message = f"Time focused: {self.time_formating(self.time_focused, show_hours=True)}\n"
		bt_message = f"Time on break: {self.time_formating(self.time_break, show_hours=True)}\n"
		message = ft_message + bt_message
		messagebox.showinfo("Stats", message)
	

		

	def focus_timer(self):
		# Control variables
		self.is_focus_ = True
		self.is_long_ = False
		self.is_running = False
		self.elapsed_focus_time = 0

		# Update label (timer type)
		print("Focus timer.")
		self.label.config(text="Focus")
		self.label.update()

		# Update timer label
	
		self.time_label.config(text=self.time_formating(self.focus_duration))
		self.time_label.update()

	def short_break_timer(self):
		# Control variables
		self.is_focus_ = False
		self.is_long_ = False
		self.is_running = False

		# Update label (timer type)
		print("Short break timer.")
		self.label.config(text="Short Break")
		self.label.update()

		# Update timer label
		self.time_label.config(text=self.time_formating(self.short_break))
		self.time_label.update()

	def long_break_timer(self):
		# Control variables
		self.is_focus_ = False
		self.is_long_ = True
		self.is_running = False

		# Update label (timer type)
		print("Long break timer.")
		self.label.config(text="Long Break")
		self.label.update()

		# Update timer label
		self.time_label.config(text=self.time_formating(self.long_break))
		self.time_label.update()

	def countdown_time(self):
		"""Method to calculate the countdown time"""
		if self.is_focus_:
			if self.elapsed_focus_time > 0:
				countdown_time = self.focus_duration - self.elapsed_focus_time
			else:
				countdown_time = self.focus_duration
		else:
			if self.elapsed_break_time > 0:
				if self.is_long_:
					countdown_time = self.long_break - self.elapsed_break_time
				else:
					countdown_time = self.short_break - self.elapsed_break_time
			
			else:
				if self.is_long_:
					countdown_time = self.long_break
				else:
					countdown_time = self.short_break

		return countdown_time

	def _countdown(self):
		"""Method to handle the countdown and update the GUI"""
		
		countdown_time = self.countdown_time()
		
		while countdown_time > -1 and self.is_running:
			timer = self.time_formating(countdown_time)
			self.time_label.config(text=timer)
			self.time_label.update()
			time.sleep(1)
			countdown_time -= 1

		# Here either:
		# 1. The countdown has finished
		# 2. The user has stopped the timer (self.is_running = False)
		if self.is_running:
			# It means the timer is 0
			if self.is_focus_:
				self.label.config(text="Focus session is over!")
				self.label.update()
				self.elapsed_focus_time = 0
				self.completed_cycles += 1
				self.time_focused += self.focus_duration 	# Add focus time
				if self.completed_cycles % self.cycles_to_long_break == 0:
					self.long_break_timer()
				else:
					self.short_break_timer()
			else:
				self.label.config(text="Break time is over!")
				self.label.update()
				self.elapsed_break_time = 0
				if self.is_long_:
					self.time_break += self.long_break
				else:
					self.time_break += self.short_break
				self.focus_timer()
		else:
			# User stopped the timer
			if self.is_focus_:
				self.label.config(text="Focus session paused.")
				self.label.update()
				self.elapsed_focus_time = self.focus_duration - countdown_time
			else:
				self.label.config(text="Break paused.")
				self.label.update()
				if self.is_long_:
					self.elapsed_break_time = self.long_break - countdown_time
				else:
					self.elapsed_break_time = self.short_break - countdown_time			



# Run app
if __name__ == "__main__":
	root = tk.Tk()
	app = Sharptiming(root)
	root.mainloop()