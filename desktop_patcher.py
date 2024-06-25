#!/bin/python3

# Not made to be written perfectly, but compact & in 1 file

import argparse
from dataclasses import dataclass
from enum import Enum
import os

class PatchType(Enum):
    GTKPICKER = 1
    WAYLAND = 2
    QTZOOM = 3
    NVIDIA = 4
    OTHER = 999

@dataclass
class Patch:
    patch_type: PatchType
    file_name: str
    match: str
    replacement: str
    folder_path: str = "/usr/share/applications/"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-np", "--noprint", required=False, default=False, action="store_true", help="Disables prints (except error prints)")
    parser.add_argument("-g", "--gtkpicker", required=False, default=True, action="store_true", help="Enables GTK Picker patches")
    parser.add_argument("-w", "--wayland", required=False, default=True, action="store_true", help="Enables Wayland patches")
    parser.add_argument("-q", "--qtzoom", required=False, default=False, action="store_true", help="Enables QT zoom patches")
    parser.add_argument("-nv", "--nvidia", required=False, default=False, action="store_true", help="Enables NVIDIA specific patches")
    parser.add_argument("-o", "--other", required=False, default=False, action="store_true", help="Enables misc patches")
    parser.add_argument("--all", required=False, default=False, action="store_true", help="Enables all patches")
    return parser.parse_args()

args = get_args()
args_dict = {
    PatchType.GTKPICKER: args.gtkpicker,
    PatchType.WAYLAND: args.wayland,
    PatchType.QTZOOM: args.qtzoom,
    PatchType.OTHER: args.other
}

patches: list[Patch] = [
    Patch(
        PatchType.GTKPICKER,
        "org.qbittorrent.qBittorrent.desktop", 
        "Exec=qbittorrent %U", 
        "Exec=env XDG_CURRENT_DESKTOP=gnome qbittorrent %U"
    ),
    Patch(
        PatchType.GTKPICKER,
        "org.telegram.desktop.desktop",
        "Exec=telegram-desktop -- %u",
        "Exec=env XDG_CURRENT_DESKTOP=gnome telegram-desktop -- %u"
    ),
    Patch(
        PatchType.GTKPICKER,
        "onlyoffice-desktopeditors.desktop",
        "Exec=/usr/bin/onlyoffice-desktopeditors %U",
        "Exec=env XDG_CURRENT_DESKTOP=gnome /usr/bin/onlyoffice-desktopeditors %U"
    ),
    Patch(
        PatchType.GTKPICKER,
        "sqlitebrowser.desktop",
        "Exec=sqlitebrowser %f",
        "Exec=env XDG_CURRENT_DESKTOP=gnome sqlitebrowser %f"
    ),
    Patch(
        PatchType.GTKPICKER,
        "com.obsproject.Studio.desktop",
        "Exec=obs",
        "Exec=env XDG_CURRENT_DESKTOP=gnome obs"
    ),
    Patch(
        PatchType.WAYLAND,
        "discord.desktop",
        "Exec=/usr/bin/discord\n",
        "Exec=/usr/bin/discord --ozone-platform-hint=auto\n"
    ),
    Patch(
        PatchType.WAYLAND,
        "discord-canary.desktop",
        "Exec=/usr/bin/discord-canary\n",
        "Exec=/usr/bin/discord-canary --ozone-platform-hint=auto\n"
    ),
    Patch(
        PatchType.WAYLAND,
        "vesktop.desktop",
        "Exec=vesktop\n",
        "Exec=vesktop --ozone-platform-hint=auto\n"
    ),
    Patch(
        PatchType.WAYLAND,
        "signal-desktop.desktop",
        "Exec=signal-desktop -- %u\n",
        "Exec=signal-desktop --ozone-platform-hint=auto -- %u\n"
    ),
    Patch(
        PatchType.WAYLAND,
        "code.desktop",
        "Exec=/usr/bin/code %F",
        "Exec=/usr/bin/code --ozone-platform-hint=auto %F"
    ),
    # Note: i'm a lunarclient maintainer on the AUR, but still want to separate this.
    Patch(
        PatchType.WAYLAND,
        "lunarclient.desktop",
        "Exec=env DESKTOPINTEGRATION=false /usr/bin/lunarclient --no-sandbox %U",
        "Exec=env DESKTOPINTEGRATION=false /usr/bin/lunarclient --ozone-platform-hint=auto --no-sandbox %U"
    ),
    # Note: this is having issues as of now, there's no GUI if you set this flag.
    # Patch(
    #     PatchType.WAYLAND,
    #     "cider.desktop",
    #     "Exec=/opt/Cider/cider %U",
    #     "Exec=/opt/Cider/cider --ozone-platform-hint=auto %U"
    # ),
    Patch(
        PatchType.WAYLAND,
        "postman.desktop",
        "Exec=/opt/postman/Postman %U",
        "Exec=/opt/postman/Postman --ozone-platform-hint=auto %U"
    ),   
    Patch(
        PatchType.WAYLAND,
        "firefox.desktop",
        "Exec=/usr/lib/firefox/firefox %u",
        "Exec=env MOZ_ENABLE_WAYLAND=1 /usr/lib/firefox/firefox %u"
    ),    
    Patch(
        PatchType.QTZOOM,
        "org.prismlauncher.PrismLauncher.desktop",
        "Exec=prismlauncher",
        "Exec=env QT_SCALE_FACTOR=1.7 prismlauncher"
    ),
    Patch(
        PatchType.QTZOOM,
        "multimc.desktop",
        "Exec=multimc",
        "Exec=env QT_SCALE_FACTOR=1.7 multimc"
    ),
    # Note: suboptimal, patches for both w & without wayland
    # SHOULD ADD A REGEX OPTION FOR THE PATCHES
    # BUT REALLY CANT BE BOTHERED RN TBH
    Patch(
        PatchType.NVIDIA,
        "firefox.desktop",
        "Exec=env MOZ_ENABLE_WAYLAND=1 /usr/lib/firefox/firefox %u",
        "Exec=env MOZ_ENABLE_WAYLAND=1 MOZ_DISABLE_RDD_SANDBOX=1 LIBVA_DRIVER_NAME=nvidia __EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/10_nvidia.json /usr/lib/firefox/firefox %u"
    ),
    Patch(
        PatchType.NVIDIA,
        "firefox.desktop",
        "Exec=/usr/lib/firefox/firefox %u",
        "Exec=env MOZ_DISABLE_RDD_SANDBOX=1 LIBVA_DRIVER_NAME=nvidia __EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/10_nvidia.json /usr/lib/firefox/firefox %u"
    ),
]

