import json
from codecs import open
from functools import total_ordering


@total_ordering
class Time:
    def __init__(self, hour: int, minute: int):
        self.hour = hour
        self.minute = minute
        self.minutes = hour * 60 + minute

    def __int__(self):
        return self.minutes

    def __str__(self):
        return "{:0>2d}:{:0>2d}".format(self.hour, self.minute)

    def __eq__(self, other):
        return int(self) == int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __sub__(self, other):
        return self.minutes - int(other)

    def __add__(self, other):
        minutes = self.minutes + other
        hour = minutes // 60
        minute = minutes % 60
        return Time(hour, minute)


@total_ordering
class TimeNode:
    def __init__(self, start_time: Time, end_time: Time):
        self.start_time = start_time
        self.end_time = end_time

    def __eq__(self, other):
        return self.start_time == other.start_time \
               and self.end_time == other.end_time

    def __gt__(self, other):
        return self.start_time > other.start_time

    def __len__(self):
        return self.end_time - self.start_time

    def __sub__(self, other):
        return self.start_time - other.end_time

    def get_info(self):
        return {
            "endTime": str(self.end_time),
            "node": None,
            "startTime": str(self.start_time),
            "timeTable": None
        }


class TimeTable:
    def __init__(self, name, table_id=1):
        self.name = name
        self.id = table_id
        self.courseLen = None
        self.sameBreakLen = None
        self.sameLen = None
        self.theBreakLen = None
        self.time_nodes = []

    def add_time_node(self, node: TimeNode):
        self.time_nodes.append(node)
        if len(self.time_nodes) == 1:
            self.courseLen = len(node)
            self.sameLen = True
        elif self.sameLen is True:
            if self.courseLen != len(node):
                self.sameLen = False

    def __str__(self):
        self.time_nodes.sort()
        interval = self.time_nodes[1] - self.time_nodes[0]
        for ind in range(1, len(self.time_nodes) - 1):
            if interval != self.time_nodes[ind + 1] - self.time_nodes[ind]:
                self.sameBreakLen = False
                self.theBreakLen = 10
                break
        if self.sameBreakLen is None:
            self.sameBreakLen = True
            self.theBreakLen = interval

        nodes_info = []
        for node in self.time_nodes:
            info = node.get_info()
            info["node"] = self.time_nodes.index(node) + 1
            info["timeTable"] = self.id
            nodes_info.append(info)

        while len(nodes_info) < 30:
            nodes_info.append({
                "endTime": str(Time(0, 0) + self.courseLen),
                "node": len(nodes_info) + 1,
                "startTime": "00:00",
                "timeTable": self.id
            })

        table_info = {
            "name": self.name,
            "id": self.id,
            "courseLen": self.courseLen,
            "sameBreakLen": self.sameBreakLen,
            "sameLen": self.sameLen,
            "theBreakLen": self.theBreakLen,
        }

        return json.dumps(table_info) + "\n" + json.dumps(nodes_info) + "\n"


class Activity:
    def __init__(self, day: int, start_period: int, length: int, start_week: int, end_week: int,
                 location="", teacher="", week_type=0):
        self.day = day
        self.start_period = start_period
        self.length = length
        self.start_week = start_week
        self.end_week = end_week
        self.location = location
        self.teacher = teacher
        self.week_type = week_type

    def can_merge(self, other):
        return \
            self.day == other.day \
            and self.start_period == other.start_period \
            and self.length == other.length \
            and self.start_week == other.start_week \
            and self.end_week == other.end_week \
            and self.location == other.location \
            and self.week_type == other.week_type

    def merge_with(self, other):
        self.teacher += "\n"
        self.teacher += other.teacher

    def get_info(self) -> dict:
        return {
            "day": self.day,
            "endTime": "",
            "endWeek": self.end_week,
            "level": 0,
            "ownTime": False,
            "room": self.location,
            "startNode": self.start_period,
            "startTime": "",
            "startWeek": self.start_week,
            "step": self.length,
            "tableId": 1,
            "teacher": self.teacher,
            "type": self.week_type
        }


class Course:
    def __init__(self, name="未命名", credit=1.0, note="", color="#ffd717ff"):
        self.name = name
        self.credit = credit
        self.color = color
        self.id = 0
        self.note = note
        self.activity_list = []

    def add_activity(self, activity: Activity):
        self.activity_list.append(activity)

    def get_info(self):
        return {
            "color": self.color,
            "courseName": self.name,
            "credit": self.credit,
            "id": self.id,
            "note": self.note,
            "tableId": 1
        }

    def get_activities_info(self):
        for activity in self.activity_list:
            result = activity.get_info()
            result["id"] = self.id
            yield result


class CourseTable:
    def __init__(self, name="未命名", start_date="2021-1-1", maxweek=18, time_table=None):
        self.name = name
        self.start_date = start_date
        self.maxweek = maxweek
        self.time_table = time_table
        self.course_list = []

    def add_course(self, course: Course):
        course.id = len(self.course_list) + 1
        self.course_list.append(course)

    def set_time_table(self, time_table: TimeTable):
        self.time_table = time_table

    def get_course(self, course_name):
        for course in self.course_list:
            if course.name == course_name:
                return course
        return None

    def write_file(self, filename: str):
        course_table_info = {
            "background": "",
            "courseTextColor": -1,
            "id": 1,
            "itemAlpha": 60,
            "itemHeight": 64,
            "itemTextSize": 12,
            "maxWeek": self.maxweek,
            "nodes": len(self.time_table.time_nodes),
            "showOtherWeekCourse": True,
            "showSat": False,
            "showSun": False,
            "showTime": False,
            "startDate": self.start_date,
            "strokeColor": -2130706433,
            "sundayFirst": False,
            "tableName": self.name,
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

        courses_info = []
        activities_info = []
        for course in self.course_list:
            courses_info.append(course.get_info())
            for activity in course.get_activities_info():
                activities_info.append(activity)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(self.time_table))
            f.write(json.dumps(course_table_info) + '\n')
            f.write(json.dumps(courses_info) + '\n')
            f.write(json.dumps(activities_info) + '\n')

