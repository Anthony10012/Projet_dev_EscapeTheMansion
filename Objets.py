import pygame

class GameObject:
    def __init__(self, image, x, y,name=None,gives_item=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.picked = False
        self.name = name
        self.gives_item = gives_item

    def draw(self, screen):
        if not self.picked:
            screen.blit(self.image, self.rect)

    def interact(self, player_rect):
        return self.rect.colliderect(player_rect.inflate(40, 40))
