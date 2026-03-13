import arcade
import math
import random
import os
from typing import Optional, List

LEVEL_1 = [
    "WWWWWWWWWWWWWWWWWWWWWWWW",
    "W P                    W",
    "W WWWWWWWWWWWWWWWWWW   W",
    "W W B                W W",
    "W W   WWWWWWWWWWWWWW W W",
    "W W W S            W W W",
    "W W W WWWWWWWWWW   W W W",
    "W W W W G          W W W",
    "W W W WWWWWWWWWWWWWW W W",
    "W W W                W W",
    "W W WWWWWWWWWWWWWWWWWW W",
    "W W                    W",
    "WWWWWWWWWWWWWWWWWWWW   W",
    "W                      E",
    "WWWWWWWWWWWWWWWWWWWWWWWW"
]

LEVEL_2 = [
    "WWWWWWWWWWWWWWWWWWWWWWWW",
    "W P                  X W",
    "W WWWWWWWWWWWWWWWWWW   W",
    "W W B              X W W",
    "W W   WWWWWWWWWWWWWW W W",
    "W W W S            X W W",
    "W W W WWWWWWWWWW   W W W",
    "W W W W G            W W",
    "W W W WWWWWWWWWWWWWWWW W",
    "W W W              X   W",
    "W W WWWWWWWWWWWWWWWWWW W",
    "W W X                  W",
    "WWWWWWWWWWWWWWWWWWWW   W",
    "W                      E",
    "WWWWWWWWWWWWWWWWWWWWWWWW"
]

LEVEL_3 = [
    "WWWWWWWWWWWWWWWWWWWWWWWW",
    "W P                  X W",
    "W WWWWWWWWWWWWWWWWWW   W",
    "W W                  W W",
    "W W   WWWWWWWWWWWWWW W W",
    "W W W X            W W W",
    "W W W WWWWWWWWWW   W W W",
    "W W W W K        W W W W",
    "W W W WWWWWWWWWWWW W W W",
    "W W W X          W W W W",
    "W W WWWWWWWWWWWWWW W W W",
    "W W X                  W",
    "WWWWWWWWWWWWWWWWWWWW D W",
    "W                    D E",
    "WWWWWWWWWWWWWWWWWWWWWWWW"
]

LEVEL_4 = [
    "WWWWWWWWWWWWWWWWWWWWWWWW",
    "W P                  X W",
    "W WWWWWWWWWWWWWWWWWW   W",
    "W W K              X W W",
    "W W   WWWWWWWWWWWWWW W W",
    "W W W X            W W W",
    "W W W WWWWWWWWWW   W W W",
    "W W W W B        W W W W",
    "W W W WWWWWWWWWWWW W W W",
    "W W W X          W W W W",
    "W W WWWWWWWWWWWWWW W W W",
    "W W X                  W",
    "WWWWWWWWWWWWWWWWWWWW D W",
    "W   G                D E",
    "WWWWWWWWWWWWWWWWWWWWWWWW"
]

LEVEL_5 = [
    "WWWWWWWWWWWWWWWWWWWWWWWW",
    "W P X                K W",
    "W WWWWWWWWWWWWWWWWWW   W",
    "W W X                W W",
    "W W   WWWWWWWWWWWWWW W W",
    "W W W B            X W W",
    "W W W WWWWWWWWWW   W W W",
    "W W W W S      X W W W W",
    "W W W WWWWWWWWWWWW W W W",
    "W W W X            W W W",
    "W W WWWWWWWWWWWWWW W W W",
    "W W X                  W",
    "WWWWWWWWWWWWWWWWWWWW D W",
    "W   G                D E",
    "WWWWWWWWWWWWWWWWWWWWWWWW"
]

LEVELS: List[List[str]] = [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5]

def read_score() -> int:
    if os.path.exists("results.txt"):
        try:
            with open("results.txt", "r", encoding="utf-8") as f:
                return int(f.read().strip())
        except Exception:
            pass
    return 0

def write_score(score: int) -> None:
    if score > read_score():
        with open("results.txt", "w", encoding="utf-8") as f:
            f.write(str(score))

