import tkinter as tk
import random
import math
border = 20

class TrianglePointApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Triangle Point App")
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        # Define triangle coordinates
        self.triangle_coords = [100, 300, 200, 100, 300, 300, 100, 300]

        # Define point coordinates
        self.point_coords = [random.randint(100, 400), random.randint(100, 400)]

        # Draw triangle with a thick border
        self.triangle = self.canvas.create_polygon(self.triangle_coords, fill='blue', outline='black', width=1)

        # Draw point and store its ID
        self.point = self.canvas.create_oval(self.point_coords[0]-5, self.point_coords[1]-5, self.point_coords[0]+5, self.point_coords[1]+5, fill='red')

        # Bind mouse events to move point
        self.canvas.bind('<Button-1>', self.start_move_point)
        self.canvas.bind('<B1-Motion>', self.move_point)
        self.canvas.bind('<ButtonRelease-1>', self.stop_move_point)

        self.moving_point = False

    def start_move_point(self, event):
        self.moving_point = True

    def move_point(self, event):
        if self.moving_point:
            # Get mouse coordinates
            x, y = event.x, event.y

            # Update point coordinates
            self.point_coords = [x, y]

            # Delete only the point and redraw it
            self.canvas.delete(self.point)  # Only delete the point, not the entire canvas
            self.point = self.canvas.create_oval(self.point_coords[0]-5, self.point_coords[1]-5, self.point_coords[0]+5, self.point_coords[1]+5, fill=self.get_point_color(self.point_coords, self.triangle_coords))

    def stop_move_point(self, event):
        self.moving_point = False

    def is_point_inside_triangle(self, point, triangle):
        x1, y1 = triangle[0], triangle[1]
        x2, y2 = triangle[2], triangle[3]
        x3, y3 = triangle[4], triangle[5]
        x, y = point

        # Calculate the denominator for barycentric coordinates
        denominator = ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
        if denominator == 0:
            return False  # Degenerate triangle

        # Calculate barycentric coordinates (u, v, w)
        u = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
        v = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
        w = 1 - u - v

        # Check if point is inside the triangle (all barycentric coordinates between 0 and 1)
        return (0 <= u <= 1) and (0 <= v <= 1) and (0 <= w <= 1)

    def is_point_on_border(self, point, triangle, border_thickness=border):
        x1, y1 = triangle[0], triangle[1]
        x2, y2 = triangle[2], triangle[3]
        x3, y3 = triangle[4], triangle[5]
        x, y = point

        # Check distance to each line segment
        dist1 = self.distance_to_line(x, y, x1, y1, x2, y2)
        dist2 = self.distance_to_line(x, y, x2, y2, x3, y3)
        dist3 = self.distance_to_line(x, y, x3, y3, x1, y1)

        # Check if any distance is within the border thickness
        return dist1 < border_thickness or dist2 < border_thickness or dist3 < border_thickness

    def distance_to_line(self, x, y, x1, y1, x2, y2):
        """Calculate the perpendicular distance from a point (x, y) to a line segment from (x1, y1) to (x2, y2)."""
        # Calculate the perpendicular distance
        numerator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        denominator = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        return numerator / denominator

    def get_point_color(self, point, triangle):
        # Check if point is inside the triangle first
        if self.is_point_inside_triangle(point, triangle):
            # Check if it's near the border (within half the border's thickness)
            if self.is_point_on_border(point, triangle, border_thickness=border // 2):
                return 'yellow'  # Inside and near the border
            else:
                return 'green'   # Inside but not near the border
        else:
            return 'red'  # Outside the triangle



root = tk.Tk()
app = TrianglePointApp(root)
root.mainloop()










