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
		pygame.display.set_caption("Time Tracker")

		# Colors and Font
		self.bg_color = (30, 30, 30)  # Background color
		self.text_color = (255, 255, 255)  # Text color
		self.font = pygame.font.SysFont(None, 55)

		# To control the loop
		self.clock = pygame.time.Clock()

		# Timer text
		self.timer_text = self.timer._time_formating(self.timer.focus_time)

		self.paused = False
		
		self.counter = self.timer.focus_time
		pygame.time.set_timer(pygame.USEREVENT, 1000)

	def _render_text(self, text, pos):
		"""Helper method to render text on the screen."""
		rendered_text = self.font.render(text, True, self.text_color)
		self.screen.blit(rendered_text, pos)

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
	
	def button(self, x, y, w, h, ic, ac, text=None, action=None):
		"""Create a button."""
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if x+w > mouse[0] > x and y+h > mouse[1] > y:
			pygame.draw.rect(self.screen, ac, (x, y, w, h))
			if click[0] == 1 and action != None:
				action()
		else:
			pygame.draw.rect(self.screen, ic, (x, y, w, h))

		if text:
			self._render_text(text, (x + 10, y + 10))
		

	def run(self):
		"""Main loop for running the GUI."""
		running = True
		while running:

			running = self.handle_events()  # Handle events
			
				
			# self.timer.update()  # Update the timer

			self.screen.fill(self.bg_color)  # Fill the screen
			self._render_text(self.timer_text, (self.width // 2 - 50, self.height // 2 - 50))
			if self.paused:
				text = "Paused!"
				self._render_text(text, (self.width // 2 - 11*len(text), self.height // 2 - 100))
			
			self.button(x=100, y=50, w=100, h=50, ic=(130, 255, 0), ac=(0, 200, 200),
			   text='test', action=self.timer.start_focus)

			pygame.display.flip()  # Update the display
			self.clock.tick(self.fps)  # Control the frame rate
			

if __name__ == "__main__":
	gui = TimeTrackerGUI()
	gui.run()