class Collectable(arcade.Sprite):
    def __init__(self, image: str, scale: float, x: float, y: float):
        super().__init__(image, scale=scale)
        self.center_x = x
        self.center_y = y
        self.start_y = y
        self.timer = random.uniform(0, 6.28)

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.timer += delta_time * 5
        self.center_y = self.start_y + math.sin(self.timer) * 5

class Coin(Collectable):
    def __init__(self, x: float, y: float, coin_type: str):
        if coin_type == "B":
            super().__init__(":resources:images/items/coinBronze.png", 0.5, x, y)
            self.value = 10
        elif coin_type == "S":
            super().__init__(":resources:images/items/coinSilver.png", 0.5, x, y)
            self.value = 50
        else:
            super().__init__(":resources:images/items/coinGold.png", 0.5, x, y)
            self.value = 100

class Key(Collectable):
    def __init__(self, x: float, y: float):
        super().__init__(":resources:images/items/keyYellow.png", 0.5, x, y)

class Bullet(arcade.SpriteSolidColor):
    def __init__(self, x: float, y: float, direction: str):
        super().__init__(15, 5, arcade.color.YELLOW)
        self.center_x = x
        self.center_y = y
        self.speed = 10
        
        if direction == 'R':
            self.change_x = self.speed
        elif direction == 'L':
            self.change_x = -self.speed
        elif direction == 'U':
            self.change_y = self.speed
            self.width, self.height = self.height, self.width
        elif direction == 'D':
            self.change_y = -self.speed
            self.width, self.height = self.height, self.width

