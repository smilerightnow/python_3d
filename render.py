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
	
	def set_pan(self, x_scale, y_scale):
		for p in self.points:
			p.set_coordinates([
				p.get_coordinates()[0] + x_scale,
				p.get_coordinates()[1] + y_scale,
				p.get_coordinates()[2]
			])
	
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
	def __init__(self, group, bg="cyan", height=0, width=0):
		self.group = group ## the 3d group
		
		self.window = tk.Tk()
		self.window.winfo_toplevel().title("3D render")
		
		if not height or not width:	self.window.attributes("-zoomed", True)
		
		self.window.update()
		self.height = height if height else self.window.winfo_height()
		self.width = width if width else self.window.winfo_width()
		
		self.canvas = tk.Canvas(self.window, bg=bg, height=self.height, width=self.width)
		self.canvas.configure(scrollregion=(-self.width/2,-self.height/2, self.width/2, self.height/2)) ##setting 0,0 in the center
		self.canvas.pack()

		self.mouse_pressed = {"left":False, "right":False, "middle": False}
		self.last_mouse_pos = {"x":0, "y":0}
		self.canvas.bind('<ButtonPress>', self.on_mouse_pressed)
		self.canvas.bind('<ButtonRelease>', self.on_mouse_released)
		self.canvas.bind('<Motion>', self.mouse_motion)

	def on_mouse_pressed(self, event):
		if event.num == 5: ##zooming out
			self.group.set_scale(self.group.scale - 0.05)
		
		if event.num == 4: ##zooming in
			self.group.set_scale(self.group.scale + 0.05)
			
		if event.num == 3: self.mouse_pressed["right"] = True ## move 3d world
		if event.num == 2: self.mouse_pressed["middle"] = True ## rotate 3d world
		if event.num == 1: self.mouse_pressed["left"] = True ## pan 3d world
		## note: i didn't implement a camera, im modifying the 3d group coordinates directly. when exporting, i need to rotate the model to 0degrees on all axis.
	def on_mouse_released(self, event):
		if event.num == 3: self.mouse_pressed["right"] = False
		if event.num == 2: self.mouse_pressed["middle"] = False
		if event.num == 1: self.mouse_pressed["left"] = False
	def mouse_motion(self, event):
		d_x = event.x - self.last_mouse_pos["x"]
		d_y = event.y - self.last_mouse_pos["y"]
		mouse_movement_speed = 5
		mouse_rotation_speed = 2
		
		if self.mouse_pressed["right"]: ## move the 3d world around
			if abs(d_x) > mouse_movement_speed or abs(d_y) > mouse_movement_speed: ## updating every ${mouse_movement_speed}px
				d_x = np.sign(d_x) * mouse_movement_speed ## limit the number
				d_y = np.sign(d_y) * mouse_movement_speed
				
				self.last_mouse_pos["x"] = event.x
				self.last_mouse_pos["y"] = event.y
				
				self.group.y_rotate((self.group.y_angle-d_x/100)) ## it seems a - here and a + bottom works perfectly. nice.
				self.group.x_rotate((self.group.x_angle+d_y/100))
		
		if self.mouse_pressed["middle"]: ## rotating the 3d world around z-axis
			if abs(d_x) > mouse_rotation_speed or abs(d_y) > mouse_rotation_speed: ## updating every ${mouse_rotation_speed}px
				d_x = np.sign(d_x) * mouse_rotation_speed ## limit the number
				
				self.last_mouse_pos["x"] = event.x
												
				self.group.z_rotate((self.group.z_angle-d_x/100))
		
		if self.mouse_pressed["left"]: ## panning the 3d world
			if abs(d_x) > mouse_movement_speed or abs(d_y) > mouse_movement_speed: ## updating every ${mouse_movement_speed}px
				d_x = np.sign(d_x) * mouse_movement_speed ## limit the number
				d_y = np.sign(d_y) * mouse_movement_speed
				
				self.last_mouse_pos["x"] = event.x
				self.last_mouse_pos["y"] = event.y
				
				self.group.set_pan(d_x, d_y)
