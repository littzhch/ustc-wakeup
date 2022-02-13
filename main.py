from os import system
from jw import JwConnection


def get_cas_info() -> (str, str):
    print("统一身份认证")
    usr = input("用户名（学号）：")
    pwd = input("密码：")
    if system("cls") != 0:
        system("clear")
    return usr, pwd


def get_semester_selection(info: dict):
    for key in reversed(info.keys()):
        print("{:>4s} {}".format(key, info[key]))
    return input("输入编号以选择学期（不输入默认为当前学期）：")


if __name__ == "__main__":
    user, pswd = get_cas_info()
    try:
        jc = JwConnection(user, pswd)
    except ValueError as err:
        print(err)
        input("按回车退出")
        exit(0)
    selection = get_semester_selection(jc.semester_list)
    if selection != "":
        jc.selected_semester_id = selection
    data = jc.load_semester_json().get_data()
    table = data.generate_course_table()
    for course in data.generate_courses():
        table.add_course(course)
    table.write_file(data.semester_name + ".wakeup_schedule")
    input("文件已保存，按回车退出")






