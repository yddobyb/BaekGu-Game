import random
import time
from helpers import is_alive, display_stats, display_skills, display_inventory, get_item_choice, lose_heart
import warnings

warnings.filterwarnings("ignore")


def show_current_hp(hp, original_hp, name):
    if hp <= 0:
        hp = 0
        print(f'*** 🩸 {name} HP: {hp}/{original_hp} ***\n')
        return True
    else:
        print(f'*** 🩸 {name} HP: {hp}/{original_hp} ***\n')
        return False


def display_attack_description(enemy_name):
    """
    Display a randomly chosen attack description, customized for the given enemy.

    Replace the placeholder "enemy" in the sentence with the provided enemy name.

    :param enemy_name: enemy's name as a string
    :precondition: enemy_name must be a string representing the name of enemy being attacked
    :postcondition: print one of the descriptions with "enemy" replaced by the given name
    """
    attack_descriptions = [
        "🗡️ You strike fiercely, leaving a mark on the enemy!",
        "🗡️ Your attack lands cleanly, leaving the enemy struggling to recover!",
        "🗡️ With a focused attack, you manage to break through the enemy's guard, causing visible pain!",
        "🗡️ Your powerful attack stunned the enemy.",
        "🗡️ Your strike pierced through the enemy with precision."
    ]
    print(random.choice(attack_descriptions).replace("enemy", enemy_name))


def configure_enemy_stat():
    # Configure enemies
    # HP, Attack damage, Skill damage random
    level = ["Level 1", "Level 2", "Level 3", "Level 4", "Boss"]
    hp_range = [(80, 100), (101, 200), (201, 300), (301, 400), (500, 600)]
    attack_dmg = [(5, 10), (15, 30), (35, 50), (60, 90), (100, 250)]
    skill_dmg = [(10, 25), (26, 45), (46, 70), (75, 100), (130, 250)]

    # return {
    #     "HP Range": {
    #         "Level 1": (80, 100),
    #         "Level 2": (101, 200),
    #         "Level 3": (201, 300),
    #         "Level 4": (301, 400),
    #         "Boss": (500, 600)
    #     },
    #     "Basic Attack": {
    #         "Level 1": (5, 10),
    #         "Level 2": (15, 30),
    #         "Level 3": (35, 50),
    #         "Level 4": (60, 90),
    #         "Boss": (100, 300)
    #     },
    #     "Skill Damage": {
    #         "Level 1": (10, 25),
    #         "Level 2": (26, 45),
    #         "Level 3": (46, 70),
    #         "Level 4": (75, 100),
    #         "Boss": (130, 300)
    #     }
    # }
    return {"HP Range": {level: hp_range for level, hp_range in zip(level, hp_range)},
            "Basic Attack": {level: damage_range for level, damage_range in zip(level, attack_dmg)},
            "Skill Damage": {level: damage_range for level, damage_range in zip(level, skill_dmg)}}


def make_enemies(name, icon, description, level, hp_range, basic_attack, skill_damage, skill_name):
    return {
        "Name": name,
        "Icon": icon,
        "Description": description,
        "Level": level,
        "HP": random.randint(*hp_range),
        "Attack":
            {
                f"{skill_name}": random.randint(*skill_damage),
                "Basic Attack": random.randint(*basic_attack)
            }
    }


