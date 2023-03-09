import time
import datetime


def get_current_timeformat(fmt="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间格式
    """
    return time.strftime(fmt)


def get_current_timestamp(by_sc=False, by_ms=False, by_mcs=False):
    """
    @params by_sc 秒级
    @params by_ms 毫秒级
    @params by_mcs 微秒级
    """
    if by_sc:
        return int(time.time())
    if by_ms:
        return int(time.time() * 1000)
    if by_mcs:
        return int(time.time() * 1000000)
    return int(time.time())


def timestamp_2_format(timestamp, format="%Y-%m-%d %H:%M:%S") -> str:
    """
    时间戳转化为日期字符串
    """
    time_array = time.localtime(timestamp)
    return time.strftime(format, time_array)


def timestamp_2_datetime(timestamp) -> str:
    """时间戳转datetime"""
    return datetime.datetime.fromtimestamp(timestamp)


def formattime_2_timestamp(formattime, format="%Y-%m-%d %H:%M:%S") -> int:
    """
    时间字符串转化为时间戳
    """
    if not formattime:
        return 0
    return int(time.mktime(time.strptime(formattime, format)))


def datetime_operation(date, day: int = None, week: int = None, month: int = None, year: int = None):
    """时间运算
    # TODO: 事件运算月年不准确,后续进行调整
    date: datetime.now() 类型
    op: str add, sub
    """

    def add_op(d, timedelta):
        return d + timedelta

    date_r = date

    if day:
        timedelta = datetime.timedelta(days=day)
        date_r = add_op(date_r, timedelta)

    if week:
        timedelta = datetime.timedelta(days=week*7)
        date_r = add_op(date_r, timedelta)

    if month:
        timedelta = datetime.timedelta(days=month*30)
        date_r = add_op(date_r, timedelta)

    if year:
        timedelta = datetime.timedelta(days=year*365)
        date_r = add_op(date_r, timedelta)

    return date_r


def timestamp_merge(interval1: list, interval2: list):
    """时间段求交集"""
    interval_sorted = sorted([interval1, interval2], key=lambda interval: interval[0])
    start = interval_sorted[1][0]
    end = min(interval_sorted[0][1], interval_sorted[1][1])

    # 不存在交集
    if start > end:
        start = None
        end = None

    return start, end
