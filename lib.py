import numpy as np
import tkinter as tk

def distance_between_two_points(p1, p2):
	return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)

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

class Edge:
	def __init__(self, two_points):
		self.two_points = two_points
		self.p1 = two_points[0]
		self.p2 = two_points[1]
		self.selected = False

	def chamfer(self, current_group):
		value = 0.3 ##will be modifiable with gui
		
		shared_edges = []
		for edge in current_group.edges:
			if edge.two_points == self.two_points: continue
			if self.p1 in edge.two_points or self.p2 in edge.two_points:
				shared_edges.append(edge)
		
		if len(shared_edges)>4:
			print("only 4 shared edges allowed for chamfer")
		
		## I need to add 4 points. one on each shared edge.
		new_points = []
		for edge in shared_edges:
			new_p = []
			if distance_between_two_points(self.p1.get_coordinates(), [(edge.p2.x-edge.p1.x)*value+edge.p1.x,(edge.p2.y-edge.p1.y)*value+edge.p1.y,(edge.p2.z-edge.p1.z)*value+edge.p1.z]) < distance_between_two_points(self.p1.get_coordinates(), [(edge.p1.x-edge.p2.x)*value+edge.p2.x,(edge.p1.y-edge.p2.y)*value+edge.p2.y,(edge.p1.z-edge.p2.z)*value+edge.p2.z]) or distance_between_two_points(self.p2.get_coordinates(), [(edge.p2.x-edge.p1.x)*value+edge.p1.x,(edge.p2.y-edge.p1.y)*value+edge.p1.y,(edge.p2.z-edge.p1.z)*value+edge.p1.z]) < distance_between_two_points(self.p2.get_coordinates(), [(edge.p1.x-edge.p2.x)*value+edge.p2.x,(edge.p1.y-edge.p2.y)*value+edge.p2.y,(edge.p1.z-edge.p2.z)*value+edge.p2.z]): ##comparing the distance to place the new points in the nearest place to the selected edge points.
				
				new_p = [(edge.p2.x-edge.p1.x)*value+edge.p1.x,(edge.p2.y-edge.p1.y)*value+edge.p1.y,(edge.p2.z-edge.p1.z)*value+edge.p1.z]
				current_group.add_point(new_p)
			else:
				new_p = [(edge.p1.x-edge.p2.x)*value+edge.p2.x,(edge.p1.y-edge.p2.y)*value+edge.p2.y,(edge.p1.z-edge.p2.z)*value+edge.p2.z]
				current_group.add_point(new_p)
			
			new_points.append(new_p)
			##conneting the new points with old points
			if self.p1 is edge.p1 or self.p2 is edge.p1: edge.p1 = current_group.get_point_index(new_p)
			if self.p1 is edge.p2 or self.p2 is edge.p2: edge.p2 = current_group.get_point_index(new_p)
		
		##connecting the new points to each other
		sorted_new_points = []
		for n in new_points:#####calculating distance between new points:
			for nn in new_points:
				if not n is nn:
					sorted_new_points.append([n, nn, distance_between_two_points(n, nn)])
			break
		sorted_new_points = sorted(sorted_new_points, key=lambda x:x[2])
				
		current_group.edges.append(Edge([current_group.get_point_index(sorted_new_points[0][0]), current_group.get_point_index(sorted_new_points[0][1])]))
		current_group.edges.append(Edge([current_group.get_point_index(sorted_new_points[1][0]), current_group.get_point_index(sorted_new_points[1][1])]))
		current_group.edges.append(Edge([current_group.get_point_index(sorted_new_points[0][1]), current_group.get_point_index(sorted_new_points[2][1])]))
		current_group.edges.append(Edge([current_group.get_point_index(sorted_new_points[1][1]), current_group.get_point_index(sorted_new_points[2][1])]))
		
		##removing the selected line and points
		current_group.points.remove(self.p1)
		current_group.points.remove(self.p2)
		current_group.edges.remove(self)
	
	def fillet(self):
		pass

