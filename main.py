from manim import *
from objects import *
from processing import *
from animations import *

dots_color=[RED, ManimColor("#2f9e44"), ManimColor("#228be6"), ManimColor("#a5d8ff"), GREY]
lines_color = [YELLOW, ORANGE, PURPLE]

class Scene01_Intro(MovingCameraScene):
    def construct(self):
        # self.add(NumberPlane())
        head = LinearNode(1, dots_color[1])
        head = insert_LS(head, 2, dots_color[2])
        head = insert_LS(head, 3, dots_color[3])

        Chain1 = Chain(head, x_distance=1.5)
        Chain1.build_structure_with_entry(head)
        move_by_anchor(Chain1, [-3.5,2,0], "left")

        txt_1 = Tex("Visit every node?")
        txt_1.move_to(Chain1, DOWN)
        txt_1.shift(DOWN)

        LChain = LinearizedChain(head)
        LChain.build_structure_with_entry(head)
        LChain.next_to(Chain1, DOWN, buff = 0.2)
        LChain.scale_all(0.8)
        
        #2.1 (rec)
        Chain1.display(self, wait=0.2)
        self.play(Write(txt_1))
        self.wait(2)
        self.play(txt_1.animate.move_to([0, 3, 0]))
        #4.4 (rec)
        LChain.display(self, wait=0.3)
        self.wait()

        indicate_steps_pre(self, LChain)
        for i, tag in enumerate(LChain.tags[1:].add(LChain.exit_dot)):
            indicate_steps_unit(self, LChain, tag, i)
        self.wait()
        #5.3 (rec)
        txt2 = Tex("Simple enough?").move_to([-4.5,0,0])
        txt3 = Tex("Linked list").move_to([4.5,0,0])
        txt3_HI = add_highlight_to_text(txt3, 0, 12, color=GREEN_D, opacity=0.8)
        self.play(Write(txt2), run_time=2)
        self.wait()
        #5.4 (rec)
        self.play(GrowFromPoint(txt3, Chain1.get_center(), run_time=2))
        self.play(GrowFromEdge(txt3_HI, LEFT, run_time=2))
        self.wait()

        frame = self.camera.frame.copy()
        frame.set_stroke(color=WHITE,opacity=1,width=5)
        self.play(
            Create(frame),
            self.camera.frame.animate.scale(2).move_to(frame.get_critical_point(DR))
        )
        txt4 = Text("Quick note", font_size=100).move_to([14,1,0])
        txt4_SUR=SurroundingRectangle(txt4, color=RED_D, buff=0.4)
        txt4_SUR.set_stroke(width=10)
        txt4_GP = VGroup(txt4_SUR, txt4)
        #phi (rec)
        self.play(Create(txt4_SUR), Write(txt4))
        self.wait(3)
        scale_factor = 3
        phi = VGroup(Chain1.lines[2].copy().scale(scale_factor), Chain1.tags[-1].copy().scale(scale_factor))
        phi[0].stroke_width *= scale_factor
        phi[1].circle.stroke_width *= scale_factor
        phi[1].outline.stroke_width *= scale_factor
        self.play(phi.animate.next_to(txt4_GP, DOWN, buff=1))

        txt5 = Tex("Isn't part of the list", font_size=140).move_to([7, -6.5, 0])
        txt5_HI = add_highlight_to_text(txt5, 0, 4, color=RED_D, opacity=0.8)
        self.play(Write(txt5), GrowFromEdge(txt5_HI, LEFT), run_time=2)
        self.wait()
        txt7 = Tex(r"$\text{Convention}\;\Rightarrow\;\text{END}$", font_size=100).next_to(txt5, DOWN, buff=1.5)
        self.play(Write(txt7), run_time=2)
        self.wait(4)
        self.play(
            Indicate(txt7[0][-3:]),
            Indicate(phi[1]),
            run_time = 2
        )
        self.wait(7)
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(frame.get_center()),
            FadeOut(frame)
        )
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])

class Scene02_ShowBTree_1(Scene):
    def construct(self):
        self.dots_color = dots_color
        self.lines_color = lines_color
        # self.add(NumberPlane())
        naive_tarversal_scene(self)
        self.wait(8)
        show_solution(self)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

