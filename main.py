import pygame
import sys
from player import Player
from menu import create_menu
from collision_player import *
from map import Map
from Objets import GameObject

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape The Mansion")

# Chargement des ressources

# Background
background = pygame.image.load("./design/Background/chambre.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_2 = pygame.image.load("./design/Background/Couloir.png").convert()
background_2 = pygame.transform.scale(background_2, (WIDTH, HEIGHT))
background_3 = pygame.image.load("./design/Background/FrontDoor_the_end.png").convert()
background_3 = pygame.transform.scale(background_3, (WIDTH, HEIGHT))

#le personnage
dossier_perso = "./design/Character"
player = Player(screen, dossier_perso)

#Les objets
lit = pygame.image.load("./design/Items/lit_chambre.png").convert_alpha()
lit = pygame.transform.scale(lit, (190, 190))
tiroir1 = pygame.image.load("./design/Items/tiroire_chambre.png").convert_alpha()
tiroir1 = pygame.transform.scale(tiroir1, (190, 190))
tiroir2 = pygame.image.load("./design/Items/Tiroir_Couloir.png").convert_alpha()
tiroir2 = pygame.transform.scale(tiroir2, (190, 190))
porte_chambre = pygame.image.load("./design/Items/porte_chambre.png").convert_alpha()
porte_chambre = pygame.transform.scale(porte_chambre, (28, 82))
porte_sortie = pygame.image.load("./design/Items/FrontDoor.png").convert_alpha()
porte_sortie = pygame.transform.scale(porte_sortie, (183, 247))


#Clé de la chambre  (Objet interactive)
cle_chambre_obj= GameObject(tiroir1, 60, 80, name="tiroir")
cle_chambre_obj.contains_item = "clé de la chambre"
cle_chambre_obj.item_taken = False

#Porte de la chambre bloquée (Objet interactive)
porte_chambre_obj= GameObject(porte_chambre,20,270,name="porte")
porte_chambre_obj.locked = True #Porte fermé
porte_chambre_obj.requires_item = "clé de la chambre"

# Clé pour la sortie  (Objet interactive)
cle_sortie_obj = GameObject(tiroir2, 100, 80, name="clé sortie")
cle_sortie_obj.contains_item = "clé de sortie"
cle_sortie_obj.item_taken = False


# Porte de sortie bloquée ( Objet interactive)
porte_sortie_obj = GameObject(porte_sortie, 0, 122, name="porte sortie")
porte_sortie_obj.locked = True
porte_sortie_obj.requires_item = "clé de sortie"



#Emplacement des objets
obj1 = GameObject(lit, 570, 100)
obj2 = cle_chambre_obj
obj3 = GameObject(tiroir2, 300, 80)
obj4 = GameObject(tiroir2, 350, 250)
obj5 = GameObject(tiroir2, 400, 80)
obj6 = GameObject(tiroir2, 500, 250)
obj7 = GameObject(tiroir2, 500, 80)
obj8 = GameObject(tiroir2, 250, 80)
obj9 = GameObject(tiroir2, 200, 80)
obj10 = GameObject(tiroir2, 150, 80)
obj11 = cle_sortie_obj



#les Maps
map1 = Map(800, 600, background, "map1", [obj1, obj2,porte_chambre_obj])
map2 = Map(800, 600, background_2, "map2", [obj3,obj7,cle_sortie_obj])
map3 = Map(800, 600, background_3, "map3", [obj4,obj6,porte_sortie_obj])

# Le menu
FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 64)


# Création du menu principal
menu = create_menu(screen, FONT, BIG_FONT, player, map1,map2,map3)

#map de départ
current_map = map1




# Boucle principale du menu
clock = pygame.time.Clock()
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys,  current_map.get_surface(), current_map.objects)

    # Changement de map si nécessaire
    current_map = Map.switch_map(current_map, player, map1, map2, map3)



    # Dessin de la map active et du joueur
    current_map.draw(screen)
    player.draw()

    # Menu
    menu.update(events)
    menu.draw(screen)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()
