import pygame
import random
import sys

# INICIAR PYGAME
pygame.init()

# CONFIGURAR PANTALLA
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DINORITO")

# COLORES Y FUENTE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

# VELOCIDAD INICIAL
obstacle_speed = 5
player_speed = 5
increase_difficulty_interval = 5000  # 5 segundos


# CARGAR IMG
def load_image(path, size=None):
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image


menu_image = load_image("img/menu.jpg", (WIDTH, HEIGHT))
background_image = load_image(
    "img/active-volcanoes-lava-green-ferns-600nw-740013958.webp", (WIDTH, HEIGHT)
)
dino_image = load_image("img/dinopj.png", (70, 70))
meteor_image = load_image("img/meteorito.png", (60, 80))

# VARIABLES
player_size = 45
player = pygame.Rect(WIDTH // 2, HEIGHT - player_size * 2, player_size, player_size)
obstacles = []
score = 0
last_time_difficulty_increased = pygame.time.get_ticks()


def start_screen():
    # MENU
    screen.blit(menu_image, (0, 0))
    title_text = FONT.render("== D I N O R I T O ==", True, WHITE)
    start_text = FONT.render("Presiona ENTER para comenzar", True, WHITE)
    exit_text = FONT.render("Presiona ESC para salir", True, WHITE)
    instructions_text = FONT.render("Usa <- -> o A y D para moverte", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(
        instructions_text,
        (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2),
    )
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT * 3 // 4))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT * 4 // 5))
    pygame.display.flip()


def create_obstacle():
    x_pos = random.randint(0, WIDTH - meteor_image.get_width())
    y_pos = -meteor_image.get_height()
    obstacles.append(
        pygame.Rect(x_pos, y_pos, meteor_image.get_width(), meteor_image.get_height())
    )


def game_over_screen():
    # PANTALLA FINAL
    screen.fill(WHITE)
    game_over_text = FONT.render("¡Juego Terminado!", True, BLACK)
    score_text = FONT.render(f"Puntuación: {score}", True, BLACK)
    screen.blit(
        game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3)
    )
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)


def game_loop():
    global score, obstacle_speed, last_time_difficulty_increased
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.blit(background_image, (0, 0))  # BACKGROUND IMG

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # MOVIMIENTOS
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed

        # QUE NO SE SALGA DE LA PANTALLA
        player.x = max(0, min(WIDTH - player_size, player.x))

        if random.randint(1, 20) == 1:
            create_obstacle()

        for obstacle in obstacles[:]:
            obstacle.y += obstacle_speed
            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle)
                score += 1
            elif player.colliderect(obstacle):
                game_over_screen()
                return
            else:
                screen.blit(meteor_image, (obstacle.x, obstacle.y))

        # SUBIR LA DIFICULTAD
        current_time = pygame.time.get_ticks()
        if current_time - last_time_difficulty_increased > increase_difficulty_interval:
            obstacle_speed += 1
            last_time_difficulty_increased = current_time

        # DINO IMG
        screen.blit(dino_image, (player.x, player.y))

        # PUNTOS
        score_text = FONT.render(f"Puntuación: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)


while True:
    start_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                obstacles.clear()
                score = 0
                game_loop()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
