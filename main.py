from manim import *
from objects import *
from processing import *
from animations import *

dots_color=[RED, ManimColor("#2f9e44"), ManimColor("#228be6"), ManimColor("#a5d8ff"), GREY]
lines_color = [YELLOW, ORANGE, PURPLE]

class Scene05_Trace(Scene):
    def construct(self):
        # self.add(NumberPlane())
        # self.add(Rectangle(width=9, height=4, color= RED, fill_opacity=0).set_stroke(color=RED, width=4).move_to([-2.5, 1, 0]))
        # self.add(Rectangle(width=5, height=3, color= GREEN, fill_opacity=0).set_stroke(color=GREEN, width=4).move_to([4.5, -2.5,0]))
        LBTree = LinearizedBTree(root=buildTree(dots_color, 3), x_start=-10, x_distance=0.9, y_start=-2 ,y_distance=1.5, dots_color=dots_color, lines_color=lines_color)
        LBTree.build_structure_with_entry(LBTree.root)
        LBTree.move_to([-2.5, 1, 0])
        LBTree.scale_all(0.7)
        self.add(LBTree)
        self.wait()

        BTree = BinaryTree(root=buildTree(dots_color, 3), x_start=0, x_distance=3, y_start=3 ,y_distance=1, dots_color=dots_color, lines_color=lines_color)
        BTree.build_structure(BTree.root)
        BTree.add_double_tags()
        BTree.move_to([4.5, -2.5,0])
        BTree.scale_all(0.5)
        self.add(BTree)
        self.wait(1)

        timeline = NumberLine(
            x_range=[0, 12, 1],
            length=7,
            color=WHITE,
            include_numbers=False,
            stroke_width=5,
            tick_size=0.1,
            numbers_with_elongated_ticks=[0,12]
        )
        align_center(timeline, LBTree, 'x')
        timeline.shift(DOWN*2)
        self.add(timeline)
        for tick in timeline.ticks:
            tick.set_color(YELLOW)
        self.trace_dot_LBTree = Dot(color=YELLOW, radius=0.1).align_to(LBTree,DL)
        self.trace_circle_BTree = Circle(color=YELLOW, radius=BTree.tags[0].outline.radius+0.07).move_to(BTree.entry_dot.get_center())
        print("Radius:", BTree.tags[0].outline.radius)

        traversal_scene_data = traversal_scene(self, LBTree, BTree, timeline)
        show_order_scene(self, traversal_scene_data[0], traversal_scene_data[1], timeline)

class Scene01_Intro(Scene):
    def construct(self):
        head = LinearNode(1, RED)
        head = insert_LS(head, 2, BLUE_C)
        head = insert_LS(head, 3, GREEN_D)

        LChain = LinearizedChain(head)
        LChain.build_structure_with_entry(head)
        LChain.display(self, wait=0.3)

        Chain1 = Chain(head, x_distance=1.5)
        Chain1.build_structure_with_entry(head)
        Chain1.display(self, wait=0.2)

