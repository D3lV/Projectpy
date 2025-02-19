import pygame
import random

pygame.init()

# Definición de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Shooter")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)

# Inicialización de variables de puntuación y vidas
score = 0
lives = 5
paused = False

# Cargar imágenes
background_image = pygame.image.load('images/background.jpg').convert()
background_image = pygame.transform.scale(background_image, (width, height))
player_image = pygame.image.load('images/Nave1.png').convert_alpha()
enemy_image = pygame.image.load('images/NaveE.png').convert_alpha()
bullet_image = pygame.image.load('images/Proyectil.png').convert_alpha()
enemy_bullet_image = pygame.image.load('images/DisparoE.png').convert_alpha()
explosion_image = pygame.image.load('images/explosion.png').convert_alpha()
game_over_image = pygame.image.load('images/gameover.png').convert()
game_over_image = pygame.transform.scale(game_over_image, (width, height))
cover_image = pygame.image.load('images/NaveeP.jpg').convert()
cover_image = pygame.transform.scale(cover_image, (width, height))

# Cargar música y efectos de sonido
pygame.mixer.music.load('sounds/backgroundmusic.mp3')
pygame.mixer.music.set_volume(0.5)
shoot_sound = pygame.mixer.Sound('sounds/disparo.mp3')
enemy_shoot_sound = pygame.mixer.Sound('sounds/Edisparos.mp3')
explosion_sound = pygame.mixer.Sound('sounds/explosion.mp3')

# Función para configurar la fuente del título
def set_title_font(font_path, size):
    return pygame.font.Font(font_path, size)

# Función para configurar la fuente del juego
def set_game_font(font_path, size):
    return pygame.font.Font(font_path, size)

# Función para configurar la fuente del Game Over
def set_game_over_font(font_path, size):
    return pygame.font.Font(font_path, size)

# Definición de la fuente y tamaño para la puntuación y vidas
font_path = 'todooo/Xirod.otf'  # Reemplaza con la ruta a tu fuente de juego
title_font_path = 'titulo/cyberr.otf'  # Reemplaza con la ruta a tu fuente del título
game_over_font_path = 'todooo/Xirod.otf'  # Reemplaza con la ruta a tu fuente de Game Over
font = set_game_font(font_path, 16)
title_font = set_title_font(title_font_path, 66)
game_over_font = set_game_over_font(game_over_font_path, 22)

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height - 50)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += 5
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < height:
            self.rect.y += 5

# Clase de los disparos
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        shoot_sound.play()

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

# Clase de los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(-150, -50)

    def update(self):
        self.rect.y += 5
        if self.rect.top > height:
            self.rect.x = random.randint(0, width - self.rect.width)
            self.rect.y = random.randint(-150, -50)

# Clase de los disparos enemigos
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        enemy_shoot_sound.play()

    def update(self):
        self.rect.y += 10
        if self.rect.top > height:
            self.kill()

# Clase de la explosión
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = explosion_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lifetime = 30  # Duración de la explosión en frames
        explosion_sound.play()

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

