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



'''
Here are several strong arguments that highlight why barycentric coordinates could be a valuable tool for this type of application:

1. Accurate Point Positioning within Complex Zones
Fine Control: Barycentric coordinates allow you to precisely locate a point within a triangular zone. This precision can be highly useful if your project requires not just determining whether the fisherman is inside a safety zone, but also how far or how close the point is to critical boundaries or danger zones.
Edge and Vertex Detection: The use of barycentric coordinates naturally helps detect if a point is on an edge or at a vertex. This makes it easy to apply specific safety rules for fishermen if they are close to these critical points (e.g., if approaching a border where strong currents begin).
2. Interpolation of Safety Metrics
Dynamic Data Interpolation: If you are working with zones where safety metrics (such as danger levels, weather conditions, or proximity to resources like lifeboats) vary across the area, barycentric coordinates allow for easy interpolation between the vertices of the triangle. For example, you could assign different risk levels to the vertices and smoothly interpolate the risk for any point inside the triangle.
Advanced Situational Awareness: Knowing the exact position within a triangle (using coordinates u,v,w) could help you map risk gradients, where danger increases gradually as the fisherman drifts closer to a specific danger point. This is particularly useful for early warnings.
3. Natural Decomposition of Zones
Triangulation Helps with Complex Zones: If you are dividing the fishing area into zones of varying danger, triangulating the region and applying barycentric coordinates is an effective way to manage and monitor these zones. Each triangular sub-region can have its own safety conditions or rules, allowing for fine-tuned safety monitoring.
Adaptability for Concave Regions: Even if the safety zones are complex (concave polygons), decomposing them into triangles allows for easier computation and analysis. Many triangulation algorithms can handle complex shapes, giving you the benefit of barycentric coordinates even in non-trivial polygons.
4. Speed and Efficiency for Repeated Queries
Once Triangulated, Fast Checks: Once you have triangulated a safety zone, you can reuse the triangular mesh to quickly and efficiently determine a point's location within any part of the zone. For real-time applications (such as tracking multiple fishing vessels at sea), this can significantly improve performance as the computations for a point inside a triangle are simple and fast.
Batch Processing of Data: If you're tracking multiple boats at once, barycentric coordinates allow you to efficiently process the safety data for many points across the triangles without needing to reprocess the entire polygon.
5. Handling of 3D Data (Future Expansion)
Extension to 3D: If your fisherman safety project ever evolves to include 3D data (e.g., depth or height information for certain hazards or zones), barycentric coordinates can be extended to tetrahedrons in 3D space. This would allow you to model not only the 2D safety zones on the surface of the water but also incorporate underwater hazards or weather systems in a more comprehensive safety model.
6. Real-World Usage in Similar Applications
Used in Geographic and Simulation Models: Barycentric coordinates are widely used in geospatial applications, such as weather modeling, disaster zones, and terrain mapping, where interpolation between points is necessary. For instance, interpolating wind speeds or wave heights within triangular areas can help predict hazardous conditions for fishermen.
Finite Element Method (FEM): In engineering simulations and disaster preparedness modeling, barycentric coordinates are often used to break down complex regions into smaller triangles or tetrahedrons for precise analysis. For example, predicting how a current affects a vessel in a specific triangular region could provide actionable insights.
7. Detailed Visualization of Safety Zones
Visualization and Graphics: If your project involves presenting visual safety maps to fishermen, barycentric coordinates are well-suited to rendering smooth gradients across safety zones. Triangulating areas allows for clear, visually appealing maps where risk is displayed in a continuous, intuitive way. This could make it easier for fishermen to understand safe routes or danger areas based on their location.
Conclusion:
While point-in-polygon methods are simpler for basic "inside-outside" tests, barycentric coordinates provide a richer set of tools for detailed positional information, interpolation of data, and real-time safety monitoring. In the context of your fisherman safety project, barycentric coordinates offer fine-grained control, particularly when triangulating safety zones and monitoring dynamic risk factors. If your safety model needs to expand in complexity or precision (e.g., considering weather, risks, or underwater hazards), 
barycentric coordinates will provide the flexibility and precision required for advanced analysis and visualization.
'''









