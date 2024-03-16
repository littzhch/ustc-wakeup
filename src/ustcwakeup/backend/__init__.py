from abc import ABC, abstractmethod
from datetime import date
from ..course_table import *


class CourseTableOutput(ABC):
    @abstractmethod
    def suggest_file_name(self) -> str:
        """
        不包含后缀名
        """
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """
        不包含 '.'
        """
        pass
    
    @abstractmethod
    def get_content(self) -> bytes:
        pass


class CourseTableHandler(ABC):    
    @abstractmethod
    def __init__(self, semester_name: str):
        pass
    
    @abstractmethod
    def add_course(self, course: Course):
        pass
    
    @abstractmethod
    def set_semester_start_date(self, start_date: date):
        """
        第一周周一的前一天
        """
        pass
    
    @abstractmethod
    def set_semester_weeks(self, amount: int):
        pass
    
    @abstractmethod
    def finish(self) -> CourseTableOutput:
        pass

available_handlers: dict[str, type[CourseTableHandler]] = {}

def register_handler(handler: type[CourseTableHandler], name: str):
    available_handlers[name] = handler

from .wakeup import WakeupHandler

__all__ = ["CourseTableHandler", "CourseTableOutput", "register_handler", "available_handlers"]

