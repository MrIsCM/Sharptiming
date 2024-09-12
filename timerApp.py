import time
import keyboard as kb
import json
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class TimeTracker:

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
		
		self.focus_duration = int(focus_duration * 60)		# in seconds
		self.short_break = int(short_break * 60)		# in seconds
		self.long_break = int(long_break * 60)		# in seconds
		self.total_cycles = total_cycles
		self.cycles_to_long_break = cycles_to_long_break
		self.pressed_q = pressed_q
		self.data_file = data_file

		# Some paramters to keep track
		self.completed_cycles = 0
		self.time_focused = 0
		self.time_break = 0

		self.project = project
		self.task = task

		# Dict with project names, tasks names and time spent on each task
		self.tracked_time = {}

		# Load the tracked time from the file
		self.load_tracked_time()

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

	def show_stats(self):

		focus_time = self.time_formating(self.time_focused)
		break_time = self.time_formating(self.time_break)

		print(Fore.LIGHTYELLOW_EX + "\n" + "="*40)
		print(Fore.LIGHTYELLOW_EX + "Pomodoro session stats:")
		print(Fore.LIGHTYELLOW_EX + "-"*35)
		print(Fore.GREEN + f"Time focused: {focus_time}")
		print(Fore.CYAN + f"Time on break: {break_time}")
		print(Fore.LIGHTMAGENTA_EX + f"Completed cycles: {self.completed_cycles}")
		print(Fore.LIGHTYELLOW_EX + "="*40)

		print(Fore.LIGHTYELLOW_EX + "\n" + "="*40)
		print(Fore.LIGHTYELLOW_EX + "Time per project and task:")
		print(Fore.LIGHTYELLOW_EX + "-"*35)
		for project, tasks in self.tracked_time.items():
			print(Fore.BLUE + f"Project: {project}")
			for task, time_spent in tasks.items():
				task_time = self.time_formating(time_spent)
				print(Fore.LIGHTMAGENTA_EX + f"\t-{task} : {task_time}")
		print(Fore.LIGHTYELLOW_EX + "="*40)

	def start_focus_session(self):
		focus_time = self.time_formating(self.focus_duration)
		print(Fore.LIGHTYELLOW_EX + f"Starting focus session #{self.completed_cycles+1}. Time: {focus_time}")
		self._countdown(self.focus_duration)
		self.completed_cycles += 1

	def start_break(self, is_long=False):
		if self.completed_cycles == self.total_cycles:
			return

		if is_long:
			break_time = self.time_formating(self.long_break)
			print(Fore.CYAN + f"Starting long break. Time: {break_time}")
			self._break_countdown(self.long_break, is_long=True)
		else:
			break_time = self.time_formating(self.short_break)
			print(Fore.CYAN + f"Starting short break. Time: {break_time}")
			self._break_countdown(self.short_break)

	def _countdown(self, time_seconds):
		total_time = time_seconds
		while time_seconds:
			timer = self.time_formating(time_seconds)
			print(Fore.GREEN + timer, end="\r")

			# Progress bar
			progress = (total_time - time_seconds + 1) / total_time
			bar = f"[{'#' * int(progress * 20):<20}]"
			print(Fore.LIGHTGREEN_EX + bar, end=" ")

			time_seconds -= 1
			time.sleep(1)
			self.pressed_q = kb.is_pressed("q")
			if self.pressed_q:
				self.time_focused += self.focus_duration - time_seconds
				self.completed_cycles -= 1
				print(Fore.RED + "Session cancelled.")
				break
		if not self.pressed_q:
			self.time_focused += self.focus_duration
			print(Fore.GREEN + "Time's up!")

	def _break_countdown(self, time_seconds, is_long=False):
		total_time = time_seconds
		while time_seconds:
			timer = self.time_formating(time_seconds)
			print(Fore.CYAN + timer, end="\r")

			# Progress bar
			progress = (total_time - time_seconds + 1) / total_time
			bar = f"[{'#' * int(progress * 20):<20}]"
			print(Fore.LIGHTCYAN_EX + bar, end=" ")

			time_seconds -= 1
			time.sleep(1)
			self.pressed_q = kb.is_pressed("q")
			if self.pressed_q:
				if is_long:
					print(Fore.RED + "Long break cancelled.")
					self.time_break += self.long_break - time_seconds
				else:
					print(Fore.RED + "Short break cancelled.")
					self.time_break += self.short_break - time_seconds

				break

		if not self.pressed_q:
			if is_long:
				self.time_break += self.long_break
			else:
				self.time_break += self.short_break
	
			print(Fore.CYAN + "Time's up! Get back to work.")


	def run_pomodoro(self):

		if not self.project or not self.task:
			self.project = input("Enter the project name: ")
			self.task = input("Enter the task name: ")
			
		while self.completed_cycles < self.total_cycles:
			self.start_focus_session()
			if self.pressed_q:
				break
			if self.completed_cycles % self.cycles_to_long_break == 0:
				self.start_break(is_long=True)
			else:
				self.start_break()
		
		if self.pressed_q:
			print("Pomodoro session interrupted.")
			self.log_time()
			self.show_stats()
		else:
			print("Pomodoro session completed.")
			self.log_time()
			self.show_stats()

if __name__ == "__main__":
	tt = TimeTracker(focus_duration=0.2, short_break=0.05, long_break=0.1, total_cycles=5, cycles_to_long_break=2)
	tt.run_pomodoro()