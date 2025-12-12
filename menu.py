import pygame
import pygame_menu
import sys

from Objets import GameObject
from map import *





# ----------------------
# Menu Pause
# ----------------------
def draw_button(surface, rect, text, font):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    color = (60, 60, 60) if rect.collidepoint(mouse_x, mouse_y) else (40, 40, 40)
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, (200, 200, 200), rect, 2, border_radius=8)
    txt = font.render(text, True, (255, 255, 255))
    surface.blit(txt, txt.get_rect(center=rect.center))


def pause_menu(surface, FONT, BIG_FONT):
    clock = pygame.time.Clock()
    btn_w, btn_h = 300, 50
    center_x = surface.get_width() // 2
    start_y = surface.get_height() // 2 - 60
    resume_rect = pygame.Rect(center_x - btn_w // 2, start_y, btn_w, btn_h)
    save_rect = pygame.Rect(center_x - btn_w // 2, start_y + 70, btn_w, btn_h)
    quit_rect = pygame.Rect(center_x - btn_w // 2, start_y + 140, btn_w, btn_h)

    # Capture de l'écran avant pause
    screenshot = surface.copy()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'resume'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if resume_rect.collidepoint(mx, my):
                    return 'resume'
                if save_rect.collidepoint(mx, my):
                    return 'save_game'
                if quit_rect.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

        surface.blit(screenshot, (0, 0))
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        title_surf = BIG_FONT.render("PAUSE", True, (255, 255, 255))
        surface.blit(title_surf, title_surf.get_rect(center=(surface.get_width()//2, surface.get_height()//2 - 130)))

        draw_button(surface, resume_rect, "Resume", FONT)
        draw_button(surface, save_rect, "Save Game", FONT)
        draw_button(surface, quit_rect, "Quit", FONT)

        pygame.display.flip()
        clock.tick(60)


# ----------------------
# Boucle de jeu
# ----------------------
def start_game(screen, FONT, BIG_FONT, player, map1, map2, map3):
    clock = pygame.time.Clock()
    running = True
    current_map = map1  # map de départ

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                action = pause_menu(screen, FONT, BIG_FONT)
                if action == 'resume':
                    continue

        keys = pygame.key.get_pressed()
        player.update(keys, current_map.get_surface(), current_map.objects)
        print(player.rect.x, player.rect.y)

        # Changement de map si nécessaire
        current_map = Map.switch_map(current_map, player, map1, map2, map3)

        # Dessin
        current_map.draw(screen)# background + objets

        player.draw()             # joueur par-dessus

        for obj in current_map.objects:
            if obj.interact(player.feet):
                # ---- Récupération d’un item dans un objet ----
                if hasattr(obj, "contains_item") and not getattr(obj, "item_taken", False):
                    txt = FONT.render(f"Appuyez sur E pour prendre {obj.contains_item}", True, (255, 255, 255))
                    screen.blit(txt, (player.rect.x - 40, player.rect.y - 40))
                    if keys[pygame.K_e]:
                        player.inventory.append(obj.contains_item)
                        obj.item_taken = True
                        print(f"{obj.contains_item} récupérée !")

                # ---- Porte verrouillée ----
                elif hasattr(obj, "locked") and obj.locked:
                    if hasattr(obj, "requires_item") and obj.requires_item in player.inventory:
                        txt = FONT.render("Appuyez sur E pour ouvrir la porte", True, (255, 255, 255))
                        screen.blit(txt, (player.rect.x - 40, player.rect.y - 40))
                        if keys[pygame.K_e]:
                            obj.locked = False
                            print("Porte ouverte !")
                            current_map.objects.remove(obj)
                    else:
                        txt = FONT.render("La porte est verrouillée", True, (255, 0, 0))
                        screen.blit(txt, (player.rect.x - 40, player.rect.y - 40))

        # Info ou menu overlay
        info = FONT.render("Appuyez sur ESC pour pause", True, (200, 200, 200))
        screen.blit(info, (20, 20))

        pygame.display.flip()
        clock.tick(60)



# ----------------------
# Menu principal
# ----------------------
def create_menu(screen, FONT, BIG_FONT, player, map1,map2,map3):
    import pygame_menu

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
        screen.get_width() * 0.7,
        screen.get_height() * 0.7,
        theme=custom_theme
    )

    menu.add.button("PLay", lambda: start_game(screen, FONT, BIG_FONT, player, map1, map2, map3))
    menu.add.button("Quit", pygame_menu.events.EXIT)

    return menu
