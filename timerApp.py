import time
import keyboard as kb
import json
from pathlib import Path
from colorama import Fore, Style, init

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


	def __init__(self, focus_duration=25, short_break=5, long_break=15, cycles_to_long_break=4, total_cycles=4, pressed_q=False, project=None, task=None, data_file="tracked_time.json"):

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
		
		self.focus_duration = int(focus_duration * 60)	# in seconds
		self.short_break = int(short_break * 60)		# in seconds
		self.long_break = int(long_break * 60)			# in seconds
		self.total_cycles = total_cycles
		self.cycles_to_long_break = cycles_to_long_break
		self.data_file = data_file

		# Some paramters to keep track
		self.completed_cycles = 0
		self.time_focused = 0
		self.time_break = 0
		self.elapsed_time = 0

		# Project and task names
		self.project = project
		self.task = task

		# Dict with project names, tasks names and time spent on each task
		self.tracked_time = {}

		# Load the tracked time from the file
		self.load_tracked_time()

		# Flag to check if the app is running
		self.is_running = True

		# Flag to check if it's the first run
		self.first_run = True


	def __repr__(self):
		return f"{self.__class__.__name__}(focus_duration={self.focus_duration}, short_break={self.short_break}, long_break={self.long_break}, total_cycles={self.total_cycles}, cycles_to_long_break={self.cycles_to_long_break})"

	def time_formating(self, time_seconds):
		mins, secs = divmod(time_seconds, 60)
		hours, mins = divmod(mins, 60)
		return f"{hours:02d}:{mins:02d}:{secs:02d}"
	
	def save_tracked_time(self):
		data_file = Path(self.data_file)
		data_file.touch(exist_ok=True)
		with open(data_file, "w") as file:
			json.dump(self.tracked_time, file, indent=4)

	def load_tracked_time(self):
		data_file = Path(self.data_file)
		if data_file.exists():
			with open(data_file, "r") as file:
				self.tracked_time = json.load(file)

	def log_time(self):
		if self.project and self.task:

			# Check if the project is already in the dict
			if self.project not in self.tracked_time:
				self.tracked_time[self.project] = {}
			# Check if the task is already in the dict
			if self.task not in self.tracked_time[self.project]:
				self.tracked_time[self.project][self.task] = 0

		# Update the time spent on the task
		self.tracked_time[self.project][self.task] += self.time_focused

		# Save the tracked time to the file
		self.save_tracked_time()

	def settings(self):

		intro = "Welcome to Pomodoro Timer App!\n"
		msg = "Here are the commands you can use:\n"
		msg += "\t- Show Current Settings	(sh)\n"
		msg += "\t- Change Settings	(ch)\n"
		msg += "\t- Start Focuss Session	(fs)\n"
		msg += "\t- Start Short Break	(sb)\n"
		msg += "\t- Start Long Break	(lb)\n"
		msg += "\t- Data Handling	(dt)\n"
		msg += "\t- Show Current Stats	(st)\n"
		msg += "\t- Exit			(q)\n"

		if self.first_run:
			print(announce_color + intro)
			self.ask_project_task()
			self.first_run = False
		command = input(msg_color + msg)
		if command == "sh":
			self.show_settings()
		elif command == "ch":
			self.change_settings()
		elif command == "fs":
			self.start_focus_session()
		elif command == "sb":
			self.start_break()
		elif command == "lb":
			self.start_break(is_long=True)
		elif command == "st":
			self.show_stats()
		elif command == "dt":
			self.data_handling()
		elif command == "q":
			return
		else:
			return

	def show_settings(self):
		time.sleep(1)
		print(Fore.LIGHTYELLOW_EX + "\n" + "="*40)
		print(Fore.MAGENTA + "Pomodoro settings:")
		print(Fore.LIGHTYELLOW_EX + "-"*35)
		print(Fore.GREEN + f"Focus duration:\t\t {self.time_formating(self.focus_duration)}")
		print(Fore.CYAN + f"Short break:\t\t {self.time_formating(self.short_break)}")
		print(Fore.LIGHTMAGENTA_EX + f"Long break:\t\t {self.time_formating(self.long_break)}")
		print(Fore.GREEN + f"\nCycles to long break:\t {self.cycles_to_long_break}")
		print(Fore.LIGHTYELLOW_EX + "="*40)

		# Call the settings method again
		self.settings()

	def change_settings(self):
		command = input("Enter the setting you want to change:\n\t- Focus duration (f) \n\t- Short break (s) \n\t- Long break (l) \n\t- Cycles to long break (c) \n\t- Show Current Settings (sh) \n\t- Back (q) \n")

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
		
		self.settings()

	def show_stats(self):

		print(Fore.LIGHTYELLOW_EX + "\n" + "="*40)
		print(Fore.MAGENTA + "Pomodoro session stats:")
		print(Fore.LIGHTYELLOW_EX + "-"*35)
		print(Fore.GREEN + f"Time focused: {self.time_formating(self.time_focused)}")
		print(Fore.CYAN + f"Time on break: {self.time_formating(self.time_break)}")
		print(Fore.LIGHTMAGENTA_EX + f"Completed cycles: {self.completed_cycles}")
		print(Fore.LIGHTYELLOW_EX + "="*40)

		print(Fore.LIGHTYELLOW_EX + "\n" + "="*40)
		print(Fore.MAGENTA + "Time per project and task:")
		print(Fore.LIGHTYELLOW_EX + "-"*35)
		for project, tasks in self.tracked_time.items():
			print(Fore.BLUE + f"Project: {project}")
			for task, time_spent in tasks.items():
				task_time = self.time_formating(time_spent)
				print(Fore.LIGHTMAGENTA_EX + f"\t-{task} : {task_time}")
		print(Fore.LIGHTYELLOW_EX + "="*40)

		# Call the settings method again
		self.settings()

	def start_focus_session(self):
		focus_time = self.time_formating(self.focus_duration)
		print(Fore.MAGENTA + f"Starting focus session #{self.completed_cycles+1}. Time: {focus_time}")
		self._countdown(self.focus_duration)
		self.completed_cycles += 1
		self.continue_session(focus=False)

	def start_break(self, is_long=False):

		if is_long:
			break_time = self.time_formating(self.long_break)
			print(Fore.CYAN + f"Starting long break. Time: {break_time}")
			self._break_countdown(self.long_break, is_long=True)
			self.continue_session(focus=True)
		else:
			break_time = self.time_formating(self.short_break)
			print(Fore.CYAN + f"Starting short break. Time: {break_time}")
			self._break_countdown(self.short_break)
			self.continue_session(focus=True)

	def _countdown(self, time_seconds):
		total_time = time_seconds
		while time_seconds > 0:

			timer = self.time_formating(time_seconds)
			print(Fore.GREEN + "\t" + timer, end="\r")

			# Progress bar
			progress = (total_time - time_seconds + 1) / total_time
			bar = f"[{'#' * int(progress * 20):<30}]"
			print(Fore.LIGHTGREEN_EX + bar, end=" ")

			time_seconds -= 1
			time.sleep(1)

			pressed_q = kb.is_pressed("q")
			pressed_p = kb.is_pressed("p")

			if pressed_p:
				print(Fore.RED + "Session paused. \nPress again 'p' to resume.")
				while True:
					time.sleep(1)
					pressed_p = kb.is_pressed("p")
					if pressed_p:
						print(Fore.GREEN + "Session resumed.")
						break
				pressed_p = False
				
			if pressed_q:
				self.time_focused += self.focus_duration - time_seconds
				self.elapsed_time = time_seconds
				self.completed_cycles -= 1
				print(Fore.RED + "Session cancelled.")
				break

		if not pressed_q:
			self.time_focused += self.focus_duration
			print(Fore.GREEN + "Time's up!")
		pressed_q = False

	def _break_countdown(self, time_seconds, is_long=False):
		total_time = time_seconds
		while time_seconds:
			timer = self.time_formating(time_seconds)
			print(Fore.CYAN + "\t" + timer, end="\r")

			# Progress bar
			progress = (total_time - time_seconds + 1) / total_time
			bar = f"[{'#' * int(progress * 20):<30}]"
			print(Fore.LIGHTCYAN_EX + bar, end=" ")

			time_seconds -= 1
			time.sleep(1)
			pressed_q = kb.is_pressed("q")
			pressed_p = kb.is_pressed("p")

			if pressed_p:
				print(Fore.RED + "Break paused. \nPress again 'p' to resume.")
				while True:
					time.sleep(1)
					pressed_p = kb.is_pressed("p")
					if pressed_p:
						print(Fore.CYAN + "Break resumed.")
						break
				pressed_p = False
			if pressed_q:
				if is_long:
					print(Fore.RED + "Long break cancelled.")
					self.time_break += self.long_break - time_seconds
				else:
					print(Fore.RED + "Short break cancelled.")
					self.time_break += self.short_break - time_seconds

		if not pressed_q:
			if is_long:
				self.time_break += self.long_break
			else:
				self.time_break += self.short_break
	
			print(Fore.CYAN + "Time's up! Get back to work.")
		pressed_q = False

	def data_handling(self):
		pass

	def play_sound(self):
		pass

	def ask_project_task(self):
		self.project = input("Enter the project name: ")
		self.task = input("Enter the task name: ")

	def continue_session(self, focus):
		is_long = self.completed_cycles % self.cycles_to_long_break == 0
		if focus:
			control = input("Do you want to continue with the focus session? (y/n): ")
			if control == "y":
				self.start_focus_session()
		else:
			if is_long:
				control = input("Do you want to continue with the long break? (y/n): ")
				if control == "y":
					self.start_break(is_long=True)
			else:
				control = input("Do you want to continue with the short break? (y/n): ")
				if control == "y":
					self.start_break(is_long=False)

		# If 'n' --> go back to settings
		self.settings()

	def run(self):
		self.settings()

if __name__ == "__main__":
	tt = TimeTracker(focus_duration=0.2, short_break=0.05, long_break=0.1, total_cycles=5, cycles_to_long_break=2)
	tt.run()