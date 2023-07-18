import os
import time
import codecs
from datetime import datetime
from colorama import init, Fore, Back

init()

class CombatLogAnalyzer:
    def __init__(self):
        self.color_map = {
            '250': Back.RED, #Blood (Death Knight)',
            '251': Back.RED, #Frost (Death Knight)',
            '252': Back.RED, #Unholy (Death Knight)',
            '577': Back.MAGENTA, #Havoc (Demon Hunter)',
            '581': Back.MAGENTA, #Vengeance (Demon Hunter)',
            '102': Back.YELLOW, #Balance (Druid)',
            '103': Back.YELLOW, #Feral (Druid)',
            '104': Back.YELLOW, #Guardian (Druid)',
            '105': Back.YELLOW, #Restoration (Druid)',
            '1467': Back.GREEN, #Devastation (Evoker)',
            '1468': Back.GREEN, #Preservation (Evoker)',
            '1473': Back.GREEN, #Augmentation (Evoker)',
            '253': Back.LIGHTGREEN_EX, #Beast Mastery (Hunter)',
            '254': Back.LIGHTGREEN_EX, #Marksmanship (Hunter)',
            '255': Back.LIGHTGREEN_EX, #Survival (Hunter)',
            '62': Back.BLUE, #Arcane (Mage)',
            '63': Back.BLUE, #Fire (Mage)',
            '64': Back.BLUE, #Frost (Mage)',
            '268': Back.GREEN, #Brewmaster (Monk)',
            '270': Back.GREEN, #Mistweaver (Monk)',
            '269': Back.GREEN, #Windwalker (Monk)',
            '65': Back.MAGENTA, #Holy (Paladin)',
            '66': Back.MAGENTA, #Protection (Paladin)',
            '70': Back.MAGENTA, #Retribution (Paladin)',
            '256': Back.WHITE, #Discipline (Priest)',
            '257': Back.WHITE, #Holy (Priest)',
            '258': Back.WHITE, #Shadow (Priest)',
            '259': Back.YELLOW, #Assassination (Rogue)',
            '260': Back.YELLOW, #Outlaw (Rogue)',
            '261': Back.YELLOW, #Subtlety (Rogue)',
            '262': Back.BLUE, #Elemental (Shaman)',
            '263': Back.BLUE, #Enhancement (Shaman)',
            '264': Back.BLUE, #Restoration (Shaman)',
            '265': Back.MAGENTA, #Affliction (Warlock)',
            '266': Back.MAGENTA, #Demonology (Warlock)',
            '267': Back.MAGENTA, #Destruction (Warlock)',
            '71': Back.LIGHTWHITE_EX, #Arms (Warrior)',
            '72': Back.LIGHTWHITE_EX, #Fury (Warrior)',
            '73': Back.LIGHTWHITE_EX, #Protection (Warrior)'
        }
        self.newest_file = None
        self.line_count = 0
        self.player_data = {}
        self.start_timestamp = None
        self.end_timestamp = None

    def get_file_size(self, file_path):
        try:
            size = os.path.getsize(file_path)
            return size
        except OSError:
            return -1

    def find_newest_file(self):
        newest_file = None
        newest_timestamp = 0

        for filename in os.listdir('.'):
            if "WoWCombatLog" in filename:
                file_timestamp = os.path.getmtime(filename)
                if file_timestamp > newest_timestamp:
                    newest_file = filename
                    newest_timestamp = file_timestamp

        return newest_file

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def process_log_file(self, filename):
        with codecs.open(filename, "r", encoding="utf-8") as file:
            for line in file:
                self.process_log_entry(line)

    def process_log_entry(self, line):
        if "COMBATANT_INFO" in line:
            columns = line.split(",")
            spec_id = columns[24]
            player_id = columns[1].strip('"')
            if player_id not in self.player_data:
                self.player_data[player_id] = {"spec_id": spec_id, "damage": 0, "name": "", "spells": {}}
        elif "SPELL_DAMAGE_SUPPORT" in line or "SPELL_PERIODIC_DAMAGE_SUPPORT" in line:
            columns = line.split(",")
            if "Player" not in columns[1]:
                return
            current_player_id = columns[39].strip('"\r\n')
            player_id = columns[1].strip('"')
            damage_value = float(columns[29])
            if current_player_id in self.player_data:
                self.player_data[current_player_id]["damage"] += damage_value

            if player_id in self.player_data:
                self.player_data[player_id]["damage"] = self.player_data[player_id]["damage"] - damage_value
        elif "SWING_DAMAGE" in line or "RANGE_DAMAGE" in line:
            columns = line.split(",")
            player_id = columns[1].strip('"')
            if "Player" not in columns[1]:
                return
            damage_value = float(columns[25])
            if float(columns[25]) > 0:
                damage_value - float(columns[27])
            if player_id in self.player_data:
                self.player_data[player_id]["damage"] += damage_value
        elif "SPELL_DAMAGE" in line:
            columns = line.split(",")
            timestamp = columns[0].strip('  SPELL_DAMAGE')
            player_id = columns[1].strip('"')
            if "Player" not in columns[1]:
                return
            damage_value = float(columns[29])
            if float(columns[31]) > 0:
                damage_value - float(columns[31])

            spell_name = columns[10].strip('"')
            spell_dict = {}
            spell_dict[spell_name] = damage_value

            if player_id in self.player_data:
                self.player_data[player_id]["damage"] += damage_value
                if "spells" in self.player_data[player_id]:
                    if spell_name in self.player_data[player_id]["spells"]:
                        self.player_data[player_id]["spells"][spell_name] += damage_value
                    else:
                        self.player_data[player_id]["spells"][spell_name] = damage_value
                else:
                    self.player_data[player_id]["spells"] = spell_dict

            if self.start_timestamp is None:
                self.start_timestamp = datetime.strptime(timestamp, "%m/%d %H:%M:%S.%f")
            self.end_timestamp = datetime.strptime(timestamp, "%m/%d %H:%M:%S.%f")

            if player_id in self.player_data and self.player_data[player_id]["name"] == "":
                player_name = columns[2].strip('"')
                self.player_data[player_id].update({"name": player_name})
        elif "SPELL_PERIODIC_DAMAGE" in line:
            columns = line.split(",")
            player_id = columns[1].strip('"')

            if "Player" not in columns[1]:
                return
            damage_value = float(columns[29])

            if player_id in self.player_data:
                self.player_data[player_id]["damage"] += damage_value

    def print_player_stats(self, verbose=None):
        sorted_data = sorted(self.player_data.items(), key=lambda x: x[1]["damage"], reverse=True)
        max_value = sorted_data[0][1]["damage"]
        time_diff = (self.end_timestamp - self.start_timestamp).total_seconds()
        max_name_length = max(len(data["name"]) for _, data in sorted_data)

        if verbose:
            for player_id, (accumulated_value, player_name, spell_dict) in sorted_data:
                print("Player ID:", player_id)
                print("Player Name:", player_name)
                print("Accumulated Value (in hundreds of millions):", accumulated_value / 1000000)
                print("DPS:", accumulated_value / time_diff)
                print("---")

        self.clear_screen()
        for player_id, data in sorted_data:
            accumulated_value = data["damage"]
            player_name = data["name"]
            percentage = accumulated_value / max_value * 100
            bar_length = int(percentage / 5)
            alignment_space = max_name_length - len(player_name)
            color = self.color_map.get(data["spec_id"], Back.RESET)
            bar = color + " " * bar_length + Fore.RESET + Back.RESET
            print(f"{player_name}{' ' * alignment_space}: {bar} {accumulated_value / 1000000:.2f}M, {accumulated_value / time_diff / 1000:.2f}K DPS")

    def run(self):
        while True:
            if self.find_newest_file() != self.newest_file:
                self.newest_file = self.find_newest_file()
            if not self.newest_file:
                time.sleep(5)
            if self.line_count > 0 and self.get_file_size(self.newest_file) == self.line_count:
                time.sleep(5)
                continue
            else:
                self.line_count = self.get_file_size(self.newest_file)
            self.player_data = {}
            self.start_timestamp = None
            self.end_timestamp = None
            self.process_log_file(self.newest_file)
            self.print_player_stats()
            time.sleep(5)

analyzer = CombatLogAnalyzer()
analyzer.run()
