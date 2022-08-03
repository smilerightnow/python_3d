from render import *
import numpy as np
import tkinter

g = Group()
g.set_default_cube()

print(g.get_coordinates())

g.set_scale(100)

top = tkinter.Tk()

C = tkinter.Canvas(top, bg="cyan", height=500, width=500)

def do():
	C.delete("all")

	g.y_rotate((g.x_angle+0.02))
	g.x_rotate((g.y_angle+0.02))
	g.z_rotate((g.z_angle+0.02))
	
	for p in g.points:
		C.create_rectangle(p.x, p.y, p.x+5, p.y+5, fill="white")
	
	C.after(50, do)


C.pack()


##making 0 the origin
C.configure(scrollregion=(-250,-250, 250, 250))


do()

top.mainloop()
