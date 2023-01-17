import os
import pathlib  # to create the full path of a directory / you compose it as you can see in line 21 - 25
import random  # to shuffle the list
import subprocess  # to run the apple script

SET_DESKTOPBACKGROUND_OSASCRIPT = """/usr/bin/osascript<<END 
tell application "System Events"
    tell every desktop
        set picture to "{}"
    end tell
end tell
END"""  # apple script


def set_background():
    os.chdir('/Users/nezaraboghanem/Documents/Programming/main_programming_languages/Python_native_language/projects_2022/desktop_background_automate') # to change directory to where your python files are located as when it runs auto it doesn't run from this directory 
    COUNTRIES = 'countries' # name of the folder 
    files = os.listdir(COUNTRIES) # list of the items in the folder 
    random.shuffle(files) # shuffle the list 
    next_db = files[0] # choose the first one
    full_image_path = os.path.join(
        pathlib.Path().absolute(),
        COUNTRIES,
        next_db
    ) # make the directory path for that item to assign to the apple script
    subprocess.Popen(SET_DESKTOPBACKGROUND_OSASCRIPT.format(
        full_image_path), shell=True) # run the apple script 


set_background() # call the function 
