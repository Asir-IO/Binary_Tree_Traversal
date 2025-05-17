from manim import *

x_distance= 0.5
y_distance= 1.5

dots_color = [RED, GREY, ManimColor("#228be6"), ManimColor("#2f9e44")]
lines_color = [YELLOW, ORANGE, PURPLE] 

class NumberTag(VGroup):
    def __init__(self, number: int, fill_color=BLUE, radius=0.5, num_to_circle_ratio=100,**kwargs):
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
        self.circle = circle
        self.outline = outline
        self.label = label

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
def buildTree():
    r = Node(4, dots_color[1])
    insert(r, 2, dots_color[2])
    insert(r, 6, dots_color[2])
    return r

class RecursiveTreeStructure(Scene):
    def construct(self):
        self.x, self.y = -4, -2

        self.add(NumberPlane())
        self.dots = VGroup()
        self.lines = VGroup()
        self.tags = VGroup()
        #Entry dot
        self.draw_dot(dots_color[0])
        self.draw_line([self.x, self.y, 0], [self.x + x_distance, self.y + y_distance, 0], False, color=lines_color[0])

        self.x += x_distance
        self.y += y_distance
        self.build_structure(buildTree())
        #Exit dot
        self.draw_line([self.x - x_distance, self.y + y_distance, 0], [self.x, self.y, 0], True, color=lines_color[0])
        self.draw_dot(dots_color[0]) 
        self.dots.z_index = 10
        self.tags.z_index = 11
        self.add(self.dots)
        self.add(self.lines)
        self.add(self.tags)
        self.wait()

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
        tag.move_to([self.x, self.y, 0])  # Offset slightly above the dot
        self.tags.add(tag)


    def build_structure(self, node, parent=None):
        if node is None:
            self.draw_dot(dots_color[3])
            self.add_number_tag(None, dots_color[3])
            if parent is not None:
                if parent.left is None:
                    self.draw_line([self.x, self.y, 0], [self.x + x_distance, self.y - y_distance, 0], True, color=lines_color[2])
                else:
                    self.draw_line([self.x, self.y, 0], [self.x + x_distance, self.y - y_distance, 0], True, color=lines_color[1])
            self.x += x_distance
            self.y -= y_distance
            return

        # Preorder
        self.draw_dot(node.color)
        self.add_number_tag(node.val, node.color)
        self.draw_line([self.x, self.y, 0], [self.x + x_distance, self.y + y_distance, 0], False, color=lines_color[2])    
        self.x += x_distance
        self.y += y_distance

        self.build_structure(node.left, node)

        # Inorder
        self.draw_dot(node.color)
        self.add_number_tag(node.val, node.color)
        self.draw_line([self.x, self.y, 0], [self.x + x_distance, self.y + y_distance, 0], False, color=lines_color[1])  
        self.x += x_distance
        self.y += y_distance

        self.build_structure(node.right, node)

        # Postorder
        self.draw_dot(node.color)
        self.add_number_tag(node.val, node.color)
        if parent is not None:
            if node == parent.left:
                self.draw_line([self.x, self.y, 0], [self.x + x_distance, self.y - y_distance, 0], True, color=lines_color[2])
            else:
                self.draw_line([self.x, self.y, 0], [self.x + x_distance, self.y - y_distance, 0], True, color=lines_color[1])

        self.x += x_distance
        self.y -= y_distance
