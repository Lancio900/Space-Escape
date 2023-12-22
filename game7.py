import pygame
import sys
import random
import time

# Inizializza Pygame
pygame.init()

# Definisci le costanti
WIDTH, HEIGHT = 800, 600
FPS = 60

# Inizializza la finestra di gioco
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space escape!")

# Inizializza il colore di sfondo
bg_color = (0, 0, 0)
new_bg_color = (255, 255, 255)  # Nuovo colore di sfondo dopo 5 minuti
background_change_time = 300  # Tempo in secondi prima di cambiare lo sfondo
background_change_timer = time.time() + background_change_time

# Inizializza il giocatore con un'immagine PNG
player_image = pygame.image.load("escape-from-the-ships/player2.png")  # Sostituisci con il tuo percorso e nome del file
player_image = pygame.transform.scale(player_image, (50, 50))  # Regola le dimensioni dell'immagine se necessario
player_rect = player_image.get_rect()
player_rect.x = WIDTH // 2 - player_rect.width // 2
player_rect.y = HEIGHT - 2 * player_rect.height
player_speed = 5

# Inizializza la skin per i nemici
enemy_image = pygame.image.load("escape-from-the-ships/enemy.png")  # Sostituisci con il tuo percorso e nome del file
enemy_image = pygame.transform.scale(enemy_image, (30, 30))  # Regola le dimensioni dell'immagine se necessario

# Inizializza la lista dei nemici
enemy_speed = 5
enemies = []

# Inizializza le palline verdi (bonus di velocità)
bonus_image = pygame.image.load("escape-from-the-ships/speed.png")  # Sostituisci con il tuo percorso e nome del file
bonus_image = pygame.transform.scale(bonus_image, (20, 20))  # Regola le dimensioni dell'immagine se necessario
bonuses = []

# Inizializza il clock per controllare il framerate
clock = pygame.time.Clock()

# Inizializza il punteggio
score = 0
font = pygame.font.Font(None, 36)

# Inizializza lo stato del gioco
game_started = False

# Inizializza le variabili del menu
menu_font = pygame.font.Font(None, 48)
play_button = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
info_button = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 60, WIDTH // 2, 50)

# Inizializza le informazioni
info_text = (
    "GIOCO CREATO DA: Christian Lancini.\n"
    "Muovi il tuo personaggio con i tasti A e D.\n"
    "Evita i quadrati blu e cerca di rimanere in gioco \n il più a lungo possibile."
)
info_font = pygame.font.Font(None, 24)
info_visible = False

# Funzione per generare un nuovo nemico
def spawn_enemy():
    enemy_x = random.randint(0, WIDTH - 30)
    enemy_y = 0
    enemies.append(pygame.Rect(enemy_x, enemy_y, 30, 30))

# Funzione per generare un bonus di velocità
def spawn_bonus():
    bonus_x = random.randint(0, WIDTH - 20)
    bonus_y = 0
    bonuses.append(pygame.Rect(bonus_x, bonus_y, 20, 20))

# Funzione per cambiare lo sfondo e aumentare la difficoltà
def change_background_and_difficulty():
    global bg_color, new_bg_color, enemy_speed
    bg_color = new_bg_color
    enemy_speed += 1

# Funzione per visualizzare il menu
def show_menu():
    screen.fill(bg_color)

    title_text = menu_font.render("Avoid the Enemies!", True, (255, 255, 255))
    screen.blit(title_text, (WIDTH // 4, HEIGHT // 4))

    pygame.draw.rect(screen, (0, 255, 0), play_button)
    pygame.draw.rect(screen, (0, 255, 0), info_button)

    play_text = menu_font.render("Play", True, (0, 0, 0))
    info_button_text = menu_font.render("Information", True, (0, 0, 0))

    screen.blit(play_text, (play_button.x + play_button.width // 4, play_button.y + play_button.height // 4))
    screen.blit(info_button_text, (info_button.x + info_button.width // 4, info_button.y + info_button.height // 4))

    # Mostra le informazioni se sono visibili
    if info_visible:
        pygame.draw.rect(screen, (255, 255, 255), (info_button.x, info_button.y + info_button.height + 10, info_button.width, 150))
        lines = info_text.split("\n")
        for i, line in enumerate(lines):
            line_rendered = info_font.render(line, True, (0, 0, 0))
            screen.blit(line_rendered, (info_button.x + 10, info_button.y + info_button.height + 10 + i * 30))

# Ciclo di gioco
running = True
bonus_timer = time.time() + 60  # Inizializza il timer per il bonus di velocità
bonus_active = False

while running:
    # Gestione degli eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if play_button.collidepoint(mouse_x, mouse_y):
                game_started = True
            elif info_button.collidepoint(mouse_x, mouse_y):
                info_visible = not info_visible

    # Se il gioco non è ancora iniziato, mostra il menu
    if not game_started:
        show_menu()
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # Input del giocatore
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_rect.x > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_d] and player_rect.x < WIDTH - player_rect.width:
        player_rect.x += player_speed

    # Genera nuovi nemici casualmente
    if random.randint(0, 100) < 5:
        spawn_enemy()

    # Muovi i nemici verso il basso
    for enemy in enemies:
        enemy.y += enemy_speed

    # Rimuovi i nemici che sono usciti dalla schermata e aumenta il punteggio
    enemies = [enemy for enemy in enemies if enemy.y < HEIGHT]
    score += len(enemies)

    # Controlla le collisioni con i nemici
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            print("Hai perso! Punteggio:", score)
            running = False

    # Genera un bonus di velocità ogni minuto
    if time.time() > bonus_timer:
        if not bonus_active:
            spawn_bonus()
            bonus_active = True
        bonus_timer = time.time() + 60  # Resetta il timer

    # Muovi i bonus verso il basso
    for bonus in bonuses:
        bonus.y += enemy_speed

    # Controlla le collisioni con i bonus di velocità
    for bonus in bonuses:
        if player_rect.colliderect(bonus):
            player_speed += 7
            bonuses.remove(bonus)
            bonus_active = False

    # Cambia lo sfondo e aumenta la difficoltà dopo 5 minuti
    if time.time() > background_change_timer:
        change_background_and_difficulty()
        background_change_timer = time.time() + background_change_time

    # Rimuovi i bonus che sono usciti dalla schermata
    bonuses = [bonus for bonus in bonuses if bonus.y < HEIGHT]

    # Aggiorna la schermata
    screen.fill(bg_color)
    screen.blit(player_image, (player_rect.x, player_rect.y))

    # Disegna i nemici
    for enemy in enemies:
        screen.blit(enemy_image, (enemy.x, enemy.y))

    # Disegna i bonus di velocità
    for bonus in bonuses:
        screen.blit(bonus_image, (bonus.x, bonus.y))

    # Disegna il punteggio
    score_text = font.render("Punteggio: {}".format(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Aggiorna la finestra di gioco
    pygame.display.flip()

    # Imposta il framerate
    clock.tick(FPS)

# Termina Pygame
pygame.quit()
sys.exit()
