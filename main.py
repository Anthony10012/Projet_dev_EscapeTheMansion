import pygame
import sys
from player import Player
from menu import create_menu

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape The Mansion")

# Chargement des ressources
background = pygame.image.load("./design/Background/chambre.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
dossier_perso = "./design/Character"
FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 64)
player = Player(screen, dossier_perso)

# Création du menu principal
menu = create_menu(screen, FONT, BIG_FONT, player, background)

# Boucle principale du menu
clock = pygame.time.Clock()
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    menu.update(events)
    menu.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
