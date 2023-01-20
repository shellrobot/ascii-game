# ====================
# ascii game function code stuff
# ====================

# Imports
import os,time,sys,random as rnd, logging
from colorama import just_fix_windows_console
from readchar import readchar

# fixes windows console
just_fix_windows_console()

# Variables
area = [] # Map
playerChar = "■" # Player char
borderChar = "█" # Border char
score = 0 # Score
loop = False

# For custom errors
class error(Exception):
	pass

# Map class
class map:
	x = 0
	y = 0
	randWallAmt = 0
	active = False
	walls = []
	borders = []
	random = False

# Player class
class player:
	spawned = False
	x = 0
	y = 0

# Block class
class block:
	spawned = False
	x = 0
	y = 0
	def delete():
		"""Deletes the objective block"""
		if block.spawned == False:
			return 0
		block.x = 0
		block.y = 0

class wall:
	topLeft = "┌"
	bottomLeft = "└"
	topRight = "┐"
	bottomRight = "┘"
	leftRight = "│"
	side = "─"
	inside = " "

	def setWall(type,char):
		"""Changes char of certain wall spots"""
		
		if type == "topLeft":
			wall.topleft = char
		elif type == "bottomLeft":
			wall.bottomleft = char
		elif type == "topRight":
			wall.topRight = char
		elif type == "bottomRight":
			wall.bottomRight = char
		elif type == "leftRight":
			wall.bottomRight = char
		elif type == "side":
			wall.side = char
		elif type == "inside":
			wall.inside = char
			

class gameRule:
	speed = .125 # input cooldown (for slower machines)
	recursionLimit = 100000 # recursion limit
	clearScreen = True
	debug = False

sys.setrecursionlimit(gameRule.recursionLimit)
	
# Changes the variable
def setVar(var,value,ext1="",ext2=""):
	"""Changes variables in the game easily without editing code"""

	global playerChar,borderChar
	if var == "speed": # Sets the speed of the game
		gameRule.speed = value
	elif var == "playerChar":
		playerChar = value
	elif var == "borderChar":
		borderChar = value
	elif var == "wallChar":
		wall.setWall(ext1,ext2)
	elif var == "recursionLimit":
		gameRule.recursionLimit = value
		sys.setrecursionlimit(gameRule.recursionLimit)
	elif var == "clearScreen":
		gameRule.clearScreen = value
	elif var == "debug":
		gameRule.debug = value


		
# Creates the area
def createMap(x,y):
	"""Creates the map with the given x and y"""
	
	if map.active == True:
		raise error("Map already active")
	map.x = x
	map.y = y
	for i in range(y):
		area.append([])
		for o in range(x):
			if o == 0: # Left side border
				area[i].append(borderChar+borderChar)
				
			area[i].append(" ")
			
			if o+1 == x: # Right side border
				area[i].append(borderChar+borderChar)

	# Top and Bottom Border
	area.insert(0,[])
	area.insert(len(area),[])
	# Adds border to top and bottom of area
	for i in range(map.x+3): 
		area[0].append(borderChar) 
		area[len(area)-1].append(borderChar) 
	map.active = True # Sets area to active

# Prints the area
def printMap():
	"""Prints the map if its active"""
	
	areaString = ""
	if gameRule.clearScreen == True:
		os.system('cls' if os.name == 'nt' else 'clear') # Clears the screen
	for yPos, y in enumerate(area):
		for xPos, x in enumerate(area[yPos]):
			areaString = areaString + str(area[yPos][xPos])
			try: 
				if area[yPos][xPos] == borderChar and area[yPos][xPos+1] == borderChar:
					areaString = areaString + str(borderChar) # Prints double border char
				else: # Prints blank space
					areaString = areaString + ' '
			except: # Prints blank space
				areaString = areaString + ' '
					
		areaString = areaString + "\n" # New line
	print(areaString)
	areaString = ""
	if gameRule.debug == True:
		print(f"   MAP: {map.x}x{map.y}") # Prints area size 
		print(f"PLAYER: {player.x},{player.y} ")
		print(f" BLOCK: {block.x},{block.y} ")
		print(f" SCORE: {score} ") 
		print(f"WALL #: {map.randWallAmt}")


# Spawns a player at x and y
def spawnPlayer(x,y):
	"""Spawns the player at the given x and y cordinates"""
	
	# Checks to see if x and y are inside of the area
	if x not in list(range(1,map.y+1)) or y not in list(range(1,map.x+1)):
		return 0

	player.x = x
	player.y = y
	if player.spawned == True: # Checks to see if player is already spawned
		raise error("Player already spawned")
	player.spawned = True 

	#print(map.x,x,y,map.y) # Debug

	area[y][x] = playerChar # Spawns player

# Spawns a wall at x and y with width and height
def spawnWall(x,y,w=1,h=1):
	"""Spawn a wall at the given x and y cordinates with width of 'w' and height of 'h'"""
	
	if map.active == False: # Checks to see if area is active
		raise error("Map must be active to spawn wall")
		return 0

	preMap = []
	for i in range(w): 
		for o in range(h):
			# append all the wall cords to a list
			preMap.append([x+i,y+o])

	if player.spawned == True: # Checks to see if player is in the way of the wall
		if player.x in list(range(x,x+w)) and player.y in list(range(y,y+h)):
			raise error("Player is the way of wall")


	if x + w > map.x+1 or y + h > map.y+1:
		raise error("Wall overlaps Border")
		
		
	for i in range(w):
		for o in range(h):
			if i == 0 and o == 0: # Top Left
				wallChar = "┌"
			elif i == 0 and o+1 == h: # Bottom Left
				wallChar = "└"
			elif i+1 == w and o == 0: # Top Right
				wallChar = "┐"
			elif i+1 == w and o+1 == h: # Bottom Right
				wallChar = "┘"
			elif i == 0 or i+1 == w: # Left and Right
				wallChar = "│"
			elif o == 0 or o+1 == h: # Top and Bottom
				wallChar = "─"
			else: # ever
				wallChar = " "

			area[y+o][x+i] = wallChar
			map.walls.append([x+i,y+o])
			wall.active.append([x,y,w,h])

