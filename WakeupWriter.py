import json
from codecs import open


useless_information = "{\"courseLen\": 45,\"id\": 1,\"name\": \"ustc_timetable\",\"sameBreakLen\": false,\
\"sameLen\": true,\"theBreakLen\": 10}\n\
[{\"endTime\": \"08:35\",\"node\": 1,\"startTime\": \"07:50\",\"timeTable\": 1},\
{\"endTime\": \"09:25\",\"node\": 2,\"startTime\": \"08:40\",\"timeTable\": 1},\
{\"endTime\": \"10:30\",\"node\": 3,\"startTime\": \"09:45\",\"timeTable\": 1},\
{\"endTime\": \"11:20\",\"node\": 4,\"startTime\": \"10:35\",\"timeTable\": 1},\
{\"endTime\": \"12:10\",\"node\": 5,\"startTime\": \"11:25\",\"timeTable\": 1},\
{\"endTime\": \"14:45\",\"node\": 6,\"startTime\": \"14:00\",\"timeTable\": 1},\
{\"endTime\": \"15:35\",\"node\": 7,\"startTime\": \"14:50\",\"timeTable\": 1},\
{\"endTime\": \"16:40\",\"node\": 8,\"startTime\": \"15:55\",\"timeTable\": 1},\
{\"endTime\": \"17:30\",\"node\": 9,\"startTime\": \"16:45\",\"timeTable\": 1},\
{\"endTime\": \"18:20\",\"node\": 10,\"startTime\": \"17:35\",\"timeTable\": 1},\
{\"endTime\": \"20:15\",\"node\": 11,\"startTime\": \"19:30\",\"timeTable\": 1},\
{\"endTime\": \"21:05\",\"node\": 12,\"startTime\": \"20:20\",\"timeTable\": 1},\
{\"endTime\": \"21:55\",\"node\": 13,\"startTime\": \"21:10\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 14,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 15,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 16,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 17,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 18,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 19,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 20,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 21,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 22,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 23,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 24,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 25,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 26,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 27,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 28,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 29,\"startTime\": \"00:00\",\"timeTable\": 1},\
{\"endTime\": \"00:45\",\"node\": 30,\"startTime\": \"00:00\",\"timeTable\": 1}]\n"


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

    def all_activities(self):
        for activity in self.activity_list:
            result = activity.get_info()
            result["id"] = self.id
            yield result


class CourseTable:
    def __init__(self, name="未命名", start_date="2021-1-1", maxweek=18):
        self.name = name
        self.start_date = start_date
        self.maxweek = maxweek
        self.course_list = []

    def add_course(self, course: Course):
        course.id = len(self.course_list) + 1
        self.course_list.append(course)

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
                "nodes": 13,
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
            for activity in course.all_activities():
                activities_info.append(activity)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(useless_information)
            f.write(json.dumps(course_table_info) + '\n')
            f.write(json.dumps(courses_info) + '\n')
            f.write(json.dumps(activities_info) + '\n')

