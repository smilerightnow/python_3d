from render import *

###CAD:
## selecting points.
## lines/edges.
## extrude points and lines.
##constraints: horizental, vertical...
## chamfer and fillet on 3d

g = Group()
g.set_default_cube()
g.set_scale(100)

gui = GUI(g, "cyan", 600, 600)

def draw():
	gui.canvas.delete("all") ##clearing the canvas before redrawing
	
	for p in sorted(g.points, key=lambda x:x.selected):
		gui.canvas.create_rectangle(p.x, p.y, p.x+gui.settings["points_width"], p.y+gui.settings["points_width"], fill="red" if p.selected else "white") ##drawing points
		
	gui.canvas.after(50, draw) ##draw every 50ms

draw()
gui.window.mainloop()


###TOFIX:
## make the model rotate/move relative to its center. this is a problem when a model has been moved/panned (is not in the center) of the screen.
