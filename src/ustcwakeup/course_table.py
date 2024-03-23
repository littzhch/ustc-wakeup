class WeekSelection:

    def __init__(self,
                 first_week: int | None = None,
                 last_week: int | None = None,
                 week_type: int | None = None):
        assert first_week is not None and last_week is not None and week_type is not None and week_type >= 0 and week_type <= 2
        self.first_week = first_week
        self.last_week = last_week
        self.week_type = week_type
        if week_type == 0:
            self.weeks = list(range(first_week, last_week + 1))
        elif week_type == 1:
            first_week = first_week if first_week % 2 == 1 else first_week + 1
            self.weeks = list(range(first_week, last_week + 1, 2))
        else:
            first_week = first_week if first_week % 2 == 0 else first_week + 1
            self.weeks = list(range(first_week, last_week + 1, 2))

    def __eq__(self, other: "WeekSelection") -> bool:
        return isinstance(other, WeekSelection) and self.weeks == other.weeks


class TimePeriod:
    """
    表示一周当中的一个时间段。
    `self.week`: 1~6，表示周一到周六，0表示周日
    `self.start`: int，表示开始节次
    `self.end`: int|Time，表示结束节次
    """

    def __init__(self, weekday: int, start: int, end: int):
        assert weekday >= 0 and weekday <= 6
        self.weekday = weekday
        self.start = start
        self.end = end

    def __eq__(self, other: "TimePeriod") -> bool:
        return isinstance(other, TimePeriod) \
            and self.weekday == other.weekday \
            and self.start == other.start \
            and self.end == other.end


class Teacher:
    """
    self.name_zh: str，中文名
    self.name_en: str，英文名
    self.gender: int，0表示女，1表示男
    self.title: str，职称，可能为空字符串
    self.email: str，邮箱地址
    """

    def __init__(self):
        self.name_zh: str = None
        self.name_en: str = None
        self.gender: int = None
        self.age: int = None
        self.title: str = None
        self.email: str = None


class Activity:

    def __init__(self, week_range: WeekSelection, time_period: TimePeriod,
                 location: str, teachers: list[Teacher]):
        self.week_range = week_range
        self.time_period = time_period
        self.location = location
        self.teachers = teachers


class Course:

    def __init__(self):
        self.name_zh: str = None
        self.name_en: str = None
        self.credits: float = None
        self.course_id: str = None
        self.class_id: str = None
        self.teachers: list[Teacher] = []
        self.activities: list[Activity] = []

    def add_activity(self, activity: Activity):
        for exist_activity in self.activities:
            if exist_activity.week_range == activity.week_range \
            and exist_activity.time_period == activity.time_period \
            and exist_activity.location == activity.location:
                exist_activity.teachers.extend(activity.teachers)
                return
        self.activities.append(activity)
