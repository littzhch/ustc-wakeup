from os import system
import getpass
import argparse
import re
import socket
import requests.packages.urllib3.util.connection as urllib3_cn

from .jw import JwConnection


def main():
    args = get_args()
    ask_for_info(args)
    
    if args['6']:
        urllib3_cn.allowed_gai_family = lambda: socket.AF_INET6
    elif args['4']:
        urllib3_cn.allowed_gai_family = lambda: socket.AF_INET
    
    try:
        jc = JwConnection(args["username"], args["password"])
    except ValueError as err:
        print(err)
        exit(1)
    
    id = get_semester_id(args["semester"], jc.semester_list)
    if id is None:
        print(args["semester"] + "目前没有课表")
        exit(2)
    jc.selected_semester_id = id

    data = jc.load_semester_json().get_data()
    table = data.generate_course_table()
    for course in data.generate_courses():
        table.add_course(course)
    table.write_file(args["output"])
    print("文件已保存")


def get_semester_id(semester_name: str, id_table: dict[str, str]) -> str | None:
    ids = [key for key, value in id_table.items() if value == semester_name]
    if len(ids) > 0:
        return ids[0]
    

def get_args():
    parser = argparse.ArgumentParser(description='读取 USTC 教务系统课表数据并导出为 wakeup 课程表备份文件的工具')
    parser.add_argument('--username', '-u', type=str, help='统一身份认证用户名（学号）')
    parser.add_argument('--password', '-p', type=str, help='统一身份认证密码')
    parser.add_argument('--semester', '-s', type=str, help='需要导出的课程表所在学期（例如：\"2020夏\"）')
    parser.add_argument('--output', '-o', type=str, help='输出文件名')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-6', action='store_true', help='强制使用 ipv6')
    group.add_argument('-4', action='store_true', help='强制使用 ipv4')
    return vars(parser.parse_args())


def ask_for_info(args: dict):
    if args["semester"] is None:
        args["semester"] = get_semester_selection()
    else:
        args["semester"] = parse_semester_selection(args["semester"])
    if args["output"] is None:
        args["output"] = args["semester"] + ".wakeup_schedule"
    if args["username"] is None:
        args["username"] = input("统一身份认证用户名（学号）：").strip()
    if args["password"] is None:
        args["password"] = getpass.getpass("统一身份认证密码：")
        
def get_semester_selection() -> str:
    raw = input("请输入学期名（例如：2020夏、2021秋）：").strip()
    return parse_semester_selection(raw)
    
def parse_semester_selection(raw: str) -> str:
    while True:
        pattern = r"(\d{4})[\S\s]*?(春|夏|秋)"
        match = re.search(pattern, raw)
        if match:
            return f"{match.group(1)}年{match.group(2)}季学期"
        print("学期名称格式有误，请重试")
        raw = input("请输入学期名（例如：2020夏、2021秋）：").strip()


if __name__ == "__main__":
    main()







