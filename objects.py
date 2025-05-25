from manim import *
from processing import *
import math

# Simple binary tree node
class Node:
    def __init__(self, key, color=WHITE):
        self.left = None
        self.right = None
        self.parent = None
        self.color = color
        self.val = key
    def get_height(self):
        if self is None:
            return -1  # or 0 depending on your convention

        left_height = self.left.get_height() if self.left else -1
        right_height = self.right.get_height() if self.right else -1

        return 1 + max(left_height, right_height)

# Insert node into BST
def insert(root, key, color):
    if root is None:
        return Node(key, color)
    if key < root.val:
        newChild = insert(root.left, key, color)
        root.left = newChild
        newChild.parent = root
    elif key > root.val:
        newChild = insert(root.right, key, color)
        root.right = newChild
        newChild.parent = root
    return root

# Create a basic tree
def buildTree(dots_color=None, num_nodes=3):
    if dots_color is None:
        dots_color = [RED] + [RED] * int(math.log(num_nodes + 1, 2)) + [GREY]
    def median_order(start, end, level, nodes):
        if start > end:
            return
        mid = (start + end) // 2
        nodes.append((mid, level))
        median_order(start, mid - 1, level + 1, nodes)
        median_order(mid + 1, end, level + 1, nodes)

    nodes = []
    median_order(1, num_nodes, 0, nodes)
    if not nodes:
        return None

    max_level = max(level for _, level in nodes)
    color_list = dots_color[1:]
    color_list = color_list[:-1]

    if len(color_list) <= max_level:
        raise ValueError("Not enough colors in dots_color to cover all tree levels.")
    def color_for_level(level):
        return color_list[level]

    r = Node(nodes[0][0], color_for_level(nodes[0][1]))
    for val, level in nodes[1:]:
        insert(r, val, color_for_level(level))
    return r


class LinearNode:
    def __init__(self, key, color=WHITE):
        self.next = None
        self.color = color
        self.val = key

# Insert node into Chain
def insert_LS(head, key, color):
    new_node = LinearNode(key, color)
    if head is None:
        return new_node 
    current = head
    while current.next:
        current = current.next
    current.next = new_node
    return head

class NumberTag(VGroup):
    def __init__(self, number: int, fill_color=BLUE, radius=0.5, num_to_circle_ratio=130,**kwargs):
        super().__init__(**kwargs)

        circle = Circle(radius=radius, color=WHITE, stroke_width=5)
        outline = Circle(radius=radius+0.1, color=fill_color, stroke_width=5)
        circle.set_fill(fill_color, opacity=0.8)
        outline.set_fill(fill_color, opacity=0.8)

        if not number:  
            label = MathTex(r"\boldsymbol{\phi}", font_size=radius * num_to_circle_ratio, color=WHITE)
        else:
            label = Text(str(number), font_size=radius * num_to_circle_ratio, color=WHITE)

        self.add(outline, circle, label)
        self.number=number
        self.circle = circle
        self.outline = outline
        self.label = label
        self.radius = radius
    def set_color(self, color):
        self.circle.set_fill(color)
        self.outline.set_fill(color)
        self.outline.color=color

class StepFrame(VGroup):
    def __init__(self, stroke_color=YELLOW, width=2, height=6, step=1,**kwargs):
        super().__init__(**kwargs)
        self.rec = Rectangle(width=width, height=height)
        self.rec.set_stroke(color=stroke_color)
        self.step=step
        self.text_group = always_redraw(self.make_text_group)
        self.txt1 = self.text_group[0]
        self.txt2 = self.text_group[1]
        self.add(self.rec, self.text_group)
    def make_text_group(self):
        txt1 = Tex(
            "Move",
            font_size=font_size_by_ratio("Move", width=self.rec.width, ratio=4/5)
        )
        txt2 = Tex(str(self.step), font_size= 2*txt1.font_size)
        group = VGroup(txt1, txt2).arrange(DOWN)
        group.move_to(self.rec.get_bottom() + UP * (group.height))
        return group
    def update_text(self):
        self.txt1.font_size = 30 * self.width
        self.txt2.font_size = self.txt1.font_size * 1.5


