_colors = [  # RGB str
    "a474ab",
    "c98787",
    "f2b880",
    "0fa3b1",
    "b0d197",
]

_current = 0


def get_color(course_name: str) -> str:
    """
    决定课程的颜色
    :param course_name: 课程名称
    :return: RGB颜色字符串，如 "00ff00"（绿色）
    """
    global _current
    result = _colors[_current]
    _current = (_current + 1) % len(_colors)
    return result


__all__ = ["get_color"]



