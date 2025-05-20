from manim import *
from objects import *
from processing import *

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
        BTree.move_to([4.5, -2.5,0])
        BTree.scale_all(0.5)
        self.add(BTree)
        self.wait(1)

        OFFSET = 0.05 * UP  # or RIGHT, or use a random vector for variety

        for L in BTree.Ls:
            # Slight upward shift to prevent overlap
            self.add(Dot(color=GREEN, radius=0.1).move_to(L[0].get_start() + OFFSET))
            self.add(Dot(color=BLUE, radius=0.1).move_to(L[1].get_start() + OFFSET))
            
            # Slight downward shift for end dots
            self.add(Dot(color=RED, radius=0.1, fill_opacity=1).move_to(L[0].get_end() - OFFSET))
            self.add(Dot(color=PINK, radius=0.1, fill_opacity=1).move_to(L[1].get_end() - OFFSET))
            
            self.wait(0.2)

        
        

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
        # trace_dot_LBTree = Dot(color=YELLOW, radius=0.1).align_to(LBTree,DL)
        # trace_dot_BTree = Dot(color=YELLOW, radius=0.1).move_to(BTree.entry_dot.get_center())

        
        # for i, (LBtag, line, Btag, L, tick) in enumerate(zip(LBTree.tags, LBTree.lines, BTree.tags, BTree.Double_Ls, timeline.ticks)):
        #     if not isinstance(line, DashedLine) and not isinstance(L[0], DashedLine):
        #         if i == 0:
        #             L = BTree.entry_line
        #             BTreeDotAni1 = MoveAlongPath(trace_dot_BTree, L)
        #             LBTreeDotAni = MoveAlongPath(trace_dot_LBTree, line)
        #             self.play(AnimationGroup(BTreeDotAni1, LBTreeDotAni), run_time=2)
        #             self.wait(0.2)
        #         else:
        #             self.play(Indicate(L[1], color=GREEN), run_time=2)
        #             BTreeDotAni1 = MoveAlongPath(trace_dot_BTree, L[1])
        #             self.play(Indicate(L[0], color=YELLOW), run_time=2)
        #             BTreeDotAni2 = MoveAlongPath(trace_dot_BTree, L[0])
        #             LBTreeDotAni = MoveAlongPath(trace_dot_LBTree, line)
        #             self.play(AnimationGroup(Succession(BTreeDotAni1, BTreeDotAni2), LBTreeDotAni), run_time=2)
        #             self.wait(0.2)
        #     else:
        #         if i == 0:
        #             L = BTree.entry_line
        #             fullLine = Line(line.get_start(), line.get_end())
        #             LBTreeDotAni = MoveAlongPath(trace_dot_LBTree, fullLine)
        #             BTreeDotAni1 = MoveAlongPath(trace_dot_BTree, L)
        #             self.play(AnimationGroup(BTreeDotAni1, LBTreeDotAni), run_time=2)
        #             self.wait(0.2)
        #         else:
        #             full_L = VGroup(Line(L[0].get_start(), L[0].get_end()), Line(L[1].get_start(), L[1].get_end()))
        #             fullLine = Line(line.get_start(), line.get_end())
        #             BTreeDotAni1 = MoveAlongPath(trace_dot_BTree, full_L[1])
        #             BTreeDotAni2 = MoveAlongPath(trace_dot_BTree, full_L[0])
        #             LBTreeDotAni = MoveAlongPath(trace_dot_LBTree, fullLine)
        #             self.play(AnimationGroup(Succession(BTreeDotAni1, BTreeDotAni2), LBTreeDotAni), run_time=2)
        #             self.wait(0.2)

        #     LBtag_copy = LBtag.copy()
        #     LBtag_copy.generate_target()
        #     LBtag_copy.target.move_to(tick.get_center())
        #     LBTreeTagAni = MoveToTarget(LBtag_copy)
        #     BTreeTagAni = Indicate(Btag, color=YELLOW) 
        #     self.play(LBTreeTagAni, BTreeTagAni)
        #     self.wait(0.2)

        # self.wait(2)

        

        