class LinearizedBTree(VGroup):
    def __init__(self, root, x_start=-4, x_distance=0.5, y_start=-2, y_distance=1.5, dots_color=[RED, GREY, ManimColor("#228be6"), ManimColor("#2f9e44")], lines_color=[YELLOW, ORANGE, PURPLE], **kwargs):
        super().__init__(**kwargs)
        self.root = root
        self.x = x_start
        self.x_distance = x_distance
        self.y = y_start
        self.y_distance = y_distance
        self.lines = VGroup()
        self.tags = VGroup()
        self.entry_dot = None
        self.entry_line = None
        self.exit_dot = None
        self.exit_line = None
        self.dots_color = dots_color
        self.lines_color = lines_color
        self.add(self.lines, self.tags)

    def draw_line(self, start, end, dashed, color=WHITE):
        if dashed:
            line = DashedLine(start, end, dash_length=0.3, dashed_ratio=0.7, stroke_width=7, color=color)
        else:
            line = Line(start, end, stroke_width=7, color=color)
        self.lines.add(line)
        return line

    def add_number_tag(self, number, color):
        tag = NumberTag(number=number, fill_color=color, radius=0.3)
        tag.move_to([self.x, self.y, 0])
        tag.scale(0.85)
        self.tags.add(tag)
        return tag

    def build_structure(self, node, child_side=None):
        if node is None:
            self.add_number_tag(None, self.dots_color[-1])
            if child_side is not None:
                if child_side == "left":
                    self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y - self.y_distance, 0], False, color=self.lines_color[2])  # PURPLE
                elif child_side == "right":
                    self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y - self.y_distance, 0], False, color=self.lines_color[1])  # ORANGE
            self.x += self.x_distance
            self.y -= self.y_distance
            return

        # Preorder
        self.add_number_tag(node.val, node.color)
        self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y + self.y_distance, 0], False, color=self.lines_color[2])
        self.x += self.x_distance
        self.y += self.y_distance

        self.build_structure(node.left, "left")

        # Inorder
        self.add_number_tag(node.val, node.color)
        self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y + self.y_distance, 0], False, color=self.lines_color[1])
        self.x += self.x_distance
        self.y += self.y_distance

        self.build_structure(node.right, "right")

        # Postorder
        self.add_number_tag(node.val, node.color)
        if child_side is not None:
            if child_side == "left":
                self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y - self.y_distance, 0], False, color=self.lines_color[2])
            elif child_side == "right":
                self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y - self.y_distance, 0], False, color=self.lines_color[1])
        self.x += self.x_distance
        self.y -= self.y_distance
    def build_structure_with_entry(self, root):
        self.entry_dot = Dot(color=self.dots_color[0], radius=0.25).move_to([self.x, self.y, 0])
        self.add(self.entry_dot)
        self.entry_line = self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y + self.y_distance, 0], False, color=self.lines_color[0])
        self.x += self.x_distance
        self.y += self.y_distance
        self.build_structure(root)
        self.exit_line = self.draw_line([self.x - self.x_distance, self.y + self.y_distance, 0], [self.x, self.y, 0], False, color=self.lines_color[0])
        self.exit_dot = Dot(color=self.dots_color[0], radius=0.25).move_to([self.x, self.y, 0])
        self.add(self.exit_dot)
    def display(self, scene):
        # Animate the first dot and line
        self.entry_line.z_index = 0
        self.entry_dot.z_index = 3
        scene.play(FadeIn(self.entry_dot), run_time=1)
        scene.play(Create(self.entry_line), run_time=1)
        scene.bring_to_front(self.entry_dot)
        scene.wait(0.5)

        # Animate tags and lines for the rest
        for i, (ln, tg) in enumerate(zip(self.lines[1:], self.tags)):
            ln.z_index = 0
            tg.z_index = 3
            scene.play(FadeIn(tg), run_time=1)
            scene.wait(0.1)
            scene.play(Create(ln), run_time=1)
            scene.bring_to_front(tg)
            scene.wait(0.5)

        # Animate the final dot
        self.exit_dot.z_index = 3
        scene.play(FadeIn(self.exit_dot), run_time=1)
        scene.bring_to_front(self.exit_dot)
        scene.wait(0.5)

    def scale_all(self, scale_factor):
        for tag in self.tags:
            tag.circle.stroke_width *= scale_factor
            tag.circle.radius *= scale_factor
            tag.outline.stroke_width *= scale_factor
            tag.outline.radius *= scale_factor
            tag.label.font_size *= (scale_factor*1.5)
        self.scale(scale_factor)