class Group:
	def __init__(self):
		self.points = []
		self.edges = []
	
	def set_default_cube(self): ## this is just a function that draws a cube. 
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
				
		self.edges.extend([
			Edge([self.points[2], self.points[6]]),
			Edge([self.points[3], self.points[7]]),
			Edge([self.points[2], self.points[3]]),
			Edge([self.points[6], self.points[7]]),
			Edge([self.points[0], self.points[3]]),
			Edge([self.points[4], self.points[7]]),
			Edge([self.points[0], self.points[4]]),
			Edge([self.points[0], self.points[1]]),
			Edge([self.points[1], self.points[5]]),
			Edge([self.points[1], self.points[2]]),
			Edge([self.points[5], self.points[6]]),
			Edge([self.points[4], self.points[5]])
		])
	
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
			if isinstance(c, Point):
				self.points.append(c)
			else:
				self.points.append(Point(c[0], c[1], c[2]))
	
	def add_point(self, c):
		if isinstance(c, Point):
			self.points.append(c)
		else:
			self.points.append(Point(c[0], c[1], c[2]))
	
	def get_point_index(self, coor):
		for p in self.points:
			if coor == p.get_coordinates():
				return p
	
	def get_coordinates(self):
		coor = []
		for p in self.points:
			coor.append(p.get_coordinates())
		return coor
	
	def get_selected(self):
		selected = {"points":[], "edges":[]}
		for p in self.points:
			if p.selected:
				selected["points"].append(p)
		for e in self.edges:
			if e.selected:
				selected["edges"].append(e)
		return selected
	
	def get_edges_points(self): ##endpoints of all lines: [[Point, Point],...]
		p = []
		for e in self.edges:
			p.append(e.two_points)
		return p
	
	def clear_selection(self):
		for a in self.points+self.edges:
			if a.selected:
				a.selected = False
	
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
		
		self.settings = {"point_width":5, "line_width":2, "line_color": "#2e2e2e", "point_color": "white", "point_selected_color": "red"}
		
		self.window = tk.Tk()
		self.window.winfo_toplevel().title("3D render")
		
		if fullscreen: self.window.attributes("-zoomed", True)
		
		self.window.update()
		self.height = height if height and not fullscreen else self.window.winfo_height()
		self.width = width if width and not fullscreen else self.window.winfo_width()
		
		self.canvas = tk.Canvas(self.window, bg=bg, height=self.height, width=self.width)
		self.canvas.configure(scrollregion=(-self.width/2,-self.height/2, self.width/2, self.height/2)) ##setting 0,0 in the center
		self.canvas.pack()
		
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
			
			selected_something = False
			scrolled_x = int(event.x-self.width/2) ## moving x because origin is center, not top left
			scrolled_y = int(event.y-self.height/2)
			for p in self.group.points: ##select point
				if scrolled_x in list(range(int(p.x), int(p.x)+self.settings["point_width"]+10)) and scrolled_y in list(range(int(p.y), int(p.y)+self.settings["point_width"]+10)):
					p.selected = not p.selected
					selected_something = True
					break ## selecting the first point and stop. don't select two points at the same time.
			
			if not selected_something:
				for e in self.group.edges:
					
					##drawing a rectangle around the line
					x_center = int((e.p1.x + e.p2.x) / 2)
					y_center = int((e.p1.y + e.p2.y) / 2)
					dist = np.sqrt( (e.p2.x - e.p1.x)**2 + (e.p2.y - e.p1.y)**2 )
					dx = abs(e.p2.x - e.p2.y)
					dy = abs(e.p2.y - e.p1.y)
					horizental = int(dist/4) if dx>dy else int(dist/10)
					vertical = int(dist/4) if dx<dy else int(dist/10)
					##
					
					if scrolled_x in list(range(x_center-horizental, x_center+horizental)) and scrolled_y in list(range(y_center-vertical, y_center+vertical)):
						e.selected = not e.selected
						selected_something = True
						break
			
			if not selected_something:
				self.group.clear_selection()

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
		# print(event)
		if event.state == 20 and event.keycode == 24: ## if ctrl+a ## select all
			self.select_all = not self.select_all
			for a in self.group.points+self.group.edges:
				a.selected = self.select_all 
		if event.char == "p": ## add a point
			pass
		if event.char == "f": ## fillet line
			pass
		
		if event.char == "c": ## chamfer line
			group_selected = self.group.get_selected()
			if len(group_selected["edges"]) == 1:
				group_selected["edges"][0].chamfer(self.group)
			self.group.clear_selection()
			
		if event.char == "l": ## add a line when selecting two points
			group_selected = self.group.get_selected()
			current_edges = self.group.get_edges_points()
			if len(group_selected["points"]) == 2:
				if not group_selected["points"] in current_edges: ## if it's not already a line.
					self.group.edges.append(Edge(group_selected["points"]))
			self.group.clear_selection()
