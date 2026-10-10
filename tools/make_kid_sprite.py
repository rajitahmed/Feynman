# /// script
# requires-python = ">=3.14"
# dependencies = ["pillow"]
# ///
"""One-off generator for the kid sprite sheet: 6 frames x 3 rows (generic, confused, got it).

Run from the repo root: uv run tools/make_kid_sprite.py
"""

import math
from collections.abc import Callable
from pathlib import Path

from PIL import Image, ImageDraw

OUTPUT_PATH = Path(__file__).parent.parent / "client" / "public" / "sprites" / "kid.png"

FRAME_SIZE = 256
# Drawn this many times larger, then shrunk, for smooth edges.
SUPERSAMPLE_FACTOR = 4
FRAMES_PER_ROW = 6

AVATAR_CENTER_X = 128
AVATAR_CENTER_Y = 140
AVATAR_RADIUS = 90

Color = tuple[int, ...]
Point = tuple[float, float]
DrawExtras = Callable[[ImageDraw.ImageDraw], None]

BACKGROUND_COLOR: Color = (209, 210, 212, 255)
BODY_COLOR: Color = (167, 168, 172, 255)
FACE_COLOR: Color = (70, 72, 80, 255)
OUTLINE_COLOR: Color = (60, 60, 70, 255)
BRIM_COLOR: Color = (40, 40, 52, 255)
RED: Color = (231, 76, 60, 255)
YELLOW: Color = (245, 196, 40, 255)
BLUE: Color = (52, 152, 219, 255)
GREEN: Color = (46, 204, 113, 255)
SWEAT_COLOR: Color = (120, 190, 240, 255)
BLUSH_COLOR: Color = (240, 150, 150, 170)
HAT_PANEL_COLORS = [RED, YELLOW, BLUE, GREEN]
PROPELLER_BLADE_COLORS = [RED, BLUE]

BEANIE_DOME_HALF_WIDTH = 33
BEANIE_DOME_HEIGHT = 34
PROPELLER_STICK_LENGTH = 9

FULL_TURN = 2 * math.pi
# The propeller spins in a flat ellipse, seen from the side.
PROPELLER_FLATTENING = 0.28


def scale(value: float) -> int:
    return int(round(value * SUPERSAMPLE_FACTOR))


def scale_points(points: list[Point]) -> list[tuple[int, int]]:
    return [(scale(point_x), scale(point_y)) for point_x, point_y in points]


def new_layer() -> Image.Image:
    size = FRAME_SIZE * SUPERSAMPLE_FACTOR
    return Image.new("RGBA", (size, size), (0, 0, 0, 0))


def draw_ellipse(
    draw: ImageDraw.ImageDraw,
    center: Point,
    radius_x: float,
    radius_y: float,
    fill: Color,
    outline: Color | None = None,
    outline_width: float = 0,
) -> None:
    center_x, center_y = center
    box = [
        scale(center_x - radius_x),
        scale(center_y - radius_y),
        scale(center_x + radius_x),
        scale(center_y + radius_y),
    ]
    if outline is None:
        draw.ellipse(box, fill=fill)
    else:
        draw.ellipse(box, fill=fill, outline=outline, width=scale(outline_width))


def draw_base_layer() -> Image.Image:
    """The static badge: a grey circle with shoulders clipped inside it."""
    badge = new_layer()
    avatar_center = (AVATAR_CENTER_X, AVATAR_CENTER_Y)
    draw_ellipse(
        ImageDraw.Draw(badge), avatar_center, AVATAR_RADIUS, AVATAR_RADIUS, BACKGROUND_COLOR
    )
    shoulders = new_layer()
    shoulders_center = (AVATAR_CENTER_X, AVATAR_CENTER_Y + 94)
    draw_ellipse(ImageDraw.Draw(shoulders), shoulders_center, 78, 80, BODY_COLOR)
    circle_mask = Image.new("L", badge.size, 0)
    ImageDraw.Draw(circle_mask).ellipse(
        [
            scale(AVATAR_CENTER_X - AVATAR_RADIUS),
            scale(AVATAR_CENTER_Y - AVATAR_RADIUS),
            scale(AVATAR_CENTER_X + AVATAR_RADIUS),
            scale(AVATAR_CENTER_Y + AVATAR_RADIUS),
        ],
        fill=255,
    )
    no_mask = Image.new("L", badge.size, 0)
    shoulders_mask = Image.composite(shoulders.split()[3], no_mask, circle_mask)
    badge.paste(shoulders, (0, 0), shoulders_mask)
    return badge


