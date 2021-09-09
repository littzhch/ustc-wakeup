import re


activity_match_regex = \
    r"[\s\S]*?<activities>"\
    r"[\s\S]*?<coursename>(?P<name>[\s\S]*?)</coursename>"\
    r"[\s\S]*?<weeksstr>(?P<startweek>[0-9]*)(?P<weekfollow>\S*?)(?:(?P<weekendsign>(,))|(?:</weeksstr>))"\
    r"[\s\S]*?(?:(?:<room>(?P<room>[\s\S]*?)</room>)|(?:<room />))"\
    r"[\s\S]*?<weekday>(?P<day>[1-9])</weekday>"\
    r"[\s\S]*?<startunit>(?P<startperiod>[0-9]*)</startunit>"\
    r"[\s\S]*?<endunit>(?P<endperiod>[0-9]*)</endunit>"\
    r"[\s\S]*?(?:(?:<lessonremark>(?P<note>[\s\S]*?)</lessonremark>)|(?:<lessonremark />))"\
    r"[\s\S]*?<teachers>\s*<teachers>(?P<teacher>[\s\S]*?)</teachers>"\
    r"[\s\S]*?<credits>(?P<credit>[\s\S]*?)</credits>"\
    r"[\s\S]*?(?:(?:<customplace>(?P<customplace>[\s\S]*?)</customplace>)|(?:<customplace />))"\
    r"[\s\S]*?</activities>"
rawstring = ""


def _read_single_activity():
    global rawstring
    result = {}
    match_obj = re.match(activity_match_regex, rawstring)
    if not match_obj:
        return None

    result["course_name"] = match_obj["name"]
    result["location"] = \
        match_obj["customplace"] if match_obj["customplace"] \
        else (match_obj["room"] if match_obj["room"] else "")
    result["day"] = int(match_obj["day"])
    result["start_period"] = int(match_obj["startperiod"])
    result["length"] = int(match_obj["endperiod"]) - result["start_period"] + 1
    result["teacher"] = match_obj["teacher"]
    result["credit"] = float(match_obj["credit"])
    result["note"] = match_obj["note"] if match_obj["note"] else ""

    result["start_week"] = int(match_obj["startweek"])
    if match_obj["weekfollow"]:
        if match_obj["weekfollow"][-1] == '双':
            result["week_type"] = 2
            result["end_week"] = int(match_obj["weekfollow"][1:-1])
        elif match_obj["weekfollow"][-1] == '单':
            result["week_type"] = 1
            result["end_week"] = int(match_obj["weekfollow"][1:-1])
        else:
            result["week_type"] = 0
            result["end_week"] = int(match_obj["weekfollow"][1:])
    else:
        result["week_type"] = 0
        result["end_week"] = result["start_week"]

    if match_obj["weekendsign"]:
        rawstring = re.sub(r"<weeksstr>[\S]*?,", "<weeksstr>", rawstring, count=1)
    else:
        rawstring = rawstring[match_obj.span()[1]:]

    return result


def read_activities(rawstr: str):
    global rawstring
    rawstring = rawstr
    result = []
    while True:
        info_dict = _read_single_activity()
        if not info_dict:
            break
        result.append(info_dict)
    return result