class Scene03_Trace(Scene):
    def construct(self):
        # self.add(NumberPlane())
        # self.add(Rectangle(width=9, height=4, color= RED, fill_opacity=0).set_stroke(color=RED, width=4).move_to([-2.5, 1, 0]))
        # self.add(Rectangle(width=5, height=3, color= GREEN, fill_opacity=0).set_stroke(color=GREEN, width=4).move_to([4.5, -2.5,0]))
        txt1 = Tex("The solution", font_size=100)
        txt1.shift(UP)
        txt2 = Tex("(explained)", font_size=70)
        txt2_HI = add_highlight_to_text(txt2, 1, 9, color=GREEN, opacity=0.8)
        txt2_GP = VGroup(txt2, txt2_HI)
        txt1_2_GP  = VGroup(txt1, txt2_GP).arrange(direction=DOWN)
        self.play(Write(txt1_2_GP), run_time=2)
        self.wait()
        self.play(FadeOut(txt1_2_GP))
        self.wait()

        LBTree = LinearizedBTree(root=buildTree(dots_color, 3), x_start=-10, x_distance=0.9, y_start=-2 ,y_distance=1.5, dots_color=dots_color, lines_color=lines_color)
        LBTree.build_structure_with_entry(LBTree.root)
        LBTree.move_to([-2.5, 1, 0])
        LBTree.scale_all(0.7)

        BTree = BinaryTree(root=buildTree(dots_color, 3), x_start=0, x_distance=3, y_start=3 ,y_distance=1, dots_color=dots_color, lines_color=lines_color)
        BTree.build_structure(BTree.root)
        BTree.add_double_tags()
        BTree.move_to([4.5, -2.5,0])
        BTree.scale_all(0.5)
        
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
        for tick in timeline.ticks:
            tick.set_color(YELLOW)
        self.trace_dot_LBTree = Dot(color=YELLOW, radius=0.1).align_to(LBTree,DL)
        self.trace_circle_BTree = Circle(color=YELLOW, radius=BTree.tags[0].outline.radius+0.07).move_to(BTree.entry_dot.get_center())
        
        self.play(Create(BTree), Create(LBTree), Create(timeline), run_time=5)
        self.wait(2)
        traversal_scene_data = traversal_scene(self, LBTree, BTree, timeline)
        self.wait(4)
        show_order_scene(self, traversal_scene_data[0], traversal_scene_data[1], timeline)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

class Scene04_Conclusion(Scene):
    def construct(self):
        # self.add(NumberPlane())
        txt1 = Tex("Question", font_size=70)
        txt1_SUR = SurroundingRectangle(txt1, color=GREEN_D, buff=0)
        txt1_SUR.stretch_to_fit_height(txt1.height+0.3)
        txt1_SUR.stretch_to_fit_width(txt1.width+0.6)
        txt1_SUR.set_stroke(width=5)
        txt1_GP = VGroup(txt1_SUR, txt1).move_to([0,2.5,0])
        self.play(Create(txt1_SUR), Write(txt1), run_time=2)

        txt2 = Tex("Create a traversal diagram for an n-ary", font_size=60)
        txt3 = Tex("tree data structure?", font_size=60)
        txt2_3 = VGroup(txt2, txt3).arrange(direction=DOWN)
        txt2_HI = add_highlight_to_text(txt2, 28, 32, color=GREEN_D, opacity=0.8)
        txt2_3_GP = VGroup(txt2_3, txt2_HI).next_to(txt1_GP, DOWN, buff=1.5)
        self.wait(2)
        self.play(
            Succession(
            Write(txt2),
            Write(txt3,)),
        )
        self.play(GrowFromEdge(txt2_HI, LEFT))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

