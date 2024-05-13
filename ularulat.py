import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Variabel layar
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ular Melawan Ulat")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

# Objek Ular
class Snake:
    def __init__(self, color, start_pos):
        self.body = [start_pos]
        self.direction = 'RIGHT'
        self.color = color

    def draw(self, win):
        for segment in self.body:
            pygame.draw.rect(win, self.color, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    def move(self):
        head = self.body[0]
        x, y = head

        if self.direction == 'UP':
            y -= GRID_SIZE
        elif self.direction == 'DOWN':
            y += GRID_SIZE
        elif self.direction == 'LEFT':
            x -= GRID_SIZE
        elif self.direction == 'RIGHT':
            x += GRID_SIZE

        self.body.insert(0, (x, y))
        self.body.pop()  # Hapus bagian belakang badan ular

    def grow(self):
        self.body.append(self.body[-1])

# Objek Apel
class Coin:
    def __init__(self):
        self.x = random.randrange(0, WIDTH, GRID_SIZE)
        self.y = random.randrange(0, HEIGHT, GRID_SIZE)

    def draw(self, win):
        pygame.draw.circle(win, GOLD, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), GRID_SIZE // 3)

# Fungsi utama
def main():
    snake_green = Snake(GREEN, (200, 200))
    snake_red = Snake(RED, (600, 400))
    coin = Coin()
    clock = pygame.time.Clock()
    player_score = 0
    worm_score = 0
    worm_move_counter = 0
    WORM_MOVE_INTERVAL = 1  # Atur interval gerakan ulat merah

    run = True
    while run:
        clock.tick(5)  # Ubah kecepatan gerakan ular di sini

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Pergerakan ular hijau
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake_green.direction != 'DOWN':
            snake_green.direction = 'UP'
        elif keys[pygame.K_DOWN] and snake_green.direction != 'UP':
            snake_green.direction = 'DOWN'
        elif keys[pygame.K_LEFT] and snake_green.direction != 'RIGHT':
            snake_green.direction = 'LEFT'
        elif keys[pygame.K_RIGHT] and snake_green.direction != 'LEFT':
            snake_green.direction = 'RIGHT'

        snake_green.move()

        # Pergerakan ular merah (otomatis)
        worm_move_counter += 1
        if worm_move_counter >= WORM_MOVE_INTERVAL:
            worm_move_counter = 0
            directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            direction = random.choice(directions)
            if direction == 'UP' and snake_red.direction != 'DOWN':
                snake_red.direction = 'UP'
            elif direction == 'DOWN' and snake_red.direction != 'UP':
                snake_red.direction = 'DOWN'
            elif direction == 'LEFT' and snake_red.direction != 'RIGHT':
                snake_red.direction = 'LEFT'
            elif direction == 'RIGHT' and snake_red.direction != 'LEFT':
                snake_red.direction = 'RIGHT'
            snake_red.move()

        # Tabrakan dengan koin
        if snake_green.body[0] == (coin.x, coin.y):
            coin = Coin()
            snake_green.grow()
            player_score += 1

        if snake_red.body[0] == (coin.x, coin.y):
            coin = Coin()
            snake_red.grow()
            worm_score += 1

        # Tabrakan dengan dinding
        if (snake_green.body[0][0] < 0 or snake_green.body[0][0] >= WIDTH or
            snake_green.body[0][1] < 0 or snake_green.body[0][1] >= HEIGHT or
            snake_red.body[0][0] < 0 or snake_red.body[0][0] >= WIDTH or
            snake_red.body[0][1] < 0 or snake_red.body[0][1] >= HEIGHT):
            run = False  # Game selesai, salah satu ular kalah

        # Render
        WIN.fill(BLACK)
        snake_green.draw(WIN)
        snake_red.draw(WIN)
        coin.draw(WIN)

        # Tampilkan skor
        font = pygame.font.Font(None, 36)
        player_text = font.render(f'Snake Score: {player_score}', True, WHITE)
        worm_text = font.render(f'Worm Score: {worm_score}', True, WHITE)
        WIN.blit(player_text, (10, 10))
        WIN.blit(worm_text, (10, 50))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
