from lib import *

###CAD:
## fillet
## add top view, side view...etc
## extrude points and lines.
## constraints: horizental, vertical...

g = Group()
g.set_default_cube()

gui = GUI(g, "cyan", 600, 600)

def draw():
	gui.canvas.delete("all") ##clearing the canvas before redrawing

	for p in sorted(g.points, key=lambda x:x.selected): ##drawing points
		gui.canvas.create_rectangle(p.x, p.y, p.x+gui.settings["point_width"], p.y+gui.settings["point_width"], \
		fill=gui.settings["point_selected_color"] if p.selected else gui.settings["point_color"])
	
	for e in sorted(g.edges, key=lambda x:x.selected): ##drawing edges
		gui.canvas.create_line(e.p1.x, e.p1.y, e.p2.x, e.p2.y,\
		fill="red" if e.selected else gui.settings["line_color"],\
		width=gui.settings["line_width"], smooth=True)
			
	gui.canvas.after(50, draw) ##draw every 50ms

draw()
gui.window.mainloop()


###TOFIX:
## make the model rotate/move relative to mouse pos. this is a problem when a model has been moved/panned (is not in the center) of the screen.
## chamfered edges are not stable to chamfer again and can break the program.
