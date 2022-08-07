import numpy as np
import tkinter as tk


class Point:
	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z
		self.selected = False
	
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
	def __init__(self, points=[]):
		self.points = points
		self.edges = []
	
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
		
		self.set_scale(100)
	
	def set_scale(self, scale):
		for p in self.points:
			p.set_coordinates((np.array(p.get_coordinates()) * scale).tolist())
	
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
	
	def get_selected_points(self): ## add in the future: selected edges, faces.
		selected_points = []
		for i, p in enumerate(self.points):
			if p.selected:
				selected_points.append([i, p])
		
		return selected_points
	
	def x_rotate(self, x_angle):
		for p in self.points:
			p.set_coordinates(np.matmul(
				[
					[1.0, 0.0, 0.0],
					[0.0, np.cos(x_angle), np.sin(x_angle)],
					[0.0, -np.sin(x_angle), np.cos(x_angle)]
				],
				p.get_coordinates()
			).tolist())
	
	def y_rotate(self, y_angle):
		for p in self.points:
			p.set_coordinates(np.matmul(
				[
					[np.cos(y_angle), 0.0, -np.sin(y_angle)],
					[0.0, 1.0, 0.0],
					[np.sin(y_angle), 0.0, np.cos(y_angle)]
				],
				p.get_coordinates()
			).tolist())
	
	def z_rotate(self, z_angle):
		for p in self.points:
			p.set_coordinates(np.matmul(
				[
					[np.cos(z_angle), np.sin(z_angle), 0.0],
					[-np.sin(z_angle), np.cos(z_angle), 0.0],
					[0.0, 0.0, 1.0]
				],
				p.get_coordinates()
			).tolist())
		
class GUI:
	def __init__(self, group, bg="cyan", height=0, width=0, fullscreen=False):
		self.group = group ## the 3d group
		
		self.settings = {"points_width":5}
		
		self.window = tk.Tk()
		self.window.winfo_toplevel().title("3D render")
		
		if fullscreen: self.window.attributes("-zoomed", True)
		
		self.window.update()
		self.height = height if height and not fullscreen else self.window.winfo_height()
		self.width = width if width and not fullscreen else self.window.winfo_width()
		
		self.canvas = tk.Canvas(self.window, bg=bg, height=self.height, width=self.width)
		self.canvas.configure(scrollregion=(-self.width/2,-self.height/2, self.width/2, self.height/2)) ##setting 0,0 in the center
		self.canvas.pack()
		
		self.mouse_lock = False
		self.select_all = False
		
		###KEYBOARD
		self.window.bind('<KeyPress>', self.key_commands)
		
		###MOUSE
		self.mouse_pressed = {"left":False, "right":False, "middle": False}
		self.last_mouse_pos = {"x":0, "y":0}
		self.canvas.bind('<ButtonPress>', self.on_mouse_pressed)
		self.canvas.bind('<ButtonRelease>', self.on_mouse_released)
		self.canvas.bind('<Motion>', self.mouse_motion)

	def on_mouse_pressed(self, event):
		if event.num == 5: ##zooming out
			self.group.set_scale(1-0.05)
		
		if event.num == 4: ##zooming in
			self.group.set_scale(1+0.05)
			
		if event.num == 3: self.mouse_pressed["right"] = True ## move 3d world
		if event.num == 2: self.mouse_pressed["middle"] = True ## rotate 3d world
		
		if event.num == 1:
			self.mouse_pressed["left"] = True ## pan 3d world
			
			for p in self.group.points: ##select point
				scrolled_x = int(event.x-self.width/2) ## moving x because origin is center, not top left
				scrolled_y = int(event.y-self.height/2)
												
				if scrolled_x in list(range(int(p.x), int(p.x)+self.settings["points_width"]+10)) and scrolled_y in list(range(int(p.y), int(p.y)+self.settings["points_width"]+10)):
					p.selected = not p.selected
					break

		
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
		
		if not self.mouse_lock:
			if self.mouse_pressed["right"]: ## move the 3d world around
				if abs(d_x) > mouse_movement_speed or abs(d_y) > mouse_movement_speed: ## updating every ${mouse_movement_speed}px
					d_x = np.sign(d_x) * mouse_movement_speed ## limit the number
					d_y = np.sign(d_y) * mouse_movement_speed
					
					self.last_mouse_pos["x"] = event.x
					self.last_mouse_pos["y"] = event.y
					
					self.group.y_rotate(-d_x/100) ## it seems a - here and a + bottom works perfectly. nice.
					self.group.x_rotate(+d_y/100)
			
			if self.mouse_pressed["middle"]: ## rotating the 3d world around z-axis
				if abs(d_x) > mouse_rotation_speed or abs(d_y) > mouse_rotation_speed: ## updating every ${mouse_rotation_speed}px
					d_x = np.sign(d_x) * mouse_rotation_speed ## limit the number
					
					self.last_mouse_pos["x"] = event.x
													
					self.group.z_rotate(-d_x/100)
			
			if self.mouse_pressed["left"]: ## panning the 3d world
				if abs(d_x) > mouse_movement_speed or abs(d_y) > mouse_movement_speed: ## updating every ${mouse_movement_speed}px
					d_x = np.sign(d_x) * mouse_movement_speed ## limit the number
					d_y = np.sign(d_y) * mouse_movement_speed
					
					self.last_mouse_pos["x"] = event.x
					self.last_mouse_pos["y"] = event.y
					
					self.group.set_pan(d_x, d_y)
	
	def key_commands(self, event):
		print(event)
		
		if event.state == 20 and event.keycode == 24: ## if ctrl+a ## select all
			self.select_all = not self.select_all
			for p in self.group.points:
				p.selected = self.select_all 
		if event.char == "p": ## add a point
			pass
		if event.char == "l": ## add a line when selecting two points
			pass
