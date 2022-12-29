# PandaRescue

A simple platformer game in which the player is an explorer in the wild that needs to collect as many baby pandas as he can and tranfer them to safety and avoid getting killed.

## Player movement

Player can control the movement of the play by using:
* Left arrow - to move left
* Right arrow - to move right
* Space bar - to jump
* Down arrow - to bent down

## Levels

Higher levels are more difficult with more obstacles such as spikes, moving platforms or simply larger distances between platforms. The files Level1 - Level10 are the files with the information about the level composition in a form of a matrix. The number in the matrix corresponds to the specific class of an object added to the world such as: tunnel, ground, platform, spikes etc.. The files are opened with the help of pickle library.

Files:
main.py - contains code for running a chosen level of the game as well as the matrix to create new levels.
menu.py - version of the game with a menu and automatic transition to higher levels.

## Resources

The folder resources contains sprites used in the game that were created with the help of Gimp.

## Game window
![screen](https://user-images.githubusercontent.com/83085295/209990260-31a36dd9-9f72-4df7-931d-5ef2e235b97c.png)
