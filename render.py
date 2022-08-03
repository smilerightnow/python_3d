import math
import numpy as np

class Point:
	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z
	
	def get_coordinates(self):
		return [self.x, self.y, self.z]
	
	def set_coordinates(self, coor):
		self.x = coor[0]
		self.y = coor[1]
		self.z = coor[2]
	
	def move_by(self, x, y, z):
		self.x += x
		self.y += y
		self.z += z

class Group:
	def __init__(self, points=[], scale=1.0, x_angle=0.0, y_angle=0.0, z_angle=0.0):
		self.points = points
		self.scale = scale
		self.x_angle = x_angle
		self.y_angle = y_angle
		self.z_angle = z_angle
	
	def set_default_cube(self):
		coor = [
				[1., 1., 1.],
				[-1., 1., 1.],
				[-1., -1., 1.],
				[1., -1., 1.],
				[1., 1., -1.],
				[-1., 1., -1.],
				[-1., -1., -1.],
				[1., -1., -1.]
			]
		for c in coor:
			self.points.append(Point(c[0], c[1], c[2]))
	
	def add_points(self, coor):
		coor = []
		for c in coor:
			self.points.append(Point(c[0], c[1], c[2]))
	
	def add_point(self, c):
		self.points.append(Point(c[0], c[1], c[2]))
	
	def add_point_p(self, p):
		self.points.append(p)
	
	def get_coordinates(self):
		coor = []
		for p in self.points:
			coor.append(p.get_coordinates())
		
		return coor
	
	def x_rotate(self, x_angle):
		for p in self.points:
			p.set_coordinates(list(np.matmul(
				[
					[1.0, 0.0, 0.0],
					[0.0, math.cos(x_angle), math.sin(x_angle)],
					[0.0, -math.sin(x_angle), math.cos(x_angle)]
				],
				p.get_coordinates()
			)))
	
	def y_rotate(self, y_angle):
		for p in self.points:
			p.set_coordinates(list(np.matmul(
				[
					[math.cos(y_angle), 0.0, -math.sin(y_angle)],
					[0.0, 1.0, 0.0],
					[math.sin(y_angle), 0.0, math.cos(y_angle)]
				],
				p.get_coordinates()
			)))
	
	def z_rotate(self, z_angle):
		for p in self.points:
			p.set_coordinates(list(np.matmul(
				[
					[math.cos(z_angle), math.sin(z_angle), 0.0],
					[-math.sin(z_angle), math.cos(z_angle), 0.0],
					[0.0, 0.0, 1.0]
				],
				p.get_coordinates()
			)))
		
