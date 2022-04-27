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
        #t1 = Tex("test").scale(0.8)
        #self.play(Write(t1))
        graph_list = VGroup()
        prev_scale, prev_camera_scale = 1,1
        #displayed_name = Tex('')
        #self.add(displayed_name)
        def plot_line_graph(item, prev_scale, name, prev_name):
            scale_factor = 0
            xs = [x for x,_ in item]
            ys = [y for _,y in item]
            max_x, min_x, max_y, min_y = max(xs), min(xs), max(ys), 0
            mid_x, mid_y = (max_x+min_x)/2, max_y/2
            camera_x = 6*(mid_x-axes_max_x/2)/(axes_max_x/2)
            camera_y = 3*(mid_y-axes_max_y/2)/(axes_max_y/2)
            scale_factor_y = axes_max_y/(max_y-min_y)
            scale_factor_x = axes_max_x/(max_x-min_x)
            #camera_scale_factor = prev_camera_scale*(axes_max_y/max_y)
            scale_factor = 10/prev_scale if min(axes_max_y/(max_y-min_y), axes_max_x/(max_x-min_x)) > 10 else min(scale_factor_x, scale_factor_y)/prev_scale
            current_scale_factor = scale_factor*prev_scale
            prev_scale = min(axes_max_y/(max_y-min_y), axes_max_x/(max_x-min_x), 10)
            if prev_name is not None:
                self.play(Transform(prev_name, Tex(name)))
            else:
                prev_name = Tex(name)
                self.play(Write(prev_name))
            #displayed_name = Tex(name)
            #self.play(Write(name))
            self.play(self.camera.frame.animate.scale(1/scale_factor).move_to([camera_x - 6*0*(max_x-min_x)/axes_max_x, camera_y, 0]))
            #self.play(ApplyMatrix([[1, 0], [0, scale_factor]], VGroup(axes, graph_list)))
            #self.play(Transform(t1, Tex(str(min_x) + ", "+ str(mid_x)+ ", " + str(max_x)).scale(0.8)))
            #self.play(Transform(t1, Tex(str(1/min(scale_factor_y, scale_factor_x))).scale(0.8)))
            #print(prev_scale)
            #print(current_scale_factor)
            #print(1/(min(scale_factor_y, scale_factor_x)/prev_scale))
            print('xs:', xs)
            print('ys:', ys)
            new_graph = axes.plot_line_graph(x_values=xs, y_values=ys, add_vertex_dots=False, stroke_width = 1)
            graph_list.add(new_graph)
            self.play(Create(new_graph))
            return prev_scale, prev_name

        self.add(axes)
        values = cumulated_revenue_by_rent_time_from_first.values().__reversed__() if reverse == False else cumulated_revenue_by_rent_time_from_first.values()
        test = cumulated_revenue_by_rent_time_from_first.keys().__reversed__() if reverse == False else cumulated_revenue_by_rent_time_from_first.keys()
        prev_name=None
        for item, name in zip(values, test):
            print('key:', name)
            if name[0] == '★': name= name[2:]
            help, help2 = plot_line_graph(item["revenue_history"], prev_scale, name, prev_name)
            prev_scale = help
            prev_name = help2
        self.play(self.camera.frame.animate.scale(prev_scale).move_to([0,0,0]))