def draw_beanie_dome(head: Image.Image, center_x: float, base_y: float) -> None:
    dome_half_width, dome_height = BEANIE_DOME_HALF_WIDTH, BEANIE_DOME_HEIGHT
    panels = new_layer()
    panels_draw = ImageDraw.Draw(panels)
    panel_width = (2 * dome_half_width) / len(HAT_PANEL_COLORS)
    for panel_index, panel_color in enumerate(HAT_PANEL_COLORS):
        panel_left = center_x - dome_half_width + panel_index * panel_width
        panels_draw.rectangle(
            [
                scale(panel_left),
                scale(base_y - dome_height),
                scale(panel_left + panel_width),
                scale(base_y + 2),
            ],
            fill=panel_color,
        )
    dome_box = [
        scale(center_x - dome_half_width),
        scale(base_y - dome_height),
        scale(center_x + dome_half_width),
        scale(base_y + dome_height),
    ]
    dome_mask = Image.new("L", head.size, 0)
    dome_mask_draw = ImageDraw.Draw(dome_mask)
    dome_mask_draw.ellipse(dome_box, fill=255)
    dome_mask_draw.rectangle([0, scale(base_y), head.size[0], head.size[1]], fill=0)
    head.paste(panels, (0, 0), dome_mask)

    draw = ImageDraw.Draw(head)
    draw.arc(dome_box, 180, 360, fill=OUTLINE_COLOR, width=scale(1.4))
    for seam_index in range(1, len(HAT_PANEL_COLORS)):
        seam_x = center_x - dome_half_width + seam_index * panel_width
        offset_ratio = (seam_x - center_x) / dome_half_width
        seam_top = base_y - dome_height * math.sqrt(max(0, 1 - offset_ratio * offset_ratio))
        draw.line(
            [scale(seam_x), scale(seam_top), scale(seam_x), scale(base_y)],
            fill=OUTLINE_COLOR,
            width=scale(0.9),
        )
    draw.rounded_rectangle(
        [
            scale(center_x - dome_half_width - 2),
            scale(base_y - 1),
            scale(center_x + dome_half_width + 2),
            scale(base_y + 5),
        ],
        radius=scale(2.5),
        fill=BRIM_COLOR,
    )
    dome_top_y = base_y - dome_height
    draw_ellipse(draw, (center_x, dome_top_y), 4, 3.2, YELLOW, OUTLINE_COLOR, 1)
    draw.line(
        [
            scale(center_x),
            scale(dome_top_y),
            scale(center_x),
            scale(dome_top_y - PROPELLER_STICK_LENGTH),
        ],
        fill=OUTLINE_COLOR,
        width=scale(2),
    )


def draw_propeller(draw: ImageDraw.ImageDraw, hub: Point, angle: float) -> None:
    hub_x, hub_y = hub
    blade_length = 24
    blade_tip_half_width = 3.2
    blade_root_half_width = 1.6
    for blade_index, blade_color in enumerate(PROPELLER_BLADE_COLORS):
        blade_angle = angle + blade_index * math.pi
        tip_x = hub_x + blade_length * math.cos(blade_angle)
        tip_y = hub_y + blade_length * PROPELLER_FLATTENING * math.sin(blade_angle)
        normal_x = -math.sin(blade_angle) * PROPELLER_FLATTENING
        normal_y = math.cos(blade_angle)
        blade = [
            (hub_x + normal_x * blade_root_half_width, hub_y + normal_y * blade_root_half_width),
            (
                tip_x + normal_x * blade_tip_half_width,
                tip_y + normal_y * blade_tip_half_width * 0.6,
            ),
            (
                tip_x - normal_x * blade_tip_half_width,
                tip_y - normal_y * blade_tip_half_width * 0.6,
            ),
            (hub_x - normal_x * blade_root_half_width, hub_y - normal_y * blade_root_half_width),
        ]
        draw.polygon(scale_points(blade), fill=blade_color, outline=OUTLINE_COLOR)
    draw_ellipse(draw, hub, 2.4, 2.4, YELLOW, OUTLINE_COLOR, 0.9)


def draw_confused_face(draw: ImageDraw.ImageDraw, center_x: float, eye_y: float) -> None:
    draw_ellipse(draw, (center_x - 11, eye_y), 4.2, 4.2, FACE_COLOR)
    draw_ellipse(draw, (center_x + 11, eye_y + 0.5), 2.2, 2.2, FACE_COLOR)
    raised_eyebrow = [
        scale(center_x + 5),
        scale(eye_y - 9),
        scale(center_x + 17),
        scale(eye_y - 11),
    ]
    draw.line(raised_eyebrow, fill=FACE_COLOR, width=scale(1.6))
    wobbly_mouth = [
        (center_x - 9 + point_index * 3, eye_y + 14 + 2.2 * math.sin(point_index * 1.6))
        for point_index in range(7)
    ]
    draw.line(
        scale_points(wobbly_mouth),
        fill=FACE_COLOR,
        width=scale(1.8),
        joint="curve",
    )