class ParticleSprite(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__(":resources:images/items/star.png", scale=0.3)
        self.center_x = x
        self.center_y = y
        self.change_x = random.uniform(-4, 4)
        self.change_y = random.uniform(-4, 4)
        self.alpha = 255

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.alpha > 10:
            self.alpha -= 10
        else:
            self.alpha = 0
            self.remove_from_sprite_lists()

class Enemy(arcade.Sprite):
    def __init__(self, x: float, y: float, level_map: List[str], col_idx: int, row_idx: int):
        super().__init__(":resources:images/enemies/slimeBlue.png", scale=0.25)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0

        h_space = 0
        for c in range(col_idx + 1, len(level_map[row_idx])):
            if level_map[row_idx][c] == 'W':
                break
            h_space += 1
        for c in range(col_idx - 1, -1, -1):
            if level_map[row_idx][c] == 'W':
                break
            h_space += 1

        v_space = 0
        for r in range(row_idx + 1, len(level_map)):
            if level_map[r][col_idx] == 'W':
                break
            v_space += 1
        for r in range(row_idx - 1, -1, -1):
            if level_map[r][col_idx] == 'W':
                break
            v_space += 1

        if h_space >= v_space:
            self.change_x = 2
        else:
            self.change_y = 2

class PlayerSprite(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 0.35
        self.timer = 0
        self.frame = 0

        self.idle_textures = [arcade.load_texture(":resources:images/animated_characters/female_person/femalePerson_idle.png")]
        self.walk_right_textures = []
        self.walk_left_textures = []
        self.walk_up_textures = []
        self.walk_down_textures = []

        for i in range(8):
            tex = arcade.load_texture(f":resources:images/animated_characters/female_person/femalePerson_walk{i}.png")
            self.walk_right_textures.append(tex)
            self.walk_left_textures.append(tex.flip_left_right())
            self.walk_up_textures.append(tex)
            self.walk_down_textures.append(tex)

        self.texture = self.idle_textures[0]

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.timer += 1
        if self.timer % 5 == 0:
            self.frame += 1

        if self.change_x > 0:
            self.texture = self.walk_right_textures[self.frame % 8]
        elif self.change_x < 0:
            self.texture = self.walk_left_textures[self.frame % 8]
        elif self.change_y > 0:
            self.texture = self.walk_up_textures[self.frame % 8]
        elif self.change_y < 0:
            self.texture = self.walk_down_textures[self.frame % 8]
        else:
            self.texture = self.idle_textures[0]

class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.title = arcade.Text("ПОБЕГ ИЗ ЛАБИРИНТА", 400, 400, arcade.color.WHITE, 40, anchor_x="center", font_name=("Arial", "sans-serif"))
        self.prompt = arcade.Text("Нажмите любую кнопку мыши, чтобы начать", 400, 300, arcade.color.LIGHT_GRAY, 20, anchor_x="center", font_name=("Arial", "sans-serif"))

    def on_show_view(self) -> None:
        self.window.background_color = arcade.color.MIDNIGHT_BLUE

    def on_draw(self) -> None:
        self.clear()
        self.title.draw()
        self.prompt.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class PauseView(arcade.View):
    def __init__(self, game_view: arcade.View):
        super().__init__()
        self.game_view = game_view
        self.title = arcade.Text("ПАУЗА", 400, 400, arcade.color.WHITE, 50, anchor_x="center", font_name=("Arial", "sans-serif"))
        self.prompt = arcade.Text("Отпустите ESC для продолжения", 400, 300, arcade.color.LIGHT_GRAY, 25, anchor_x="center", font_name=("Arial", "sans-serif"))
        self.hold_text = arcade.Text("", 400, 250, arcade.color.RED, 20, anchor_x="center", font_name=("Arial", "sans-serif"))
        self.esc_pressed = True
        self.esc_timer = 0.0

    def on_draw(self) -> None:
        self.clear()
        self.title.draw()
        self.prompt.draw()
        if self.esc_timer > 0:
            self.hold_text.text = f"Удержание для выхода: {int(self.esc_timer)}/10"
            self.hold_text.draw()

    def on_update(self, delta_time: float) -> None:
        if self.esc_pressed:
            self.esc_timer += delta_time
            if self.esc_timer >= 10.0:
                arcade.exit()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.ESCAPE:
            self.esc_pressed = True

    def on_key_release(self, key: int, modifiers: int) -> None:
        if key == arcade.key.ESCAPE:
            self.esc_pressed = False
            self.window.show_view(self.game_view)

class GameOverView(arcade.View):
    def __init__(self, score: int):
        super().__init__()
        self.score = score
        self.title = arcade.Text("ИГРА ОКОНЧЕНА", 400, 400, arcade.color.RED, 50, anchor_x="center", font_name=("Arial", "sans-serif"))
        self.score_text = arcade.Text(f"Счёт: {self.score}", 400, 300, arcade.color.WHITE, 30, anchor_x="center", font_name=("Arial", "sans-serif"))
        self.prompt = arcade.Text("Кликните для перезапуска", 400, 200, arcade.color.GRAY, 20, anchor_x="center", font_name=("Arial", "sans-serif"))

    def on_show_view(self) -> None:
        self.window.background_color = arcade.color.BLACK

    def on_draw(self) -> None:
        self.clear()
        self.title.draw()
        self.score_text.draw()
        self.prompt.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        view = GameView()
        view.setup()
        self.window.show_view(view)

class VictoryView(arcade.View):
    def __init__(self, score: int):
        super().__init__()
        self.score = score
        self.high_score = read_score()
        self.title = arcade.Text("ВЫ ПОБЕДИЛИ!", 400, 400, arcade.color.GREEN, 50, anchor_x="center", font_name=("Arial", "sans-serif"))
        self.score_text = arcade.Text(f"Счёт: {self.score}", 400, 300, arcade.color.WHITE, 30, anchor_x="center", font_name=("Arial", "sans-serif"))
        self.high_text = arcade.Text(f"Рекорд: {self.high_score}", 400, 250, arcade.color.YELLOW, 30, anchor_x="center", font_name=("Arial", "sans-serif"))
        self.prompt = arcade.Text("Кликните для новой игры", 400, 150, arcade.color.GRAY, 20, anchor_x="center", font_name=("Arial", "sans-serif"))

    def on_show_view(self) -> None:
        self.window.background_color = arcade.color.BLACK

    def on_draw(self) -> None:
        self.clear()
        self.title.draw()
        self.score_text.draw()
        self.high_text.draw()
        self.prompt.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        view = GameView()
        view.setup()
        self.window.show_view(view)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.camera_sprites = arcade.camera.Camera2D()
        self.camera_gui = arcade.camera.Camera2D()

        self.coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.win_sound = arcade.load_sound(":resources:sounds/upgrade1.wav")
        self.hurt_sound = arcade.load_sound(":resources:sounds/hurt2.wav")
        self.door_sound = arcade.load_sound(":resources:sounds/secret4.wav")
        self.key_sound = arcade.load_sound(":resources:sounds/coin5.wav")
        self.attack_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/explosion1.wav")

        self.hint1 = arcade.Text("ESC - Пауза", 10, 580, arcade.color.LIGHT_GRAY, 12, font_name=("Arial", "sans-serif"))
        self.hint2 = arcade.Text("Удерж. ESC (10с) - Выход", 10, 565, arcade.color.LIGHT_GRAY, 12, font_name=("Arial", "sans-serif"))
        self.hint3 = arcade.Text("Z - СТРЕЛЬБА", 10, 550, arcade.color.LIGHT_GRAY, 12, font_name=("Arial", "sans-serif"))
        self.hint4 = arcade.Text("", 10, 535, arcade.color.RED, 12, font_name=("Arial", "sans-serif"))

        self.score_text = arcade.Text("", 10, 480, arcade.color.WHITE, 16, font_name=("Arial", "sans-serif"))
        self.lives_text = arcade.Text("", 10, 455, arcade.color.WHITE, 16, font_name=("Arial", "sans-serif"))
        self.time_text = arcade.Text("", 10, 430, arcade.color.WHITE, 16, font_name=("Arial", "sans-serif"))
        self.level_text = arcade.Text("", 10, 405, arcade.color.WHITE, 16, font_name=("Arial", "sans-serif"))
        self.key_text = arcade.Text("", 10, 380, arcade.color.YELLOW, 16, font_name=("Arial", "sans-serif"))

    def setup(self) -> None:
        self.score = 0
        self.lives = 3
        self.current_level = 0
        self.setup_level()

    def setup_level(self) -> None:
        self.has_key = False
        self.time_left = 120.0
        self.esc_pressed = False
        self.esc_timer = 0.0

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.facing = 'R'
        self.attack_timer = 0.0

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.door_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.particle_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player = PlayerSprite()
        self.player_list.append(self.player)

        self.window.background_color = arcade.color.SPACE_CADET

        level_map = LEVELS[self.current_level]
        for row_index, row in enumerate(level_map):
            for col_index, char in enumerate(row):
                x = col_index * 64 + 32
                y = (len(level_map) - 1 - row_index) * 64 + 32

                if char == "W":
                    wall = arcade.Sprite(":resources:images/tiles/brickBrown.png", scale=0.5)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
                elif char == "P":
                    self.player.center_x = x
                    self.player.center_y = y
                elif char in ["B", "S", "G"]:
                    self.coin_list.append(Coin(x, y, char))
                elif char == "K":
                    self.key_list.append(Key(x, y))
                elif char == "D":
                    door = arcade.Sprite(":resources:images/tiles/lockYellow.png", scale=0.5)
                    door.center_x = x
                    door.center_y = y
                    self.wall_list.append(door)
                    self.door_list.append(door)
                elif char == "X":
                    self.enemy_list.append(Enemy(x, y, level_map, col_index, row_index))
                elif char == "E":
                    exit_sprite = arcade.Sprite(":resources:images/tiles/signExit.png", scale=0.5)
                    exit_sprite.center_x = x
                    exit_sprite.center_y = y
                    self.exit_list.append(exit_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)

    def die(self) -> None:
        arcade.play_sound(self.hurt_sound)
        self.lives -= 1
        if self.lives <= 0:
            write_score(self.score)
            self.window.show_view(GameOverView(self.score))
        else:
            self.setup_level()

    def on_draw(self) -> None:
        self.clear()
        
        self.camera_sprites.use()
        self.wall_list.draw()
        self.coin_list.draw()
        self.key_list.draw()
        self.exit_list.draw()
        self.enemy_list.draw()
        self.particle_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

        self.camera_gui.use()
        self.hint1.draw()
        self.hint2.draw()
        self.hint3.draw()

        if self.esc_timer > 0:
            self.hint4.text = f"Выход через: {10 - int(self.esc_timer)}с"
            self.hint4.draw()

        self.score_text.text = f"Счёт: {self.score}"
        self.lives_text.text = f"Жизни: {self.lives}"
        self.time_text.text = f"Время: {int(self.time_left)}"
        self.level_text.text = f"Уровень: {self.current_level + 1}"
        self.key_text.text = "Ключ: Найден!" if self.has_key else ""
        
        self.score_text.draw()
        self.lives_text.draw()
        self.time_text.draw()
        self.level_text.draw()
        self.key_text.draw()

    def on_update(self, delta_time: float) -> None:
        if self.esc_pressed:
            self.esc_timer += delta_time
            if self.esc_timer >= 10.0:
                arcade.exit()

        self.time_left -= delta_time
        if self.time_left <= 0:
            self.die()
            return

        self.player.change_x = 0
        self.player.change_y = 0

        if self.up_pressed:
            self.player.change_y = 5
            self.facing = 'U'
        if self.down_pressed:
            self.player.change_y = -5
            self.facing = 'D'
        if self.left_pressed:
            self.player.change_x = -5
            self.facing = 'L'
        if self.right_pressed:
            self.player.change_x = 5
            self.facing = 'R'

        if self.attack_timer > 0:
            self.attack_timer -= delta_time

        self.physics_engine.update()
        self.player.update_animation(delta_time)
        self.coin_list.update(delta_time)
        self.key_list.update(delta_time)
        self.particle_list.update(delta_time)
        self.bullet_list.update()

        for bullet in self.bullet_list:
            if arcade.check_for_collision_with_list(bullet, self.wall_list):
                bullet.remove_from_sprite_lists()
                continue
            
            hit_enemies = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hit_enemies:
                arcade.play_sound(self.hit_sound)
                for enemy in hit_enemies:
                    self.score += 150
                    for _ in range(15):
                        self.particle_list.append(ParticleSprite(enemy.center_x, enemy.center_y))
                    enemy.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()

        for enemy in self.enemy_list:
            enemy.center_x += enemy.change_x
            enemy.center_y += enemy.change_y
            if arcade.check_for_collision_with_list(enemy, self.wall_list):
                enemy.center_x -= enemy.change_x
                enemy.center_y -= enemy.change_y
                enemy.change_x *= -1
                enemy.change_y *= -1

        if arcade.check_for_collision_with_list(self.player, self.enemy_list):
            self.die()
            return

        hit_keys = arcade.check_for_collision_with_list(self.player, self.key_list)
        for key in hit_keys:
            arcade.play_sound(self.key_sound)
            self.has_key = True
            key.remove_from_sprite_lists()
            
            if len(self.door_list) > 0:
                arcade.play_sound(self.door_sound)
                for door in self.door_list:
                    door.remove_from_sprite_lists()
                self.door_list.clear()

        hit_coins = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in hit_coins:
            arcade.play_sound(self.coin_sound)
            self.score += coin.value
            for _ in range(12):
                self.particle_list.append(ParticleSprite(coin.center_x, coin.center_y))
            coin.remove_from_sprite_lists()

        hit_exits = arcade.check_for_collision_with_list(self.player, self.exit_list)
        if len(hit_exits) > 0:
            arcade.play_sound(self.win_sound)
            self.current_level += 1
            if self.current_level >= len(LEVELS):
                write_score(self.score)
                self.window.show_view(VictoryView(self.score))
            else:
                self.setup_level()

        self.camera_sprites.position = (self.player.center_x, self.player.center_y)

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.Z:
            if self.attack_timer <= 0:
                arcade.play_sound(self.attack_sound)
                bullet = Bullet(self.player.center_x, self.player.center_y, self.facing)
                self.bullet_list.append(bullet)
                self.attack_timer = 0.5
        elif key == arcade.key.ESCAPE:
            self.esc_pressed = True

    def on_key_release(self, key: int, modifiers: int) -> None:
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.ESCAPE:
            self.esc_pressed = False
            if self.esc_timer < 10.0:
                self.window.show_view(PauseView(self))
            self.esc_timer = 0.0

def main():
    window = arcade.Window(800, 600, "Побег из лабиринта")
    window.show_view(StartView())
    arcade.run()

if __name__ == "__main__":
    main()