# Spawns a block at x and y
def spawnObj(x="x",y="y"):
	"""Spawns the objective block at the given x and y cordinates"""
	
	if player.spawned == False:
		print("Player must be spawned to spawn objective block")
		return 0
	if map.active == False:
		print("Map must be active to spawn objective block")
		return 0
	
	if x == "x" and y == "y":
		while True:
			blockx = rnd.randrange(1,map.x)
			blocky = rnd.randrange(1,map.y)
			if [blockx,blocky] not in map.walls:
				if [blockx,blocky] != [player.x,player.y]:
					break

	if x != "x" and y == "y" or x == "x" and y != "y":
		print("Invalid x,y cords")
		return 0
	if x != "x" and y != "y":
		if [x,y] in map.walls:
			raise error("Can't spawn block on wall")
			return 0
		blockx = x
		blocky = y

	block.spawned = True
	block.x = blockx
	block.y = blocky
	area[blocky][blockx] = "@"
	return 1

# Moves the player
def move(direction="Direction"):
	"""Takes user input from keyboard and executes action based on it"""
	
	if player.spawned != True:
		raise error("Player is not spawned")
		return 0

	validDirections = ["W","A","S","D","E","R"]
	if direction.upper() not in validDirections:
		print("Invalid direction")
		return 0
	
	if direction.upper() == "E":
		print("Exiting")
		exit()

	if direction.upper() == 'W': # Move Up (-Y)
		if player.y <= 1:
			print("Can't move up due to border")
		elif [player.x,player.y-1] in map.walls:
			print("Can't move up due to wall")
		else:
			area[player.y][player.x] = " " # Clear players last position
			player.y-=1
			area[player.y][player.x] = playerChar # Set players new position

			
	elif direction.upper() == 'S': # Move Down (+Y)
		if player.y >= map.y:
			print("Can't move down due to border")
		elif [player.x,player.y+1] in map.walls:
			print("Can't move down due to wall")
		else:
			area[player.y][player.x] = " "
			player.y+=1
			area[player.y][player.x] = playerChar

	
	elif direction.upper() == 'A': # Move Left (-X)
		if player.x <= 1:
			print("Can't move left due to border")
		elif [player.x-1,player.y] in map.walls:
			print("Can't move left due to wall")
		else:
			area[player.y][player.x] = " "
			player.x-=1
			area[player.y][player.x] = playerChar 

		
	elif direction.upper() == 'D': # Move Right (+X)
		if player.x >= map.x: 
			print("Can't move right due to border") 
		elif [player.x+1,player.y] in map.walls: 
			print("Can't move right due to wall") 
		else:
			area[player.y][player.x] = " " 
			player.x+=1 
			area[player.y][player.x] = playerChar 


	elif direction.upper() == 'R': # Reload Map
		random(map.randWallAmt)

# Checks if player is on the block
def detectScore():
	"""Checks if player is on top of the objective block"""
	
	# Check if player and block are spawned
	if player.spawned == False and block.spawned == False:
		return 0

	# Check if player is on block
	if player.x == block.x and player.y == block.y:
		block.delete() # Delete block
		return 1
	else:
		return 0

# Random area generator
def random(wallAmt=1):
	"""Generates random map, walls, player, and objective block variable"""
	
	map.randWallAmt = wallAmt
	global area
	map.random = True
	area = []
	map.active = False
	map.walls = []
	player.spawned = False
	try:
		# rnd area size (5-30)
		map.x = rnd.randrange(10,30)
		map.y = rnd.randrange(10,30)

		# rnd player spawn (1-4)
		playerSpawn = rnd.randrange(1,4)

		# rnd wall spawn in the area with width and height (5-10)

		# Spawn area
		createMap(map.x,map.y)
		# Spawn player
		spawnPlayer(playerSpawn,playerSpawn)
		# Spawn wall
		for x in range(map.randWallAmt):
			wallSpawnX = rnd.randrange(2,10)
			wallSpawnY = rnd.randrange(2,10)
			wallWidth = rnd.randrange(2,10)
			wallHeight = rnd.randrange(2,10)
			spawnWall(wallSpawnX,wallSpawnY,wallWidth,wallHeight)

		spawnObj(rnd.randrange(1,map.x),rnd.randrange(1,map.y))

	except:
		print("Error occured while generating random area")
		print("Generating new area")
		random(map.randWallAmt)


# Start loop	
def start():
	"""Starts the game loop"""
	global score
	 # Print area

	if loop == True:
		return "Game loop already active"

	
	if map.random == True:
		spawnObj()
		move("r")
	printMap()

	# Game loop
	while True:
		move(readchar()) # Move player
		sensor = detectScore() # Check if player is on block
		if sensor == 1: # If player is on block
			score += 1 # Add 1 to score
			if map.random == True:
				random(map.randWallAmt)
			else:
				spawnObj()
		printMap() # Print area
		time.sleep(gameRule.speed) # Wait for next move

# prevents the code from running if not imported
if __name__ == "__main__": # If this file is ran
	raise error("DONT RUN THIS, IMPORT IT") # Raise error