def draw_happy_face(draw: ImageDraw.ImageDraw, center_x: float, eye_y: float) -> None:
    for eye_offset in (-11, 11):
        eye_box = [
            scale(center_x + eye_offset - 5),
            scale(eye_y - 4),
            scale(center_x + eye_offset + 5),
            scale(eye_y + 6),
        ]
        draw.arc(eye_box, 200, 340, fill=FACE_COLOR, width=scale(2))
    smile_box = [scale(center_x - 11), scale(eye_y + 4), scale(center_x + 11), scale(eye_y + 20)]
    draw.arc(smile_box, 15, 165, fill=FACE_COLOR, width=scale(2.2))
    draw_ellipse(draw, (center_x - 19, eye_y + 8), 4.5, 3, BLUSH_COLOR)
    draw_ellipse(draw, (center_x + 19, eye_y + 8), 4.5, 3, BLUSH_COLOR)


FaceDrawer = Callable[[ImageDraw.ImageDraw, float, float], None]


def draw_head_layer(propeller_angle: float, draw_face: FaceDrawer | None) -> Image.Image:
    """The head, beanie and propeller, in frame coordinates so it can move as one piece."""
    head = new_layer()
    head_center_x, head_center_y, head_radius = AVATAR_CENTER_X, AVATAR_CENTER_Y - 31.5, 34.3
    draw_ellipse(
        ImageDraw.Draw(head), (head_center_x, head_center_y), head_radius, head_radius, BODY_COLOR
    )
    dome_base_y = head_center_y - 18
    draw_beanie_dome(head, head_center_x, dome_base_y)
    draw = ImageDraw.Draw(head)
    propeller_hub = (head_center_x, dome_base_y - BEANIE_DOME_HEIGHT - PROPELLER_STICK_LENGTH)
    draw_propeller(draw, propeller_hub, propeller_angle)
    if draw_face is not None:
        draw_face(draw, head_center_x, head_center_y + 6)
    return head


def draw_question_mark(draw: ImageDraw.ImageDraw, center: Point, size: float, color: Color) -> None:
    center_x, center_y = center
    stroke_width = scale(size * 0.42)
    curl_box = [
        scale(center_x - size),
        scale(center_y - size),
        scale(center_x + size),
        scale(center_y + size * 0.9),
    ]
    draw.arc(curl_box, 180, 90 + 360, fill=color, width=stroke_width)
    stem = [
        scale(center_x),
        scale(center_y + size * 0.9),
        scale(center_x),
        scale(center_y + size * 1.3),
    ]
    draw.line(stem, fill=color, width=stroke_width)
    draw_ellipse(draw, (center_x, center_y + size * 2.0), size * 0.28, size * 0.28, color)


def draw_sparkle(draw: ImageDraw.ImageDraw, center: Point, radius: float) -> None:
    center_x, center_y = center
    star_points = []
    for point_index in range(8):
        point_angle = point_index * math.pi / 4
        is_tip = point_index % 2 == 0
        point_radius = radius if is_tip else radius * 0.28
        star_points.append(
            (
                scale(center_x + point_radius * math.cos(point_angle)),
                scale(center_y + point_radius * math.sin(point_angle)),
            )
        )
    draw.polygon(star_points, fill=YELLOW)


def resize_around_pivot(
    head: Image.Image, pivot: tuple[int, int], width_scale: float, height_scale: float
) -> Image.Image:
    width, height = head.size
    resized = head.resize((int(width * width_scale), int(height * height_scale)), Image.LANCZOS)
    pivot_x, pivot_y = pivot
    repositioned = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    repositioned.paste(
        resized, (int(pivot_x - pivot_x * width_scale), int(pivot_y - pivot_y * height_scale))
    )
    return repositioned


def compose_frame(
    propeller_angle: float,
    shift_x: float = 0,
    shift_y: float = 0,
    tilt_degrees: float = 0,
    width_scale: float = 1.0,
    height_scale: float = 1.0,
    draw_face: FaceDrawer | None = None,
    draw_extras: DrawExtras | None = None,
) -> Image.Image:
    frame = draw_base_layer()
    head = draw_head_layer(propeller_angle, draw_face)
    # The neck: the head squashes and tilts around this point.
    pivot = (scale(AVATAR_CENTER_X), scale(AVATAR_CENTER_Y + 6))
    if width_scale != 1.0 or height_scale != 1.0:
        head = resize_around_pivot(head, pivot, width_scale, height_scale)
    if tilt_degrees:
        head = head.rotate(tilt_degrees, resample=Image.BICUBIC, center=pivot)
    shifted_head = new_layer()
    shifted_head.paste(head, (scale(shift_x), scale(shift_y)))
    frame = Image.alpha_composite(frame, shifted_head)
    if draw_extras is not None:
        draw_extras(ImageDraw.Draw(frame))
    return frame.resize((FRAME_SIZE, FRAME_SIZE), Image.LANCZOS)


