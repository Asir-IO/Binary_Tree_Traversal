from manim import *
from objects import *
from processing import *

def traversal_scene(self, LBTree, BTree, timeline):
    LBtags_seen = {}
    Linearized_tags = VGroup()
    Arrows = VGroup()
    for i, (LBtag, line, Btag, tick) in enumerate(zip(LBTree.tags, LBTree.lines, BTree.Double_tags, timeline.ticks)):
        count = LBtags_seen.get(LBtag.number, 0) + 1
        LBtags_seen[LBtag.number] = count

        if not isinstance(line, DashedLine):
            line = Line(line.get_start(), line.get_end())
        LBTreeDotAni = MoveAlongPath(self.trace_dot_LBTree, line)
        BTreeCircleAni = self.trace_circle_BTree.animate.move_to(Btag.get_center())

        LBtag_copy = LBtag.copy()
        LBtag_copy.order = count
        Linearized_tags.add(LBtag_copy)
        LBtag_copy.generate_target()
        LBtag_copy.target.move_to(tick.get_center())
        LBTreeTagAni = MoveToTarget(LBtag_copy)

        node_code = NodeCode(LBtag.copy())
        if count == 1:
            indication_color =  BLUE_C
            indicated_lines = node_code.to_be_displayed("preorder")
        elif count == 2:
            indication_color = YELLOW_D
            indicated_lines = node_code.to_be_displayed("inorder")
            if LBtag.number:
                for ln in node_code.to_be_displayed("preorder"):
                    ln.set_color(BLUE_C)
        elif count == 3:
            indication_color = RED_D
            indicated_lines = node_code.to_be_displayed("postorder")
            if LBtag.number:
                for ln in node_code.to_be_displayed("preorder"):
                    ln.set_color(BLUE_C)
                for ln in node_code.to_be_displayed("inorder"):
                    ln.set_color(YELLOW_D)
        if not LBtag.number:
            indication_color = BLUE_C
            indicated_lines = node_code.to_be_displayed("base")

        # FadeIn the code_block
        self.play(FadeIn(node_code))
        self.wait()
        
        arrow = Arrow(start=tick.get_bottom() + DOWN*1, end= tick.get_bottom() + DOWN*0.2, color = indication_color, stroke_width=12, buff=0, max_stroke_width_to_length_ratio=10)
        Arrows.add(arrow)
        arrow.order = count

        LBtag.z_index = max(self.trace_dot_LBTree.z_index, LBtag_copy.z_index) + 1
        LBTree.entry_dot.z_index = self.trace_dot_LBTree.z_index + 1
        # Move circle and dot, and then indicate tag, and then linearize tag, and then add arrow
        temp_copy = LBtag.outline.copy()
        temp_copy.z_index=LBtag.z_index+1
        temp_copy.set_fill(opacity=0)
        self.play(Succession(AnimationGroup(BTreeCircleAni, LBTreeDotAni, lag_ratio=0, run_time=2), temp_copy.animate.set_stroke(color=YELLOW)))
        self.wait()
        self.play(Succession(AnimationGroup(Indicate(LBtag, color=indication_color), Succession(Indicate(indicated_lines[0], color=indication_color), indicated_lines[0].animate.set_color(indication_color)))))
        self.wait()
        self.play(LBTreeTagAni)
        self.wait()
        self.play(GrowArrow(arrow))
        self.wait(2)
        self.play(Succession(Indicate(indicated_lines[1], color=indication_color), indicated_lines[1].animate.set_color(indication_color)))
        self.wait()
        self.play(FadeOut(node_code), FadeOut(temp_copy))
        self.wait()
    self.play(FadeOut(self.trace_circle_BTree, self.trace_dot_LBTree))
    return VGroup(Linearized_tags, Arrows)

