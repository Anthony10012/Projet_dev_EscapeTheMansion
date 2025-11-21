import pygame
import pygame_menu
import sys

from pygame_menu.examples.other.image_background import background_image

# -------------------------------------------------------
# Initialisation générale de Pygame
# -------------------------------------------------------
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape The Mansion - Menu")

# Petite font pour le jeu / overlay
FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 64)


# -------------------------------------------------------
# Menu pause écrit "manuellement" (overlay) — renvoie une action
# -------------------------------------------------------
def pause_menu(surface):
    """
    Affiche un menu pause simple (overlay) et renvoie :
      - 'resume' : reprendre la partie
      - 'save game' : sauvegarde la partie
      - 'quit' : quitter complètement le jeu
    Ce menu gère aussi l'événement QUIT (croix) en quittant l'application.
    """
    clock = pygame.time.Clock()
    # Prépare les rectangles des boutons (centrés)
    btn_w, btn_h = 300, 50
    center_x = WIDTH // 2
    start_y = HEIGHT // 2 - 60
    resume_rect = pygame.Rect(center_x - btn_w // 2, start_y, btn_w, btn_h)
    save_game = pygame.Rect(center_x - btn_w // 2, start_y + 70, btn_w, btn_h)
    quit_rect = pygame.Rect(center_x - btn_w // 2, start_y + 140, btn_w, btn_h)

    while True:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Si on clique sur la croix pendant le menu pause on ferme tout
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Appuyer sur Esc dans le menu pause = reprendre
                    return 'resume'

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if resume_rect.collidepoint(mx, my):
                    return 'resume'
                if save_game.collidepoint(mx, my):
                    return 'save_game'
                if quit_rect.collidepoint(mx, my):
                    # Quitter complètement le jeu
                    pygame.quit()
                    sys.exit()

        # Dessin de l'overlay semi-transparent
        surface.fill((255, 0, 0))  # on suppose que l'arrière-plan du jeu est noir - redessine si besoin
        # créer un overlay translucide
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))  # (r,g,b,alpha) alpha=150 -> translucide
        surface.blit(overlay, (0, 0))

        # Titre "Paused"
        title_surf = BIG_FONT.render("PAUSE", True, (255,255,255))
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 130))
        surface.blit(title_surf, title_rect)

        # Dessiner les boutons (rectangles + texte)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # fonction utilitaire pour dessiner un bouton
        def draw_button(rect, text):
            # changer l'apparence au survol
            if rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(surface, (60, 60, 60), rect, border_radius=8)
            else:
                pygame.draw.rect(surface, (40, 40, 40), rect, border_radius=8)
            # bordure
            pygame.draw.rect(surface, (200, 200, 200), rect, width=2, border_radius=8)
            # texte centré
            txt = FONT.render(text, True, (255, 255, 255))
            txt_rect = txt.get_rect(center=rect.center)
            surface.blit(txt, txt_rect)

        draw_button(resume_rect, "Resume")
        draw_button(save_game, "Save Game")
        draw_button(quit_rect, "Quit Game")

        pygame.display.flip()
        clock.tick(60)


# -------------------------------------------------------
# Fonction qui lance la partie (boucle du jeu)
# -------------------------------------------------------
def start_game():
    """
    Cette fonction contient la boucle principale de la partie.
    - si l'utilisateur clique sur la croix : quitte complètement
    - si l'utilisateur appuie sur Esc : ouvre le menu pause
    - si l'utilisateur choisit 'Quit to Menu' dans le menu pause : on retourne au menu principal
    """
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Cliquer sur la croix doit fermer toute l'application directement
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Appuyer sur Esc : ouvrir le menu pause
                    action = pause_menu(screen)
                    if action == 'resume':
                        # simplement reprendre la boucle (rien à faire)
                        pass


        # ----- Logique/affichage de la partie -----
        # Fond du jeu
        screen.fill((255, 0, 0))

        # Exemple : dessiner du texte pour montrer qu'on est en jeu
        info = FONT.render("Game running - press ESC for pause", True, (200, 200, 200))
        screen.blit(info, (20, 20))

        pygame.display.flip()
        clock.tick(60)  # limiter à 60 FPS


# -------------------------------------------------------
# Création du menu principal avec pygame_menu
# -------------------------------------------------------
custom_theme = pygame_menu.Theme(
    title_font=pygame_menu.font.FONT_FRANCHISE,
    title_font_size=60,
    title_font_color=(255, 255, 255),
    background_color=(20, 20, 40),
    widget_font=pygame_menu.font.FONT_FIRACODE,
    widget_font_color=(255, 255, 255),
    widget_font_size=40,
    selection_color=(0, 150, 255),
    widget_padding=25,
)

menu = pygame_menu.Menu(
    "Escape The Mansion",
    WIDTH * 0.7,
    HEIGHT * 0.7,
    theme=custom_theme
)

# Bouton Play : lance start_game (qui peut retourner au menu)
menu.add.button("Play", start_game)
# Quit du menu principal : quitte proprement l'application
menu.add.button("Quit", pygame_menu.events.EXIT)


# -------------------------------------------------------
# Boucle principale du menu (affichage du menu)
# -------------------------------------------------------
def main_loop():
    """
    Boucle principale qui affiche le menu (et attend que l'utilisateur lance une action).
    Quand start_game() retourne (par 'Quit to Menu'), on revient ici.
    """
    running = True
    clock = pygame.time.Clock()
    while running:
        # Récupérer les événements et permettre au menu de les utiliser
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False  # clique sur la croix dans le menu principal => quitter

        # Dessin de fond
        screen.fill((10, 10, 30))

        # Mettre à jour et dessiner le menu avec les événements capturés
        menu.update(events)
        menu.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    # Quand on sort de la boucle du menu on ferme proprement
    pygame.quit()
    sys.exit()


# Lancer la boucle principale
if __name__ == "__main__":
    main_loop()
