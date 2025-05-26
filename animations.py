from manim import *
from objects import *
from processing import *

def traversal_scene(scene, LBTree, BTree, timeline):
    LBtags_seen = {}
    Linearized_tags = VGroup() 
    Arrows = VGroup()
    indicate_steps_pre(scene, LBTree, color=YELLOW)
    for i, (LBtag, line, Btag, tick) in enumerate(zip(LBTree.tags, LBTree.lines, BTree.Double_tags, timeline.ticks)):
        count = LBtags_seen.get(LBtag.number, 0) + 1
        LBtags_seen[LBtag.number] = count

        if isinstance(line, DashedLine):
            line = Line(line.get_start(), line.get_end())
        LBTreeDotAni = MoveAlongPath(scene.trace_dot_LBTree, line)
        BTreeCircleAni = scene.trace_circle_BTree.animate.move_to(Btag.get_center())

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
        scene.play(FadeIn(node_code))
        scene.wait()

        arrow = Arrow(start=tick.get_bottom() + DOWN*1, end= tick.get_bottom() + DOWN*0.2, color = indication_color, stroke_width=12, buff=0, max_stroke_width_to_length_ratio=10)
        Arrows.add(arrow)
        arrow.order = count

        LBtag.z_index = max(scene.trace_dot_LBTree.z_index, LBtag_copy.z_index) + 1
        LBTree.entry_dot.z_index = scene.trace_dot_LBTree.z_index + 1
        # Move circle and dot, and then indicate tag, and then linearize tag, and then add arrow
        temp_copy = LBtag.outline.copy()
        temp_copy.z_index=LBtag.z_index+1
        temp_copy.set_fill(opacity=0)

        if i==0:
            scene.play(Create(scene.trace_circle_BTree))
        scene.play(Succession(AnimationGroup(BTreeCircleAni, LBTreeDotAni, lag_ratio=0, run_time=2), temp_copy.animate.set_stroke(color=YELLOW)))
        indicate_steps_unit(scene, LBTree, LBtag, i, False)
        scene.wait()
        scene.play(Succession(AnimationGroup(Indicate(LBtag, color=indication_color), Succession(Indicate(indicated_lines[0], color=indication_color), indicated_lines[0].animate.set_color(indication_color)))))
        scene.wait()
        scene.play(LBTreeTagAni)
        scene.wait()
        scene.play(GrowArrow(arrow))
        scene.wait(2)
        scene.play(Succession(Indicate(indicated_lines[1], color=indication_color), indicated_lines[1].animate.set_color(indication_color)))
        scene.wait()
        scene.play(FadeOut(node_code), FadeOut(temp_copy))
        scene.wait()
        scene.i=i
    line = Line(LBTree.exit_line.get_start(), LBTree.exit_line.get_end())
    LBTreeDotAni = MoveAlongPath(scene.trace_dot_LBTree, line)
    BTreeCircleAni = scene.trace_circle_BTree.animate.move_to(BTree.entry_dot.get_center())
    scene.play(AnimationGroup(BTreeCircleAni, LBTreeDotAni, lag_ratio=0, run_time=2))
    indicate_steps_unit(scene, LBTree, LBTree.exit_dot, scene.i, False)
    scene.play(FadeOut(scene.trace_circle_BTree, scene.trace_dot_LBTree))
    return VGroup(Linearized_tags, Arrows)

def show_order_sub_scene(scene, Linearized_tags, Arrows, timeline, type):
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
        if type == "preorder" and tag.number is None:
            chosen_objs.add(tag, arrow)
        elif tag.number is not None and tag.order == order_match and arrow.order == order_match:
            chosen_objs.add(tag, arrow)
        else:
            ommited_objs.add(tag, arrow)
    scene.play(FadeOut(ommited_objs), run_time=1)
    scene.wait()
    scene.play(Indicate(chosen_objs, color=indication_color), FadeIn(order_text), run_time=2)
    scene.wait()
    scene.play(FadeOut(order_text))
    scene.wait()
    scene.play(FadeIn(ommited_objs), run_time=1)
    scene.wait()
    

def show_order_scene(scene, Linearized_tags, Arrows, timeline):
    #Show preorder
    show_order_sub_scene(scene, Linearized_tags, Arrows, timeline, "preorder")
    #Show inorder
    show_order_sub_scene(scene, Linearized_tags, Arrows, timeline, "inorder")
    #Show postorder
    show_order_sub_scene(scene, Linearized_tags, Arrows, timeline, "postorder")

