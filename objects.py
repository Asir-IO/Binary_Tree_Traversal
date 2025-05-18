from manim import *

# Simple binary tree node
class Node:
    def __init__(self, key, color=WHITE):
        self.left = None
        self.right = None
        self.parent = None
        self.color = color
        self.val = key

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
def buildTree(dots_color, num_nodes):
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


class TraversalTree(VGroup):
    def __init__(self, root, x_start=-4, x_distance=0.5, y_start=-2, y_distance=1.5, dots_color=[RED, GREY, ManimColor("#228be6"), ManimColor("#2f9e44")], lines_color=[YELLOW, ORANGE, PURPLE], **kwargs):
        super().__init__(**kwargs)
        self.root = root
        self.x = x_start
        self.x_distance = x_distance
        self.y = y_start
        self.y_distance = y_distance
        self.dots = VGroup()
        self.lines = VGroup()
        self.tags = VGroup()
        self.dots_color = dots_color
        self.lines_color = lines_color
        self.add(self.dots, self.lines, self.tags)

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
        tag.scale(0.85)
        self.tags.add(tag)

    def build_structure(self, node, child_side=None):
        if node is None:
            self.draw_dot(self.dots_color[-1])
            self.add_number_tag(None, self.dots_color[-1])
            if child_side is not None:
                if child_side == "left":
                    self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y - self.y_distance, 0], True, color=self.lines_color[2])  # PURPLE
                elif child_side == "right":
                    self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y - self.y_distance, 0], True, color=self.lines_color[1])  # ORANGE
            self.x += self.x_distance
            self.y -= self.y_distance
            return

        # Preorder
        self.draw_dot(node.color)
        self.add_number_tag(node.val, node.color)
        self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y + self.y_distance, 0], False, color=self.lines_color[2])
        self.x += self.x_distance
        self.y += self.y_distance

        self.build_structure(node.left, "left")

        # Inorder
        self.draw_dot(node.color)
        self.add_number_tag(node.val, node.color)
        self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y + self.y_distance, 0], False, color=self.lines_color[1])
        self.x += self.x_distance
        self.y += self.y_distance

        self.build_structure(node.right, "right")

        # Postorder
        self.draw_dot(node.color)
        self.add_number_tag(node.val, node.color)
        if child_side is not None:
            if child_side == "left":
                self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y - self.y_distance, 0], True, color=self.lines_color[2])
            elif child_side == "right":
                self.draw_line([self.x, self.y, 0], [self.x + self.x_distance, self.y - self.y_distance, 0], True, color=self.lines_color[1])
        self.x += self.x_distance
        self.y -= self.y_distance