def show_order_sub_scene(self, Linearized_tags, Arrows, timeline, type):
    #Show preorder
    ommited_objs = VGroup()
    chosen_objs = VGroup()
    if type == "preorder":
        indication_color = BLUE_C
        order_text = Tex("Pre-order visits")
        order_text[0][0:9].set_color(indication_color)
        order_match = 1
    elif type == "inorder":
        indication_color = YELLOW_D
        order_text = Tex("In-order visits")
        order_text[0][0:8].set_color(indication_color)
        order_match = 2
    elif type == "postorder":
        indication_color = RED_D
        order_text = Tex("Post-order visits")
        order_text[0][0:10].set_color(indication_color)
        order_match = 3  
    order_text.next_to(timeline, DOWN, buff = 1)
    align_center(order_text, timeline, 'x')

    for tag, arrow in zip(Linearized_tags, Arrows):
        # Ommit others
        if tag.order != order_match or arrow.order != order_match or tag.number is None:
            ommited_objs.add(tag, arrow)
        else:
            chosen_objs.add(tag, arrow)
    self.play(FadeOut(ommited_objs), run_time=1)
    self.wait()
    self.play(Indicate(chosen_objs, color=BLUE_C), FadeIn(order_text), run_time=2)
    self.wait()
    self.play(FadeOut(order_text))
    self.wait()
    self.play(FadeIn(ommited_objs), run_time=1)
    self.wait()
    

def show_order_scene(self, Linearized_tags, Arrows, timeline):
    #Show preorder
    show_order_sub_scene(self, Linearized_tags, Arrows, timeline, "preorder")
    #Show inorder
    show_order_sub_scene(self, Linearized_tags, Arrows, timeline, "inorder")
    #Show postorder
    show_order_sub_scene(self, Linearized_tags, Arrows, timeline, "postorder")

# Scene01_Intro
def indicate_steps(self, structure):
    tag_radius = structure.tags[0].outline.radius
    frame = StepFrame(width=tag_radius*2 + (0.1*tag_radius/0.32), height=structure.height+1)
    print(f"radius: {structure.tags[0].outline.radius}")
    frame.move_to(structure.tags[0].get_center())
    frame.align_to(structure, DOWN)
    frame.shift(DOWN*0.5)
    self.play(FadeIn(frame))
    self.wait(0.5)
    self.play(Indicate(structure.tags[0]))
    self.wait()
    for i, tag in enumerate(structure.tags[1:].add(structure.exit_dot)):
        step = frame.text_group.copy()
        print("i:", i)
        if(tag == structure.exit_dot):
            new_txt = Tex(f"{i+1}", font_size=frame.txt2.font_size).move_to(frame.text_group[1])
            self.play(ReplacementTransform(frame.text_group[1], new_txt))
            frame.text_group[1] = new_txt
            final_txt = frame.text_group.copy()
            self.play(Unwrite(frame.text_group))

            self.play(frame.animate.match_x(tag))
            new_number = Tex(f"{i+2}", font_size=frame.txt2.font_size).move_to(final_txt[1])
            final_txt[1].become(new_number)  

            final_txt.move_to(frame.rec.get_top() + DOWN * (final_txt.height + 0.025))
            self.play(Write(final_txt))
            self.wait()
            self.play(FadeOut(frame, final_txt))
        else:
            step[1] = Tex(f"{i+1}", font_size=frame.txt2.font_size).move_to(frame.text_group[1].get_center())
            self.play(ReplacementTransform(frame.text_group, step))     
            frame.text_group = step
            self.play(AnimationGroup(frame.animate.match_x(tag)))
            self.play(Indicate(tag))

