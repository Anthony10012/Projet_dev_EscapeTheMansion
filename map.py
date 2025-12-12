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
        if current_map == map1 and player.rect.x <= 0:
            player.rect.x = 650
            player.rect.y = 268  # assure-toi d'être en dehors d'un obstacle
            return map2
        elif current_map == map2:
            if player.rect.x <= 0:
                player.rect.x = map3.width - 64
                player.rect.y = 268
                return map3
            elif player.rect.x > map2.width:
                player.rect.x = 0
                player.rect.y = 268
                return map1
        elif current_map == map3 and player.rect.x > map3.width:
            player.rect.x = 0
            player.rect.y = 268
            return map2
        return current_map


    def get_surface(self):
        return self.bg_image




