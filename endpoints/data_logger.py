from gameplay.enums import ActionCost
import csv


class DataLogger(object):
    def __init__(self):
        self.player_data = {'skip': [],
                            'squish': [],
                            'scram': [],
                            'save': [],
                            'capacity': [],
                            'suggest': [],
                            'act': [],
                            'info': [],
                            'paramedic': [],
                            'protector': [],
                            'filter_count': []}
        self.action_number = 1

    def add_data(self, action_type, capacity, chose_suggest, suggested_action, chose_info, state, paramedic, protector, filter_count):
        if action_type is ActionCost:
            self.player_data["act"].append(1)
        else:
            self.player_data["act"].append(0)
        if action_type == ActionCost.SKIP:
            self.player_data["skip"].append(1)
        else:
            self.player_data["skip"].append(0)
        if action_type == ActionCost.SAVE:
            self.player_data["save"].append(1)
        else:
            self.player_data["save"].append(0)
        if action_type == ActionCost.SQUISH:
            self.player_data["squish"].append(1)
        else:
            self.player_data["squish"].append(0)
        if action_type == ActionCost.SCRAM:
            self.player_data["scram"].append(1)
        else:
            self.player_data["scram"].append(0)
        self.player_data["capacity"].append(capacity)

        if chose_suggest:
            self.player_data["suggest"].append(f"1, {suggested_action}")
        else:
            self.player_data["suggest"].append(f"0, {suggested_action}")
        if chose_info:
            self.player_data["info"].append(f"1, {state}")
        else:
            self.player_data["info"].append(f"0, {state}")
        if paramedic:
            self.player_data["paramedic"].append(1)
        else:
            self.player_data["paramedic"].append(0)
        if protector:
            self.player_data["protector"].append(1)
        else:
            self.player_data["protector"].append(0)
        self.player_data["filter_count"].append(filter_count)
        self.action_number += 1

    def save_player_data_to_csv(self, file_name):
        with open(file_name, mode='w', newline='') as file:
            max_actions = max(len(choices) for choices in self.player_data.values())

            fieldnames = ['Action'] + [f'Action {i}' for i in range(1, max_actions + 1)]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for action_name in self.player_data.keys():
                row_data = {'Action': action_name}

                choices = self.player_data[action_name]
                for i in range(len(choices)):
                    row_data[f'Action {i + 1}'] = choices[i]

                writer.writerow(row_data)
