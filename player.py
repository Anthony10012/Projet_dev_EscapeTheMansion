import pygame
import os

class Player:
    def __init__(self, screen, dossier_perso):
        self.screen = screen

        # --- Position ---
        self.x = 368
        self.y = 268
        self.vitesse = 2

        # --- Animation ---
        self.frame_index = 0
        self.frame_speed = 0.03
        self.derniere_direction = "front"

        # Chargement des animations
        self.animations = {
            #Animation lorsqu'il ne bouge pas

            "idle_left":  self.charger_animation(dossier_perso, ["idle_0.png", "idle1.png"]),
            "idle_right": self.charger_animation(dossier_perso, ["idle_0_right.png", "idle1_right.png"]),
            "idle_front": self.charger_animation(dossier_perso, ["idle0_front.png", "idle1_front.png"]),
            "idle_back":  self.charger_animation(dossier_perso, ["idle0_back.png", "idle1_back.png"]),

            #Animation lorsqu'il marche
            "walk_front": self.charger_animation(dossier_perso, ["front_walk0.png", "front_walk1.png", "front_walk2.png", "front_walk3.png", "front_walk4.png", "front_walk5.png"]),
            "walk_back": self.charger_animation(dossier_perso, ["back_walk0.png", "back_walk1.png", "back_walk2.png", "back_walk3.png", "back_walk4.png", "back_walk5.png"]),
            "walk_left": self.charger_animation(dossier_perso, ["walk_left0.png", "walk_left1.png"]),
            "walk_right": self.charger_animation(dossier_perso, ["walk_right1.png", "walk_right0.png"])
        }

        # Animation par défaut
        self.current_animation = self.animations["idle_front"]

    # --------------------------
    # Charger une animation
    # --------------------------
    def charger_animation(self, dossier, noms_images, taille=(128, 128)):
        frames = []
        for nom in noms_images:
            chemin = os.path.join(dossier, nom)
            image = pygame.image.load(chemin).convert_alpha()
            image = pygame.transform.scale(image, taille)
            frames.append(image)
        return frames

    # --------------------------
    # Récupérer la frame actuelle
    # --------------------------
    def get_frame(self):
        self.frame_index += self.frame_speed
        if self.frame_index >= len(self.current_animation):
            self.frame_index = 0
        return self.current_animation[int(self.frame_index)]

    # --------------------------
    # Déplacer le joueur
    # --------------------------
    def update(self, keys):
        en_mouvement = False

        # Déplacements
        if keys[pygame.K_UP]:
            self.y -= self.vitesse
            self.current_animation = self.animations["walk_back"]
            self.derniere_direction = "back"
            en_mouvement = True

        elif keys[pygame.K_DOWN]:
            self.y += self.vitesse
            self.current_animation = self.animations["walk_front"]
            self.derniere_direction = "front"
            en_mouvement = True

        elif keys[pygame.K_LEFT]:
            self.x -= self.vitesse
            self.current_animation = self.animations["walk_left"]
            self.derniere_direction = "left"
            en_mouvement = True

        elif keys[pygame.K_RIGHT]:
            self.x += self.vitesse
            self.current_animation = self.animations["walk_right"]
            self.derniere_direction = "right"
            en_mouvement = True

        # Pas en mouvement → idle
        if not en_mouvement:
            self.current_animation = self.animations[f"idle_{self.derniere_direction}"]

    # --------------------------
    # Afficher
    # --------------------------
    def draw(self):
        frame = self.get_frame()
        self.screen.blit(frame, (self.x, self.y))