# Scene01_Intro
def indicate_steps_pre(scene, structure, color=YELLOW):
    #Add initial frame
    tag_radius = structure.tags[0].outline.radius
    scene.frame = StepFrame(width=tag_radius*2 + (0.1*tag_radius/0.32), height=structure.height+1, color=color)
    print(f"radius: {structure.tags[0].outline.radius}")
    scene.frame.move_to(structure.tags[0].get_center())
    scene.frame.align_to(structure, DOWN)
    scene.frame.shift(DOWN*0.5)
    scene.play(FadeIn(scene.frame))
    scene.wait(0.5)

def indicate_steps_unit(scene, structure, tag, i, indicate_tag=True):
    step = scene.frame.text_group.copy()
    print("i:", i)
    if(tag == structure.exit_dot):
        new_txt = Tex(f"{i+1}", font_size=scene.frame.txt2.font_size).move_to(scene.frame.text_group[1])
        scene.play(ReplacementTransform(scene.frame.text_group[1], new_txt))
        scene.frame.text_group[1] = new_txt
        final_txt = scene.frame.text_group.copy()
        scene.play(Unwrite(scene.frame.text_group))

        scene.play(scene.frame.animate.match_x(tag))
        new_number = Tex(f"{i+2}", font_size=scene.frame.txt2.font_size).move_to(final_txt[1])
        final_txt[1].become(new_number)  

        final_txt.move_to(scene.frame.rec.get_top() + DOWN * (final_txt.height + 0.025))
        scene.play(Write(final_txt))
        scene.wait()
        scene.play(FadeOut(scene.frame, final_txt))
    else:
        step[1] = Tex(f"{i+1}", font_size=scene.frame.txt2.font_size).move_to(scene.frame.text_group[1].get_center())
        scene.play(ReplacementTransform(scene.frame.text_group, step))     
        scene.frame.text_group = step
        scene.play(AnimationGroup(scene.frame.animate.match_x(tag)))
        if indicate_tag:
            scene.play(Indicate(tag))

def naive_tarversal_scene(scene):
    scene.BTree = BinaryTree(root=buildTree(scene.dots_color, 3), dots_color=scene.dots_color, lines_color=scene.lines_color)
    scene.BTree.build_structure(scene.BTree.root)
    txt1 = Tex("Binary Tree")
    txt1.move_to([-3, -2, 0])
    txt2 = Tex("Visit every node?")
    txt2.move_to([3, -2, 0])
    txt3 = Tex("Simple enough!", font_size=80)
    txt3.move_to([0, -2, 0])

    #6.1 (recording)
    scene.BTree.display(scene)
    scene.wait()
    #7 (rec)
    scene.play(Write(txt1), run_time=2)
    scene.wait(3)
    #7.1 (rec)
    scene.play(Write(txt2), run_time=2)
    scene.wait(2)
    scene.play(ReplacementTransform(VGroup(txt1, txt2), txt3), run_time = 2)
    #8.2
    naive_traversal_BTree(scene)
    scene.wait()
    scene.play(Unwrite(txt3), run_time=2)
    # 9 (rec)
    scene.wait(4)
    txt4 = Tex("Clone yourself?")
    txt4.move_to([-3, -2, 0])
    txt5 = Tex("Split your conciousness?")
    txt5.move_to([3, -2, 0])
    scene.play(Write(txt4), run_time=2)
    scene.wait()
    scene.play(Write(txt5), run_time=2)
    scene.wait(3)
    
    #10.2 (rec)
    txt7 = Tex("Splitting")
    txt7.move_to([-3, -2, 0])
    txt7_HI = add_highlight_to_text(txt7, 0, 14, color=RED_D, opacity=0.8, text_z_index=txt7.z_index)
    txt8 = Tex("Parallel moves")
    txt8.move_to([3, -2, 0])
    txt8_HI = add_highlight_to_text(txt8, 0, 24, color=RED_D, opacity=0.8, text_z_index=txt8.z_index)
    scene.play(ReplacementTransform(txt4, txt7), run_time=2)
    scene.wait()
    scene.play(ReplacementTransform(txt5, txt8), run_time=2)
    scene.wait()
    scene.play(GrowFromEdge(txt7_HI, edge=LEFT),GrowFromEdge(txt8_HI, edge=LEFT),run_time=2)
    scene.wait()
    scene.play(FadeOut(VGroup(txt7, txt7_HI, txt8, txt8_HI)), run_time=2)
    scene.wait(2)
    
    #11.6 (rec)
    txt6 = Tex("Sequential way?", font_size=80)
    txt6.move_to([0, -2, 0])
    txt6_HI = add_highlight_to_text(txt6, 0, 9, color=GREEN_D, opacity=0.8, text_z_index=txt6.z_index)
    scene.play(Write(txt6), GrowFromEdge(txt6_HI, edge=LEFT), run_time=2)
    scene.wait(6)
    scene.txt6_GP = VGroup(txt6, txt6_HI)

