from manim import *

def align_center(aligned, other, component):
    if component == 'x':
        aligned.move_to([other.get_center()[0], aligned.get_center()[1], 0])
    elif component == 'y':
        aligned.move_to([aligned.get_center()[0], other.get_center()[1], 0])

def spread_in_grid(vgroup: VGroup, rows: int = 8, cols: int = 14, padding: float = 0.1):
        total = len(vgroup)
        max_items = rows * cols

        if total > max_items:
            print(f"Warning: VGroup has more items ({total}) than grid cells ({max_items}). Some will be skipped.")
        
        # Calculate cell dimensions
        frame_width = config.frame_width
        frame_height = config.frame_height
        cell_width = frame_width / cols
        cell_height = frame_height / rows

        for i, mob in enumerate(vgroup[:max_items]):
            row = i // cols
            col = i % cols

            x = -frame_width / 2 + (col + 0.5) * cell_width
            y = frame_height / 2 - (row + 0.5) * cell_height

            mob.move_to([x, y, 0])