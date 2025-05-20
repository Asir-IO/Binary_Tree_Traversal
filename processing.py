from manim import *

def align_center(aligned, other, component):
    if component == 'x':
        aligned.move_to([other.get_center()[0], aligned.get_center()[1], 0])
    elif component == 'y':
        aligned.move_to([aligned.get_center()[0], other.get_center()[1], 0])