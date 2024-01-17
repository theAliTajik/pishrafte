import pygame
import sys

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480
CELL_SIZE = 20
PACMAN_SIZE = 20
PACMAN_SPEED = 0.000001
BACKGROUND_COLOR = (0, 0, 0)
PELLET_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 255)
PELLET_SIZE = 5

# Level design: 0 = path, 1 = wall
LEVEL = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

class PacMan(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (PACMAN_SIZE, PACMAN_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.speed = PACMAN_SPEED
        self.direction = None
        self.queued_direction = None

    def set_direction(self, new_direction):
        if self.can_move(new_direction):
            self.direction = new_direction
        else:
            self.queued_direction = new_direction

    def can_move(self, direction):
        grid_x, grid_y = self.rect.x // CELL_SIZE, self.rect.y // CELL_SIZE
        dx, dy = 0, 0
        if direction == 'LEFT':
            dx = -1
        elif direction == 'RIGHT':
            dx = 1
        elif direction == 'UP':
            dy = -1
        elif direction == 'DOWN':
            dy = 1

        next_grid_x, next_grid_y = grid_x + dx, grid_y + dy
        return 0 <= next_grid_x < len(LEVEL[0]) and 0 <= next_grid_y < len(LEVEL) and LEVEL[next_grid_y][next_grid_x] == 0

    def update(self):
        if self.direction is None:
            return

        if self.queued_direction and self.can_move(self.queued_direction):
            self.direction = self.queued_direction
            self.queued_direction = None

        if self.can_move(self.direction):
            dx, dy = 0, 0
            if self.direction == 'LEFT':
                dx = -1
            elif self.direction == 'RIGHT':
                dx = 1
            elif self.direction == 'UP':
                dy = -1
            elif self.direction == 'DOWN':
                dy = 1
            
            self.rect.x += dx * CELL_SIZE
            self.rect.y += dy * CELL_SIZE

# Pellets
pellets = []
# Calculate the offset needed to center the pellet in the cell
offset = (CELL_SIZE - PELLET_SIZE) // 2
# Apply the offset to each pellet's position
pellets = [(x * CELL_SIZE + offset, y * CELL_SIZE + offset) for y, row in enumerate(LEVEL) for x, cell in enumerate(row) if cell == 0]


pacman = PacMan("pacman/Pac_Man.png", (CELL_SIZE, CELL_SIZE))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.set_direction('LEFT')
            elif event.key == pygame.K_RIGHT:
                pacman.set_direction('RIGHT')
            elif event.key == pygame.K_UP:
                pacman.set_direction('UP')
            elif event.key == pygame.K_DOWN:
                pacman.set_direction('DOWN')

    pacman.update()

    # Collision detection for pellets
    pellets = [pellet for pellet in pellets if not pacman.rect.collidepoint(pellet[0] + PELLET_SIZE // 2, pellet[1] + PELLET_SIZE // 2)]

    # Drawing
    screen.fill(BACKGROUND_COLOR)

    # Draw walls
    for y, row in enumerate(LEVEL):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, WALL_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw pellets
    for pellet in pellets:
        pygame.draw.rect(screen, PELLET_COLOR, (pellet[0], pellet[1], PELLET_SIZE, PELLET_SIZE))

    # Draw Pac-Man using the sprite
    screen.blit(pacman.image, pacman.rect)

    pygame.display.flip()
    pygame.time.Clock().tick(20)

pygame.quit()
sys.exit()