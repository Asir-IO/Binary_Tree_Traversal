from manim import *
from objects import *
from processing import *
from scenes import *

dots_color=[RED, ManimColor("#2f9e44"), ManimColor("#228be6"), ManimColor("#a5d8ff"), GREY]
lines_color = [YELLOW, ORANGE, PURPLE]

class RecursiveTreeStructure(Scene):
    def construct(self):
        self.add(NumberPlane())
        self.add(Rectangle(width=9, height=4, color= RED, fill_opacity=0).set_stroke(color=RED, width=4).move_to([-2.5, 1, 0]))
        self.add(Rectangle(width=5, height=3, color= GREEN, fill_opacity=0).set_stroke(color=GREEN, width=4).move_to([4.5, -2.5,0]))
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

        LBtags_seen = {}
        for i, (LBtag, line, Btag, tick) in enumerate(zip(LBTree.tags, LBTree.lines, BTree.Double_tags, timeline.ticks)):
            count = LBtags_seen.get(LBtag.number, 0) + 1
            LBtags_seen[LBtag.number] = count

            if not isinstance(line, DashedLine):
                line = Line(line.get_start(), line.get_end())
            LBTreeDotAni = MoveAlongPath(self.trace_dot_LBTree, line)
            BTreeCircleAni = self.trace_circle_BTree.animate.move_to(Btag.get_center())

            LBtag_copy = LBtag.copy()
            LBtag_copy.generate_target()
            LBtag_copy.target.move_to(tick.get_center())
            LBTreeTagAni = MoveToTarget(LBtag_copy)
            if count == 1:
                indication_color =  ManimColor("#74D479")
            elif count == 2:
                indication_color = ManimColor("#FFC940")
            elif count == 3:
                indication_color = ManimColor("#FF3264")
            if not LBtag.number:
                indication_color = ManimColor("#74D479")

            arrow = Arrow(start=tick.get_bottom() + DOWN*1, end= tick.get_bottom(), color = indication_color, stroke_width=2,buff=0.1, max_stroke_width_to_length_ratio=1)

            # Run LBTreeDotAni and BTreeCircleAni in parallel, then LBTreeTagAni
            LBtag.z_index = self.trace_dot_LBTree.z_index + 1
            self.play(
                Succession(
                    AnimationGroup(BTreeCircleAni, LBTreeDotAni, lag_ratio=0, run_time=2),
                    Indicate(LBtag, color=indication_color),
                    LBTreeTagAni,
                    GrowArrow(arrow)
                ),
                run_time=4
            )
            self.wait(0.2)
        self.wait(2)

    


