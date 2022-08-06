from render import *

###TODO:
## move 3d model with mouse
## workplanes: 2d, 3d
## can only draw on 2d then extrude to 3d
## chamfer and fillet on 3d

g = Group()
g.set_default_cube()
g.set_scale(100)

gui = GUI(g, "cyan", 600, 600)

def draw():
	gui.canvas.delete("all") ##clearing the canvas before redrawing

	# g.y_rotate((g.x_angle+0.02))
	# g.x_rotate((g.y_angle+0.02))
	# g.z_rotate((g.z_angle+0.02))
	
	for p in g.points:
		gui.canvas.create_rectangle(p.x, p.y, p.x+5, p.y+5, fill="white") ##drawing points
	
	gui.canvas.after(50, draw) ##draw every 50ms

draw()
gui.window.mainloop()
