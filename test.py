from render import *
import numpy as np
import tkinter

g = Group()
g.set_default_cube()


print(g.get_coordinates())


g.y_rotate(30)
g.x_rotate(30)

print(g.get_coordinates())

g.set_scale(100)
g.set_pan(250)


top = tkinter.Tk()

C = tkinter.Canvas(top, bg="blue", height=500, width=500)


for p in g.get_coordinates():
	C.create_rectangle(p[0], p[1], list(np.array(p) + 5)[0], list(np.array(p) + 5)[1], fill="red")

C.pack()
top.mainloop()
