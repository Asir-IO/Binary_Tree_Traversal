from manim import *

x_distance= 0.5
y_distance= 1.5

dots_color = [RED, WHITE, BLUE, GREEN]
lines_color = [YELLOW, ORANGE, PURPLE] 

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
    r = Node(4, WHITE)
    insert(r, 2, BLUE)
    insert(r, 6, BLUE)
    return r

class RecursiveTreeStructure(Scene):
    def construct(self):
        self.x, self.y = -4, -2

        self.add(NumberPlane())
        self.dots = VGroup()
        self.lines = VGroup()
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
        self.add(self.dots)
        self.add(self.lines)
        self.wait()

    def draw_dot(self, color=WHITE):
        dot = Dot(color=color, radius=0.1).move_to([self.x, self.y, 0])
        self.dots.add(dot)

    def draw_line(self, start, end, dashed, color=WHITE):
        if dashed:
            line = DashedLine(start, end, color=color)
        else:
            line = Line(start, end, color=color)
        self.lines.add(line)

    def build_structure(self, node, parent=None):
        if node is None:
            self.draw_dot(dots_color[3])
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
        self.draw_line([self.x, self.y, 0], [self.x + x_distance, self.y + y_distance, 0], False, color=lines_color[2])    
        self.x += x_distance
        self.y += y_distance

        self.build_structure(node.left, node)

        # Inorder
        self.draw_dot(node.color)
        self.draw_line([self.x, self.y, 0], [self.x + x_distance, self.y + y_distance, 0], False, color=lines_color[1])  
        self.x += x_distance
        self.y += y_distance

        self.build_structure(node.right, node)

        # Postorder
        self.draw_dot(node.color)
        if parent is not None:
            if node == parent.left:
                self.draw_line([self.x, self.y, 0], [self.x + x_distance, self.y - y_distance, 0], True, color=lines_color[2])
            else:
                self.draw_line([self.x, self.y, 0], [self.x + x_distance, self.y - y_distance, 0], True, color=lines_color[1])

        self.x += x_distance
        self.y -= y_distance
