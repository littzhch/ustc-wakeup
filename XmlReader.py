import re


activity_match_regex = \
    r"[\s\S]*?<activities>[\s\S]*?"\
    r"<coursename>([\s\S]*?)</coursename>[\s\S]*?"\
    r"<weeksstr>([0-9]*)(\S*?)(?:(,)|(?:</weeksstr>))"\
    r"[\s\S]*?(?:(?:<room>([\s\S]*?)</room>)|(?:<room />))[\s\S]*?"\
    r"<weekday>([1-9])</weekday>[\s\S]*?"\
    r"<startunit>([0-9]*)</startunit>"\
    r"[\s\S]*?<endunit>([0-9]*)</endunit>[\s\S]*?"\
    r"<teachers>[\s]*<teachers>([\s\S]*?)</teachers>"\
    r"[\s\S]*?<credits>([\s\S]*?)</credits>"\
    r"[\s\S]*?(?:(?:<customplace>([\s\S]*?)</customplace>)|(?:<customplace />))"\
    r"[\s\S]*?</activities>"
rawstring = ""


def _read_single_activity():
    global rawstring
    result = {}
    match_obj = re.match(activity_match_regex, rawstring)
    if not match_obj:
        return None

    result["course_name"] = match_obj.group(1)
    result["location"] = \
        match_obj.group(11) if match_obj.group(11) \
        else (match_obj.group(5) if match_obj.group(5) else "")
    result["day"] = int(match_obj.group(6))
    result["start_period"] = int(match_obj.group(7))
    result["length"] = int(match_obj.group(8)) - result["start_period"] + 1
    result["teacher"] = match_obj.group(9)
    result["credit"] = float(match_obj.group(10))

    result["start_week"] = int(match_obj.group(2))
    if match_obj.group(3):
        if match_obj.group(3)[-1] == '双':
            result["week_type"] = 2
            result["end_week"] = int(match_obj.group(3)[1:-1])
        elif match_obj.group(3)[-1] == '单':
            result["week_type"] = 1
            result["end_week"] = int(match_obj.group(3)[1:-1])
        else:
            result["week_type"] = 0
            result["end_week"] = int(match_obj.group(3)[1:])
    else:
        result["week_type"] = 0
        result["end_week"] = result["start_week"]

    if match_obj.group(4):
        rawstring = re.sub(r"<weeksstr>[\S]*?,", "<weeksstr>", rawstring, count=1)
    else:
        rawstring = rawstring[match_obj.span()[1]:]

    print(result)
    return result


def read_activities(rawstr: str):
    global rawstring
    rawstring = rawstr
    result = []
    start = re.search(r"</credits>\s*<activities>", rawstr).span()[1]
    rawstring = rawstring[start:]
    while True:
        info_dict = _read_single_activity()
        if not info_dict:
            break
        result.append(info_dict)
    return result



