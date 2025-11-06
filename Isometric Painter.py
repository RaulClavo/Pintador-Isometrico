import tkinter as tk
import math

num_columns, num_rows = 35, 15
triangle_size, padding = 40, 2
triangle_height = triangle_size * (3 ** 0.5) / 2
current_color = "#ff0000"
triangles = []

root = tk.Tk()
root.title("Isometric Painter")

canvas_width = num_columns * triangle_height + triangle_height
canvas_height = num_rows * triangle_size + triangle_size / 2
canvas = tk.Canvas(root, width=canvas_width + 2 * padding, height=canvas_height + 2 * padding, bg="white")
canvas.grid(row=0, column=0, columnspan=8, padx=8, pady=8)

# Color buttons
colors = {"Red": "#ff0000", "Yellow": "#ffff00", "Blue": "#0000ff", "Green": "#00ff00", "Orange": "#ffa500", "Violet": "#8000ff", "White": "#ffffff", "Reset": "reset"}

def point_in_triangle(point, a, b, c):
    x, y = point
    x1, y1 = a; x2, y2 = b; x3, y3 = c
    denominator = (y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3)
    if denominator == 0:
        return False
    u = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / denominator
    v = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / denominator
    return 0 <= u <= 1 and 0 <= v <= 1 and u + v <= 1

def draw_grid():
    canvas.delete("all")
    triangles.clear()
    for row in range(num_rows):
        for column in range(num_columns):
            base_x = column * triangle_height
            base_y = row * triangle_size + (triangle_size / 2) * (column % 2)

            upper_triangle = (
                (base_x, base_y + triangle_size / 2),
                (base_x + triangle_height, base_y),
                (base_x + triangle_height, base_y + triangle_size)
            )
            lower_triangle = (
                (base_x + triangle_height, base_y),
                (base_x + 2 * triangle_height, base_y + triangle_size / 2),
                (base_x + triangle_height, base_y + triangle_size)
            )

            for triangle in (upper_triangle, lower_triangle):
                coords = [coord for point in triangle for coord in point]
                shape_id = canvas.create_polygon(*coords, outline="gray", fill="")
                triangles.append({'points': triangle, 'id': shape_id})

def find_triangle(x, y):
    for triangle_index in reversed(range(len(triangles))):
        if point_in_triangle((x, y), *triangles[triangle_index]['points']):
            return triangle_index
    return None

def on_left_click(event):
    index = find_triangle(event.x, event.y)
    if index is not None:
        canvas.itemconfig(triangles[index]['id'], fill=current_color)

def on_right_click(event):
    index = find_triangle(event.x, event.y)
    if index is None:
        return
    triangle = triangles.pop(index)
    canvas.delete(triangle['id'])

    a, b, c = triangle['points']
    click_point = (event.x, event.y)
    closest_vertex = min((a, b, c), key=lambda p: math.dist(p, click_point))
    opposite_vertices = [p for p in (a, b, c) if p != closest_vertex]
    midpoint = (
        (opposite_vertices[0][0] + opposite_vertices[1][0]) / 2,
        (opposite_vertices[0][1] + opposite_vertices[1][1]) / 2
    )

    for new_triangle in [
        (closest_vertex, opposite_vertices[0], midpoint),
        (closest_vertex, opposite_vertices[1], midpoint)
    ]:
        coords = [coord for point in new_triangle for coord in point]
        shape_id = canvas.create_polygon(*coords, outline="black", fill="")
        triangles.append({'points': new_triangle, 'id': shape_id})

def set_color(picked_color):
    global current_color
    current_color = picked_color


for i, (name, color) in enumerate(colors.items()):
    command = draw_grid if color == "reset" else lambda picked_color=color: set_color(picked_color)
    tk.Button(root, text=name, bg="white" if color == "reset" else color, width=10, height=2, command=command).grid(row=1, column=i, sticky="ew", padx=3, pady=3)

draw_grid()
canvas.bind("<Button-1>", on_left_click)
canvas.bind("<Button-3>", on_right_click)
root.mainloop()
