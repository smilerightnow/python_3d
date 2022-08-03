from render import *

g = Group()
g.set_default_cube()


print(g.get_coordinates())


g.x_rotate(30)

print(g.get_coordinates())
