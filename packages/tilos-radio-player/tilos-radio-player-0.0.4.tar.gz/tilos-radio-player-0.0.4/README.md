# Currently Tilos Player Unofficial only works on Linux.
# About

Tilos Player Unofficial is a fast way to play Tilos Rádió shows via command line.
It takes only a few keystrokes to play your selected episode in VLC media player.

This app has two modes:
- *full search*: allows you to search and select your favourite show & then choose the episode you want to play from the list of available episodes
- *play latest*: allows you to select a show from the list of all shows & play its latest episode

Upon successful installation, the app can be run from a Terminal by typing "tilos" then using the shortcuts to quickly select to episode you want to play.

# Installation
## Linux
### 0. Prerequisites
You need to have VLC, Python 3 and pip3 installed.

You can check if you have these by running `vlc --version`, `python3 --version` and `pip3 --version`
in your terminal. If you receive a "command not found" message for any of these, you need to install that particular
program.

These tutorials could help:

For VLC, see https://www.videolan.org/vlc/download-ubuntu.html

For Python 3, see https://docs.python-guide.org/starting/install3/linux/

For pip3, run `python3 -m pip install pip`

### 1. `pip3 install tilos-radio-player`

### 2. Enjoy Tilos Player Unofficial!
Run the app in the Terminal by typing `tilos` and pressing Enter.

### 3. Learn your keyboard shortcuts for best experience
For example, if you would like to listen to the latest episode of Tilos Essence the following 19
keyboard presses will start playing the episode: `Ctrl+Alt+T` then type `tilos` then `Enter` then
type `l/essence` then `Enter`.

## Windows
The app is currently not available for Windows.

# Usage
## Linux
Open your Terminal and type `tilos` followed by an Enter.

# Improvements
Feature: (headless) VLC with simple controls from the command line, e.g. pause, next episode, previous episode - not much more
Feature: play livestream
Feature: support shows from any period, not only the last couple of them
Maintainability: reorganise code

You can reach out to me at tilosplayer@gmail.com
