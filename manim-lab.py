from manim import *
from objects import *
from processing import *
from animations import *

class Test(Scene):
    def construct(self):
        node = NumberTag(1, radius= 0.15)
        node_code = NodeCode(node)
        displayed = node_code.to_be_displayed("preorder")
        self.add(node_code)
        for _ in displayed:
            self.play(Succession(Indicate(_), _.animate.set_color(YELLOW)))
            self.wait()
        self.wait()

