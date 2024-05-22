# BrickBreaker

## A fully functional brick breaker game. Written in Python using pygame

This project is an example of a game using the pygame library. I plan on using this as a placeholder game that can function in full stack client-server applications. I plan on taking this game, adding sign-in functionality, storing user's login and high score using a DBMS, and adding additional features. Still, this game is a fully functional executable in its current state.

![image](https://github.com/MatthewDutton10/BrickBreaker/assets/50933454/14bef2e4-39f2-4a42-9bb9-01b2d72ef34a)

## Setup

You will need pygame installed to run `main.py`. To install pygame, run the following command:

`pip install pygame`

Once pygame is installed, check that you have python installed and run `main.py`

To check if pygame installed correctly:

`python -m pygame --version`

## Gameplay Instructions

* **Movement:** use the arrowkeys or "A" and "D" to move left and right
* **Scoring:** each brick increases score by 50. If you break multiple bricks in one hit, a combo is added of 20 times the number of additional bricks
* **Levels:** as you progress, the speed of the ball increases making the game more difficult. The speed of the ball increases by 10% per level
* **High Score:** when you game over (lose all three lives), if your final score is greater than the current high score, the high score display will be updated
* **Pausing:** either shift button can be pressed at any point during the game to pause

## Work In Progress
* Music and sound effects
* Powerups that drop from bricks
* Unique brick/level layouts
* Unique graphics/fonts
