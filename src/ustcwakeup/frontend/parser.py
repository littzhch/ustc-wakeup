from datetime import datetime
import re
import json
import difflib
from ..course_table import *
from ..backend import *


__all__ = ["parse_and_feed_data"]


def parse_week(text: str):
    if "~" in text:
        text = text.split("~")
        if "(" in text[1]:
            text += text.pop(1).split("(")
            return int(text[0]), int(text[1]), 1 if "单" in text[2] else 2
        else:
            return int(text[0]), int(text[1]), 0
    else:
        return int(text), int(text), 0


def parse_time(text: str):
    text = text.replace("(", "[").replace(")", "]")
    tup = json.loads(text[1:])
    day = int(text[0]) % 7
    return day, tup[0], tup[-1]


def get_line_activities(text: str, teachers: list[Teacher]) -> list[Activity]:
    result = []
    re_str = r"周 ([\s\S]*?) :([\S\s]*?) ([\S\s]*)"
    location, tm, teacher_name = re.search(re_str, text).groups()
    
    possible_names = [teacher.name_zh for teacher in teachers] + [teacher.name_en for teacher in teachers]
    teacher_name = difflib.get_close_matches(teacher_name, possible_names, n=1, cutoff=0.0)
    for teacher in teachers:
        if teacher_name == teacher.name_zh or teacher_name == teacher.name_en:
            break
        
    day, start_period, end_period = parse_time(tm)
    text = text.split("周 ")[0].split(",")
    for t in text:
        start_week, end_week, week_type = parse_week(t)
        week_selection = WeekSelection(
            first_week=start_week,
            last_week=end_week,
            week_type=week_type,
        )
        time_period = TimePeriod(
            weekday=day,
            start=start_period,
            end=end_period,
        )
        result.append(Activity(
            week_range=week_selection,
            time_period=time_period,
            location=location,
            teachers=[teacher],
        ))
    return result
            

def parse_and_feed_data(data: str, handler: CourseTableHandler):
    re_exp = r"(\d+)~(\d+)(?:\(([单|双])\))?周 ([\s\S]*) :(\d)\((\d+)[\s\S]*?(\d+)\)"
    re_exp = re.compile(re_exp)
    
    start_date = data["oddWeekIndex2dayOfWeek2Date"]["1"]["7"]
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    handler.set_semester_start_date(start_date)
    week_amount = len(data["weekIndices"])
    handler.set_semester_weeks(week_amount)
    
    for course_data in data["lessons"]:
        course = Course()
        course.name_zh = course_data["course"]["nameZh"]
        course.name_en = course_data["course"]["nameEn"]
        course.credits = course_data["course"]["credits"]
        course.course_id = course_data["course"]["code"]
        course.class_id = course_data["code"].split(".")[-1]
        
        for teacher_data in course_data["teacherAssignmentList"]:
            teacher = Teacher()
            teacher.name_zh = teacher_data["person"]["nameZh"]
            teacher.name_en = teacher_data["person"]["nameEn"]
            teacher.age = teacher_data["age"]
            teacher.email = teacher_data["email"]
            if teacher_data["teacher"]["title"]:
                teacher.title = teacher_data["teacher"]["title"]["nameZh"]
            else:
                teacher.title = ""
            teacher.gender = teacher_data["teacher"]["person"]["gender"]["id"] % 2
            course.teachers.append(teacher)
        
        activity_text = course_data["scheduleText"]["dateTimePlacePersonText"]["textZh"]
        if activity_text:
            for single_line in activity_text.split("\n"):
                activities = get_line_activities(single_line, course.teachers)
                for activity in activities:
                    course.add_activity(activity)
                
        handler.add_course(course)