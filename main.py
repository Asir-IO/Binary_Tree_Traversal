from manim import *
from objects import *

class RecursiveTreeStructure(Scene):
    def construct(self):
        self.add(NumberPlane())
        dots_color=[RED, ManimColor("#2f9e44"), ManimColor("#228be6"), ManimColor("#a5d8ff"), GREY]
        lines_color = [YELLOW, ORANGE, PURPLE]
        tree = TraversalTree(root=buildTree(dots_color, 7), x_start=-10, x_distance=0.5, y_start=-2 ,y_distance=1.5, dots_color=dots_color, lines_color=lines_color)
        
        # Entry dot and line
        tree.draw_dot(tree.dots_color[0])
        tree.draw_line([tree.x, tree.y, 0], [tree.x + tree.x_distance, tree.y + tree.y_distance, 0], False, color=tree.lines_color[0])
        tree.x += tree.x_distance
        tree.y += tree.y_distance
        tree.build_structure(tree.root)
        
        # Exit dot and line
        tree.draw_line([tree.x - tree.x_distance, tree.y + tree.y_distance, 0], [tree.x, tree.y, 0], True, color=tree.lines_color[0])
        tree.draw_dot(tree.dots_color[0])

        tree.scale(0.6)
        tree.move_to([-(6.5+0.125), -(1+0.125), 0], aligned_edge=DL)

        tree.lines[0].z_index = 0
        tree.dots[0].z_index = 3
        self.play(Create(tree.lines[0]), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(tree.dots[0]), run_time=1)
        self.wait(0.5)

        for i, (dt, ln, tg) in enumerate(zip(tree.dots[1:], tree.lines[1:], tree.tags)):
            self.play(Create(ln), run_time=1)
            self.wait(0.5)
            self.play(FadeIn(tg), run_time=1)
            self.wait(0.5) 
        self.wait()