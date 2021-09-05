from XmlReader import *
from WakeupWriter import *


filename = input("文件名：")
with open(filename, encoding='utf-8') as f:
    string = f.read()
semester_name = get_semester_name(string)
semester_start_date = get_semester_start_date(string)


activity_list = read_activities(string)
table = CourseTable(name=semester_name, start_date=get_semester_start_date(string))
for activity_dict in activity_list:
    activity = Activity(day=activity_dict["day"],
                        start_period=activity_dict["start_period"],
                        length=activity_dict["length"],
                        start_week=activity_dict["start_week"],
                        end_week=activity_dict["end_week"],
                        location=activity_dict["location"],
                        teacher=activity_dict["teacher"],
                        week_type=activity_dict["week_type"])
    course = table.get_course(activity_dict["course_name"])
    if course:
        course.add_activity(activity)
    else:
        course = Course(activity_dict["course_name"], activity_dict["credit"])
        course.add_activity(activity)
        table.add_course(course)

table.write_file(semester_name + ".wakeup_schedule")






