#!/bin/python3

BASE_DESKTOP_PATH = "/usr/share/applications/"
PATCHES = {
    "org.qbittorrent.qBittorrent.desktop": {
        "match": "Exec=qbittorrent %U",
        "replacement": "Exec=env XDG_CURRENT_DESKTOP=gnome qbittorrent %U"
    },
    "org.telegram.desktop.desktop": {
        "match": "Exec=telegram-desktop -- %u",
        "replacement": "Exec=env XDG_CURRENT_DESKTOP=gnome telegram-desktop -- %u"
    }
}

for key in PATCHES:
    file_path = BASE_DESKTOP_PATH + key
    content: str
    with open(file_path, "r") as open_file:
        content = open_file.read()
        current_patch = PATCHES.get(key)
        content = content.replace(current_patch["match"], current_patch["replacement"])
    
    try:
        with open(file_path, "w") as open_file: open_file.write(content)
        print("Added for file", key)
    except PermissionError:
        print("You don't have permission to write to that folder! try running as root")
        exit(1)
    except Exception as e:
        print("Exception happened !", e)
