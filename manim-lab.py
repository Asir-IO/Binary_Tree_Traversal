from manim import *
from objects import *
from processing import *
from animations import *

dots_color=[RED, ManimColor("#2f9e44"), ManimColor("#228be6"), ManimColor("#a5d8ff"), GREY]
lines_color = [YELLOW, ORANGE, PURPLE]

class Test(Scene):
    def construct(self):
        BTree = BinaryTree(root = buildTree())
        BTree.build_structure(BTree.root)
        BTree.display(self)
        self.wait()
        BTree.generate_target()
        BTree.target.move_to([0,-2,0])
        BTree.target.scale_all(0.7)
        self.play(MoveToTarget(BTree))
        self.wait()
