from enum import IntEnum
import pygame
from pygame.locals import *


BOARD_SIZE = 50
CHESS_RADIUS = BOARD_SIZE//2 - 3
CHESS_LEN = 15
MAP_WIDTH = CHESS_LEN * BOARD_SIZE
MAP_HEIGHT = CHESS_LEN * BOARD_SIZE

INFO_WIDTH = 200
BUTTON_WIDTH = 140
BUTTON_HEIGHT = 50

SCREEN_WIDTH = MAP_WIDTH + INFO_WIDTH
SCREEN_HEIGHT = MAP_HEIGHT

class MAP_ENTRY_TYPE(IntEnum):
	MAP_EMPTY = 0,
	MAP_PLAYER_ONE = 1,
	MAP_PLAYER_TWO = 2,
	MAP_NONE = 3,
	
class Map():
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.map = [[0 for x in range(self.width)] for y in range(self.height)]
		self.steps = []
	
	def reset(self):
		for y in range(self.height):
			for x in range(self.width):
				self.map[y][x] = 0
		self.steps = []
	
	def reverseTurn(self, turn):
		if turn == MAP_ENTRY_TYPE.MAP_PLAYER_ONE:
			return MAP_ENTRY_TYPE.MAP_PLAYER_TWO
		else:
			return MAP_ENTRY_TYPE.MAP_PLAYER_ONE

	def getMapUnitRect(self, x, y):
		map_x = x * BOARD_SIZE
		map_y = y * BOARD_SIZE
		
		return (map_x, map_y, BOARD_SIZE, BOARD_SIZE)
	
	def MapPosToIndex(self, map_x, map_y):
		x = map_x // BOARD_SIZE
		y = map_y // BOARD_SIZE		
		return (x, y)
	
	def isInMap(self, map_x, map_y):
		if (map_x <= 0 or map_x >= MAP_WIDTH or 
			map_y <= 0 or map_y >= MAP_HEIGHT):
			return False
		return True
	
	def isEmpty(self, x, y):
		return (self.map[y][x] == 0)
	
	def click(self, x, y, type):
		self.map[y][x] = type.value
		self.steps.append((x,y))

	def drawChess(self, screen):
		player_one = (25, 25, 25)
		player_two = (255, 255, 255)
		player_color = [player_one, player_two]
		
		font = pygame.font.SysFont(None, BOARD_SIZE*2//3)
		for i in range(len(self.steps)):
			x, y = self.steps[i]
			map_x, map_y, width, height = self.getMapUnitRect(x, y)
			pos, radius = (map_x + width//2, map_y + height//2), CHESS_RADIUS
			turn = self.map[y][x]
			if turn == 1:
				op_turn = 2
			else:
				op_turn = 1
			surf = (255, 255, 255)
			pygame.draw.circle(screen, player_color[turn-1], pos, radius)
			
			msg_image = font.render(str(i+1), True, player_color[op_turn-1], player_color[turn-1])
			msg_image_rect = msg_image.get_rect()
			msg_image_rect.center = pos
			screen.blit(msg_image, msg_image_rect)
			
		
		if len(self.steps) > 0:
			last_pos = self.steps[-1]
			map_x, map_y, width, height = self.getMapUnitRect(last_pos[0], last_pos[1])
			red_color = (255, 0, 0)
			point_list = [(map_x, map_y), (map_x + width, map_y), 
					(map_x + width, map_y + height), (map_x, map_y + height)]
			pygame.draw.lines(screen, red_color, True, point_list, 1)
			
	def drawBackground(self, screen):
		color = (0, 0, 0)
		for y in range(self.height):
			start_pos, end_pos= (BOARD_SIZE//2, BOARD_SIZE//2 + BOARD_SIZE * y), (MAP_WIDTH - BOARD_SIZE//2, BOARD_SIZE//2 + BOARD_SIZE * y)
			if y == (self.height)//2:
				width = 1
			else:
				width = 1
			pygame.draw.line(screen, color, start_pos, end_pos, width)
		
		for x in range(self.width):
			start_pos, end_pos= (BOARD_SIZE//2 + BOARD_SIZE * x, BOARD_SIZE//2), (BOARD_SIZE//2 + BOARD_SIZE * x, MAP_HEIGHT - BOARD_SIZE//2)
			if x == (self.width)//2:
				width = 1
			else:
				width = 1
			pygame.draw.line(screen, color, start_pos, end_pos, width)
				
		
		BOARD_size = 6
		pos = [(3,3), (11,3), (3, 11), (11,11), (7,7)]
		for (x, y) in pos:
			pygame.draw.rect(screen, color, (BOARD_SIZE//2 + x * BOARD_SIZE - BOARD_size//2, BOARD_SIZE//2 + y * BOARD_SIZE - BOARD_size//2, BOARD_size, BOARD_size))
		