import pygame

# Liste des couleurs qui empêche le joueur de traverser(Collision)


obstacle_colors= [
    (50,41,71),
    (0,0,0),
    (43,36,60)]

def check_collision_with_color(surface, x, y):
    """
    Vérifie si un pixel de la surface correspond à une couleur de collision.
    Renvoie True si collision détectée.
    """
    # Vérifie que le pixel est dans l'écran
    if x < 0 or y < 0 or x >= surface.get_width() or y >= surface.get_height():
        return True  # hors map → considéré comme collision

    couleur = surface.get_at((x, y))[:3]  # ignore alpha

    # Compare à toutes les couleurs interdites
    return couleur in obstacle_colors




