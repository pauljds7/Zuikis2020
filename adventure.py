import numpy as np
import math
import configurations

####
#Mechanics of the zuikis adventure.
####

class Actions:

	def __init__(self, configuration, dim, carrot_energy, manh_distance=4):
		self.rabbit_place, self.wolf_places, self.carrot_places = configuration
		self.init_energy = dim ** 2
		self.dim = dim
		self.energy = self.init_energy
		self.carrot_energy = carrot_energy
		self.manh_distance = manh_distance
		
	def is_goal(self):
		""" Checks if adventure is finished """
		if self.energy <= 0: return True
		return False

	def interactions(self):
		""" Interactions when agents are in the same cell """
		a = self.rabbit_vision()
		for i, wolf_place in enumerate(self.wolf_places):
			if self.rabbit_place == wolf_place:
				self.energy -= self.init_energy * 3 / 4
				self.move_rabbit(cells=4)
				path = (self.rabbit_place, self.wolf_places, self.carrot_places, self.energy)
				return path

		for i, carrot_place in enumerate(self.carrot_places):
			if self.rabbit_place == carrot_place:
				self.energy += self.carrot_energy
				self.eat_carrot(i)
				self.add_carrot()
				path = (self.rabbit_place, self.wolf_places, self.carrot_places, self.energy)
				return path
		return (self.rabbit_place, self.wolf_places, self.carrot_places, self.energy)
		
	def add_carrot(self):
		""" Add a new carrot from the uniform distribution """
		pass

	def eat_carrot(self, index):
		""" Delete eaten carrot from the carrot list """
		del self.carrot_places[index]

	def move_rabbit(self, cells=1):
		""" Move rabbit to another cell """
		arr = np.array([-cells, 0, cells])
		new_positions = []
		for x in arr:
			for y in arr:
				if x == self.rabbit_place[0] and y == self.rabbit_place[1]: continue
				if x < 0 or y < 0: continue
				new_x = self.rabbit_place[0] + x
				new_y = self.rabbit_place[1] + y
				new_positions.append((new_x, new_y))

		if cells == 1:
			rand_pos = new_positions[random.randint(0, (cells * 2 + 1) ** 2)]
			self.rabbit_place = rand_pos
		else:  # If rabbit moves because of the encounter with the wolf
			center = int(self.dim / 2)  # Center of the grid
			center_coord = (center, center)
			distances = []
			best_distance = self.dim
			for new_p in new_positions:
				distance = math.sqrt((self.rabbit_place[0] - new_p[0]) ** 2 + \
					                 (self.rabbit_place[1] - new_p[1]) ** 2)
				if distance < best_distance:     # Move to  a cell closest to the center of the grid
					best_distance = distance
					new_position = new_p
			self.rabbit_place = new_position

	def move_wolf(self, index):
		""" Move wolf """
		pass
	
	def rabbit_vision(self):
		""" Rabbit's space of vision """
		rabbit_vision = []
		for i in range(-self.manh_distance, self.manh_distance + 1):
			for j in range(-self.manh_distance, self.manh_distance + 1):
				if np.abs(i) + np.abs(j) > self.manh_distance: continue  # Discard cells outside
											 # Manhattan space
				x_vision = self.rabbit_place[0] + i
				y_vision = self.rabbit_place[1] + j
				# Boundary conditions
				if self.is_outside_boundaries(x_vision) or self.is_outside_boundaries(y_vision): continue
				rabbit_vision.append((x_vision, y_vision))
		return rabbit_vision
	
	def is_outside_boundaries(self, coord):
		""" Check if the coordinate is outside the boundaries of the grid """
		if coord < 0 or coord > self.dim: return True
		else: return False
		
	def wolf_vision(self, wolf_place, wolf_dir):
		""" Wolf's space of vision """

		intervals = {
					 (-1, 1): [(-4, 2), (-2, 4)],
					 (0, 1): [(-4, 4), (0, 4)],
					 (1, 1): [(-2, 4), (-2, 4)],
					 (1, 0): [(0, 4), (-4, 4)],
					 (1, -1): [(-2, 4), (-4, 2)],
					 (0, -1): [(-4, 0), (-4, 4)],
					 (-1, -1): [(-4, 2), (-4, 2)],
					 (-1, 0): [(-4, 0), (-4, 4)]
		}
		manh_boundaries = intervals[self.move[wolf_dir]]

		wolf_vision = []
		for i in range(-self.manh_distance, self.manh_distance + 1):
			for j in range(-self.manh_distance, self.manh_distance + 1):
				if i >= manh_boundaries[0][0] and i <= manh_boundaries[0][1] and \
				   j >= manh_boundaries[1][0] and j <= manh_boundaries[1][1]:
					if np.abs(i) + np.abs(j) > self.manh_distance: continue
					x_vision = wolf_place[0] + i
					y_vision = wolf_place[1] + j
					if self.is_outside_boundaries(x_vision) or self.is_outside_boundaries(y_vision): continue
					wolf_vision.append((self.rabbit_place[0] + i, self.rabbit_place[1] + j))
		return wolf_vision
