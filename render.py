import numpy as np
import tkinter as tk


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
	
	def set_scale(self, scale):
		for p in self.points:
			p.set_coordinates(list(np.array(p.get_coordinates()) * scale))
	
	def set_pan(self, scale):
		for p in self.points:
			p.set_coordinates(list(np.array(p.get_coordinates()) + scale))
	
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
					[0.0, np.cos(x_angle), np.sin(x_angle)],
					[0.0, -np.sin(x_angle), np.cos(x_angle)]
				],
				p.get_coordinates()
			)))
	
	def y_rotate(self, y_angle):
		for p in self.points:
			p.set_coordinates(list(np.matmul(
				[
					[np.cos(y_angle), 0.0, -np.sin(y_angle)],
					[0.0, 1.0, 0.0],
					[np.sin(y_angle), 0.0, np.cos(y_angle)]
				],
				p.get_coordinates()
			)))
	
	def z_rotate(self, z_angle):
		for p in self.points:
			p.set_coordinates(list(np.matmul(
				[
					[np.cos(z_angle), np.sin(z_angle), 0.0],
					[-np.sin(z_angle), np.cos(z_angle), 0.0],
					[0.0, 0.0, 1.0]
				],
				p.get_coordinates()
			)))
		
class GUI:
	def __init__(self, bg="cyan", height=0, width=0):		
		self.top = tk.Tk()
		if not height or not width:	self.top.attributes("-zoomed", True)
		
		self.top.update()
		self.height = height if height else self.top.winfo_height()
		self.width = width if width else self.top.winfo_width()
		
		self.canvas = tk.Canvas(self.top, bg=bg, height=self.height, width=self.width)
		self.canvas.configure(scrollregion=(-self.width/2,-self.height/2, self.width/2, self.height/2)) ##making 0 the origin
		self.canvas.pack()
		
		self.mouse_pressed = {"left":False, "right":False}

		
		self.canvas.bind('<ButtonPress>', self.on_mouse_pressed)
		self.canvas.bind('<ButtonRelease>', self.on_mouse_released)
		self.canvas.bind('<Motion>', self.mouse_motion)

	def on_mouse_pressed(self, event):
		if event.num == 3: self.mouse_pressed["right"] = True ## right mouse is 3
	def on_mouse_released(self, event):
		if event.num == 3: self.mouse_pressed["right"] = False
	def mouse_motion(self, event):
		if self.mouse_pressed["right"]:
			print(event.x, event.y)

	
