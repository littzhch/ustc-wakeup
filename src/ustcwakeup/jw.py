import requests as rq
import re
from .ustc_cas import *
from .data_parse import Data

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50"
}
login_url = "https://jw.ustc.edu.cn/ucas-sso/login"
table_url = "https://jw.ustc.edu.cn/for-std/course-table/"
data_url = "https://jw.ustc.edu.cn/for-std/course-table/get-data"
timetable_url = "https://jw.ustc.edu.cn/static/coursetableprint/js/course-table-print-config.js"


def _get_semester_list(html: str):
    re_str_list = r"<option[\S\s]*?value=\"([0-9]+?)\">([\S\s]+?季学期)</option>"
    re_str_default = r"<option selected[\S\s]*?value=\"([0-9]+?)\">[\S\s]+?季学期</option>"
    return dict(re.findall(re_str_list, html)), re.search(re_str_default, html).group(1)


class JwConnection:
    def __init__(self, student_id, password):
        self.cookie_jar = None
        self.data_id = None
        self.semester_list = None
        self.selected_semester_id = None
        self.coursetable_html = None
        self.semester_json = None
        self.timetable_js = None

        rsps = rq.get(login_url, headers=header, allow_redirects=False)
        self.cookie_jar = rsps.cookies
        result = cas_login(student_id, password, login_url)
        if result is None:
            raise ValueError("统一身份认证登录失败，请检查学号和密码")
        rq.get(login_url, params={"ticket": result[1]}, headers=header, cookies=self.cookie_jar)
        self.data_id = rq.get(table_url, headers=header, cookies=self.cookie_jar,
                              allow_redirects=False).headers["location"][-6:]

        self.coursetable_html = rq.get(table_url, headers=header, cookies=self.cookie_jar).text
        self.timetable_js = rq.get(timetable_url, headers=header).text
        self.semester_list, self.selected_semester_id = _get_semester_list(self.coursetable_html)

    def load_semester_json(self):
        params = {
            "bizTypeId": "2",
            "semesterId": self.selected_semester_id,
            "dataId": self.data_id
        }
        self.semester_json = rq.get(data_url, params=params, headers=header, cookies=self.cookie_jar).text
        return self

    def get_data(self) -> Data:
        return Data(semester_id=self.selected_semester_id,
                    semester_json=self.semester_json,
                    timetable_js=self.timetable_js,
                    coursetable_html=self.coursetable_html)


