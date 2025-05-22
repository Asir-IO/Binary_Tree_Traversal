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
    frame = StepFrame()
    frame.rec.stretch_to_fit_width(width=structure.tags[0].outline.radius * 2 + 0.1)
    frame.rec.stretch_to_fit_height(structure.height+1)
    frame.update_text()
    frame.move_to(structure.tags[0].get_center())
    frame.align_to(structure, DOWN)
    frame.shift(DOWN*0.5)
    self.play(Write(frame), run_time=1)
    self.wait(0.5)
    self.play(Indicate(structure.tags[0]))
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
