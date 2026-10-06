"""Draw a recursive Koch snowflake with turtle or save it as SVG."""

import argparse
import math
import turtle
from pathlib import Path
from xml.etree import ElementTree


def koch_curve(start: complex, end: complex, level: int) -> list[complex]:
    """Return recursive curve vertices, excluding the final endpoint."""
    if level == 0:
        return [start]

    third = (end - start) / 3
    first = start + third
    peak = first + third * complex(0.5, math.sqrt(3) / 2)
    second = start + 2 * third
    points = []
    for left, right in ((start, first), (first, peak), (peak, second), (second, end)):
        points.extend(koch_curve(left, right, level - 1))
    return points


def snowflake_points(level: int, side: float = 600) -> list[complex]:
    """Build a closed snowflake from three clockwise triangle sides."""
    if level < 0:
        raise ValueError("level must be non-negative")
    if side <= 0:
        raise ValueError("side must be positive")
    height = side * math.sqrt(3) / 2
    vertices = [
        complex(-side / 2, height / 3),
        complex(side / 2, height / 3),
        complex(0, -2 * height / 3),
    ]
    points = []
    for index in range(3):
        points.extend(koch_curve(vertices[index], vertices[(index + 1) % 3], level))
    return points + [points[0]]


def save_svg(points: list[complex], output: Path) -> None:
    """Save the same vertices as a scalable image without a GUI."""
    margin = 20
    xs = [point.real for point in points]
    ys = [-point.imag for point in points]
    view_box = (
        f"{min(xs) - margin} {min(ys) - margin} "
        f"{max(xs) - min(xs) + 2 * margin} {max(ys) - min(ys) + 2 * margin}"
    )
    root = ElementTree.Element(
        "svg",
        xmlns="http://www.w3.org/2000/svg",
        width="800",
        height="800",
        viewBox=view_box,
    )
    ElementTree.SubElement(
        root,
        "polyline",
        points=" ".join(f"{point.real},{-point.imag}" for point in points),
        fill="#cffafe",
        stroke="#0369a1",
        **{"stroke-width": "1", "stroke-linejoin": "round"},
    )
    ElementTree.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)


def draw_snowflake(points: list[complex], level: int) -> None:
    """Display the snowflake in a turtle window."""
    screen = turtle.Screen()
    screen.setup(900, 900)
    screen.title(f"Koch snowflake - recursion level {level}")
    screen.bgcolor("#f8fafc")
    screen.tracer(0)
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.color("#0369a1", "#cffafe")
    pen.penup()
    pen.goto(points[0].real, points[0].imag)
    pen.pendown()
    pen.begin_fill()
    for point in points[1:]:
        pen.goto(point.real, point.imag)
    pen.end_fill()
    screen.update()
    screen.exitonclick()


def main() -> None:
    """Read a recursion level and display or export the snowflake."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("level", nargs="?", type=int, default=3)
    parser.add_argument(
        "--output", type=Path, help="Save an SVG instead of opening a window"
    )
    args = parser.parse_args()
    if not 0 <= args.level <= 6:
        parser.error("level must be between 0 and 6")

    points = snowflake_points(args.level)
    if args.output:
        try:
            save_svg(points, args.output)
        except OSError as error:
            parser.exit(1, f"Cannot save SVG: {error}\n")
        print(f"Saved {args.output} ({len(points) - 1} segments)")
    else:
        draw_snowflake(points, args.level)


if __name__ == "__main__":
    main()
