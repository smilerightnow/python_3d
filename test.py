from render import *
import numpy as np
import tkinter

g = Group()
g.set_default_cube()


print(g.get_coordinates())


g.y_rotate(0)
g.x_rotate(0)

print(g.get_coordinates())

g.set_scale(100)
# g.set_pan(250)


top = tkinter.Tk()

C = tkinter.Canvas(top, bg="blue", height=500, width=500)

i = 0

def do():
	C.delete("all")
	global i
	i += 0.01
	g.y_rotate(i)
	g.x_rotate(i)
	g.z_rotate(i)
	for p in g.get_coordinates():
		C.create_rectangle(p[0], p[1], list(np.array(p) + 5)[0], list(np.array(p) + 5)[1], fill="red")
	
	C.after(50, do)


C.pack()


##making 0 the origin
C.configure(scrollregion=(-250,-250, 250, 250))


do()

top.mainloop()
