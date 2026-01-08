import json
import os


SAVE_FILE = "savegame.json"

def sauvegarder(player, maps, current_map):
    """
    Sauvegarde la position du joueur, l'inventaire, l'état des objets
    de toutes les maps et la map courante.
    """
    maps_data = []
    for m in maps:
        objets_data = []
        for obj in m.objects:
            obj_dict = {
                "name": getattr(obj, "name", None),
                "locked": getattr(obj, "locked", None),
                "item_taken": getattr(obj, "item_taken", None),
                "active": getattr(obj, "active", True),  # <-- ajouter ici
                "x": obj.rect.x,
                "y": obj.rect.y
            }
            objets_data.append(obj_dict)
        maps_data.append({
            "bg_name": m.bg_name,
            "objects": objets_data
        })

    data = {
        "player": {
            "x": player.rect.x,
            "y": player.rect.y,
            "inventory": player.inventory
        },
        "maps": maps_data,
        "current_map": current_map.bg_name
    }

    import json
    with open("savegame.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Jeu sauvegardé !")



def charger(player, maps):
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Charger le joueur
        player.rect.x = data["player"]["x"]
        player.rect.y = data["player"]["y"]
        player.inventory = data["player"]["inventory"]

        # Trouver la map correspondante
        map_name = data.get("current_map", maps[0].bg_name)
        current_map = next((m for m in maps if m.bg_name == map_name), maps[0])

        # Restaurer l'état des objets de toutes les maps
        saved_maps = {m["bg_name"]: m for m in data.get("maps", [])}
        for m in maps:
            saved_map = saved_maps.get(m.bg_name)
            if not saved_map:
                continue

            obj_data_dict = {obj["name"]: obj for obj in saved_map["objects"] if obj.get("name")}
            for obj in m.objects:
                if not hasattr(obj, "name"):
                    continue
                saved_obj = obj_data_dict.get(obj.name)
                if saved_obj:
                    if hasattr(obj, "locked") and saved_obj.get("locked") is not None:
                        obj.locked = saved_obj["locked"]
                    if hasattr(obj, "item_taken") and saved_obj.get("item_taken") is not None:
                        obj.item_taken = saved_obj["item_taken"]
                    if "active" in saved_obj:  # <-- ajouter ceci
                        obj.active = saved_obj["active"]

        print(f"Jeu chargé ! Map actuelle : {current_map.bg_name}")
        return current_map

    except FileNotFoundError:
        print("Aucune sauvegarde trouvée")
        return maps[0]


def sauvegarde_existe():
    return os.path.exists(SAVE_FILE)