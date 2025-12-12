import pygame

class Map:
    def __init__(self, width, height,bg_image, bg_name, objects=None):
        self.width = width
        self.height = height
        self.bg_image = bg_image
        self.bg_name = bg_name
        self.objects = objects if objects else []



    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        for obj in self.objects:
            obj.draw(screen)

    @staticmethod
    def switch_map(current_map, player, map1, map2, map3):
        # Sortie à gauche
        if player.rect.x <= -10:
            if current_map == map1:
                player.rect.x = map2.width - player.rect.width  # droite de la map2
                player.rect.y = 200
                return map2
            elif current_map == map2:
                player.rect.x = map3.width - player.rect.width
                player.rect.y = player.rect.y + 128
                return map3
            elif current_map == map3:
                player.rect.x = map2.width - player.rect.width
                player.rect.y = 268
                return map2

        # Sortie à droite
        elif player.rect.x + player.rect.width >= current_map.width:
            if current_map == map1:
                player.rect.x = 0
                player.rect.y = 268
                return map2
            elif current_map == map2:
                player.rect.x = 0
                player.rect.y = 222
                return map1
            elif current_map == map3:
                player.rect.x = 0
                player.rect.y = player.rect.y - 128
                return map2

        return current_map

    def get_surface(self):
        return self.bg_image




