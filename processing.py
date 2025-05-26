from manim import *

def align_center(aligned, other, component):
    if component == 'x':
        aligned.move_to([other.get_center()[0], aligned.get_center()[1], 0])
    elif component == 'y':
        aligned.move_to([aligned.get_center()[0], other.get_center()[1], 0])

def spread_in_grid(vgroup: VGroup, rows: int = 8, cols: int = 14, y_shift=0, padding: float = 0.1):
    total = len(vgroup)
    frame_width = config.frame_width
    frame_height = config.frame_height
    cell_width = frame_width / cols
    cell_height = frame_height / rows

    max_items = rows * cols  # This needs to be handled dynamically now
    grid = [[None for _ in range(cols)] for _ in range(rows)]

    i = 0  # index into vgroup
    for row in range(rows):
        col = 0
        while col < cols and i < total:
            mob = vgroup[i]
            if mob.width > cell_width and col + 1 < cols:
                # Occupies 2 cells
                x = -frame_width / 2 + (col + 1) * cell_width
                col += 2  # skip one more cell
            else:
                x = -frame_width / 2 + (col + 0.5) * cell_width
                col += 1

            y = (frame_height / 2 - (row + 0.5) * cell_height) - y_shift
            mob.move_to([x, y, 0])
            i += 1


def move_by_anchor(obj, target, anchor):
    if (anchor == "left"):
        anchor_pos = obj.get_left()
    if (anchor == "right"):
        anchor_pos = obj.get_right()
    shift = target - anchor_pos
    obj.shift(shift)

def font_size_by_ratio(tex_string, current_font_size=48, width=1, ratio=2/3):
    temp = Tex(tex_string, font_size=current_font_size)
    tex_width = temp.width
    target_tex_width = width * ratio
    adjusted_font_size = current_font_size * (target_tex_width / tex_width)
    return adjusted_font_size

def create_position_label(obj, font_size=24, buff=0.1):
    def get_label_box():
        pos = obj.get_center()
        label = Text(f"({pos[0]:.2f}, {pos[1]:.2f})", font_size=font_size)
        box = SurroundingRectangle(label, color=BLUE, buff=buff)
        box.set_fill(BLACK, opacity=0.8)
        return VGroup(box, label).move_to(pos)
    return always_redraw(get_label_box)

def add_highlight_to_text(text, initial, final, color=GREEN, opacity=0.5, text_z_index=0):
    #SPACES ARE NOT COUNTED
    text_z_index = text.z_index
    to_be_highlighted = text[0][initial:final+1]
    highlight = Rectangle(
        width=to_be_highlighted.width * 1.05,
        height=to_be_highlighted.height,
        color=color,
        fill_opacity=opacity,
        stroke_width=0  # optional: remove border
    ).move_to(to_be_highlighted.get_center())

    highlight.shift(RIGHT * (highlight.width * 0.0008) + DOWN * (highlight.height * 0.2))
    highlight.set_z_index(text_z_index - 1)
    return highlight