class BinaryTree(VGroup):
    def __init__(self, root, x_start=0, x_distance=3, y_start=3, y_distance=1, dots_color=[RED, GREY, ManimColor("#228be6"), ManimColor("#2f9e44")], lines_color=[YELLOW, ORANGE, PURPLE], **kwargs):
        super().__init__(**kwargs)
        self.root = root
        self.x = x_start
        self.x_distance = x_distance
        self.y = y_start
        self.y_distance = y_distance
        self.Ls = VGroup()
        self.Double_tags = VGroup()
        self.tags = VGroup()
        self.entry_dot = Dot(color=RED, radius=0.25).move_to([self.x, self.y, 0])
        self.entry_line = Line([self.x, self.y, 0], [self.x, self.y - self.y_distance, 0], stroke_width=7, color=YELLOW)
        self.y -= self.y_distance
        self.dots_color = dots_color
        self.lines_color = lines_color
        self.add(self.entry_dot, self.entry_line, self.Ls, self.tags)
        self.entry_line.z_index = -100

    def draw_dot(self, color=WHITE):
        dot = Dot(color=color, radius=0.25).move_to([self.x, self.y, 0])
        self.dots.add(dot)

    def draw_line(self, start, end, dashed, color=WHITE):
        if dashed:
            line = DashedLine(start, end, dash_length=0.3, dashed_ratio=0.7, stroke_width=7, color=color)
        else:
            line = Line(start, end, stroke_width=7, color=color)
        self.lines.add(line)

    def add_number_tag(self, number, color):
        tag = NumberTag(number=number, fill_color=color, radius=0.3)
        tag.move_to([self.x, self.y, 0])
        return tag
    
    def draw_L(self, start, end, dashed, color=WHITE, x_first=True):
        if x_first:
            if dashed:
                L = VGroup(
                    DashedLine([start[0], start[1], 0], [end[0], start[1], 0], dash_length=0.3, dashed_ratio=0.7, stroke_width=7, color=color),
                    DashedLine([end[0], start[1], 0], [end[0], end[1], 0], dash_length=0.3, dashed_ratio=0.7, stroke_width=7, color=color)
                )
            else:
                L = VGroup(
                    Line([start[0], start[1], 0], [end[0], start[1], 0], stroke_width=7, color=color),
                    Line([end[0], start[1], 0], [end[0], end[1], 0], stroke_width=7, color=color)
                )
        else:
            if dashed:
                L = VGroup(
                    DashedLine([start[0], start[1], 0], [start[0], end[1], 0], dash_length=0.3, dashed_ratio=0.7, stroke_width=7, color=color),
                    DashedLine([start[0], end[1], 0], [end[0], end[1], 0], dash_length=0.3, dashed_ratio=0.7, stroke_width=7, color=color)
                )
            else:
                L = VGroup(
                    Line([start[0], start[1], 0], [start[0], end[1], 0], stroke_width=7, color=color),
                    Line([start[0], end[1], 0], [end[0], end[1], 0], stroke_width=7, color=color)
                )
        return L

    def build_structure(self, node, child_side=None, level=0):
        if node is None:
            tag = self.add_number_tag(None, self.dots_color[-1])
            self.tags.add(tag)
            self.Double_tags.add(tag)
            return
        # Pre-order
        offset = self.x_distance/(2**level)        
        original_x, original_y = self.x, self.y

        # Connect to your left child
        L = self.draw_L([self.x, self.y, 0], [self.x - offset, self.y - self.y_distance, 0], False, color=self.lines_color[2])
        self.Ls.add(L)
        node.left_L = L
        tag = self.add_number_tag(node.val, node.color)
        self.tags.add(tag)
        node.tag=tag
        self.Double_tags.add(tag)

        self.x -= offset
        self.y -= self.y_distance
        self.build_structure(node.left, "left", level + 1)

        # Inorder
        offset = self.x_distance / (2 ** level)
        self.x, self.y = original_x, original_y
        tag = self.add_number_tag(node.val, node.color)
        self.Double_tags.add(tag)

        # Connect to your right child
        L = self.draw_L([self.x, self.y, 0], [self.x + offset, self.y - self.y_distance, 0], False, color=self.lines_color[1])
        self.Ls.add(L)
        node.right_L=L

        self.x += offset
        self.y -= self.y_distance
        self.build_structure(node.right, "right", level + 1)
        # Postorder
        self.x, self.y = original_x, original_y
        tag = self.add_number_tag(node.val, node.color)
        self.Double_tags.add(tag)

    def add_double_tags(self):
        # Add return tags to the object (you never added the double tags to the object before)
        return_tags = VGroup()
        for tag in self.Double_tags:
            if tag not in self.tags:
                return_tags.add(tag)
        self.add(return_tags)

    
    def scale_all(self, scale_factor):
        for tag in self.Double_tags:
            tag.circle.stroke_width *= scale_factor
            tag.circle.radius *= scale_factor
            tag.outline.stroke_width *= scale_factor
            tag.outline.radius *= scale_factor
            tag.label.font_size *= (scale_factor*2)
        for L in self.Ls:
            for segment in L:
                segment.start = segment.start * scale_factor
                segment.end = segment.end * scale_factor
        self.entry_dot
        self.scale(scale_factor)
    def reverse_tags_order(self):
        self.remove(self.tags)
        self.tags = self.tags[::-1]
        self.add(self.tags)
    def display(self, scene):
        self.reverse_tags_order()
        scene.play(Create(VGroup(self.entry_dot, self.entry_line, self.Ls), run_time=6))
        scene.play(Create(self.remove(*VGroup(self.entry_dot, self.entry_line, self.Ls))), run_time=7)
        self.reverse_tags_order()

    def get_level_ordered_tags(self):
        res = self.level_order_rec(self.root, 0, [])
        self.level_ordered_tags = VGroup()
        for group in res:
            self.level_ordered_tags.add(*group)
        return self.level_ordered_tags
    
    def level_order_rec(self, node, level, res):
        if node is None:
            return
        if len(res) == level:
            res.append([])
        res[level].append(VGroup(node.tag, node.left_L, node.right_L))
        self.level_order_rec(node.left, level + 1, res)
        self.level_order_rec(node.right, level + 1, res)
        return res

