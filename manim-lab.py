from manim import *
from objects import *
from processing import *
from animations import *

dots_color=[RED, ManimColor("#2f9e44"), ManimColor("#228be6"), ManimColor("#a5d8ff"), GREY]
lines_color = [YELLOW, ORANGE, PURPLE]

class Test(Scene):
    def construct(self):
        BTree = BinaryTree(root=buildTree(dots_color, 7), x_start=0, x_distance=3, y_start=3 ,y_distance=1, dots_color=dots_color, lines_color=lines_color)
        BTree.build_structure(BTree.root)
        BTree.display(self)
        level_ordered_tags = BTree.get_level_ordered_tags()
        initial_dot = Dot()
        initial_dot.move_to(BTree.entry_dot.get_center())
        initial_dot.generate_target()
        self.play(FadeIn(initial_dot))
        self.play(initial_dot.animate.move_to(level_ordered_tags[0][0]))
        level_initial_dots = [VGroup(initial_dot)]
        height = BTree.root.get_height()
    
        for i in range(height+1):
            level_dots = VGroup()
            #for every dot currently in that level
            for a, dot in enumerate(level_initial_dots[i]):
                self.play(Indicate(dot), run_time=2)

                my_left_L = level_ordered_tags[2**(i)+a-1][1]
                left_dot = self.create_branching_dot(dot, my_left_L)
                level_dots.add(left_dot)
            

                my_right_L = level_ordered_tags[2**(i)+a-1][2]
                right_dot = self.create_branching_dot(dot, my_right_L)
                level_dots.add(right_dot)
            self.play(AnimationGroup(*[MoveAlongPath(dot, dot.L) for dot in level_dots]), run_time=2*(i+1))
            level_initial_dots.append(level_dots)

        traced_paths = [m for m in self.mobjects if isinstance(m, TracedPath)]
        self.play(*[FadeOut(tp) for tp in traced_paths])
        self.remove(*[tp for tp in traced_paths])

        for h in range(height+1, 0, -1):
            level_dots = level_initial_dots[h]
            for dot in level_dots:
                self.add_tracer(dot)
            self.play(AnimationGroup(*[MoveAlongPath(dot, dot.L, rate_func=lambda t:1-t) for dot in level_dots]), run_time=2)
            self.play(AnimationGroup(*[FadeOut(dot) for dot in level_dots]), run_time=2)
        self.play(initial_dot.animate.move_to(BTree.entry_dot))
        self.play(FadeOut(initial_dot))
    
    def create_branching_dot(self, parent_dot, path_segments, tracer_color=YELLOW):
        dot = Dot()
        dot.move_to(parent_dot.get_center())
        dot.original_pos = dot.get_center()
        dot.L = VMobject()
        dot.L.set_points_as_corners([path_segments[0].start, path_segments[0].end, path_segments[1].end])
        self.add_tracer(dot, tracer_color)
        return dot
    
    def add_tracer(self, dot, tracer_color=YELLOW):
        dot.tracer = TracedPath(dot.get_center, stroke_color=tracer_color, stroke_width=4)
        self.add(dot.tracer)
            