def draw_generic_frame(frame_index: int) -> Image.Image:
    progress = frame_index / FRAMES_PER_ROW
    wave = math.sin(FULL_TURN * progress)
    return compose_frame(
        propeller_angle=frame_index * (FULL_TURN / FRAMES_PER_ROW) * 0.9,
        shift_y=1.6 * wave,
        height_scale=1 + 0.012 * wave,
    )


def draw_confused_extras(draw: ImageDraw.ImageDraw, frame_index: int) -> None:
    question_growth = [0.0, 0.5, 0.85, 1.0, 1.0, 0.8][frame_index]
    if question_growth > 0:
        big_question_center = (192, 58 - 3 * question_growth)
        draw_question_mark(draw, big_question_center, 7 * question_growth + 1, RED)
    if frame_index in (2, 3, 4):
        small_question_growth = (4 - abs(frame_index - 3)) / 4
        draw_question_mark(draw, (66, 76), 4.5 * small_question_growth + 1, BLUE)
    sweat_drop_fall = [0, 0, 5, 10, 14, 0][frame_index]
    if sweat_drop_fall:
        drop_tip = [
            (205, 110 + sweat_drop_fall - 8),
            (200, 110 + sweat_drop_fall),
            (210, 110 + sweat_drop_fall),
        ]
        draw.polygon(scale_points(drop_tip), fill=SWEAT_COLOR)
        draw_ellipse(draw, (205, 112 + sweat_drop_fall), 5, 5, SWEAT_COLOR)


def draw_confused_frame(frame_index: int) -> Image.Image:
    progress = frame_index / FRAMES_PER_ROW
    tilt_degrees = 11 * math.sin(FULL_TURN * progress)
    # Every other frame spins slower, so the propeller sputters.
    sputter = 1 if frame_index % 2 == 0 else 0.4
    return compose_frame(
        propeller_angle=(math.pi * 0.35) * frame_index * sputter,
        shift_x=-tilt_degrees * 0.15,
        tilt_degrees=tilt_degrees,
        draw_face=draw_confused_face,
        draw_extras=lambda draw: draw_confused_extras(draw, frame_index),
    )


def draw_got_it_extras(draw: ImageDraw.ImageDraw, frame_index: int) -> None:
    sparkle_spots = [(40, 70), (216, 66), (222, 150), (34, 150)]
    for spot_index, spot in enumerate(sparkle_spots):
        # Each sparkle is out of step with the others, so they twinkle in turn.
        phase = (frame_index + spot_index * 1.5) % FRAMES_PER_ROW
        draw_sparkle(draw, spot, 3 + 7 * abs(math.sin(math.pi * phase / FRAMES_PER_ROW)))


def draw_got_it_frame(frame_index: int) -> Image.Image:
    progress = frame_index / FRAMES_PER_ROW
    bounce_height = abs(math.sin(math.pi * progress)) * 9
    squash = 1 + 0.06 * math.cos(FULL_TURN * progress)
    return compose_frame(
        propeller_angle=frame_index * (FULL_TURN / FRAMES_PER_ROW) * 2.3,
        shift_y=-bounce_height,
        tilt_degrees=3 * math.sin(FULL_TURN * progress),
        width_scale=2 - squash,
        height_scale=squash,
        draw_face=draw_happy_face,
        draw_extras=lambda draw: draw_got_it_extras(draw, frame_index),
    )


# Row order must match KID_SPRITE_ROW_BY_MOOD in client/src/components/kidMood.ts.
ROW_DRAWERS = [draw_generic_frame, draw_confused_frame, draw_got_it_frame]


def make_sprite_sheet() -> Image.Image:
    sheet = Image.new("RGBA", (FRAME_SIZE * FRAMES_PER_ROW, FRAME_SIZE * len(ROW_DRAWERS)))
    for row_index, draw_frame in enumerate(ROW_DRAWERS):
        for frame_index in range(FRAMES_PER_ROW):
            sheet.paste(draw_frame(frame_index), (frame_index * FRAME_SIZE, row_index * FRAME_SIZE))
    return sheet


if __name__ == "__main__":
    make_sprite_sheet().save(OUTPUT_PATH)
    print(f"Saved {OUTPUT_PATH}")
