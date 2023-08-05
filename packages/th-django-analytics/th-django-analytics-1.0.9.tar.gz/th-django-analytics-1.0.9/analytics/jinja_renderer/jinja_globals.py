from datetime import datetime, timedelta


def today():
    return datetime.now().strftime("%Y-%m-%d")


def tomorrow():
    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")


def next_days(n: int, x=None, fmt="br"):
    fmt_dict = {"br": "%d/%m/%Y", "us": "%Y-%m-%d"}
    options = list()
    now = datetime.now()
    inc = 1
    while len(options) < n:
        option = now + timedelta(days=inc)
        if option.weekday() not in [5, 6]:  # not saturday nor sunday
            options.append((inc, option.strftime(fmt_dict[fmt])))
        inc += 1
    if x is not None:
        for inc, option in options:
            if x == inc:
                return option
    return options