# Función para mostrar la pantalla de Game Over
def game_over():
    global score, lives
    message = game_over_font.render(f"Game Over! Score: {score}", True, WHITE)
    restart_button = game_over_font.render("Presiona (R) para Reiniciar o (Q) para Salir", True, WHITE)
   
    screen.fill(BLACK)
    screen.blit(game_over_image, (0, 0))
    screen.blit(message, (width // 2 - message.get_rect().width // 2, height // 3))
    screen.blit(restart_button, (width // 2 - restart_button.get_rect().width // 2, height // 2))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar
                    score = 0
                    lives = 5
                    return True
                elif event.key == pygame.K_q:  # Salir
                    pygame.quit()
                    exit()

# Función para pausar el juego y mostrar el menú de pausa
def toggle_pause():
    global paused
    paused = not paused
    if paused:
        pygame.time.set_timer(pygame.USEREVENT, 0)  # Detener temporizador
        show_pause_menu()
    else:
        pygame.time.set_timer(pygame.USEREVENT, 1000)  # Reanudar temporizador

# Función para mostrar la pantalla de inicio
def show_start_screen():
    pygame.mixer.music.play(-1)
    screen.fill(BLACK)
    title = title_font.render("SPACE SHOOTER", True, RED)
    start_button = font.render("Iniciar (1)", True, RED)
    new_game_button = font.render("Nueva Partida (2)", True, RED)
    score_button = font.render("Puntuacion (3)", True, RED)
    quit_button = font.render("Salir (Q)", True, RED)

    screen.blit(cover_image, (0, 0))
    screen.blit(title, (width // 4, height // 6))
    screen.blit(start_button, (width // 2.5, height // 2.5))
    screen.blit(new_game_button, (width // 2.5, height // 2.5 + 50))
    screen.blit(score_button, (width // 2.5, height // 2.5 + 100))
    screen.blit(quit_button, (width // 2.5, height // 2.5 + 150))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Iniciar
                    pygame.mixer.music.stop()
                    waiting_for_input = False
                elif event.key == pygame.K_2:  # Nueva Partida
                    pygame.mixer.music.stop()
                    waiting_for_input = False
                elif event.key == pygame.K_3:  # Puntuacion
                    show_score_screen()
                elif event.key == pygame.K_q:  # Salir
                    pygame.quit()
                    exit()

# Función para mostrar la pantalla de puntuación
def show_score_screen():
    screen.fill(BLACK)
    title = title_font.render("Puntuaciones", True, WHITE)
    back_button = font.render("Volver (B)", True, WHITE)

    screen.blit(background_image, (0, 0))
    screen.blit(title, (width // 4, height // 6))
    screen.blit(back_button, (width // 2.5, height // 2.5 + 200))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:  # Volver
                    waiting_for_input = False

# Función para mostrar el menú de pausa
def show_pause_menu():
    screen.fill(BLACK)
    pause_text = title_font.render("Pausa", True, WHITE)
    resume_button = font.render("Reanudar (ESC)", True, WHITE)
    restart_button = font.render("Reiniciar (R)", True, WHITE)
    quit_button = font.render("Salir (Q)", True, WHITE)

    screen.blit(background_image, (0, 0))
    screen.blit(pause_text, (width // 3, height // 6))
    screen.blit(resume_button, (width // 2.5, height // 2.5))
    screen.blit(restart_button, (width // 2.5, height // 2.5 + 50))
    screen.blit(quit_button, (width // 2.5, height // 2.5 + 100))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Reanudar
                    toggle_pause()
                    waiting_for_input = False
                elif event.key == pygame.K_r:  # Reiniciar
                    score = 0
                    lives = 5
                    toggle_pause()
                    return
                elif event.key == pygame.K_q:  # Salir
                    pygame.quit()
                    exit()

# Función principal
def main():
    global score, lives, paused
    clock = pygame.time.Clock()

    # Mostrar la pantalla de inicio
    show_start_screen()

    # Crear jugador
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Crear grupos de enemigos, disparos y disparos enemigos
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    # Spawnear enemigos
    enemy_spawn_time = 1000  # Tiempo en milisegundos entre spawns de enemigos
    pygame.time.set_timer(pygame.USEREVENT, enemy_spawn_time)

    # Loop principal
    running = True
    while running:
        clock.tick(60)  # FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                if event.key == pygame.K_p:
                    toggle_pause()
                if event.key == pygame.K_ESCAPE:
                    toggle_pause()

            if event.type == pygame.USEREVENT and not paused:
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)

        if not paused:
            # Actualizar todos los sprites
            all_sprites.update()

            # Detectar colisiones entre balas y enemigos
            hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
            for hit in hits:
                explosion = Explosion(hit.rect.centerx, hit.rect.centery)
                all_sprites.add(explosion)
                explosions.add(explosion)
                score += 10  # Incrementar puntuación cuando un enemigo es destruido

            # Detectar disparos enemigos
            for enemy in enemies:
                if random.random() < 0.01:  # Probabilidad de que un enemigo dispare
                    enemy_bullet = EnemyBullet(enemy.rect.centerx, enemy.rect.bottom)
                    all_sprites.add(enemy_bullet)
                    enemy_bullets.add(enemy_bullet)

            # Detectar colisiones entre disparos enemigos y jugador
            enemy_hits = pygame.sprite.spritecollide(player, enemy_bullets, True, pygame.sprite.collide_mask)
            for hit in enemy_hits:
                lives -= 1
                hit.kill()  # Eliminar el disparo enemigo que impactó
                if lives <= 0:
                    if not game_over():  # Si el juego se reinicia
                        running = False  # Salir del bucle principal

            # Detectar colisiones entre jugador y enemigos
            player_hits = pygame.sprite.spritecollide(player, enemies, True)
            for hit in player_hits:
                lives -= 1
                if lives <= 0:
                    if not game_over():  # Si el juego se reinicia
                        running = False  # Salir del bucle principal

        # Dibujar todo
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)

        # Mostrar puntuación y vidas
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (width - 100, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()