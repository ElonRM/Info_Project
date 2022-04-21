from manim import *
from data_analysis import *

class testScene(MovingCameraScene):
    def construct(self):
        axes_max_x = 500
        axes_max_y = 200
        axes = Axes(
            x_range =[0, axes_max_x, 30],
            y_range = [0, axes_max_y, 10],
            x_length = 12,
            y_length = 6
        )
        t1 = Tex("test").scale(0.8)
        self.play(Write(t1))
        def plot_line_graph(item):
            xs = [x for x,_ in item]
            ys = [y for _,y in item]
            max_x, min_x, max_y, min_y = max(xs), min(xs), max(ys), min(ys)
            mid_x, mid_y = (max_x+min_x)/2, (max_y+min_y)/2
            camera_x = 6*(mid_x-axes_max_x/2)/(axes_max_x/2)
            #s1 = str(min_x) + ", "+ str(mid_x)+ ", " + str(max_x)
            self.play(Transform(t1, Tex(str(min_x) + ", "+ str(mid_x)+ ", " + str(max_x)).scale(0.8)))
            self.play(self.camera.frame.animate.move_to([camera_x,0,0]))
            return axes.plot_line_graph(x_values=xs, y_values=ys, add_vertex_dots=False, stroke_width = 1)

        self.add(axes)

        for item in cumulated_revenue_by_rent_time_from_first.values().__reversed__():
            self.play(Write(plot_line_graph(item["revenue_history"])))