def choose_enemy_based_on_level(character, enemy_stat, boss_fight):
    # Create enemies
    enemies = []
    if character["Stat"]["Level"] == 1:
        # Low Level Mobs (Underground)
        mouse = make_enemies('Mouse',
                             '🐭',
                             "A tiny mouse nibbling on a piece of cheese. It looks harmless, "
                             "but don't let your guard down!",
                             '1',
                             enemy_stat["HP Range"]["Level 1"],
                             enemy_stat["Basic Attack"]["Level 1"],
                             enemy_stat["Skill Damage"]["Level 1"],
                             'Nibble'
                             )
        spider = make_enemies('Spider',
                              '🕷️',
                              'Moving slowly in the shadows with its sticky webs.',
                              '2',
                              enemy_stat["HP Range"]["Level 2"],
                              enemy_stat["Basic Attack"]["Level 2"],
                              enemy_stat["Skill Damage"]["Level 2"],
                              'Web Trap')

        enemies = [mouse, spider]
    elif character["Stat"]["Level"] == 2:
        # Mid-Level Mobs (Ground Level)
        robotic_vacuum = make_enemies('Robotic Vacuum',
                                      '🤖',
                                      'Going zoom zoom, sucking up everything in its path.',
                                      '2',
                                      enemy_stat["HP Range"]["Level 2"],
                                      enemy_stat["Basic Attack"]["Level 2"],
                                      enemy_stat["Skill Damage"]["Level 2"],
                                      'Suction')
        guard_cat = make_enemies('Guard Cat',
                                 '🐱',
                                 'A fierce feline guarding the living room.',
                                 '3',
                                 enemy_stat["HP Range"]["Level 3"],
                                 enemy_stat["Basic Attack"]["Level 3"],
                                 enemy_stat["Skill Damage"]["Level 3"],
                                 'Hiss')

        enemies = [robotic_vacuum, guard_cat]
    elif boss_fight:
        boss = make_enemies('Majestic Fluffy BunBun',
                            '🐰',
                            'An old and tattered bunny plushie, once loved but now abandoned in the attic. '
                            'Majestic Fluffy BunBun believes he is the noble protector of all the forgotten treasures '
                            'here.',
                            '10',
                            enemy_stat["HP Range"]["Boss"],
                            enemy_stat["Basic Attack"]["Boss"],
                            enemy_stat["Skill Damage"]["Boss"],
                            'Cuddle Crush')
        enemies = [boss]
    elif character["Stat"]["Level"] == 3 and not boss_fight:
        # High Level Mobs (Upper Level - Attic)
        giant_moth = make_enemies('Giant Moth',
                                  '🪰',
                                  'Every time it flaps its wings, dust comes off.',
                                  '3',
                                  enemy_stat["HP Range"]["Level 3"],
                                  enemy_stat["Basic Attack"]["Level 3"],
                                  enemy_stat["Skill Damage"]["Level 3"],
                                  'Wing Flap')
        ghost = make_enemies('Ghost',
                             '👻',
                             'A forgotten spirit, floating around silently.',
                             '4',
                             enemy_stat["HP Range"]["Level 4"],
                             enemy_stat["Basic Attack"]["Level 4"],
                             enemy_stat["Skill Damage"]["Level 4"],
                             'Chill Touch')
        enemies = [giant_moth, ghost]
    enemy = random.choice(enemies)
    return enemy, enemy.copy()


def display_skill_uses(current_skill_usage, skill_usage_limit):
    skill_used = "🔳"
    skill_not_used = "⬜️"
    print(f"SKILL USES LEFT: {skill_used * current_skill_usage}{skill_not_used * skill_usage_limit}")


def display_enemy_info(enemy):
    """
    Display information about the enemy being encountered.
    
    :param enemy: a well-formed enemy dictionary
    :precondition: enemy must be a dictionary with "Name", "Icon", "Level", "Description", "HP", and "Attack" keys
    :postcondition: print the enemy's name, icon, level, description, and current HP information
    
    >>> enemy_dict = {'Name': 'Mouse', 'Icon': '🐭',
    ... 'Description': "A tiny mouse nibbling on a piece of cheese. It looks harmless, but don't let your guard down!",
    ... 'Level': '1', 'HP': 90, 'Attack': {'Nibble': 13, 'Basic Attack': 8}}
    >>> display_enemy_info(enemy_dict)
    ------------------------------------------------------
    ‼️‼️ ENEMY ENCOUNTERED ‼️‼️
    ------------------------------------------------------
    🐭 Mouse
    A tiny mouse nibbling on a piece of cheese. It looks harmless, but don't let your guard down!
    Level: 1
    HP: 90/90
    ------------------------------------------------------
    <BLANKLINE>
    >>> enemy_dict = {'Name': 'Ghost', 'Icon': '👻', 'Description': 'A forgotten spirit, floating around silently.',
    ... 'Level': '4', 'HP': 369, 'Attack': {'Chill Touch': 99, 'Basic Attack': 72}}
    >>> display_enemy_info(enemy_dict)
    ------------------------------------------------------
    ‼️‼️ ENEMY ENCOUNTERED ‼️‼️
    ------------------------------------------------------
    👻 Ghost
    A forgotten spirit, floating around silently.
    Level: 4
    HP: 369/369
    ------------------------------------------------------
    <BLANKLINE>
    """
    print("------------------------------------------------------\n"
          "‼️‼️ ENEMY ENCOUNTERED ‼️‼️\n"
          "------------------------------------------------------\n"
          f"{enemy['Icon']} {enemy['Name']}\n"
          f"{enemy['Description']}\n"
          f"Level: {enemy['Level']}\n"
          f"HP: {enemy['HP']}/{enemy['HP']}\n"
          "------------------------------------------------------\n")


