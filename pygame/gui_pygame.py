import pygame
from timetracker import SharpTimer

class TimeTrackerGUI:
	def __init__(self, width=600, height=400, fps=30):
		pygame.init()
		self.width = width
		self.height = height
		self.fps = fps
		self.timer = SharpTimer()

		# Set up the display
		self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)	
		pygame.display.set_caption("Sharp Timings")

		# Colors and Font
		self.pastel_blue = (174, 198, 207)
		self.pastel_red = (255, 105, 97)
		self.pastel_green = (119, 221, 119)
		self.pastel_yellow = (253, 253, 150)
		self.pastel_grey = (207, 207, 196)

		self.bg_color = self.pastel_blue  # Background color
		self.text_color = self.pastel_grey  # Text color
		self.font_name = 'Arial'
		self.font = pygame.font.SysFont(self.font_name, 30)

		# To control the loop
		self.clock = pygame.time.Clock()

		# Timer text
		self.timer_text = self.timer._time_formating(self.timer.focus_time)

		self.paused = False
		
		self.counter = self.timer.focus_time
		pygame.time.set_timer(pygame.USEREVENT, 1000)

	def _render_text_center(self, text, rect, color=(255, 255, 255)):
		"""Helper method to render text on the screen."""
		text_surface = self.font.render(text, True, color)
		text_rect = text_surface.get_rect(center=rect)
		self.screen.blit(text_surface, text_rect)

	def handle_events(self):
		"""Handle button events like starting or stopping the timer."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return False
			# Add other event handling logic (like button presses) here
			elif event.type == pygame.VIDEORESIZE:
				self.width, self.height = event.size
				self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

			elif event.type == pygame.USEREVENT:
				if not self.paused:
					self.counter -= 1
				if self.counter >= 0:
					self.timer_text = self.timer._time_formating(self.counter)
				else:
					self.timer_text = "Time's up!"
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if self.timer.is_running:
						self.paused = not self.paused
					else:
						self.timer.start_focus()
				elif event.key == pygame.K_q:
					pygame.quit()
					return False
		return True
	
	def button(self, x, y, w, h, inactive_color, active_color, text=None, action=None, **kwargs):
		"""Create a button."""
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if x+w > mouse[0] > x and y+h > mouse[1] > y:
			pygame.draw.rect(self.screen, active_color, (x, y, w, h))
			self._render_text_center(text, (x + w//2, y + h//2), color=(50, 20, 20))
			if click[0] == 1 and action != None:
				action(**kwargs)
		else:
			pygame.draw.rect(self.screen, inactive_color, (x, y, w, h))
			self._render_text_center(text, (x + w//2, y + h//2), color=(255, 255, 255))
		
	def countdown(self):
		"""Countdown timer."""
		if not self.paused:
			self.counter -= 1
		if self.counter >= 0:
			self.timer_text = self.timer._time_formating(self.counter)
		else:
			self.timer_text = "Time's up!"

		screen_size = self.screen.get_size()
		self._render_text_center(self.timer_text, (screen_size[0] // 2, screen_size[1] // 2))

	def run(self):
		"""Main loop for running the GUI."""
		running = True
		while running:

			running = self.handle_events()  # Handle events

			self.screen.fill(self.bg_color)  # Fill the screen
			self.countdown()  # Display the countdown timer
			
			self.button(x=100, y=50, w=100, h=50, inactive_color=(130, 255, 0), active_color=(0, 200, 200),
			   text='test', action=self.timer.start_focus)

			pygame.display.flip()  # Update the display
			self.clock.tick(self.fps)  # Control the frame rate
			

if __name__ == "__main__":
	gui = TimeTrackerGUI()
	gui.run()
