from render import *
import numpy as np
import tkinter

g = Group()
g.set_default_cube()
g.set_scale(100)

print(g.get_coordinates())

top = tkinter.Tk()

C = tkinter.Canvas(top, bg="cyan", height=500, width=500)
##making 0 the origin
C.configure(scrollregion=(-250,-250, 250, 250))


def draw():
	C.delete("all")

	g.y_rotate((g.x_angle+0.02))
	g.x_rotate((g.y_angle+0.02))
	g.z_rotate((g.z_angle+0.02))
	
	for p in g.points:
		C.create_rectangle(p.x, p.y, p.x+5, p.y+5, fill="white")
	
	C.after(50, draw)


C.pack()
draw()
top.mainloop()
