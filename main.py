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

        tree.display(self)
        self.wait()