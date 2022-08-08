def line(x0, y0, x1, y1):
	"Bresenham's line algorithm"
	points_in_line = []
	dx = abs(x1 - x0)
	dy = abs(y1 - y0)
	x, y = x0, y0
	sx = -1 if x0 > x1 else 1
	sy = -1 if y0 > y1 else 1
	if dx > dy:
		err = dx / 2.0
		while x != x1:
			points_in_line.append((x, y))
			err -= dy
			if err < 0:
				y += sy
				err += dx
			x += sx
	else:
		err = dy / 2.0
		while y != y1:
			points_in_line.append((x, y))
			err -= dx
			if err < 0:
				x += sx
				err += dy
			y += sy
	points_in_line.append((x, y))
	return points_in_line


a = line(0, 5, 5, 5)

print(a)
