from render import *

###CAD:
## extrude points and lines.
##constraints: horizental, vertical...
## chamfer and fillet on 3d

g = Group()
g.set_default_cube()

gui = GUI(g, "cyan", 600, 600)

def draw():
	gui.canvas.delete("all") ##clearing the canvas before redrawing

	for p in sorted(g.points, key=lambda x:x.selected): ##drawing points
		gui.canvas.create_rectangle(p.x, p.y, p.x+gui.settings["points_width"], p.y+gui.settings["points_width"], fill="red" if p.selected else "white")
	
	for e in g.edges: ##drawing edges
		gui.canvas.create_line(e[0].x, e[0].y, e[1].x, e[1].y, fill="#2e2e2e", width=2)
			
	gui.canvas.after(50, draw) ##draw every 50ms

draw()
gui.window.mainloop()


###TOFIX:
## make the model rotate/move relative to its center. this is a problem when a model has been moved/panned (is not in the center) of the screen.
