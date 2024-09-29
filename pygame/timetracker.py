
class SharpTimer:

	def __init__(self, focus_time=25, short_break=5, long_break=15, cycles_to_long_break=4):
		
		self.focus_time = focus_time* 60 		# to seconds
		self.short_break = short_break* 60 		# to seconds
		self.long_break = long_break* 60 		# to seconds
		self.cycles_to_long_break = cycles_to_long_break
		
		self.current_state = "focus"
		self.is_running = False
		self.is_paused = False
		self.is_reset = False

		self.completed_cycles = 0
		self.time_focused = 0
		self.time_breaked = 0

		self.sessions_paused = 0
		self.sessions_interrupted = 0


	def _time_formating(self, time, show_hours=False):
		"""Helper method to format time in seconds to a string."""
		minutes, seconds = divmod(time, 60)
		if show_hours:
			hours, minutes = divmod(minutes, 60)
			return f"{hours:02}:{minutes:02}:{seconds:02}"
		else:
			return f"{minutes:02}:{seconds:02}"


	def start_focus(self):
		self.current_state = "focus"
		self.is_running = True

		return self.focus_time, self.current_state, self.is_running

	def start_break(self, is_long=False):
		if is_long:
			self.current_state = "long break"
			self.is_running = True
			return self.long_break, self.current_state, self.is_running
		else:
			self.current_state = "short break"
			self.is_running = True
			return self.short_break, self.current_state, self.is_running

	def change_settings(self, focus_time, short_break, long_break, cycles_to_long_break):
		self.focus_time = focus_time* 60 		# to seconds
		self.short_break = short_break* 60 		# to seconds
		self.long_break = long_break* 60 		# to seconds
		self.cycles_to_long_break = cycles_to_long_break

		return self.focus_time, self.short_break, self.long_break, self.cycles_to_long_break
	
	def get_settings(self):
		return self.focus_time, self.short_break, self.long_break, self.cycles_to_long_break
	
	def get_state(self):
		return self.current_state, self.is_running, self.is_paused, self.is_reset
	
	def get_stats(self):
		return self.completed_cycles, self.time_focused, self.time_breaked, self.sessions_paused, self.sessions_interrupted
	
	def pause(self):
		self.is_paused = True
		self.sessions_paused += 1
		return self.is_paused