class Scene05_SoFar(MovingCameraScene):
    def construct(self):
        # self.add(NumberPlane())
        head = LinearNode(1, dots_color[1])
        head = insert_LS(head, 2, dots_color[2])
        head = insert_LS(head, 3, dots_color[3])

        Chain1 = Chain(head, x_distance=1.5)
        Chain1.build_structure_with_entry(head)
        Chain1.move_to(ORIGIN)

        txt_1 = Tex("Linked List", font_size=100)
        txt_1.move_to([0,2,0])
        self.play(Write(txt_1), run_time=2)
        self.play(FadeIn(Chain1), run_time=2)
        self.play(Wiggle(Chain1, buff=0.5, run_time=2))
        self.wait()

        arr_2 = MathTex(r"\Downarrow", font_size=80)
        LChain = LinearizedChain(head)
        LChain.build_structure_with_entry(head)
        LChain.scale_all(0.8)
        move_by_anchor(LChain, [0,3.5,0], "top")
        self.play(Unwrite(txt_1))
        self.play(ReplacementTransform(Chain1, LChain), run_time=2)
        self.wait()

        txt_10 = Tex(r"``Traversal diagram''", font_size = 80)
        txt_10.next_to(LChain, DOWN, buff=0.7)
        self.play(Write(txt_10), run_time=2)
        self.play(Wiggle(LChain), run_time=2)
        self.wait()
        self.play(Unwrite(txt_10))
        self.wait()
        arr_2.next_to(LChain, DOWN, buff=0.2)
        timeline_list = NumberLine(
            x_range=[0, 6, 1],
            length=LChain.get_width(),
            color=WHITE,
            include_numbers=False,
            stroke_width=5,
            tick_size=0.1,
            numbers_with_elongated_ticks=[0,6]
        )
        align_center(timeline_list, LChain, 'x')
        timeline_list.next_to(arr_2, DOWN, buff=0)
        timeline_list.shift(DOWN*0.7)
        for tick in timeline_list.ticks:
            tick.set_color(YELLOW)

        tags_copy = LChain.tags.copy()
        for tag, tick in zip(tags_copy, timeline_list.ticks):
            tag.generate_target()
            tag.target.move_to(tick.get_center())
        self.play(Create(arr_2))
        self.play(Create(timeline_list), run_time=2)
        self.play(Indicate(LChain.tags))
        self.wait()
        self.play(*[MoveToTarget(tag) for tag in tags_copy], run_time=2)
        self.play(Indicate(tags_copy))
        self.wait(3)

        self.play(self.camera.frame.animate.shift(RIGHT * 3), run_time=2)
        txt_suc1 = Tex("Traversed", font_size=80).move_to([7.222-1.5, 2, 0])
        txt_suc2 = Tex("Sucessfully", font_size=70).next_to(txt_suc1, DR, buff=0.2)  
        txt_suc2.shift(LEFT*txt_suc1.get_width()/2)
        txt_suc2_HI = add_highlight_to_text(txt_suc2, 0, 10, color=GREEN_D, opacity=0.8)

        self.play(
            Write(txt_suc1),
            Write(txt_suc2),
            run_time=2)
        self.play(GrowFromEdge(txt_suc2_HI, LEFT))
        self.wait()
        self.play(Circumscribe(timeline_list, color=GREEN_D, buff=0.3, run_time=2))
        self.play(self.camera.frame.animate.shift(RIGHT * (11.22+3)), run_time=3)

        txt_2 = Tex("Binary Tree", font_size=100)
        txt_2.move_to([0+14.22+3,2,0])
        BTree = BinaryTree(root=buildTree(dots_color, 3), x_start=0, x_distance=3, y_start=3 ,y_distance=1, dots_color=dots_color, lines_color=lines_color)
        BTree.build_structure(BTree.root)
        BTree.add_double_tags()
        BTree.next_to(txt_2, DOWN, buff=0.3)
        txt_2.shift(UP*0.5)
        self.play(Write(txt_2), run_time=2)
        self.play(FadeIn(BTree), run_time=2)
        self.play(Wiggle(BTree, buff=0.5, run_time=2))
        self.wait()

        arr_3 = MathTex(r"\Downarrow", font_size=80)

        LBTree = LinearizedBTree(root=buildTree(dots_color, 3), x_start=-10, x_distance=0.9, y_start=-2 ,y_distance=1.5, dots_color=dots_color, lines_color=lines_color)
        LBTree.build_structure_with_entry(LBTree.root)
        LBTree.scale_all(0.8)
        move_by_anchor(LBTree, [0+14.22+3,3.5,0], "top")

        self.play(Unwrite(txt_2))
        self.play(ReplacementTransform(BTree, LBTree), run_time=2)
        arr_3.next_to(LBTree, DOWN, buff=0.2)
        self.wait()
        txt_10 = Tex(r"``Traversal diagram''", font_size = 80)
        txt_10.next_to(LBTree, DOWN, buff=0.5)
        self.play(Write(txt_10), run_time=2)
        self.play(Wiggle(LBTree), run_time=2)
        self.wait()
        self.play(Unwrite(txt_10))
        self.wait()
        timeline_list = NumberLine(
            x_range=[0, 12, 1],
            length=LBTree.get_width(),
            color=WHITE,
            include_numbers=False,
            stroke_width=5,
            tick_size=0.1,
            numbers_with_elongated_ticks=[0,12]
        )
        align_center(timeline_list, LBTree, 'x')
        timeline_list.next_to(arr_3, DOWN, buff=0)
        timeline_list.shift(DOWN*0.7)
        for tick in timeline_list.ticks:
            tick.set_color(YELLOW)
        tags_copy = LBTree.tags.copy()
        for tag, tick in zip(tags_copy, timeline_list.ticks):
            tag.generate_target()
            tag.target.move_to(tick.get_center())
        self.play(Create(arr_3))
        self.play(Create(timeline_list), run_time=2)
        self.play(Indicate(LBTree.tags))
        self.wait()
        self.play(*[MoveToTarget(tag) for tag in tags_copy], run_time=2)
        self.wait()
        self.play(Indicate(tags_copy))
        self.wait()

        self.play(self.camera.frame.animate.shift(RIGHT * 1.5), run_time=2)

        txt_suc1 = Tex("Traversed", font_size=70).move_to([7.222-1.5+17.22+1, 2, 0])
        txt_suc2 = Tex("Sucessfully", font_size=60).next_to(txt_suc1, DOWN, buff=0.2)
        txt_suc2.shift(RIGHT*0.1)
        txt_suc2_HI = add_highlight_to_text(txt_suc2, 0, 10, color=GREEN_D, opacity=0.8)

        self.play(
            Write(txt_suc1),
            Write(txt_suc2),
            run_time=2)
        self.play(GrowFromEdge(txt_suc2_HI, LEFT))
        self.wait()
        self.play(Circumscribe(timeline_list, color=GREEN_D, buff=0.3, run_time=2))
        self.play(*[FadeOut(mob) for mob in self.mobjects])