def show_solution(scene):
    txt1 = Tex("The Solution:", font_size=40)
    txt1_BX = SurroundingRectangle(txt1, color=GREEN_D, buff=0.2)
    LBTree = LinearizedBTree(root=buildTree(scene.dots_color, 3), x_start=-10, x_distance=0.9, y_start=-2 ,y_distance=1.5, dots_color=scene.dots_color, lines_color=scene.lines_color)
    LBTree.build_structure_with_entry(LBTree.root)
    LBTree.move_to([0, 1, 0])
    LBTree.scale_all(0.9)
    LBTree_SUR = SurroundingRectangle(LBTree, color=GREEN_D, buff=0)
    #buff
    LBTree_SUR.stretch_to_fit_width(LBTree_SUR.width +1.4)
    LBTree_SUR.stretch_to_fit_height(LBTree_SUR.height + 0.2)
    txt1_GP = VGroup(txt1, txt1_BX).align_to(LBTree_SUR, UL)
    trans1 = ReplacementTransform(scene.txt6_GP, VGroup(txt1_GP, LBTree_SUR), run_time=2)
    scene.BTree.generate_target()
    scene.BTree.target.move_to([0, -2.7, 0])
    scene.BTree.target.scale_all(0.6)
    
    trans2 = MoveToTarget(scene.BTree)
    scene.play(trans1, trans2)
    LBTree.display(scene, wait=0.1)
    #14.2 (rec)
    scene.wait(7)
    code = '''
                def traversal(node):
                    # Base case
                    if node == None:
                        return
                    # Preorder (1st visit)
                    visit(node)
                    traversal(node.left)

                    # Inorder (2nd visit)
                    visit(node)
                    traversal(node.right)
                    
                    # Postorder (3rd visit)
                    visit(node)
                    return'''
    py_codeblock = Code(
            code_string=code,
            language="python",
            background="window",
            formatter_style="native",
            paragraph_config={"font": "Cascadia Mono SemiBold"},
        )
    py_codeblock.move_to([-4,1,0])
    py_codeblock.scale(0.6)
    LBTree.generate_target()
    LBTree.target.shift(3*RIGHT)
    LBTree.target.scale_all(0.6)
    #15.3 (rec)
    scene.wait(5)
    scene.play(FadeOut(VGroup(txt1_GP, LBTree_SUR)))
    scene.play(MoveToTarget(LBTree))
    scene.play(FadeIn(py_codeblock), run_time=2)
    #16.2 (rec)
    scene.wait()
    scene.play(Circumscribe(py_codeblock), run_time=2)
    scene.wait(2)


def naive_traversal_BTree(scene):
    for tag in scene.BTree.tags:
        tag.z_index = 100
    scene.wait()
    level_ordered_tags = scene.BTree.get_level_ordered_tags()
    initial_dot = Dot()
    initial_dot.move_to(scene.BTree.entry_dot.get_center())
    initial_dot.generate_target()
    scene.play(FadeIn(initial_dot))
    scene.play(initial_dot.animate.move_to(level_ordered_tags[0][0]))
    level_initial_dots = [VGroup(initial_dot)]
    height = scene.BTree.root.get_height()

    for i in range(height+1):
        level_dots = VGroup()
        #for every dot currently in that level
        for a, dot in enumerate(level_initial_dots[i]):
            my_left_L = level_ordered_tags[2**(i)+a-1][1]
            left_dot = create_branching_dot(scene, dot, my_left_L)
            level_dots.add(left_dot)
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
    scene.play(initial_dot.animate.move_to(scene.BTree.entry_dot))
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