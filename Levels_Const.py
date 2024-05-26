import pygame
import Others.readingtext as reader

WIDTH, HEIGHT = 1200, 700

ENEMY_SPEED = 3

class Level1:
    def __init__(self):
        self.data = reader.read_data(1)

        self.platforms = self.get_platforms()
        self.enemies_pos = self.get_enemies()
        self.player_pos = self.get_player()

    def get_platforms(self):
        temp = []

        for rect in self.data[0]:
            temp.append(pygame.Rect(rect[0], rect[1]))

        return temp

    def get_enemies(self):
        temp = []

        for enemy in self.data[1]:
            temp.append((enemy))

        return temp

    def get_player(self):
        return self.data[2]

class Level2:
    def __init__(self):
        self.data = reader.read_data(2)

        self.platforms = self.get_platforms()
        self.enemies_pos = self.get_enemies()
        self.player_pos = self.get_player()

    def get_platforms(self):
        temp = []

        for rect in self.data[0]:
            temp.append(pygame.Rect(rect[0], rect[1]))

        return temp

    def get_enemies(self):
        temp = []

        for enemy in self.data[1]:
            temp.append((enemy))

        return temp

    def get_player(self):
        return self.data[2]

class Level3:
    def __init__(self):
        self.data = reader.read_data(3)

        self.platforms = self.get_platforms()
        self.enemies_pos = self.get_enemies()
        self.player_pos = self.get_player()

    def get_platforms(self):
        temp = []

        for rect in self.data[0]:
            temp.append(pygame.Rect(rect[0], rect[1]))

        return temp

    def get_enemies(self):
        temp = []

        for enemy in self.data[1]:
            temp.append((enemy))

        return temp

    def get_player(self):
        return self.data[2]

class Level4:
    def __init__(self):
        self.data = reader.read_data(4)

        self.platforms = self.get_platforms()
        self.enemies_pos = self.get_enemies()
        self.player_pos = self.get_player()

    def get_platforms(self):
        temp = []

        for rect in self.data[0]:
            temp.append(pygame.Rect(rect[0], rect[1]))

        return temp

    def get_enemies(self):
        temp = []

        for enemy in self.data[1]:
            temp.append((enemy))

        return temp

    def get_player(self):
        return self.data[2]

a = Level2()