def string_to_tuple(line):
    num1 = ""
    num2 = ""
    num3 = ""
    chars = 0
    ended = True
    i = 1
    if len(line) == 0:
        return ()
    if line[0] == "(":
        chars = line[i]
        while chars != ",":
            num1 = num1 + chars
            i += 1
            chars = line[i]
        
        i += 2
        chars = line[i]
        while chars != ")":
            if chars == ",":
                ended = False
                break
            num2 = num2 + chars
            i += 1
            chars = line[i]
        
        if ended:
            return (int(num1), int(num2))

        i += 2
        chars = line[i]
        while chars != ")":
            num3 = num3 + chars
            i += 1
            chars = line[i]

        return (int(num1), int(num2), int(num3))
    else:
        return ""

def read_data(level):
    with open(f"Levels/level{level}.txt", 'r') as level:
        level = level.readlines()
        i = 0

        reading_platforms = False
        platform_line = ""
        platforms_coords = []
        temp_platforms_coords = []

        reading_enemies = False
        enemy_line = ""
        enemies_coords = []
        temp_enemy_coords = ()

        reading_player = False
        player_line = ""
        player_coords = ()
        temp_player_coords = ()

        while i <= len(level) - 1:
            line = level[i].strip()

            if line == "":
                i += 1
                line = level[i].strip()

            if line == "//Platforms":
                i += 1
                reading_platforms = True
                reading_enemies = False
                reading_player = False
            elif line == "//Enemies":
                i += 1
                reading_platforms = False
                reading_enemies = True
                reading_player = False
            elif line == "//Player":
                i += 1
                reading_platforms = False
                reading_enemies = False
                reading_player = True
                
            if reading_platforms:
                i += 1
                platform_line = level[i].strip()
                while platform_line != "]":
                    temp_platforms_coords.append(string_to_tuple(platform_line))
                    i += 1
                    platform_line = level[i].strip()

                platforms_coords.append(temp_platforms_coords)
                temp_platforms_coords = []

            elif reading_enemies:
                i += 1
                enemy_line = level[i].strip()
                while enemy_line != "]":
                    temp_enemy_coords = string_to_tuple(enemy_line)
                    i += 1
                    enemy_line = level[i].strip()

                if temp_enemy_coords != ():
                    enemies_coords.append(temp_enemy_coords)
                temp_enemy_coords = ()

            elif reading_player:
                i += 1
                player_line = level[i].strip()
                while player_line != "]":
                    temp_player_coords = string_to_tuple(player_line)
                    i += 1
                    player_line = level[i].strip()

                if temp_player_coords != ():
                    player_coords = temp_player_coords
                temp_player_coords = ()
                
            i += 1

    return platforms_coords, enemies_coords, player_coords

print(read_data(4))