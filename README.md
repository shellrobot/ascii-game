# ascii-game

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

ascii game creator tool where u can make ascii games and play them. There is a player and an objective, when the player touches the objective the player gains +1 score

## Getting Started <a name = "getting_started"></a>

Instructions on how to use and what the functions do andn stuff

### Prerequisites

What you need to run this


- [python 3](https://www.python.org/)

### Installing


```
git clone https://github.com/shellrobot/ascii-game.git

cd ascii-game

pip install -r requirements.txt
```


## Usage <a name = "usage"></a>

Use the functions from the asciigame.py file to make your own ascii game

**Functions**

    createMap(x,y) # creates a map with x width and y height
    spawnPlayer(x,y) # spawns the player at x,y
    spawnWall(x,y,w,h) # spawns a wall at x,y with width w and height h
    spawnObjective(x,y) # spawns an objective at x,y
    move(char) # moves player based on char input
    printMap() # prints the map
    random(wallAmt) # generates a random map with wallAmt walls
    setVar(var,value) # change gameRule variables
    start() # start the game loop

**Game Rules**

    speed # cooldown between moves in seconds
    playerChar # char that is used to represent the player
    borderChar # char that is used to represent the border
    wallChar # char that is used to represent the wall
    blockChar # char that is used to represent the block
    recursionLimit # recursion limit for the map generator
    clearScreen # if true the screen will be cleared after every move
    debug # if true the game will print debug info

> **Note:** There are multiple wallChars (topLeft,bottomLeft,topRight,bottomRight,vertical,horizontal,inside) therefor it is used differently setVar("wallChar",side,char) ex: setVar("wallChar","topLeft","#")
