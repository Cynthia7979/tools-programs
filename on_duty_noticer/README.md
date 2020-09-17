# On Duty Noticer
This was made in an effort to prevent my classmates from forgetting that they were
on duty (which means that they have to clean the classroom).

**Note:** For security reasons, `data.json` which contains students' names has been removed.
For a template file, check `template_data.json`.

**Note:** `package/` is a pack (except `pillow`) of things you'll need when putting this program to another computer.
Say, your classroom's computer. It includes an extra Python Installer (Windows).

To really prepare this program for a new computer, you need *everything* in `package/` copied, PLUS `pip install pillow` and schedule the program
to run everyday (or on any frequency you like) using `Task Scheduler` on Windows.

Planned, upcoming features:
- [x] Read from a JSON file containing who's in which group, which group was on duty during the last update,
and the date of last update
- [x] Check the date and generate corresponding desktop wallpapers
  * The wallpaper would include:
    - [x] Which group is on duty
    - [x] Who're in the team
    - [x] Which day it is (date + day of week)
    - [x] A solid background
- [x] Change the wallpaper to the generated one
- [x] (**NEW!**) Wallpaper with picture mode
    - [x] Pic Mode 1: Picture `1080*540` at left, everything else align to the picture side
    - [x] Pic Mode 2: Picture `1920*1080` under a translucent white/dark cover, aligning is normal, text color is black.
    * To use Pic Mode, rename your image to "`picmode_source.jpg`" or "`picmode_source.png`" and put it in the same
    directory with the `.py` file.
    * **NOTE:** The program will crop Side Pic Mode wallpapers to 2:1 porportion