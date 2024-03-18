from icalendar import Calendar, Event, vRecur
from datetime import date, datetime, timedelta, timezone
from . import CourseTableHandler, CourseTableOutput, register_handler
from ..course_table import *

timetable_info = {
    1: ((7, 50), (8, 35)),
    2: ((8, 40), (9, 25)),
    3: ((9, 45), (10, 30)),
    4: ((10, 35), (11, 20)),
    5: ((11, 25), (12, 10)),
    6: ((14, 0), (14, 45)),
    7: ((14, 50), (15, 35)),
    8: ((15, 55), (16, 40)),
    9: ((16, 45), (17, 30)),
    10: ((17, 35), (18, 20)),
    11: ((19, 30), (20, 15)),
    12: ((20, 20), (21, 5)),
    13: ((21, 10), (21, 55)),
}

def get_datetime_by_period(start_period: int, end_period: int, week: int, weekday: int, start_date: date) -> tuple[datetime, datetime]:
    start_time = timetable_info[start_period][0]
    end_time = timetable_info[end_period][1]
    event_date = start_date + timedelta(days=weekday + (week - 1) * 7)
    start_datetime = datetime(event_date.year, event_date.month, event_date.day, start_time[0], start_time[1], tzinfo=timezone.utc) - timedelta(hours=8)
    end_datetime = datetime(event_date.year, event_date.month, event_date.day, end_time[0], end_time[1], tzinfo=timezone.utc) - timedelta(hours=8)
    return start_datetime, end_datetime


class Icalendar(CourseTableHandler, CourseTableOutput):
    def __init__(self, semester_name: str):
        self.semester_name = semester_name
        self.ical = Calendar()
        self.ical.add('prodid', 'ustcwakeup')
        self.ical.add('version', 2.0)
        
    def set_semester_start_date(self, start_date: date):
        self.start_date = start_date
        
    def set_semester_weeks(self, amount: int):
        self.weeks = amount
        
    def add_course(self, course: Course):
        for activity in course.activities:
            start_dt, end_dt = get_datetime_by_period(activity.time_period.start, 
                                                      activity.time_period.end, 
                                                      activity.week_range.weeks[0], 
                                                      activity.time_period.weekday,
                                                      self.start_date)
            event = Event()
            for teacher in activity.teachers:
                event.add('attendee', parameters={'cn': teacher.name_zh}, value=f'mailto:{teacher.email}')
            event.add('summary', course.name_zh)
            event.add('description', f"{course.course_id}.{course.class_id}")
            event.add('location', activity.location)
            event.add('dtstart', start_dt)
            event.add('dtend', end_dt)
            rrule = vRecur()
            rrule['freq'] = 'WEEKLY'
            rrule['interval'] = 1 if activity.week_range.week_type == 0 else 2
            rrule['byday'] = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'][activity.time_period.weekday]
            rrule['count'] = len(activity.week_range.weeks)
            rrule['wkst'] = 'SU'
            event.add('rrule', rrule)
            self.ical.add_component(event)
    
    def finish(self) -> CourseTableOutput:
        return self
    
    def suggest_file_name(self) -> str:
        return self.semester_name + "课程表"
    
    def get_file_extension(self) -> str:
        return "ics"
    
    def get_content(self) -> bytes:
        return self.ical.to_ical()
    
register_handler(Icalendar, "ical")
        
        
        