def battle(character, boss_fight=False):
    """
    Drive the battle.
    """
    enemy_stat = configure_enemy_stat()
    enemy, enemy_copy = choose_enemy_based_on_level(character, enemy_stat, boss_fight)

    # Display enemy information
    display_enemy_info(enemy)

    # Get user choice
    # Skill usage
    total_skill_use, skill_usage_limit, current_skill_usage = 5, 5, 0
    in_battle, has_won = True, False

    while is_alive(character) and enemy_copy["HP"] > 0 and in_battle:
        # options = ['Attack', 'Skill', 'Flee', 'Stats', 'Inventory']
        while not has_won:
            user_choice = input(
                "What is your next move?\n"
                "--------------------------------------------------------\n"
                " 1: 🗡️  Attack     - Attack with basic attack\n"
                " 2: ✨  Skill      - Use a special skill\n"
                " 3: 🐕  Flee       - Run away from the battle (Heart -1)\n"
                " 4: 📊  Stats      - View your current condition\n"
                " 5: 🎒  Inventory  - Use an item from your inventory\n"
                "--------------------------------------------------------\n"
                "Enter the number of your choice: "
            ).strip().lower()
            if user_choice == "1":
                display_attack_description(enemy["Name"])
                enemy_copy['HP'] -= character["Skill"]['Basic Attack']
                victory_check = show_current_hp(enemy_copy['HP'], enemy['HP'], enemy_copy['Name'])
                if victory_check:
                    has_won = True
                    break
            elif user_choice == "2":
                if skill_usage_limit > 0:
                    while True:
                        print(f"In each battle, you are allowed a total of {total_skill_use} skill uses.")
                        display_skill_uses(current_skill_usage, skill_usage_limit)
                        display_skills(character)
                        skill_choice = input("Choose skill you would like to use:").strip()

                        display_attack_description(enemy["Name"])
                        try:
                            selected_skill_damage = character['Skill']['Current Skills'][skill_choice.title()]
                        except KeyError:
                            print("❌ Invalid skill. Please enter a valid skill from the list above.\n")
                            continue
                        else:
                            enemy_copy['HP'] -= selected_skill_damage['Damage']
                            victory_check = show_current_hp(enemy_copy['HP'], enemy['HP'], enemy_copy['Name'])
                            if victory_check:
                                has_won = True
                                break
                            skill_usage_limit -= 1
                            current_skill_usage += 1
                            break
                else:
                    print("❌ You can't use skill anymore as you ran out of uses already.")
                    display_skill_uses(current_skill_usage, skill_usage_limit)
                    continue
            elif user_choice == "3":
                print(f"{enemy["Name"]} seems to be too strong for me.. Let me retreat before it's too late!")
                lose_heart(character)
                in_battle = False
                break
            elif user_choice == "4":
                display_stats(character)
                continue
            elif user_choice == "5":
                display_inventory(character)
                do_break = get_item_choice(character)
                if do_break:
                    break
            else:
                print("❌ Invalid input. Please enter a valid choice (1-5).\n")
                continue

            if enemy_copy["HP"] > 0:
                time.sleep(1.5)
                enemy_skill = random.choice(list(enemy_copy['Attack'].items()))
                character["Stat"]["Current HP"] -= enemy_skill[1]
                print(f"😣 Ouch! {enemy["Name"]} fought back!")
                print(f"{enemy["Name"]} used {enemy_skill[0]} on you!")
                victory_check = show_current_hp(character["Stat"]["Current HP"], character['Stat']['HP'], 'Your')
                if victory_check:
                    in_battle = False
                    break
    if character['Stat']['Current HP'] <= 0:
        print("I collapsed on the floor. The enemy stands victorious as my vision fades to darkness...")
        lose_heart(character)
        has_won = False
    elif has_won and not boss_fight:
        print("🎉 Woo hoo! You won against a ruff battle. Time for a treat! 🎉")
    return character, has_won


def main():
    character = {'Stat': {'Level': 3, 'Heart': 5, 'Current HP': 500, 'HP': 500}}
    battle(character)


if __name__ == '__main__':
    main()
