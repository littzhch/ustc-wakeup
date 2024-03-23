import aiohttp
import asyncio
import re
import socket
import json
from .ustc_cas import cas_login

__all__ = ["get_web_data"]

login_url = "https://jw.ustc.edu.cn/ucas-sso/login"
semester_info_url = "https://jw.ustc.edu.cn/for-std/course-table/"
data_url = "https://jw.ustc.edu.cn/for-std/course-table/get-data"
teacher_info_url = "https://jw.ustc.edu.cn/ws/for-std/course-select/teacher-info-by-lesson"
header = {
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50"
}


def parse_semester_list(html: str):
    re_str_list = r"<option[\S\s]*?value=\"([0-9]+?)\">([\S\s]+?季学期)</option>"
    semesters = dict(re.findall(re_str_list, html))
    return {value: key for key, value in semesters.items()}


async def get_web_data_async(username: str,
                             password: str,
                             semester_name: str,
                             force_ipv6: bool = False,
                             force_ipv4: bool = False) -> dict:
    # 设置 session
    assert not (force_ipv4 and force_ipv6)
    if force_ipv4:
        connector = aiohttp.TCPConnector(family=socket.AF_INET)
    elif force_ipv6:
        connector = aiohttp.TCPConnector(family=socket.AF_INET6)
    else:
        connector = aiohttp.TCPConnector()
    async with aiohttp.ClientSession(connector=connector,
                                     headers=header) as session:
        result = await cas_login(username,
                                 password,
                                 session,
                                 service=login_url,
                                 autojump=False)
        if result is None:
            raise ValueError("统一身份认证登录失败，请检查学号和密码")
        print("统一身份认证登录成功")
        await session.get(login_url, params={"ticket": result[1]})

        data_id_task = asyncio.create_task(
            session.get(semester_info_url, allow_redirects=False))
        semester_info_task = asyncio.create_task(
            session.get(semester_info_url))
        semester_info_task = asyncio.create_task((await
                                                  semester_info_task).text())
        data_id = (await data_id_task).headers["location"][-6:]
        semester_info_html = await semester_info_task
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
        semester_data = json.loads(await (await
                                          session.get(data_url,
                                                      params=params)).text())

        # 填充教师邮箱
        tasks = []

        async def fill_teacher_email(teacher_data: dict, params: dict,
                                     session):
            teacher_data["email"] = json.loads(await (await session.get(
                teacher_info_url,
                params=params)).text())["teachers"][0]["email"]

        for lesson_data in semester_data["lessons"]:
            lesson_id = lesson_data["id"]
            for teacher_data in lesson_data["teacherAssignmentList"]:
                person_id = teacher_data["person"]["id"]
                params = {
                    "lessonId": lesson_id,
                    "personId": person_id,
                    "studentId": student_id,
                }
                tasks.append(
                    asyncio.create_task(
                        fill_teacher_email(teacher_data, params, session)))
        for task in tasks:
            await task

    return semester_data


def get_web_data(username: str,
                 password: str,
                 semester_name: str,
                 force_ipv6: bool = False,
                 force_ipv4: bool = False) -> dict:
    return asyncio.run(
        get_web_data_async(username, password, semester_name, force_ipv6,
                           force_ipv4))
