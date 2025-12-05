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
        # Map 1 → Map 2
        if current_map == map1 and player.rect.x <= 0:
            player.x = 650
            return map2

        # Map 2 → Map 3
        elif current_map == map2:
            if player.rect.x <= 0:
                player.x = 650
                player.y = 356
                return map3
            elif player.rect.x > 650:
                player.x = 10
                return map1

        # Map 3 → Map 2
        elif current_map == map3 and player.rect.x > 650:
            player.x = 10
            player.y = 212
            return map2

        return current_map



