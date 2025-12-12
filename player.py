import pygame
import os

from collision_player import check_collision_with_color


class Player:
    def __init__(self, screen, dossier_perso):
        self.screen = screen

        # Position réelle du joueur
        self.x = 368
        self.y = 268
        self.vitesse = 2

        # Le sprite fait 128x128 → rect doit faire la même taille
        self.rect = pygame.Rect(self.x, self.y, 128, 128)

        # Animation
        self.frame_index = 0
        self.frame_speed = 0.03
        self.derniere_direction = "front"

        # Chargement des animations
        self.animations = {
            "idle_left":  self.charger_animation(dossier_perso, ["idle_0.png", "idle1.png"]),
            "idle_right": self.charger_animation(dossier_perso, ["idle_0_right.png", "idle1_right.png"]),
            "idle_front": self.charger_animation(dossier_perso, ["idle0_front.png", "idle1_front.png"]),
            "idle_back":  self.charger_animation(dossier_perso, ["idle0_back.png", "idle1_back.png"]),

            "walk_front": self.charger_animation(dossier_perso, [
                "front_walk0.png", "front_walk1.png", "front_walk2.png",
                "front_walk3.png", "front_walk4.png", "front_walk5.png"
            ]),
            "walk_back":  self.charger_animation(dossier_perso, [
                "back_walk0.png", "back_walk1.png", "back_walk2.png",
                "back_walk3.png", "back_walk4.png", "back_walk5.png"
            ]),
            "walk_left":  self.charger_animation(dossier_perso, ["walk_left0.png", "walk_left1.png"]),
            "walk_right": self.charger_animation(dossier_perso, ["walk_right1.png", "walk_right0.png"])
        }

        self.current_animation = self.animations["idle_front"]

        # Rectangle des pieds (pour collisions)
        # → centré sous le joueur (sprite 128 px)
        self.feet = pygame.Rect(self.x + 54, self.y + 118, 20, 10)

    def charger_animation(self, dossier, noms_images, taille=(128, 128)):
        frames = []
        for nom in noms_images:
            chemin = os.path.join(dossier, nom)
            image = pygame.image.load(chemin).convert_alpha()
            image = pygame.transform.scale(image, taille)
            frames.append(image)
        return frames

    def get_frame(self):
        self.frame_index += self.frame_speed
        if self.frame_index >= len(self.current_animation):
            self.frame_index = 0
        return self.current_animation[int(self.frame_index)]

    # ------------------------------------------------------------
    #      COLLISION
    # ------------------------------------------------------------
    def collision_pieds(self, surface, objects):
        px, py = self.feet.center

        # Collision par couleur sur la map
        if check_collision_with_color(surface, px, py):
            return True

        # Collision avec les objets
        for obj in objects:
            if self.feet.colliderect(obj.rect):
                return True

        return False

    # ------------------------------------------------------------
    #      MISE À JOUR DU JOUEUR
    # ------------------------------------------------------------
    def update(self, keys, map_surface, map_objects):
        en_mouvement = False

        # ---------- SAUVEGARDE ----------
        old_x = self.rect.x
        old_y = self.rect.y

        # ---------- MOUVEMENT AXE X ----------
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.vitesse
            self.current_animation = self.animations["walk_left"]
            self.derniere_direction = "left"
            en_mouvement = True

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.vitesse
            self.current_animation = self.animations["walk_right"]
            self.derniere_direction = "right"
            en_mouvement = True

        # update feet
        self.feet.x = self.rect.x + 54
        self.feet.y = self.rect.y + 118

        # collision sur X → rollback seulement X
        if self.collision_pieds(map_surface, map_objects):
            self.rect.x = old_x

        # ---------- MOUVEMENT AXE Y ----------
        if keys[pygame.K_UP]:
            self.rect.y -= self.vitesse
            self.current_animation = self.animations["walk_back"]
            self.derniere_direction = "back"
            en_mouvement = True

        if keys[pygame.K_DOWN]:
            self.rect.y += self.vitesse
            self.current_animation = self.animations["walk_front"]
            self.derniere_direction = "front"
            en_mouvement = True

        # update feet
        self.feet.x = self.rect.x + 54
        self.feet.y = self.rect.y + 118

        # collision sur Y → rollback seulement Y
        if self.collision_pieds(map_surface, map_objects):
            self.rect.y = old_y

        # ---------- IDLE ----------
        if not en_mouvement:
            self.current_animation = self.animations[f"idle_{self.derniere_direction}"]

    # ------------------------------------------------------------
    #      AFFICHAGE
    # ------------------------------------------------------------
    def draw(self):
        self.screen.blit(self.get_frame(), (self.rect.x, self.rect.y))
