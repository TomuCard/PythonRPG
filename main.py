import json
import os
import time

import arcade
from arcade.gui import UITextureButton

from Classes.Player import Player

from functions.save import save
from functions.load import load

CHARACTER_SCALING = 0.8
TILE_SCALING = 1
current_player = Player("Bob", 100, 100, [], [], {}, {}, {})

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960
SCREEN_TITLE = "Super Jeu de la MORT fait par Hugo, Faustine, Roland, Jiek, Tom"
SPRITE_PIXEL_SIZE = 64
DEFAULT_FONT_SIZE = 10
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

PLAYER_MOVEMENT_SPEED = 5

with open("Data/map.json", "r") as f:
    current_map = json.loads(f.read())
current_room = current_map["START"]
# Valeur qui détermine sur quel écran le joueur se trouve (Menu interface/Menu jeu)
interface = 0


#   ----------Python Arcade part----------
class GameWindow(arcade.Window):
    def __init__(self):
        # Taille de la fenêtre
        super().__init__(960, 960)
        """self.selected_armor = armors[0]
        self.selected_weapon = weapons[0]
        self.selected_consumable = consumables[0]
        self.selected_misc = miscs[0]"""

        self.start_view = StartView()
        self.game_view = GameView()
        self.inventory_view = InventoryView()
        self.menu_view = MenuView()
        self.settings_view = SettingsView()
        self.key_bindings_view = KeyBindingsView()
        self.save_view = SaveView()
        self.load_view = LoadView()
        """self.armor_view = ArmorView()
        self.weapon_view = WeaponView()
        self.consumable_view = ConsumableView()
        self.misc_view = MiscView()"""

        # Fenêtre lancée au démarrage du jeu
        self.show_view(self.start_view)


