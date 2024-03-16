import getpass
import argparse
import re

from .backend import available_handlers
from .frontend import get_course_table

def cli_main() -> int:
    args = get_args()
    if args["print_formats"]:
        for key in available_handlers.keys():
            print(key)
        return 0
    
    ask_for_info(args)
    
    if args["format"] not in available_handlers.keys():
        print("未知的输出格式：" + args["format"])
        return 1
    try:
        output = get_course_table(
            username=args["username"],
            password=args["password"],
            semester_name=args["semester"],
            Handler=available_handlers[args["format"]],
            force_ipv4=args["4"],
            force_ipv6=args["6"],
        )
    except ValueError as err:
        print(err)
        return 2
    
    if args["output"] is None:
        with open(output.suggest_file_name() + "." + output.get_file_extension(), "wb") as file:
            file.write(output.get_content())
    else:
        with open(args["output"], "wb") as file:
            file.write(output.get_content())
    print("文件已保存")
    return 0


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
    parser.add_argument('--format', '-f', type=str, default="wakeup", help='输出为何种格式的文件，默认为 wakeup 课程表备份文件')
    parser.add_argument('--print-formats', action='store_true', help='打印所有可用的输出格式')
    group =parser.add_mutually_exclusive_group()
    group.add_argument('-6', action='store_true', help='强制使用 ipv6')
    group.add_argument('-4', action='store_true', help='强制使用 ipv4')
    return vars(parser.parse_args())


def ask_for_info(args: dict):
    if args["semester"] is None:
        args["semester"] = get_semester_selection()
    else:
        args["semester"] = parse_semester_selection(args["semester"])
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


__all__ = ["cli_main"]








