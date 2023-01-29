#!/bin/python3

import argparse
from dataclasses import dataclass

@dataclass
class Patch:
    file_name: str
    match: str
    replacement: str
    folder_path: str = "/usr/share/applications/"

patches = [
    Patch(
        "org.qbittorrent.qBittorrent.desktop", 
        "Exec=qbittorrent %U", 
        "Exec=env XDG_CURRENT_DESKTOP=gnome qbittorrent %U"
    ),
    Patch(
        "org.telegram.desktop.desktop",
        "Exec=/usr/bin/telegram-desktop -- %u",
        "Exec=env XDG_CURRENT_DESKTOP=gnome /usr/bin/telegram-desktop -- %u"
    ),
    Patch(
        "onlyoffice-desktopeditors.desktop",
        "Exec=/usr/bin/onlyoffice-desktopeditors %U",
        "Exec=env XDG_CURRENT_DESKTOP=gnome /usr/bin/onlyoffice-desktopeditors %U"
    )
]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-np", "--noprint", required=False, action="store_true", help="Disables prints (except error prints)")
    return parser.parse_args()

args = get_args()

def print_valid(text: str):
    if not args.noprint:
        print(text)

if __name__ == "__main__":
    print("TODO")




for key in PATCHES:
    file_path = BASE_DESKTOP_PATH + key
    content: str
    with open(file_path, "r") as open_file:
        content = open_file.read()
        current_patch = PATCHES.get(key)
        content = content.replace(current_patch["match"], current_patch["replacement"])

    try:
        with open(file_path, "w") as open_file: open_file.write(content)
        print_valid("Added for file " + key)
    except PermissionError:
        print("You don't have permission to write to that folder! try running as root")
        exit(1)
    except Exception as e:
        print("Exception happened !", e)