class PatchResult(Enum):
    SUCCESS = 0
    UNCHANGED = 1
    FILE_NOT_FOUND = 2
    ERR_READING_FILE = 3
    NO_WRITE_PERMISSION = 4
    ERR_WRITING_FILE = 5


def print_valid(text: str):
    if not args.noprint:
        print(text)

def is_enabled(patch_type: PatchType) -> bool:
    if args.all:
        return True
    return bool(args_dict.get(patch_type))
    
def patch_file(patch: Patch) -> tuple[PatchResult, Exception | None]:
    full_path = patch.folder_path + patch.file_name
    # Try to read the old file & return error if can't
    try:
        if not os.path.isfile(full_path): 
            return (PatchResult.FILE_NOT_FOUND, None)
        with open(full_path, "r") as open_file:
            old_content = open_file.read()
    except Exception as e:
        return (PatchResult.ERR_READING_FILE, e)
    
    # patch & see if its different
    patched_content = old_content.replace(patch.match, patch.replacement)
    if patched_content == old_content:
        return (PatchResult.UNCHANGED, None)

    # if it is, try to write it back
    try:
        with open(full_path, "w") as open_file: 
            open_file.write(patched_content)
        return (PatchResult.SUCCESS, None)
    except PermissionError: return (PatchResult.NO_WRITE_PERMISSION, None)
    except Exception as e: return (PatchResult.ERR_WRITING_FILE, e)

if __name__ == "__main__":
    patch_count = 0
    for patch in patches:
        if not is_enabled(patch.patch_type):
            continue

        res, exception = patch_file(patch)
        if res == PatchResult.NO_WRITE_PERMISSION: #no write always means no permission, useless
            print_valid("No write permission, exiting.")
            exit(1)
            
        if res == PatchResult.SUCCESS:
            patch_count += 1
            print_valid(f"Patched file {patch.file_name}")
        elif res == PatchResult.UNCHANGED:
            # print_valid(f"File {patch.file_name} unchanged")
            pass
        else:
            print_valid(f"Error patching file {patch.file_name}: {res.name}")
    # After the loop, print how many files were changed
    print_valid(f"{patch_count} files changed.")
