import time
import keyboard as kb
import json
from pathlib import Path

from colorama import Fore, Style, init
from playsound import playsound

# Initialize colorama
init(autoreset=True)

class TimeTracker:

	global bar_long, line_color, announce_color, focus_color, break_color, data_color, msg_color

	bar_long = 30
	line_colors = Fore.LIGHTWHITE_EX
	announce_color = Fore.MAGENTA
	focus_color = Fore.GREEN
	break_color = Fore.CYAN
	data_color = Fore.LIGHTMAGENTA_EX
	msg_color = Fore.LIGHTYELLOW_EX


	def __init__(self, focus_duration=25, short_break=5, long_break=15, cycles_to_long_break=4, total_cycles=4, project=None, task=None, data_file="pygame/data/tracked_time.json", sound_file="pygame/sounds/Sound_1.wav"):

		"""
			Attributes:
			- focus_duration: int
				The duration of the focus session in seconds.
				Default is 25 minutes.
			- short_break: int
				The duration of the short break in seconds.
				Deafult is 5 minutes.
			- long_break: int
				The duration of the long break in seconds.
				Default is 15 minutes.
			- total_cycles: int
				The number of focus sessions.
			- cycles_to_long_break: int
				The number of focus sessions before a long break.
				Default is 4.
			- completed_cycles: int
				The number of completed focus sessions.
			- time_focused: int
				The total time spent on focus sessions.
			- time_break: int
				The total time spent on breaks.
			- pressed_q: bool
				Flag to check if the user pressed 'q' to cancel the session.
		"""
		
		# Parameters (to seconds if needed)
		self.focus_duration = int(focus_duration * 60)	# in seconds
		self.short_break = int(short_break * 60)		# in seconds
		self.long_break = int(long_break * 60)			# in seconds
		self.total_cycles = total_cycles
		self.cycles_to_long_break = cycles_to_long_break

		# File paths
		self.data_file = data_file
		self.sound_file = sound_file

		# Metrics: times and cycles
		self.completed_cycles = 0
		self.time_focused = 0
		self.time_break = 0
		self.elapsed_time = 0

		# Interruptions and pauses
		self.sessions_paused = 0
		self.sessions_interrupted = 0
		self.breaks_paused = 0
		self.breakks_interrupted = 0

		# Project and task names
		self.project = project
		self.task = task

		# Dict with project and tasks names. Time spent on each task
		self.tracked_time = {}

		# Load the tracked time from the file
		self.load_tracked_time()

		# Flag to check if the app is running
		self.is_running = True

		# Flag to check if it's the first run
		self.first_run = True


	def _time_formating(self, time_seconds, show_hours=False):
		mins, secs = divmod(time_seconds, 60)
		if show_hours:
			hours, mins = divmod(mins, 60)
			return f"{hours:02d}:{mins:02d}:{secs:02d}"
		return f"{mins:02d}:{secs:02d}"

	def _save_tracked_time(self):
		data_file = Path(self.data_file)
		data_file.touch(exist_ok=True)
		with open(data_file, "w") as file:
			json.dump(self.tracked_time, file, indent=4)

	def load_tracked_time(self):
		data_file = Path(self.data_file)
		if data_file.exists():
			with open(data_file, "r") as file:
				self.tracked_time = json.load(file)

	# TESTING
	def log_time(self):
		if self.project and self.task:
			# Check if the project is already in the dict
			if self.project not in self.tracked_time:
				self.tracked_time[self.project] = {}
			# Check if the task is already in the dict
			if self.task not in self.tracked_time[self.project]:
				self.tracked_time[self.project][self.task] = 0

		# Update the time spent on the task
		self.tracked_time[self.project][self.task] += self.elapsed_time
		
		self._save_tracked_time()		
		self.elapsed_time = 0

	def settings(self):

		if not self.is_running:
			return

		intro = "Welcome to the SharpTiming App!"
		msg = "-"*40 + "\n"
		msg += "Here are the commands you can use:\n"
		msg += "\t- Show Current Settings		(sh)\n"
		msg += "\t- Change Settings		(ch)\n"
		msg += "\t- Start Focuss Session		(fs)\n"
		msg += "\t- Start Short Break		(sb)\n"
		msg += "\t- Start Long Break		(lb)\n"
		msg += "\t- Show Stats			(st)\n"
		msg += "\t- Show Session Stats		(se)\n"
		msg += "\t- Log Session Stats		(log)\n"
		msg += "\t- Exit				(q)\n"
		msg += "-"*40 + "\n"

		if self.first_run:
			print(announce_color + "="*40)
			print(announce_color + "\t" + intro)
			print(announce_color + "="*40)
			self.ask_project_task()
			self.first_run = False
	
		command = input(msg_color + msg).lower()	
		if command == "sh":
			self.show_settings()
		elif command == "ch":
			self.change_settings()
		elif command == "fs":
			self._start_focus_session()
		elif command == "sb":
			self._start_break()
		elif command == "lb":
			self._start_break(is_long=True)
		elif command == "st":
			self.show_stats()
		elif command == "log":
			self.log_time()
		elif command == "q":
			self.is_running = False
			return
		return

	def show_settings(self):
		time.sleep(0.5)
		print(Fore.LIGHTYELLOW_EX + "\n" + "="*40)
		print(Fore.MAGENTA + "Pomodoro settings:")
		print(Fore.LIGHTYELLOW_EX + "-"*35)
		print(Fore.GREEN + f"Focus duration:\t\t {self._time_formating(self.focus_duration)}")
		print(Fore.CYAN + f"Short break:\t\t {self._time_formating(self.short_break)}")
		print(Fore.LIGHTMAGENTA_EX + f"Long break:\t\t {self._time_formating(self.long_break)}")
		print(Fore.GREEN + f"\nCycles to long break:\t {self.cycles_to_long_break}")
		print(Fore.LIGHTYELLOW_EX + "="*40)

		# Call the settings method again
		self.settings()

	def change_settings(self):

		if not self.is_running:
			return
		
		msg = "-"*40 + "\n"
		msg += "Enter the setting you want to change:\n"
		msg += "\t- Focus duration (f)\n"
		msg += "\t- Short break (s)\n"
		msg += "\t- Long break (l)\n"
		msg += "\t- Cycles to long break (c)\n"
		msg += "\t- Show Current Settings (sh)\n"
		msg += "\t- Back (q)\n"
		msg += "-"*40 + "\n"

		command = input(msg_color + msg)

		if command == "f":
			self.focus_duration = int(float(input("Enter the focus duration in minutes: ")) * 60)
		elif command == "s":
			self.short_break = int(float(input("Enter the short break duration in minutes: ")) * 60)
		elif command == "l":
			self.long_break = int(float(input("Enter the long break duration in minutes: ")) * 60)
		elif command == "c":
			self.cycles_to_long_break = int(input("Enter the number of cycles to long break: "))
		elif command == "q":
			self.settings()
		elif command == "sh":
			self.show_settings()
		
		time.sleep(0.025)
		self.change_settings()

	def show_stats(self):

		time.sleep(0.5)
		print(Fore.LIGHTYELLOW_EX + "\n" + "="*40)
		print(Fore.MAGENTA + "Pomodoro session stats:")
		print(Fore.LIGHTYELLOW_EX + "-"*35)
		print(Fore.GREEN + f"Time focused: {self._time_formating(self.time_focused)}")
		print(Fore.CYAN + f"Time on break: {self._time_formating(self.time_break)}")
		print(Fore.LIGHTMAGENTA_EX + f"Completed cycles: {self.completed_cycles}")
		print(Fore.LIGHTYELLOW_EX + "="*40)

		print(Fore.LIGHTYELLOW_EX + "\n" + "="*40)
		print(Fore.MAGENTA + "Time per project and task:")
		print(Fore.LIGHTYELLOW_EX + "-"*35)
		for project, tasks in self.tracked_time.items():
			print(Fore.BLUE + f"Project: {project}")
			for task, time_spent in tasks.items():
				task_time = self._time_formating(time_spent)
				print(Fore.LIGHTMAGENTA_EX + f"\t-{task} : {task_time}")
		print(Fore.LIGHTYELLOW_EX + "="*40)

		# Call the settings method again
		self.settings()

	def show_current_project_task_stats(self):
		print(Fore.LIGHTYELLOW_EX + "\n" + "="*40)
		print(Fore.MAGENTA + "Current session stats:")
		print(Fore.LIGHTYELLOW_EX + "-"*35)
		print(Fore.GREEN + f"Time focused: {self._time_formating(self.time_focused)}")
		print(Fore.CYAN + f"Time on break: {self._time_formating(self.time_break)}")
		print(Fore.LIGHTMAGENTA_EX + f"Completed cycles: {self.completed_cycles}")
		print(Fore.LIGHTYELLOW_EX + "="*40)

		# Call the settings method again
		self.settings()

	def _start_focus_session(self):
		focus_time = self._time_formating(self.focus_duration)
		print(Fore.MAGENTA + f"Starting focus session #{self.completed_cycles+1}. Time: {focus_time}")
		self._countdown(self.focus_duration)
		self.completed_cycles += 1
		self.log_time()
		self._continue_session(focus=False)

	def _start_break(self, is_long=False):

		if is_long:
			break_time = self._time_formating(self.long_break)
			print(Fore.CYAN + f"Starting long break. Time: {break_time}")
			self._break_countdown(self.long_break, is_long=True)
			self._continue_session(focus=True)
		else:
			break_time = self._time_formating(self.short_break)
			print(Fore.CYAN + f"Starting short break. Time: {break_time}")
			self._break_countdown(self.short_break)
			self._continue_session(focus=True)

	def _countdown(self, time_seconds):
		total_time = time_seconds
		self.elapsed_time = 0

		while time_seconds > -1:

			# Progress bar
			progress = (total_time - time_seconds) / total_time
			bar = f"[{'#' * int(progress * bar_long):<30}]"
			print(Fore.LIGHTGREEN_EX + bar, end=" ")

			# Timer
			timer = self._time_formating(time_seconds)
			print(Fore.GREEN + "\t" + timer, end="\r")
			time_seconds -= 1
			time.sleep(1)

			# Check user input (pause or quit)
			pressed_q = kb.is_pressed("q")
			pressed_p = kb.is_pressed("p")

			if pressed_p:
				print(Fore.RED + "\nSession paused. \nPress 'p' again to resume.")
				self.sessions_paused += 1
				while True:
					time.sleep(1)
					pressed_p = kb.is_pressed("p")
					if pressed_p:
						print(Fore.GREEN + "\nSession resumed.")
						break
				pressed_p = False
				
			if pressed_q:
				self.elapsed_time = self.focus_duration - time_seconds
				self.time_focused += self.elapsed_time
				self.log_time()
				self.sessions_interrupted += 1

				# This func is called inside _start_focus_session, after the countdown
				# self.completed_cycles += 1 to avoid counting the interrupted sessions
				# we simply subtract 1 from the completed_cycles that then gets added back
				# -1 + 1 = 0 (no cycles added)
				self.completed_cycles -= 1
				print(Fore.RED + "\nSession cancelled.")
				return

	
		# Getting here implies the countdown has finished
		self.time_focused += self.focus_duration
		self.elapsed_time = self.focus_duration
		self.log_time() 

		# Play the alarm sound
		self._play_sound()

	def _break_countdown(self, time_seconds, is_long=False):
		total_time = time_seconds
		while time_seconds > -1:
		
			# Progress bar
			progress = (total_time - time_seconds) / total_time
			bar = f"[{'#' * int(progress * bar_long):<30}]"
			print(Fore.LIGHTCYAN_EX + bar, end=" ")

			# Timer
			timer = self._time_formating(time_seconds)
			print(Fore.CYAN + "\t" + timer, end="\r")

			time_seconds -= 1
			time.sleep(1)

			# Check user input (pause or quit)
			pressed_q = kb.is_pressed("q")
			pressed_p = kb.is_pressed("p")

			if pressed_p:
				print(Fore.RED + "\nBreak paused. \nPress again 'p' to resume.")
				while True:
					time.sleep(1)
					pressed_p = kb.is_pressed("p")
					if pressed_p:
						print(Fore.CYAN + "\nBreak resumed.")
						break
				pressed_p = False
			if pressed_q:
				if is_long:
					print(Fore.RED + "\nLong break cancelled.")
					self.time_break += self.long_break - time_seconds
				else:
					print(Fore.RED + "\nShort break cancelled.")
					self.time_break += self.short_break - time_seconds

		if not pressed_q:
			if is_long:
				self.time_break += self.long_break
			else:
				self.time_break += self.short_break
	
			print(Fore.CYAN + "\nTime's up! Get back to work!")

		# Reset the flag
		pressed_q = False

		# Play the alarm sound
		self._play_sound()

	def data_handling(self):
		pass

	# THIS IS GIVING AN ERROR RIGHT NOW
	def _play_sound(self):
		# playsound(self.sound_file)
		pass

	def ask_project_task(self):
		self.project = input("Enter the project name: ")
		self.task = input("Enter the task name: ")

	def _continue_session(self, focus):
		is_long = self.completed_cycles % self.cycles_to_long_break == 0
		if focus:
			control = input("Do you want to continue with the focus session? (y/n): ")
			if control == "y":
				self._start_focus_session()
		else:
			if is_long:
				control = input("Do you want to continue with the long break? (y/n): ")
				if control == "y":
					self._start_break(is_long=True)
			else:
				control = input("Do you want to continue with the short break? (y/n): ")
				if control == "y":
					self._start_break(is_long=False)

		# If 'n'/anything but 'y' ==> go back to settings
		self.settings()

	def run(self):
		self.settings()
		print(Fore.RED + 'Saving the tracked time...')
		# NOT SURE IF THIS IS NEEDED/NOT A PROBLEM
		self.log_time()
		print(Fore.RED + "Exiting the app. Goodbye!")

if __name__ == "__main__":
	tt = TimeTracker(focus_duration=0.2, short_break=0.05, long_break=0.1, total_cycles=5, cycles_to_long_break=2)
	tt.run()