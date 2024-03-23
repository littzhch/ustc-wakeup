from . import CourseTableHandler, CourseTableOutput, register_handler
from ..course_table import *
from datetime import date
import json

time_table = """\
{"name": "USTC Time Table", "id": 1, "courseLen": 45, "sameBreakLen": false, "sameLen": true, "theBreakLen": 10}
[{"endTime": "08:35", "node": 1, "startTime": "07:50", "timeTable": 1}, {"endTime": "09:25", "node": 2, "startTime": "08:40", "timeTable": 1}, {"endTime": "10:30", "node": 3, "startTime": "09:45", "timeTable": 1}, {"endTime": "11:20", "node": 4, "startTime": "10:35", "timeTable": 1}, {"endTime": "12:10", "node": 5, "startTime": "11:25", "timeTable": 1}, {"endTime": "14:45", "node": 6, "startTime": "14:00", "timeTable": 1}, {"endTime": "15:35", "node": 7, "startTime": "14:50", "timeTable": 1}, {"endTime": "16:40", "node": 8, "startTime": "15:55", "timeTable": 1}, {"endTime": "17:30", "node": 9, "startTime": "16:45", "timeTable": 1}, {"endTime": "18:20", "node": 10, "startTime": "17:35", "timeTable": 1}, {"endTime": "20:15", "node": 11, "startTime": "19:30", "timeTable": 1}, {"endTime": "21:05", "node": 12, "startTime": "20:20", "timeTable": 1}, {"endTime": "21:55", "node": 13, "startTime": "21:10", "timeTable": 1}, {"endTime": "00:45", "node": 14, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 15, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 16, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 17, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 18, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 19, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 20, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 21, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 22, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 23, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 24, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 25, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 26, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 27, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 28, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 29, "startTime": "00:00", "timeTable": 1}, {"endTime": "00:45", "node": 30, "startTime": "00:00", "timeTable": 1}]
"""


class Wakeup(CourseTableHandler, CourseTableOutput):

    def __init__(self, semester_name: str):
        self.semeter_name: str = semester_name
        self.courses_info: list[dict] = []
        self.activities_info: list[dict] = []
        self.output = time_table
        self.course_table_info = {
            "background": "",
            "courseTextColor": -1,
            "id": 1,
            "itemAlpha": 60,
            "itemHeight": 64,
            "itemTextSize": 12,
            "maxWeek": None,  # fill later
            "nodes": 13,
            "showOtherWeekCourse": True,
            "showSat": False,
            "showSun": False,
            "showTime": False,
            "startDate": None,  # fill later
            "strokeColor": -2130706433,
            "sundayFirst": False,
            "tableName": self.semeter_name,
            "textColor": -16777216,
            "timeTable": 1,
            "type": 0,
            "widgetCourseTextColor": -1,
            "widgetItemAlpha": 60,
            "widgetItemHeight": 64,
            "widgetItemTextSize": 12,
            "widgetStrokeColor": -2130706433,
            "widgetTextColor": -16777216
        }

    def add_course(self, course: Course):
        if len(course.activities) == 0:
            return
        course_id = len(self.courses_info) + 1

        note = f'课堂号: {course.course_id}.{course.class_id}\n'
        for teacher in course.teachers:
            note += f'{teacher.name_zh}:\n\t'
            note += f'性别: {"女" if teacher.gender == 0 else "男"}\n\t'
            note += f'年龄: {teacher.age}\n\t'
            note += f'职称: {teacher.title}\n\t'
            note += f'邮箱: {teacher.email}\n'

        course_info = {
            "color": get_color(),
            "courseName": course.name_zh,
            "credit": course.credits,
            "id": course_id,
            "note": note,
            "tableId": 1
        }
        self.courses_info.append(course_info)
        for activity in course.activities:
            teacher_names: list[str] = [
                teacher.name_zh for teacher in activity.teachers
            ]
            activity_info = {
                "id":
                course_id,
                "day":
                activity.time_period.weekday
                if activity.time_period.weekday != 0 else 7,
                "endTime":
                "",
                "endWeek":
                activity.week_range.last_week,
                "level":
                0,
                "ownTime":
                False,
                "room":
                activity.location,
                "startNode":
                activity.time_period.start,
                "startTime":
                "",
                "startWeek":
                activity.week_range.first_week,
                "step":
                activity.time_period.end - activity.time_period.start + 1,
                "tableId":
                1,
                "teacher":
                '\n'.join(teacher_names),
                "type":
                activity.week_range.week_type
            }
            self.activities_info.append(activity_info)

    def set_semester_start_date(self, start_date: date):
        date_str = start_date.strftime("%Y-%m-%d").replace('-0', '-')
        self.course_table_info["startDate"] = date_str

    def set_semester_weeks(self, amount: int):
        self.course_table_info["maxWeek"] = amount

    def finish(self) -> CourseTableOutput:
        self.output += json.dumps(self.course_table_info) + '\n'
        self.output += json.dumps(self.courses_info) + '\n'
        self.output += json.dumps(self.activities_info) + '\n'
        return self

    def suggest_file_name(self) -> str:
        return self.semeter_name + "课程表"

    def get_file_extension(self) -> str:
        return "wakeup_schedule"

    def get_content(self) -> bytes:
        return self.output.encode("utf-8")


colors = [  # RGB str
    "a474ab",
    "c98787",
    "f2b880",
    "0fa3b1",
    "b0d197",
]
current = 0


def get_color() -> str:
    global current
    result = colors[current]
    current = (current + 1) % len(colors)
    return '#ff' + result


register_handler(Wakeup, "wakeup")
