from ..backend import *
from .parser import *
from .network import *

__all__ = ["get_course_table"]

def get_course_table(
    username: str,
    password: str, 
    semester_name: str, 
    Handler: type[CourseTableHandler], 
    force_ipv6: bool = False, 
    force_ipv4: bool = False,
) -> CourseTableOutput:
    data = get_web_data(username, password, semester_name, force_ipv6, force_ipv4)
    handler = Handler(semester_name)
    parse_and_feed_data(data, handler)
    return handler.finish()
