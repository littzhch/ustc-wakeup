import re
import codecs
import time
from wakeup import *
from color import *


def _generate_time_node(info: dict) -> TimeNode:
    start_time = Time(int(info["startTime"][0:2]), int(info["startTime"][3:5]))
    end_time = Time(int(info["endTime"][0:2]), int(info["endTime"][3:5]))
    return TimeNode(start_time, end_time)


def _date_adjust(date: str) -> str:
    struct_time = time.strptime(date, "%Y-%m-%d")
    if struct_time.tm_wday <= 3:
        day = -struct_time.tm_wday
    else:
        day = 7 - struct_time.tm_wday
    return time.strftime("%Y-%m-%d", time.localtime(time.mktime(struct_time) + 86400 * day)) \
        .replace("-0", "-")


def _parse_week(text: str):
    if "~" in text:
        text = text.split("~")
        if "(" in text[1]:
            text += text.pop(1).split("(")
            return int(text[0]), int(text[1]), 1 if "单" in text[2] else 2
        else:
            return int(text[0]), int(text[1]), 0
    else:
        return int(text), int(text), 0


def _parse_time(text: str):
    text = text.replace("(", "[").replace(")", "]")
    tup = json.loads(text[1:])
    return int(text[0]), tup[0], len(tup)


def _get_line_activities(text: str) -> list:
    result = []
    re_str = r"周 ([\s\S]*?) :([\S\s]*?) ([\S\s]*)"
    location, tm, teacher = re.search(re_str, text).groups()
    day, start_period, length = _parse_time(tm)
    text = text.split("周 ")[0].split(",")
    for t in text:
        start_week, end_week, week_type = _parse_week(t)
        result.append(Activity(day=day, start_week=start_week, start_period=start_period,
                               end_week=end_week, length=length, week_type=week_type,
                               location=location, teacher=teacher))
    return result


def _get_activities(text: str):
    activities_list = []
    lines = text.split("\n")
    for line in lines:
        line_activities = _get_line_activities(line)
        for line_activity in line_activities:
            merged = False
            for activity in activities_list:
                if activity.can_merge(line_activity):
                    activity.merge_with(line_activity)
                    merged = True
                    break
            if not merged:
                activities_list.append(line_activity)
    return activities_list


def _get_course(course_data) -> Course:
    course = Course(
        name=course_data["course"]["nameZh"],
        credit=course_data["credits"],
        note=course_data["code"],
        color="#ff" + get_color(course_data["course"]["nameZh"]),
    )
    for activity in _get_activities(course_data["scheduleText"]["dateTimePlacePersonText"]["textZh"]):
        course.add_activity(activity)
    return course


class Data:
    def __init__(self, semester_id, semester_json, timetable_js, coursetable_html):
        self.semester_id = semester_id
        self.semester_name = None
        self.semester_json = json.loads(semester_json)
        self.semester_start_date = None  # 第一周周一
        self.timetable_json = None

        re_str = r"\\\"nameZh\\\":\\\"([\S\s]{0,50}?)\\\"[\S\s]{0,50}?\\\"id\\\":" + \
                 semester_id \
                 + r"[\S\s]{0,100}?\\\"startDate\\\":\\\"([\S\s]*?)\\\""
        raw_name, self.semester_start_date = re.search(re_str, coursetable_html).groups()
        self.semester_name = codecs.getdecoder("unicode_escape")(raw_name)[0]
        self.semester_start_date = _date_adjust(self.semester_start_date)

        re_str = r"timeUnit: ({[\S\s]*?}),[\s]*?schoolName"
        table_str = re.search(re_str, timetable_js) \
            .group(1) \
            .replace("startTime", "\"startTime\"") \
            .replace("endTime", "\"endTime\"") \
            .replace("'", "\"")
        self.timetable_json = json.loads(table_str)
        self.semester_json["lessons"] = [course
                                         for course in self.semester_json["lessons"]
                                         if course["scheduleText"]["dateTimePlacePersonText"]["textZh"] is not None]

    def generate_time_table(self) -> TimeTable:
        time_table = TimeTable(self.semester_name + "时间表")
        for info in self.timetable_json.values():
            time_table.add_time_node(_generate_time_node(info))
        return time_table

    def generate_course_table(self) -> CourseTable:
        maxweek = len(self.semester_json["weekIndices"])
        return CourseTable(self.semester_name, self.semester_start_date, maxweek, self.generate_time_table())

    def generate_courses(self):
        for course_info in self.semester_json["lessons"]:
            yield _get_course(course_info)
