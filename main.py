from manim import *
from objects import *
dots_color=[RED, ManimColor("#2f9e44"), ManimColor("#228be6"), ManimColor("#a5d8ff"), GREY]
lines_color = [YELLOW, ORANGE, PURPLE]

class RecursiveTreeStructure(Scene):
    def construct(self):
        self.add(NumberPlane())
        self.add(Rectangle(width=9, height=4, color= RED, fill_opacity=0).set_stroke(color=RED, width=4).move_to([-2.5, 1, 0]))
        self.add(Rectangle(width=5, height=3, color= GREEN, fill_opacity=0).set_stroke(color=GREEN, width=4).move_to([4.5, -2.5,0]))
        tree = TraversalTree(root=buildTree(dots_color, 3), x_start=-10, x_distance=0.9, y_start=-2 ,y_distance=1.5, dots_color=dots_color, lines_color=lines_color)
        tree.build_structure_with_entry(tree.root)
        tree.move_to([-2.5, 1, 0])
        tree.scale_all(0.7)
        self.add(tree)
        self.wait()

        BTree1 = BTree(root=buildTree(dots_color, 3), x_start=0, x_distance=3, y_start=3 ,y_distance=1, dots_color=dots_color, lines_color=lines_color)
        BTree1.build_structure(BTree1.root)
        BTree1.move_to([4.5, -2.5,0])
        BTree1.scale_all(0.5)
        self.add(BTree1)
        self.wait(1)

        timeline = NumberLine(
            x_range=[0, 12, 1],
            length=12,
            color=WHITE,
            include_numbers=False,
            stroke_width=5,
        )
        timeline.next_to(BTree1, DOWN, buff=1)
        timeline.align_to(BTree1)
        self.add(timeline)
        self.wait(2)

        

        
