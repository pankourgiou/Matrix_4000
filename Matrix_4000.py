import pygame
import random
import string
import webview  # For embedded browser

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 1024
HEIGHT = 768
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Fullscreen mode
pygame.display.set_caption("Matrix")

# Colors
GREEN = (0, 255, 0)
DARK_GREEN = (0, 50, 0)
BLACK = (0, 0, 0)

# Font settings
FONT_SIZE = 50
try:
    font = pygame.font.Font("BunnyHoliday.ttf", FONT_SIZE)  # Ensure Hylian.ttf is in the same folder
except:
    font = pygame.font.Font(None, FONT_SIZE)  # Fallback font if Kaotican is missing

class CodeDrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(5, 15)
        self.chars = []
        self.update_interval = 0.05
        self.last_update = 0
        self.length = random.randint(5, 20)
        
        # Initialize with random characters
        for _ in range(self.length):
            self.chars.append(random.choice(string.ascii_letters + string.digits))
    
    def update(self, current_time):
        self.y += self.speed  # Move downward
        
        # Update characters periodically
        if current_time - self.last_update > self.update_interval:
            self.chars = [random.choice(string.ascii_letters + string.digits)] + self.chars[:-1]
            self.last_update = current_time
    
    def draw(self, surface):
        for i, char in enumerate(self.chars):
            # Calculate fade effect
            alpha = 255 - (i * (255 // len(self.chars)))
            color = (0, min(255, alpha + 50), 0)
            
            # Render character
            char_surface = font.render(char, True, color)
            surface.blit(char_surface, (self.x, self.y + i * FONT_SIZE))

class MatrixEffect:
    def __init__(self):
        self.drops = []
        self.last_spawn = 0
        self.spawn_interval = 0.35  # New drop every 0.1s
        
    def update(self):
        current_time = pygame.time.get_ticks() / 1000.0
        
        # Spawn new drops
        if current_time - self.last_spawn > self.spawn_interval:
            x = random.randint(0, WIDTH - FONT_SIZE)
            self.drops.append(CodeDrop(x, -FONT_SIZE * 2))
            self.last_spawn = current_time
        
        # Update existing drops
        for drop in self.drops[:]:
            drop.update(current_time)
            
            # Remove drops that are off screen
            if drop.y > HEIGHT:
                self.drops.remove(drop)
    
    def draw(self, surface):
        for drop in self.drops:
            drop.draw(surface)

def draw_centered_text(surface, text, font, color):
    # Calculate the position to center the text
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    surface.blit(text_surface, text_rect)

def open_browser():
    """ Opens an embedded browser window using PyWebView. """
    webview.create_window("Embedded Browser", "https://www.google.com")  # Change URL as needed
    webview.start()

def main():
    clock = pygame.time.Clock()
    matrix = MatrixEffect()
    running = True
    message = "Matrix"  # Display message
    
    # Create a surface for the fade effect
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BLACK)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_b:  # Press 'B' to open browser
                    open_browser()
        
        # Update matrix effect
        matrix.update()
        
        # Draw fade effect
        screen.blit(fade_surface, (0, 0))
        
        # Draw matrix effect
        matrix.draw(screen)
        
        # Draw the centered message
        draw_centered_text(screen, message, font, GREEN)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