class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        chest = arcade.load_texture('Assets/png/buttons/chest.png')
        open_chest = arcade.load_texture('Assets/png/buttons/open_chest.png')
        self.inventory_button = arcade.gui.UITextureButton(910, 870, texture=chest, texture_hovered=open_chest)
        self.inventory_button.on_click = self.inventory_button_clicked
        self.manager.add(self.inventory_button)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.tile_map = None

        self.player_list = None

        self.player_sprite = None

        self.physics_engine = None

        self.view_left = 0
        self.view_bottom = 0

        self.game_over = False

        self.last_time = None
        self.frame_count = 0
        self.fps_message = None

        self.end_of_map_right = 0
        self.end_of_map_left = 0
        self.end_of_map_top = 0
        self.end_of_map_bottom = 0

        self.current_room = current_room
        self.name_map_message = self.current_room["name"]
        self.setup()

    def setup(self):
        self.player_list = arcade.SpriteList()

        # Animation du player
        self.player_sprite = arcade.AnimatedWalkingSprite()
        self.player_sprite.stand_right_textures = []
        self.player_sprite.stand_right_textures.append(
            arcade.load_texture(
                "Assets/images/animated_characters/male_person/malePerson_idle.png"))

        self.player_sprite.stand_left_textures = []
        self.player_sprite.stand_left_textures.append(
            arcade.load_texture(
                "Assets/images/animated_characters/male_person/malePerson_idle.png", mirrored=True))

        self.player_sprite.walk_right_textures = []
        for i in range(7):
            self.player_sprite.walk_right_textures.append(
                arcade.load_texture(
                    f"Assets/images/animated_characters/male_person/malePerson_walk{i}.png"))

        self.player_sprite.walk_left_textures = []
        for i in range(7):
            self.player_sprite.walk_left_textures.append(
                arcade.load_texture(
                    f"Assets/images/animated_characters/male_person/malePerson_walk{i}.png", mirrored=True))

        # Paramètres du sprite du player
        self.player_sprite.scale = CHARACTER_SCALING
        self.player_sprite.center_x = 160
        self.player_sprite.center_y = 748
        self.player_list.append(self.player_sprite)

        # Charge la room du start
        self.load_level(self.current_room)

        self.game_over = False

    def load_level(self, room):
        self.tile_map = arcade.load_tilemap(
            f"Assets/maps/{room['id']}.tmx", scaling=TILE_SCALING
        )

        # self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        self.end_of_map_right = self.tile_map.width * GRID_PIXEL_SIZE
        self.end_of_map_left = 0
        self.end_of_map_top = self.tile_map.height * GRID_PIXEL_SIZE
        self.end_of_map_bottom = 0

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.tile_map.sprite_lists["GROUND"])

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

            self.view_left = 0
            self.view_bottom = 0

        print(self.current_room["id"])

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.frame_count += 1

        self.clear()
        self.tile_map.sprite_lists["background"].draw()
        self.tile_map.sprite_lists["GROUND"].draw()
        self.tile_map.sprite_lists["bottom"].draw()

        # les layers des mes objets, je n'ai pas trouvé autrement
        # que de faire un layer par item et de le dessiner que si il existe
        if "sword_1" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["sword_1"].draw()
        if "sword_2" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["sword_2"].draw()
        if "sword_3" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["sword_3"].draw()
        if "sword_4" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["sword_4"].draw()
        if "sword_5" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["sword_5"].draw()
        if "sword_6" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["sword_6"].draw()
        if "sword_7" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["sword_7"].draw()
        if "shield_1" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["shield_1"].draw()
        if "shield_2" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["shield_2"].draw()
        if "shield_3" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["shield_3"].draw()
        if "shield_4" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["shield_4"].draw()
        if "shield_5" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["shield_5"].draw()
        if "shield_6" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["shield_6"].draw()
        if "staff_1" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["staff_1"].draw()
        if "staff_2" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["staff_2"].draw()
        if "staff_3" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["staff_3"].draw()
        if "staff_4" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["staff_4"].draw()
        if "staff_5" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["staff_5"].draw()
        if "staff_6" in self.tile_map.sprite_lists:
            self.tile_map.sprite_lists["staff_6"].draw()
        self.player_list.draw()

        self.tile_map.sprite_lists["top"].draw()

        start_x = self.tile_map.height * GRID_PIXEL_SIZE - 5
        start_y = self.tile_map.width * GRID_PIXEL_SIZE
        arcade.draw_text(self.name_map_message,
                         start_x,
                         start_y,
                         arcade.color.WHITE,
                         DEFAULT_FONT_SIZE * 2,
                         width=SCREEN_WIDTH,
                         align="left",
                         bold=True,
                         anchor_x="right",
                         anchor_y="top"
                         )
        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0 / (time.time() - self.last_time) * 60
            self.fps_message = f"FPS: {fps:5.0f}"

        if self.fps_message:
            arcade.draw_text(
                self.fps_message,
                self.view_left + 10,
                self.view_bottom + 10,
                arcade.color.WHITE,
                14,
            )

        if self.frame_count % 60 == 0:
            self.last_time = time.time()

        self.manager.draw()

        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                self.view_left + 200,
                self.view_bottom + 200,
                arcade.color.BLACK,
                30,
            )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0

    def on_update(self, delta_time: float):

        if self.player_sprite.center_x >= self.end_of_map_right:
            if self.current_room["links"]["Right"] is not None:
                self.current_room = current_map[self.current_room["links"]["Right"]]
                self.load_level(self.current_room)
                self.player_sprite.center_x = 10
                self.player_sprite.center_y = self.player_sprite.center_y
                self.name_map_message = self.current_room["name"]
            else:
                self.player_sprite.center_x += -5

        elif self.player_sprite.center_x <= self.end_of_map_left:
            if self.current_room["links"]["Left"] is not None:
                self.current_room = current_map[self.current_room["links"]["Left"]]
                self.load_level(self.current_room)
                self.player_sprite.center_x = self.end_of_map_right - 20
                self.player_sprite.center_y = self.player_sprite.center_y
                self.name_map_message = self.current_room["name"]
            else:
                self.player_sprite.center_x += 5

        elif self.player_sprite.center_y >= self.end_of_map_top:
            if self.current_room["links"]["Top"] is not None:
                self.current_room = current_map[self.current_room["links"]["Top"]]
                self.load_level(self.current_room)
                self.player_sprite.center_x = self.player_sprite.center_x
                self.player_sprite.center_y = 10
                self.name_map_message = self.current_room["name"]
            else:
                self.player_sprite.center_y += -5

        elif self.player_sprite.center_y <= self.end_of_map_bottom:
            if self.current_room["links"]["Bottom"] is not None:
                self.current_room = current_map[self.current_room["links"]["Bottom"]]
                self.load_level(self.current_room)
                self.player_sprite.center_x = self.player_sprite.center_x
                self.player_sprite.center_y = self.end_of_map_top - 20
                self.name_map_message = self.current_room["name"]
            else:
                self.player_sprite.center_y += 5
        
        # Etant donné que je n'ai pas trouvé comment faire autrement, je dis que pour chaque layer d'item, si le player
        # passe sur l'item il disparait et l'ajoute dans l'inventaire
        if "sword_1" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["sword_1"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un sword de niveau 1")
        if "sword_2" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["sword_2"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un sword de niveau 2")
        if "sword_3" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["sword_3"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un sword de niveau 3")
        if "sword_4" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["sword_4"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un sword de niveau 4")
        if "sword_5" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["sword_5"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un sword de niveau 5")
        if "sword_6" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["sword_6"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un sword de niveau 6")
        if "sword_7" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["sword_7"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer L'OMEGA SUPER HYPER SWORD DE LA MORT QUI TUE DE NIVEAU 7 ! ! !")
        if "shield_1" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["shield_1"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un shield de niveau 1")
        if "shield_2" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["shield_2"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un shield de niveau 2")
        if "shield_3" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["shield_3"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un shield de niveau 3")
        if "shield_4" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["shield_4"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un shield de niveau 4")
        if "shield_5" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["shield_5"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un shield de niveau 5")
        if "shield_6" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["shield_6"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un shield de niveau 6")
        if "staff_1" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["staff_1"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un staff de niveau 1")
        if "staff_2" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["staff_2"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un staff de niveau 2")
        if "staff_3" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["staff_3"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un staff de niveau 3")
        if "staff_4" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["staff_4"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un staff de niveau 4")
        if "staff_5" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["staff_5"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un staff de niveau 5")
        if "staff_6" in self.tile_map.sprite_lists:
            items_hit = arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["staff_6"])
            for items in items_hit:
                items.remove_from_sprite_lists()
                print("Tu viens de récupérer un staff de niveau 6")
        
        if not self.game_over:
            self.physics_engine.update()

        self.player_list.update_animation()

    def inventory_button_clicked(self, event):
        self.window.show_view(self.window.inventory_view)


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        # Import des images utilisées
        play = arcade.load_texture('Assets/png/buttons/play.png')
        play_hovered = arcade.load_texture('Assets/png/buttons/play_hovered.png')
        settings = arcade.load_texture('Assets/png/buttons/settings.png')
        settings_hovered = arcade.load_texture('Assets/png/buttons/settings_hovered.png')
        save = arcade.load_texture('Assets/png/buttons/save.png')
        save_hovered = arcade.load_texture('Assets/png/buttons/save_hovered.png')
        load = arcade.load_texture('Assets/png/buttons/load.png')
        load_hovered = arcade.load_texture('Assets/png/buttons/load_hovered.png')
        quit = arcade.load_texture('Assets/png/buttons/quit.png')
        quit_hovered = arcade.load_texture('Assets/png/buttons/quit_hovered.png')

        # Création des boutons, comportant les coordonnées et les différentes textures
        self.play_button = arcade.gui.UITextureButton(381, 673, texture=play, texture_hovered=play_hovered, )
        self.settings_button = arcade.gui.UITextureButton(337, 560, texture=settings, texture_hovered=settings_hovered)
        self.save_button = arcade.gui.UITextureButton(271, 437, texture=save, texture_hovered=save_hovered)
        self.load_button = arcade.gui.UITextureButton(491, 437, texture=load, texture_hovered=load_hovered)
        self.quit_button = arcade.gui.UITextureButton(381, 314, texture=quit, texture_hovered=quit_hovered)

        # Ajouts des boutons sur la fenêtre
        self.play_button.on_click = self.play_button_clicked
        self.manager.add(self.play_button)
        self.settings_button.on_click = self.settings_button_clicked
        self.manager.add(self.settings_button)
        self.save_button.on_click = self.save_button_clicked
        self.manager.add(self.save_button)
        self.load_button.on_click = self.load_button_clicked
        self.manager.add(self.load_button)
        self.quit_button.on_click = self.quit_button_clicked
        self.manager.add(self.quit_button)

        self.background = arcade.load_texture("Assets/png/background.png")

    # Fonctions qui renvoie sur une autre fenêtre lorsqu'un bouton est cliqué
    def play_button_clicked(self, event):
        global interface
        interface = 1
        self.window.show_view(self.window.game_view)

    def settings_button_clicked(self, event):
        self.window.show_view(self.window.settings_view)

    def save_button_clicked(self, event):
        self.window.show_view(self.window.save_view)

    def load_button_clicked(self, event):
        self.window.show_view(self.window.load_view)

    def quit_button_clicked(self, event):
        arcade.exit()

    # Permet d'activer l'utilisation de la fenêtre lorsqu'on l'utilise
    def on_show_view(self):
        self.manager.enable()

    # Permet de désactiver l'utilisation de la fenêtre lorsqu'on ne l'utilise pas
    def on_hide_view(self):
        self.manager.disable()

    # Remet l'affichage de l'écran à 0
    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_lrwh_rectangle_textured(0, 0, 960, 960, self.background, alpha=40)


class InventoryView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        cross = arcade.load_texture('Assets/png/buttons/cross.png')
        cross_hovered = arcade.load_texture('Assets/png/buttons/cross_hovered.png')
        armor_img = arcade.load_texture('Assets/png/buttons/armor.png')
        weapon_img = arcade.load_texture('Assets/png/buttons/armes.png')
        consumable_img = arcade.load_texture('Assets/png/buttons/potions.png')
        misc_img = arcade.load_texture('Assets/png/buttons/divers.png')

        self.cross_button = arcade.gui.UITextureButton(910, 910, texture=cross, texture_hovered=cross_hovered)
        self.armor_button = arcade.gui.UITextureButton(260, 630, texture=armor_img)
        self.weapon_button = arcade.gui.UITextureButton(560, 630, texture=weapon_img)
        self.consumable_button = arcade.gui.UITextureButton(260, 350, texture=consumable_img)
        self.misc_button = arcade.gui.UITextureButton(560, 350, texture=misc_img)

        self.cross_button.on_click = self.cross_button_clicked
        self.manager.add(self.cross_button)

        self.armor_button.on_click = self.armor_button_clicked
        self.manager.add(self.armor_button)

        self.weapon_button.on_click = self.weapon_button_clicked
        self.manager.add(self.weapon_button)

        self.consumable_button.on_click = self.consumable_button_clicked
        self.manager.add(self.consumable_button)

        self.misc_button.on_click = self.misc_button_clicked
        self.manager.add(self.misc_button)

    def cross_button_clicked(self, event):
        self.window.show_view(self.window.game_view)

    def armor_button_clicked(self, event):
        self.window.show_view(self.window.armor_view)

    def weapon_button_clicked(self, event):
        self.window.show_view(self.window.weapon_view)

    def consumable_button_clicked(self, event):
        self.window.show_view(self.window.consumable_view)

    def misc_button_clicked(self, event):
        self.window.show_view(self.window.misc_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.set_background_color(arcade.color.GRAY)


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        play = arcade.load_texture('Assets/png/buttons/play.png')
        play_hovered = arcade.load_texture('Assets/png/buttons/play_hovered.png')
        settings = arcade.load_texture('Assets/png/buttons/settings.png')
        settings_hovered = arcade.load_texture('Assets/png/buttons/settings_hovered.png')
        save = arcade.load_texture('Assets/png/buttons/save.png')
        save_hovered = arcade.load_texture('Assets/png/buttons/save_hovered.png')
        quit = arcade.load_texture('Assets/png/buttons/quit.png')
        quit_hovered = arcade.load_texture('Assets/png/buttons/quit_hovered.png')

        self.play_button = arcade.gui.UITextureButton(381, 673, texture=play, texture_hovered=play_hovered)
        self.settings_button = arcade.gui.UITextureButton(337, 560, texture=settings, texture_hovered=settings_hovered)
        self.save_button = arcade.gui.UITextureButton(381, 437, texture=save, texture_hovered=save_hovered)
        self.quit_button = arcade.gui.UITextureButton(381, 314, texture=quit, texture_hovered=quit_hovered)

        self.play_button.on_click = self.play_button_clicked
        self.manager.add(self.play_button)
        self.settings_button.on_click = self.settings_button_clicked
        self.manager.add(self.settings_button)
        self.save_button.on_click = self.save_button_clicked
        self.manager.add(self.save_button)
        self.quit_button.on_click = self.quit_button_clicked
        self.manager.add(self.quit_button)

    def play_button_clicked(self, event):
        self.window.show_view(self.window.game_view)

    def settings_button_clicked(self, event):
        self.window.show_view(self.window.settings_view)

    def save_button_clicked(self, event):
        self.window.show_view(self.window.save_view)

    def quit_button_clicked(self, event):
        arcade.exit()

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.set_background_color(arcade.color.WHITE_SMOKE)


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        back = arcade.load_texture('Assets/png/buttons/back.png')
        back_hovered = arcade.load_texture('Assets/png/buttons/back_hovered.png')
        bindings = arcade.load_texture('Assets/png/buttons/bindings.png')
        bindings_hovered = arcade.load_texture('Assets/png/buttons/bindings_hovered.png')

        self.back_button = arcade.gui.UITextureButton(381, 320, texture=back, texture_hovered=back_hovered)
        self.bindings_button = arcade.gui.UITextureButton(337, 490, texture=bindings, texture_hovered=bindings_hovered)

        self.back_button.on_click = self.back_button_clicked
        self.manager.add(self.back_button)
        self.bindings_button.on_click = self.bindings_button_clicked
        self.manager.add(self.bindings_button)

    # Fonction qui nous fait revenir dans la fenêtre correspondant à l'endroit où le joueur à utilisé le bouton 'settings'
    def back_button_clicked(self, event):
        global interface
        if interface == 0:
            self.window.show_view(self.window.start_view)
        elif interface == 1:
            self.window.show_view(self.window.menu_view)

    def bindings_button_clicked(self, event):
        self.window.show_view(self.window.key_bindings_view)

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.set_background_color(arcade.color.WHITE_SMOKE)


class KeyBindingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        back = arcade.load_texture('Assets/png/buttons/back.png')
        back_hovered = arcade.load_texture('Assets/png/buttons/back_hovered.png')

        self.back_button = arcade.gui.UITextureButton(381, 320, texture=back, texture_hovered=back_hovered)
        self.back_button.on_click = self.back_button_clicked
        self.manager.add(self.back_button)

    def back_button_clicked(self, event):
        self.window.show_view(self.window.settings_view)

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

        # Ahout des contours d'un rectangle
        arcade.draw_rectangle_outline(480, 780, 200, 200, arcade.color.BLACK, 3)
        # Ahout du texte autour et à l'interieur du rectangle
        arcade.draw_text("CONTROLS", 390, 895, arcade.color.BLACK, font_size=23, align="left")
        arcade.draw_text("Forward : Z", 390, 850, arcade.color.BLACK, font_size=15, align="left")
        arcade.draw_text("Backward: S", 390, 825, arcade.color.BLACK, font_size=15, align="left")
        arcade.draw_text("Left: Q", 390, 800, arcade.color.BLACK, font_size=15, align="left")
        arcade.draw_text("Right: D ", 390, 775, arcade.color.BLACK, font_size=15, align="left")
        arcade.draw_text("Crouch: Left ctrl", 390, 750, arcade.color.BLACK, font_size=15, align="left")
        arcade.draw_text("Jump: Space", 390, 725, arcade.color.BLACK, font_size=15, align="left")
        arcade.draw_text("test :i", 390, 700, arcade.color.BLACK, font_size=15, align="left")

        arcade.set_background_color(arcade.color.WHITE_SMOKE)


def savecard(number, exists):
    title_x = 110 + (number - 1) * 300
    title_y = 650
    rectangle_x = 150 + (number - 1) * 300
    rectangle_y = 500
    text_x = 60 + (number - 1) * 300
    date_y = 620
    name_y = 550
    arcade.draw_rectangle_outline(rectangle_x, rectangle_y, 250, 350, arcade.color.BLACK, 3)
    if exists:
        saved_data = load(number)
        save_date = saved_data["date"]
        name = saved_data["player"].name
        arcade.draw_text(f'SAVE {number}', title_x, title_y, arcade.color.BLACK, font_size=23, align="left")
        arcade.draw_text(f"date: {save_date}", text_x, date_y, arcade.color.BLACK, font_size=23, align="left")
        arcade.draw_text(f"name: {name}", text_x, name_y, arcade.color.BLACK, font_size=23, align="left")
    else:
        arcade.draw_text('Empty', title_x, title_y, arcade.color.BLACK, font_size=23, align="left")


class SaveView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        back = arcade.load_texture('Assets/png/buttons/back.png')
        back_hovered = arcade.load_texture('Assets/png/buttons/back_hovered.png')
        save = arcade.load_texture('Assets/png/buttons/save.png')
        save_hovered = arcade.load_texture('Assets/png/buttons/save_hovered.png')
        self.back_button = arcade.gui.UITextureButton(381, 70, texture=back, texture_hovered=back_hovered)
        self.back_button.on_click = self.back_button_clicked
        self.save_button_one = arcade.gui.UITextureButton(50, 200, texture=save, texture_hovered=save_hovered)
        self.save_button_one.on_click = self.save_button_one_clicked
        self.save_button_two = arcade.gui.UITextureButton(350, 200, texture=save, texture_hovered=save_hovered)
        self.save_button_two.on_click = self.save_button_two_clicked
        self.save_button_three = arcade.gui.UITextureButton(650, 200, texture=save, texture_hovered=save_hovered)
        self.save_button_three.on_click = self.save_button_three_clicked
        self.manager.add(self.back_button)
        self.manager.add(self.save_button_one)
        self.manager.add(self.save_button_two)
        self.manager.add(self.save_button_three)

    def back_button_clicked(self, event):
        self.window.show_view(self.window.menu_view)

    def save_button_one_clicked(self, event):
        save(current_map, current_player, current_room, 1)

    def save_button_two_clicked(self, event):
        save(current_map, current_player, current_room, 2)

    def save_button_three_clicked(self, event):
        save(current_map, current_player, current_room, 3)

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

        arcade.draw_text("SAVES", 440, 895, arcade.color.BLACK, font_size=23, align="left")
        savecard(1, os.path.isfile("Data/Saves/Save_1/map_data.json"))
        savecard(2, os.path.isfile("Data/Saves/Save_2/map_data.json"))
        savecard(3, os.path.isfile("Data/Saves/Save_3/map_data.json"))
        arcade.set_background_color(arcade.color.WHITE_SMOKE)


class LoadView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        back = arcade.load_texture('Assets/png/buttons/back.png')
        back_hovered = arcade.load_texture('Assets/png/buttons/back_hovered.png')
        load = arcade.load_texture('Assets/png/buttons/load.png')
        load_hovered = arcade.load_texture('Assets/png/buttons/load_hovered.png')
        self.back_button = arcade.gui.UITextureButton(381, 70, texture=back, texture_hovered=back_hovered)
        self.back_button.on_click = self.back_button_clicked
        self.load_button_one = arcade.gui.UITextureButton(50, 200, texture=load, texture_hovered=load_hovered)
        self.load_button_one.on_click = self.load_button_one_clicked
        self.load_button_two = arcade.gui.UITextureButton(350, 200, texture=load, texture_hovered=load_hovered)
        self.load_button_two.on_click = self.load_button_two_clicked
        self.load_button_three = arcade.gui.UITextureButton(650, 200, texture=load, texture_hovered=load_hovered)
        self.load_button_three.on_click = self.load_button_three_clicked
        self.manager.add(self.back_button)
        self.manager.add(self.load_button_one)
        self.manager.add(self.load_button_two)
        self.manager.add(self.load_button_three)

    def back_button_clicked(self, event):
        self.window.show_view(self.window.menu_view)

    def load_button_one_clicked(self, event):
        loaded_save = load(1)

    def load_button_two_clicked(self, event):
        loaded_save = load(2)

    def load_button_three_clicked(self, event):
        loaded_save = load(3)

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

        arcade.draw_text("SAVES", 440, 895, arcade.color.BLACK, font_size=23, align="left")
        savecard(1, os.path.isfile("Data/Saves/Save_1/map_data.json"))
        savecard(2, os.path.isfile("Data/Saves/Save_2/map_data.json"))
        savecard(3, os.path.isfile("Data/Saves/Save_3/map_data.json"))
        arcade.set_background_color(arcade.color.WHITE_SMOKE)


def main():
    """ Main function """
    window = GameWindow()
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


main()
