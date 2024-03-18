import aiohttp
import asyncio
import re
import socket
import json
from datetime import date, datetime
from .ustc_cas import cas_login
from ..backend import CourseTableHandler, CourseTableOutput
from ..course_table import *


login_url = "https://jw.ustc.edu.cn/ucas-sso/login"
semester_info_url = "https://jw.ustc.edu.cn/for-std/course-table/"
data_url = "https://jw.ustc.edu.cn/for-std/course-table/get-data"
teacher_info_url = "https://jw.ustc.edu.cn/ws/for-std/course-select/teacher-info-by-lesson"
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50"
}

def parse_semester_list(html: str):
    re_str_list = r"<option[\S\s]*?value=\"([0-9]+?)\">([\S\s]+?季学期)</option>"
    semesters = dict(re.findall(re_str_list, html))
    return {value: key for key, value in semesters.items()}

async def get_web_data(username: str, password: str, semester_name: str, force_ipv6: bool = False, force_ipv4: bool = False) -> dict:
    # 设置 session
    assert not (force_ipv4 and force_ipv6)
    if force_ipv4:
        connector=aiohttp.TCPConnector(family=socket.AF_INET)
    elif force_ipv6:
        connector=aiohttp.TCPConnector(family=socket.AF_INET6)
    else:
        connector=aiohttp.TCPConnector()
    async with aiohttp.ClientSession(connector=connector, headers=header) as session:
        result = await cas_login(username, password, session, service=login_url, autojump=False)
        if result is None:
            raise ValueError("统一身份认证登录失败，请检查学号和密码")
        print("统一身份认证登录成功")
        await session.get(login_url, params={"ticket": result[1]})
        data_id = (await session.get(semester_info_url, allow_redirects=False)).headers["location"][-6:]
        semester_info_html = await (await session.get(semester_info_url)).text()
        semester_dict = parse_semester_list(semester_info_html)
        student_id_re = r"[\s\S]*?var studentId = (\d+);"
        student_id = re.match(student_id_re, semester_info_html).group(1)
        if semester_name not in semester_dict:
            raise RuntimeError("未找到该学期课表")
        params = {
            "bizTypeId": "2",
            "semesterId": semester_dict[semester_name],
            "dataId": data_id,
        }
        semester_data = json.loads(await (await session.get(data_url, params=params)).text())
        
        # 填充教师邮箱
        tasks = []
        async def fill_teacher_email(teacher_data: dict, params: dict, session):
            teacher_data["email"] = json.loads(await (await session.get(teacher_info_url, params=params)).text())["teachers"][0]["email"]
        for lesson_data in semester_data["lessons"]:
            lesson_id = lesson_data["id"]
            for teacher_data in lesson_data["teacherAssignmentList"]:
                person_id = teacher_data["person"]["id"]
                params={
                    "lessonId": lesson_id,
                    "personId": person_id,
                    "studentId": student_id,
                }
                tasks.append(asyncio.create_task(fill_teacher_email(teacher_data, params, session)))
        for task in tasks:
            await task
    return semester_data

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
            

def parse_data(data: str, handler: CourseTableHandler):
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
            print(teacher_data["person"]["nameZh"], teacher_data["person"]["nameEn"])
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


def get_course_table(
    username: str,
    password: str, 
    semester_name: str, 
    Handler: type[CourseTableHandler], 
    force_ipv6: bool = False, 
    force_ipv4: bool = False,
) -> CourseTableOutput:
    data = asyncio.run(get_web_data(username, password, semester_name, force_ipv6, force_ipv4))
    handler = Handler(semester_name)
    parse_data(data, handler)
    return handler.finish()

__all__ = ["get_course_table"]

    