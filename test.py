from render import *

###CAD:
## workplanes: 2d, 3d
## can only draw on 2d then extrude to 3d
## lines/edges.
##constraints: horizental, vertical...
## chamfer and fillet on 3d

g = Group()
g.set_default_cube()
g.set_scale(100)

gui = GUI(g, "cyan", 600, 600)

def draw():
	gui.canvas.delete("all") ##clearing the canvas before redrawing
	
	for p in g.points:
		gui.canvas.create_rectangle(p.x, p.y, p.x+5, p.y+5, fill="white") ##drawing points
	
	gui.canvas.after(50, draw) ##draw every 50ms

draw()
gui.window.mainloop()
