import os
import pygame
import pygame_menu
import sys
import atexit  # ← pour sauvegarde automatique à la fermeture

from Objets import GameObject
from map import Map
from saves import sauvegarder, sauvegarde_existe, charger
from player import Player

# ----------------------
# Sauvegarde automatique à la fermeture
# ----------------------
# En haut du fichier
game_finished = False  # <- nouveau drapeau

# Dans auto_save, on ne sauvegarde pas si le jeu est terminé
def auto_save(player, maps, current_map):
    if game_finished:
        return
    print("Sauvegarde automatique...")
    sauvegarder(player, maps, current_map)

# On va enregistrer automatiquement à la fermeture du programme
# maps et current_map seront définis plus tard dans la boucle de jeu
saved_game_state = {"player": None, "maps": None, "current_map": None}
atexit.register(lambda: auto_save(saved_game_state["player"], saved_game_state["maps"], saved_game_state["current_map"]))



# ----------------------
# Inventaire
# ----------------------
def inventory_menu(surface, FONT, BIG_FONT, player):
    """
    Affiche l'inventaire du joueur.
    Navigation : Flèche haut / bas pour sélectionner.
    Fermer : ESC ou I
    Affiche le nom et l'image des objets si disponible.
    Permet d'utiliser un objet en appuyant sur E (il disparait alors de l'inventaire).
    """
    clock = pygame.time.Clock()
    screenshot = surface.copy()
    selected_index = 0
    center_x = surface.get_width() // 2

    while True:
        pressed_e = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_i):
                    return  # Ferme l'inventaire
                if len(player.inventory) > 0:
                    if event.key == pygame.K_UP:
                        selected_index = max(0, selected_index - 1)
                    if event.key == pygame.K_DOWN:
                        selected_index = min(len(player.inventory) - 1, selected_index + 1)
                    if event.key == pygame.K_e:
                        pressed_e = True

        # Dessin du fond et overlay
        surface.blit(screenshot, (0, 0))
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Dessin des objets
        y = 150
        if not player.inventory:
            txt = FONT.render("L'inventaire est vide", True, (200, 200, 200))
            surface.blit(txt, (center_x - txt.get_width() // 2, 300))
        else:
            for i, item in enumerate(player.inventory):
                # Surbrillance
                if i == selected_index:
                    pygame.draw.rect(surface, (255, 255, 0), (195, y - 5, 300, 60), 2)

                # Affiche image si elle existe
                if "image_path" in item and item["image_path"] is not None:
                    img = pygame.image.load(item["image_path"]).convert_alpha()
                    img = pygame.transform.scale(img, (50, 50))
                    surface.blit(img, (200, y))

                # Nom
                name = item["name"] if isinstance(item, dict) else str(item)
                txt = FONT.render(name, True, (255, 255, 255))
                surface.blit(txt, (270, y + 10))

                y += 70

            # Utilisation de l'objet sélectionné
            if pressed_e and 0 <= selected_index < len(player.inventory):
                used_item = player.inventory.pop(selected_index)
                print(f"Vous utilisez {used_item['name'] if isinstance(used_item, dict) else used_item} !")
                selected_index = max(0, selected_index - 1)

        pygame.display.flip()
        clock.tick(60)


# ----------------------
# Cinématique de fin
# ----------------------
def exit_cutscene(screen, current_map, player, target_x, target_y):
    global game_finished
    game_finished = True  # <- indique que le jeu est terminé

    player.can_move = False
    clock = pygame.time.Clock()
    font_end = pygame.font.Font(None, 74)
    speed = 2
    moving = True

    while moving:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if abs(player.rect.y - target_y) > speed:
            if player.rect.y > target_y:
                player.rect.y -= speed
            else:
                player.rect.y += speed
        else:
            moving = False

        current_map.draw(screen)
        player.draw()
        pygame.display.flip()
        clock.tick(60)

    overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    txt = font_end.render("FÉLICITATIONS ! TU ES LIBRE !", True, (255, 255, 255))
    text_rect = txt.get_rect(center=(400, 300))
    screen.blit(txt, text_rect)

    pygame.display.flip()
    pygame.time.delay(4000)

    # --- Suppression définitive de la sauvegarde ---
    save_file = "savegame.json"
    if os.path.exists(save_file):
        os.remove(save_file)
        print("Sauvegarde supprimée après la fin du jeu.")

    pygame.quit()
    sys.exit()


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


def pause_menu(surface, FONT, BIG_FONT, player, current_map, maps):
    clock = pygame.time.Clock()
    btn_w, btn_h = 300, 50
    center_x = surface.get_width() // 2
    start_y = surface.get_height() // 2 - 60
    resume_rect = pygame.Rect(center_x - btn_w // 2, start_y, btn_w, btn_h)
    save_rect = pygame.Rect(center_x - btn_w // 2, start_y + 70, btn_w, btn_h)
    controls_rect = pygame.Rect(center_x - btn_w // 2, start_y + 140, btn_w, btn_h)
    quit_rect = pygame.Rect(center_x - btn_w // 2, start_y + 210, btn_w, btn_h)

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
                    sauvegarder(player, maps, current_map)
                if controls_rect.collidepoint(mx, my):
                    show_controls(surface, FONT)
                if quit_rect.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

        surface.blit(screenshot, (0, 0))
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        title_surf = BIG_FONT.render("PAUSE", True, (255, 255, 255))
        surface.blit(title_surf, title_surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 130)))

        draw_button(surface, resume_rect, "Resume", FONT)
        draw_button(surface, save_rect, "Save Game", FONT)
        draw_button(surface, controls_rect, "Controls", FONT)
        draw_button(surface, quit_rect, "Quit", FONT)

        pygame.display.flip()
        clock.tick(60)

def show_controls(surface, FONT):
    clock = pygame.time.Clock()
    running = True
    controls_text = [
        "Move Up: UP",
        "Move Down: DOWN",
        "Move Left: LEFT",
        "Move Right: RIGHT",
        "Interaction:" "E",
        "Pause: Esc",
    ]
    screenshot = surface.copy()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                running = False

        surface.blit(screenshot, (0, 0))
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        y_offset = 100
        for line in controls_text:
            text_surf = FONT.render(line, True, (255, 255, 255))
            surface.blit(text_surf, text_surf.get_rect(center=(surface.get_width() // 2, y_offset)))
            y_offset += 50

        pygame.display.flip()
        clock.tick(60)

# ----------------------
# Réinitialisation complète
# ----------------------
def reset_game(player, map1, map2, map3):
    player.reset()
    for m in [map1, map2, map3]:
        m.reset()


# ----------------------
# Boucle de jeu
# ----------------------
# ----------------------
# Boucle de jeu
# ----------------------
def start_game(screen, FONT, BIG_FONT, player, map1, map2, map3, start_map=None):
    clock = pygame.time.Clock()
    running = True
    current_map = start_map if start_map else map1
    maps = [map1, map2, map3]

    # On met à jour le state pour atexit
    saved_game_state["player"] = player
    saved_game_state["maps"] = maps
    saved_game_state["current_map"] = current_map

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = pause_menu(screen, FONT, BIG_FONT, player, current_map, maps)
                    if action == 'resume':
                        continue
                if event.key == pygame.K_i:
                    inventory_menu(screen, FONT, BIG_FONT, player)

        keys = pygame.key.get_pressed()
        active_objects = [obj for obj in current_map.objects if not hasattr(obj, "active") or obj.active]
        player.update(keys, current_map.get_surface(), active_objects)

        current_map = Map.switch_map(current_map, player, map1, map2, map3)
        saved_game_state["current_map"] = current_map  # mise à jour à chaque frame

        current_map.draw(screen)
        player.draw()

        for obj in current_map.objects:
            if hasattr(obj, "active") and not obj.active:
                continue
            if obj.interact(player.feet):
                # Récupération d’item
                if hasattr(obj, "contains_item") and not getattr(obj, "item_taken", False):
                    txt = FONT.render("Appuyez sur E pour récupérer la clé", True, (255, 255, 255))
                    screen.blit(txt, (player.rect.x - 60, player.rect.y - 40))

                    if keys[pygame.K_e]:
                    # Détermine le chemin de l'image selon l'objet
                        if obj.contains_item == "clé de la chambre":
                            image_path = "./design/Items/clé_chambre.png"
                        elif obj.contains_item == "clé de sortie":
                            image_path = "./design/Items/clé_porte_sortie.png"
                        else:
                            image_path = None  # pour d'autres objets sans image

                        player.inventory.append({
                            "name": obj.contains_item,
                            "image_path": image_path
                        })
                        obj.item_taken = True
                        print(f"{obj.contains_item} récupérée !")


                        # --- Sauvegarde automatique lors de l'utilisation ---
                        auto_save(player, maps, current_map)

                # Porte verrouillée
                elif hasattr(obj, "locked") and obj.locked:
                    if hasattr(obj, "requires_item") and any(
                        item["name"] == obj.requires_item for item in player.inventory if isinstance(item, dict)
                    ):
                        txt = FONT.render("Appuyez sur E pour sortir !", True, (255, 255, 255))
                        screen.blit(txt, (player.rect.x - 40, player.rect.y - 40))
                        if keys[pygame.K_e]:
                            key_item = next(item for item in player.inventory if item["name"] == obj.requires_item)
                            player.inventory.remove(key_item)
                            obj.locked = False
                            obj.active = False
                            print("la porte s'est ouverte...")

                            # --- Sauvegarde automatique lors de l'utilisation de la clé ---
                            auto_save(player, maps, current_map)

                            if obj.name == "porte sortie":
                                porte_centre_x = obj.rect.x + (obj.image.get_width() // 2)
                                player.rect.centerx = porte_centre_x
                                exit_cutscene(screen, current_map, player, player.rect.x, 150)

                    else:
                        txt = FONT.render("La porte est verrouillée", True, (255, 0, 0))
                        screen.blit(txt, (player.rect.x - 40, player.rect.y - 40))

        info = FONT.render("Appuyez sur ESC pour pause | I: Inventaire", True, (200, 200, 200))
        screen.blit(info, (20, 20))

        pygame.display.flip()
        clock.tick(60)


# ----------------------
# Option Continue
# ----------------------
def continue_game(screen, FONT, BIG_FONT, player, map1, map2, map3):
    maps = [map1, map2, map3]
    loaded_map = charger(player, maps)
    start_game(screen, FONT, BIG_FONT, player, map1, map2, map3, start_map=loaded_map)


# ----------------------
# Menu principal
# ----------------------
def create_menu(screen, FONT, BIG_FONT, player, map1, map2, map3):
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

    if sauvegarde_existe():
        menu.add.button("New Game", lambda: (
            reset_game(player, map1, map2, map3),
            start_game(screen, FONT, BIG_FONT, player, map1, map2, map3)
        ))
        menu.add.button("Continue", lambda: (
            continue_game(screen, FONT, BIG_FONT, player, map1, map2, map3)
        ))
    else:
        menu.add.button("New Game", lambda: (
            reset_game(player, map1, map2, map3),
            start_game(screen, FONT, BIG_FONT, player, map1, map2, map3)
        ))

    menu.add.button("Quit", pygame_menu.events.EXIT)
    return menu