def naive_tarversal_scene(scene):
    BTree = BinaryTree(root=buildTree([RED, ManimColor("#2f9e44"), ManimColor("#228be6"), GREY], 3))
    BTree.build_structure(BTree.root)
    txt1 = Tex("Binary Tree")
    txt1.move_to([-3, -2, 0])
    txt2 = Tex("Visit every node?")
    txt2.move_to([3, -2, 0])
    txt3 = Tex("Simple enough!", font_size=80)
    txt3.move_to([0, -2, 0])

    BTree.display(scene)
    scene.wait()
    scene.play(Write(txt1), run_time=2)
    scene.wait(2)
    scene.play(Write(txt2), run_time=2)
    scene.wait(2)
    scene.play(ReplacementTransform(VGroup(txt1, txt2), txt3), run_time = 2)
    naive_traversal_BTree(scene, BTree)
    scene.wait()
    scene.play(Unwrite(txt3), run_time=2)
    scene.wait()

    txt4 = Tex("Cloning yourself")
    txt4.move_to([-3, -2, 0])
    txt4_HI = add_highlight_to_text(txt4, 0, 14, color=RED_D, opacity=0.8, text_z_index=txt4.z_index)
    txt5 = Tex("Splitting your conciousness")
    txt5.move_to([3, -2, 0])
    txt5_HI = add_highlight_to_text(txt5, 0, 24, color=RED_D, opacity=0.8, text_z_index=txt5.z_index)
    scene.play(Write(txt4), run_time=2)
    scene.wait()
    scene.play(Write(txt5), run_time=2)
    scene.wait()
    scene.play(GrowFromEdge(txt4_HI, edge=LEFT),GrowFromEdge(txt5_HI, edge=LEFT),run_time=2)
    scene.wait()
    scene.play(FadeOut(VGroup(txt4, txt4_HI, txt5, txt5_HI)), run_time=2)
    scene.wait(2)
    
    txt6 = Tex("Sequential way?", font_size=80)
    txt6.move_to([0, -2, 0])
    txt6_HI = add_highlight_to_text(txt6, 0, 9, color=GREEN_D, opacity=0.8, text_z_index=txt6.z_index)
    scene.play(Write(txt6), GrowFromEdge(txt6_HI, edge=LEFT), run_time=2)
    scene.wait(2)
def show_solution(scene):
    return

def naive_traversal_BTree(scene, BTree):
    level_ordered_tags = BTree.get_level_ordered_tags()
    initial_dot = Dot()
    initial_dot.move_to(BTree.entry_dot.get_center())
    initial_dot.generate_target()
    scene.play(FadeIn(initial_dot))
    scene.play(initial_dot.animate.move_to(level_ordered_tags[0][0]))
    level_initial_dots = [VGroup(initial_dot)]
    height = BTree.root.get_height()
    print(f"entry_pos: {initial_dot.get_center()}")

    for i in range(height+1):
        level_dots = VGroup()
        #for every dot currently in that level
        for a, dot in enumerate(level_initial_dots[i]):
            my_left_L = level_ordered_tags[2**(i)+a-1][1]
            left_dot = create_branching_dot(scene, dot, my_left_L)
            level_dots.add(left_dot)
            print(f"left dot pos: {left_dot.get_center()}")
            # left_label = create_position_label(left_dot, font_size=12) 
            # scene.add(left_label)
            my_right_L = level_ordered_tags[2**(i)+a-1][2]
            right_dot = create_branching_dot(scene, dot, my_right_L)
            level_dots.add(right_dot)
        scene.play(AnimationGroup(*[MoveAlongPath(dot, dot.L) for dot in level_dots]), run_time=2)
        level_initial_dots.append(level_dots)
    scene.wait()
    traced_paths = [m for m in scene.mobjects if isinstance(m, TracedPath)]
    scene.play(*[FadeOut(tp) for tp in traced_paths])
    scene.remove(*[tp for tp in traced_paths])

    for h in range(height+1, 0, -1):
        level_dots = level_initial_dots[h]
        for dot in level_dots:
            add_tracer(scene, dot)
        scene.play(AnimationGroup(*[MoveAlongPath(dot, dot.L, rate_func=lambda t:1-t) for dot in level_dots]), run_time=2)
        scene.play(AnimationGroup(*[FadeOut(dot) for dot in level_dots]))
    scene.play(initial_dot.animate.move_to(BTree.entry_dot))
    scene.play(FadeOut(initial_dot))
    traced_paths = [m for m in scene.mobjects if isinstance(m, TracedPath)]
    scene.play(*[FadeOut(tp) for tp in traced_paths])
    scene.remove(*[tp for tp in traced_paths])

def create_branching_dot(scene, parent_dot, path_segments, tracer_color=YELLOW):
        dot = Dot()
        dot.move_to(parent_dot.get_center())
        dot.original_pos = dot.get_center()
        dot.L = VMobject()
        dot.L.set_points_as_corners([path_segments[0].get_start(), path_segments[0].get_end(), path_segments[1].get_end()])
        print(f"first: {path_segments[0].get_start()}")
        add_tracer(scene, dot, tracer_color)
        return dot
    
def add_tracer(scene, dot, tracer_color=YELLOW):
    dot.tracer = TracedPath(dot.get_center, stroke_color=tracer_color, stroke_width=4)
    scene.add(dot.tracer)