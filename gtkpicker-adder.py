#!/bin/python3

# Not made to be written perfectly, but compact & in 1 file

import argparse
from dataclasses import dataclass

@dataclass
class Patch:
    patch_type: str
    file_name: str
    match: str
    replacement: str
    folder_path: str = "/usr/share/applications/"

patches: list[Patch] = [
    Patch(
        "gtkpicker",
        "org.qbittorrent.qBittorrent.desktop", 
        "Exec=qbittorrent %U", 
        "Exec=env XDG_CURRENT_DESKTOP=gnome qbittorrent %U"
    ),
    Patch(
        "gtkpicker",
        "org.telegram.desktop.desktop",
        "Exec=telegram-desktop -- %u",
        "Exec=env XDG_CURRENT_DESKTOP=gnome telegram-desktop -- %u"
    ),
    Patch(
        "gtkpicker",
        "onlyoffice-desktopeditors.desktop",
        "Exec=/usr/bin/onlyoffice-desktopeditors %U",
        "Exec=env XDG_CURRENT_DESKTOP=gnome /usr/bin/onlyoffice-desktopeditors %U"
    ),
    Patch(
        "gtkpicker",
        "sqlitebrowser.desktop",
        "Exec=sqlitebrowser %f",
        "Exec=env XDG_CURRENT_DESKTOP=gnome sqlitebrowser %f"
    ),
    Patch(
        "wayland",
        "discord.desktop",
        "Exec=/usr/bin/discord\n",
        "Exec=/usr/bin/discord --enable-features=UseOzonePlatform --ozone-platform=wayland\n"
    ),
    Patch(
        "wayland",
        "discord-canary.desktop",
        "Exec=/usr/bin/discord-canary\n",
        "Exec=/usr/bin/discord-canary --enable-features=UseOzonePlatform --ozone-platform=wayland\n"
    ),
    Patch(
        "wayland",
        "firefox.desktop",
        "Exec=/usr/lib/firefox/firefox %u",
        "Exec=env MOZ_ENABLE_WAYLAND=1 /usr/lib/firefox/firefox %u"
    ),    Patch(
        "qtzoom",
        "org.prismlauncher.PrismLauncher.desktop",
        "Exec=prismlauncher",
        "Exec=env QT_SCALE_FACTOR=1.7 prismlauncher"
    ),
    Patch(
        "qtzoom",
        "multimc.desktop",
        "Exec=multimc",
        "Exec=env QT_SCALE_FACTOR=1.7 multimc"
    ),
]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-np", "--noprint", required=False, default=False, action="store_true", help="Disables prints (except error prints)")
    parser.add_argument("-g", "--gtkpicker", required=False, default=True, action="store_true", help="Enables GTK Picker patches")
    parser.add_argument("-w", "--wayland", required=False, default=True, action="store_true", help="Enables Wayland patches")
    parser.add_argument("-q", "--qtzoom", required=False, default=False, action="store_true", help="Enables QT zoom patches")
    return parser.parse_args()

args = get_args()

def print_valid(text: str):
    if not args.noprint:
        print(text)


def patch_file():
    pass

if __name__ == "__main__":
    patch_count = 0
    for patch in patches:
        if patch.patch_type == "gtkpicker" and not args.gtkpicker:
            continue
        if patch.patch_type == "wayland" and not args.wayland:
            continue
        if patch.patch_type == "qtzoom" and not args.qtzoom:
            continue
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
            print_valid(f"Patched {patch.file_name}.")
            patch_count += 1
        
        except PermissionError:
            print("You don't have permission to write to that folder. try running as root.")
            exit(1)
        
        except Exception as e:
            print("Exception happened !\n", e)
            exit(2)

    # After the loop, print how many files were changed
    print_valid(f"{patch_count} files changed.")
