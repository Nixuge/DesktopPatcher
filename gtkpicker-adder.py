#!/bin/python3

# Not made to be written perfectly, but compact & in 1 file

import argparse
from dataclasses import dataclass

@dataclass
class Patch:
    file_name: str
    match: str
    replacement: str
    folder_path: str = "/usr/share/applications/"

    def print_add(self) -> None:
        if not args.noprint:
            print(f"Added for file {self.file_name}")


patches: list[Patch] = [
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

# random functions
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-np", "--noprint", required=False, action="store_true", help="Disables prints (except error prints)")
    return parser.parse_args()

args = get_args()


if __name__ == "__main__":
    for patch in patches:
        # read the file content
        full_path = patch.folder_path + patch.file_name

        with open(full_path, "r") as open_file:
            old_content = open_file.read()
        
        # patch & see if its different
        patched_content = old_content.replace(patch.match, patch.replacement)

        if patched_content == old_content:
            continue
        
        # if it is, try to write it back
        try:
            with open(full_path, "w") as open_file: 
                open_file.write(patched_content)
            patch.print_add()
        
        except PermissionError:
            print("You don't have permission to write to that folder! try running as root")
            exit(1)
        
        except Exception as e:
            print("Exception happened !", e)
            exit(2)