class NodeCode(VGroup):
    def __init__(self, node,**kwargs):
        super().__init__(**kwargs)
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
        code_block = Code(
            code_string=code,
            language="python",
            background="window",
            formatter_style="native",
            paragraph_config={"font": "Cascadia Mono SemiBold"},
        )
        code_block.move_to([4.5, 1.5, 0])
        code_block.height *= 0.5
        code_block.width*= 1
        header_text = Tex("node = ", font_size=20*node.radius/0.15)
        node.next_to(header_text, RIGHT)
        header = VGroup(header_text, node)
        header.next_to(code_block, UP, buff=0.2)
        self.code=code
        self.code_block = code_block
        self.node=node
        self.type=type
        self.add(code_block, header)
    
    def to_be_displayed(self, type="preorder"):
        if type == "preorder":
            return self.code_block.code_lines[5:7]
        elif type == "inorder":
            return self.code_block.code_lines[9:11]
        elif type == "postorder":
            return self.code_block.code_lines[13:15]
        elif type == "base":
            return self.code_block.code_lines[2:4]
        return
    
class LinearizedChain(VGroup):
    def __init__(self, root, x_start=-4, x_distance=0.9, y_start=-2, y_distance=1.12, dots_color=[RED, ManimColor("#228be6"), ManimColor("#a5d8ff"), ManimColor("#2f9e44"), GREY], lines_color=[YELLOW, ORANGE], **kwargs):
        super().__init__(**kwargs)
        self.root = root
        self.x = x_start
        self.x_distance = x_distance
        self.y = y_start
        self.y_distance = y_distance
        self.lines = VGroup()
        self.tags = VGroup()
        self.entry_dot = None
        self.entry_line = None
        self.exit_dot = None
        self.dots_color = dots_color
        self.lines_color = lines_color
        self.add(self.lines, self.tags)

    def draw_line(self, start, end, dashed, color=WHITE):
        if dashed:
            line = DashedLine(start, end, dash_length=0.2, dashed_ratio=0.7, stroke_width=7, color=color)
        else:
            line = Line(start, end, stroke_width=7, color=color)
        self.lines.add(line)
        return line

    def add_number_tag(self, number, color):
        tag = NumberTag(number=number, fill_color=color, radius=0.3)
        tag.move_to([self.x, self.y, 0])
        tag.scale(0.85)
        self.tags.add(tag)
        return tag

    def build_structure(self, linearnode):
        if linearnode is None:
            self.add_number_tag(None, self.dots_color[-1])
            self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y - self.y_distance, 0], True, color=self.lines_color[1])  # ORANGE
            self.x += self.x_distance
            self.y -= self.y_distance
            return

        # Preorder
        self.add_number_tag(linearnode.val, linearnode.color)
        self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y + self.y_distance, 0], False, color=self.lines_color[1])
        self.x += self.x_distance
        self.y += self.y_distance

        self.build_structure(linearnode.next)

        # Postorder
        self.add_number_tag(linearnode.val, linearnode.color)
        self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y - self.y_distance, 0], True, color=self.lines_color[1])  # ORANGE
        self.x += self.x_distance
        self.y -= self.y_distance

    def build_structure_with_entry(self, head):
        self.entry_dot = Dot(color=self.dots_color[0], radius=0.25).move_to([self.x, self.y, 0])
        self.add(self.entry_dot)
        self.entry_line = self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y + self.y_distance, 0], False, color=self.lines_color[0])
        self.x += self.x_distance
        self.y += self.y_distance
        self.build_structure(head)
        self.lines[-1].set_stroke(color=self.lines_color[0])
        self.exit_dot = Dot(color=self.dots_color[0], radius=0.25).move_to([self.x, self.y, 0])
        self.add(self.exit_dot)

    def display(self, scene, wait=0.5):
        # Animate the first dot and line
        self.entry_line.z_index = 0
        self.entry_dot.z_index = 3
        scene.play(FadeIn(self.entry_dot), run_time=1)
        scene.play(Create(self.entry_line), run_time=1)
        scene.bring_to_front(self.entry_dot)
        scene.wait(wait)

        # Animate tags and lines for the rest
        for i, (ln, tg) in enumerate(zip(self.lines[1:], self.tags)):
            ln.z_index = 0
            tg.z_index = 3
            scene.play(FadeIn(tg), run_time=1)
            scene.wait(wait/5)
            scene.play(Create(ln), run_time=1)
            scene.bring_to_front(tg)
            scene.wait(wait)

        # Animate the final dot
        self.exit_dot.z_index = 3
        scene.play(FadeIn(self.exit_dot), run_time=1)
        scene.bring_to_front(self.exit_dot)
        scene.wait(wait)

    def scale_all(self, scale_factor):
        for tag in self.tags:
            tag.circle.stroke_width *= scale_factor
            tag.circle.radius *= scale_factor
            tag.outline.stroke_width *= scale_factor
            tag.outline.radius *= scale_factor
            tag.label.font_size *= (scale_factor*1.5)
        self.scale(scale_factor)

