# What's this
This is a simple utility script that edits your desktop files to make your experience better

At first, this was just a script to add `env XDG_CURRENT_DESKTOP=gnome` to desktop files so they use the Gnome file picker on i3/bspwm/other wms.
However, this has now evolved to support multiple patch types, which as of now include:
- Gtk File Picker (XDG_CURRENT_DESKTOP=gnome), original purpose described above
- Wayland (--ozone-platform-hint=auto & other), enable wayland support on electron apps & other apps, notabely fixes visual glitches & screensharing (must have on wayland tbh)
- Qt Zoom (QT_SCALE_FACTOR=1.7), more of a personal preference, only patches mc launchers because they look too small on a 1440p screen
- NVIDIA (basically only https://github.com/elFarto/nvidia-vaapi-driver)
& can theorically be used to patch any text file

# How to use
### Using the .py script
- Grab the python script
- Run it
- Done
### Using pacman hooks
- Install the package located [here](https://aur.archlinux.org/packages/desktop-patcher-hook) 
   
All done, the hook will run when installing/upgrading an app supported by this script

# Need support another app
Open an issue
