import fileinput

from typing import Dict


def refresh_settings(settings_location, key_value_to_replace: Dict[str, str]):
    for line in fileinput.input(settings_location, inplace=True):
        replaced = False
        for key_to_be_found in key_value_to_replace:
            if line.startswith(key_to_be_found):
                value = key_value_to_replace[key_to_be_found]
                replaced = True
                print(f"""{key_to_be_found}={value}\n""", end="")
                break
        if not replaced:
            print(line, end="")