class Chain(VGroup):
    def __init__(self, root, x_start=-4, x_distance=0.5, y_start=-2, dots_color=[RED, ManimColor("#228be6"), ManimColor("#a5d8ff"), ManimColor("#2f9e44"), GREY], lines_color=[YELLOW, ORANGE], **kwargs):
        super().__init__(**kwargs)
        self.root = root
        self.x = x_start
        self.x_distance = x_distance
        self.y = y_start
        self.lines = VGroup()
        self.tags = VGroup()
        self.entry_dot = None
        self.entry_line = None
        self.exit_dot = None
        self.exit_line = None
        self.dots_color = dots_color
        self.lines_color = lines_color
        self.add(self.lines, self.tags)

    def draw_line(self, start, end, dashed, color=WHITE):
        if dashed:
            line = DashedLine(start, end, dash_length=0.3, dashed_ratio=0.7, stroke_width=7, color=color)
        else:
            line = Line(start, end, stroke_width=7, color=color)
        self.lines.add(line)
        return line

    def add_number_tag(self, number, color):
        tag = NumberTag(number=number, fill_color=color, radius=0.3)
        tag.move_to([self.x, self.y, 0])
        tag.scale(0.85)
        self.tags.add(tag)
        return tag

    def build_structure(self, linearnode):
        if linearnode is None:
            self.add_number_tag(None, self.dots_color[-1])
            return

        # Preorder
        self.add_number_tag(linearnode.val, linearnode.color)
        self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y, 0], False, color=self.lines_color[1])
        self.x += self.x_distance

        self.build_structure(linearnode.next)

    def build_structure_with_entry(self, head):
        self.entry_dot = Dot(color=self.dots_color[0], radius=0.25).move_to([self.x, self.y, 0])
        self.add(self.entry_dot)
        self.entry_line = self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y, 0], False, color=self.lines_color[0])
        self.x += self.x_distance
        self.build_structure(head)

    def display(self, scene, wait=0.5):
        # Animate the first dot and line
        self.entry_line.z_index = 0
        self.entry_dot.z_index = 3
        scene.play(FadeIn(self.entry_dot), run_time=1)
        scene.play(Create(self.entry_line), run_time=1)
        scene.bring_to_front(self.entry_dot)
        scene.wait(wait)

        # Animate tags and lines for the rest
        for i, (ln, tg) in enumerate(zip(self.lines[1:], self.tags)):
            ln.z_index = 0
            tg.z_index = 3
            scene.play(FadeIn(tg), run_time=1)
            scene.wait(wait/5)
            scene.play(Create(ln), run_time=1)
            scene.bring_to_front(tg)
            scene.wait(wait)
        tg = self.tags[-1]
        tg.z_index = 3
        scene.play(FadeIn(tg), run_time=1)
        scene.wait(wait/5)

    def scale_all(self, scale_factor):
        for tag in self.tags:
            tag.circle.stroke_width *= scale_factor
            tag.outline.stroke_width *= scale_factor
            tag.label.font_size *= (scale_factor*1.5)
        self.scale(scale_factor)

