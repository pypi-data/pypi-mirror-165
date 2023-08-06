# Currently Tilos Player Unofficial only works on Linux.
# Usage
*Read also the note on 0.1*

Tilos Player Unofficial is a fast way to play Tilos Rádió shows via command line.
It takes only a few keystrokes to play your selected episode in VLC media player.

This app has two modes:
- full search: allows you to search and select your favourite show & then choose the episode you want to play from the list of available episodes
- play latest: allows you to select a show from the list of all shows & play its latest episode

Upon successful installation, the app can be run from a bash CLI by typing "tilos" then using the shortcuts to quickly select to episode you want to play.

# Note on 0.1

The current version is 0.1. Installation and usage was tested on Ubuntu 20.04 and Q4OS Gemini.

It provides all the currently envisaged basic functionalities that lets you quickly play
your desired show & save a lot of clicks and loading times. The [improvements](#improvements)
section provides additional functionalities that could be added eventually.

# Installation
## Ubuntu
### 0. Prerequisites
You need to have VLC, Python 3 and pip3 installed.

You can check if you have these by running `vlc --version`, `python3 --version` and `pip3 --version`
in your terminal. If you receive a "command not found" message for any of these, you need to install that particular
program.

These tutorials could help:

For VLC, see https://www.videolan.org/vlc/download-ubuntu.html

For Python 3, see https://docs.python-guide.org/starting/install3/linux/

For pip3, run `python3 -m pip install pip`

### 1. Open your bash terminal (usually Ctrl+Alt+T)

### 2. Navigate to your Downloads folder
usually: `cd Downloads`

### 3. Download Tilos Player Unofficial from GitHub
At the top of the script's GitHub page, download the zip file by clicking on the green "Code" button
and selecting "Download ZIP". Make sure you download the zip to your Downloads folder.

Or you could try `wget https://github.com/xa49/tilos_player/archive/refs/heads/main.zip`

### 4. Unzip the files
`unzip main.zip`

### 5. Navigate to the folder where the unzipped files are stored
`cd tilos_player-main`

### 6. Make the setup script executable
`sudo chmod 754 bash_setup`
Note: Before this step you might want to open the setup script to ensure it does not contain
harmful code or any command that you do not want executed. You can do this by `cat bash_setup`.

### 7. Run the setup script
`./bash_setup`

### 8. Enjoy Tilos Player Unofficial!
Run the app in the Terminal by typing `tilos` and pressing Enter. (You might have to reopen your Terminal if it doesn't work straight away.)

### 9. Learn your keyboard shortcuts for best experience
For example, if you would like to listen to the latest episode of Tilos Essence the following 19
keyboard presses will start playing the episode: Ctrl+Alt+T then type "tilos" then Enter then
"l/essence" then Enter.

## Windows
The app is currently not available for Windows.[^1]

# Usage
## Ubuntu
Open your Terminal and type `tilos` followed by an Enter.
Try running python3 install.py in the tilos_player-main folder if some shows work for you but others do not.

# Improvements
Feature: (headless) VLC with simple controls from the command line, e.g. pause, next episode, previous episode - not much more
Stability: copy the files to a safe location where users won't delete / move the files
Feature: play livestream
Stability: downloading as main.zip is risky. if there is already a main.zip then copying further instructions won't work

[^1]: Notes: termios is not implemented for Windows. Later on users will have to add VLC to path.
