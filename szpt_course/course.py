import html
import re

import requests

from . import common
from .model import CourseModel


class Course:
    def __init__(self, host):
        self._url = 'http://%s/kb/WebKb/Kbcx.aspx' % host

        self._data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': 'FC27A109',
            '__VIEWSTATEENCRYPTED': '',
            '__EVENTVALIDATION': '',
            'txtStudntID': '',
            'btnStuNo': '按学号查询',
        }

    def refresh_state(self):
        resp = requests.get(self._url)
        form_1 = common.generate_data(common.extract_forms(resp.text)[0]['inputs'])
        self._data['__VIEWSTATE'] = form_1['__VIEWSTATE']
        self._data['__EVENTVALIDATION'] = form_1['__EVENTVALIDATION']

    def query(self, student_id, count=0):
        data = self._data.copy()
        data['txtStudntID'] = student_id
        resp = requests.post(self._url, data)
        courses_data = self._parse(self._match(resp.text))
        if courses_data is not None:
            courses = []
            for course in courses_data:
                course = CourseModel(**course)
                courses.append(course)
            return courses
        elif count < 3:
            count += 1
            self.refresh_state()
            return self.query(student_id, count)

    @staticmethod
    def _match(courses_str):
        def match(content):
            courses = []
            prev_course = {}
            for line in content.splitlines():
                course = re.match(
                    '''<td align="center" valign="middle"><font color="#330099" size="2">(?P<type>.*?)</font></td><td><font color="#330099" size="2"><a target="_blank">(?P<class_>.*?)</a></font></td><td align="center" valign="middle"><font color="#330099" size="2">(?P<szpt_course>.*?)</font></td><td align="center" valign="middle"><font color="#330099" size="2">(?P<teacher>.*?)</font></td><td align="center" valign="middle"><font color="#330099" size="2">(?P<teacher_spare>.*?)</font></td><td align="center" valign="middle"><font color="#330099" size="2">(?P<week>.*?)</font></td><td align="center" valign=".*?"><font color="#330099" size="2">(?P<place>.*?)</font></td><td align="center" valign="middle"><font color="#330099" size="2">(?P<day>.*?)</font></td><td align="center" valign="middle"><font color="#330099" size="2">(?P<range>.*?)</font></td><td align="center" valign="middle"><font color="#330099" size="2">(?P<remark>.*?)</font></td>''',
                    line.strip())
                if course is not None:
                    course = course.groupdict()
                    if course['class_'] == '' and course['szpt_course'] == '':
                        course.update(prev_course)
                    if course['teacher'] != '':
                        courses.append(course)
                    if course['type'] == '整周' and course['teacher'] == '':
                        pks = []
                        for k, v in course.items():
                            if v == '':
                                pks.append(k)
                        for k in pks:
                            course.pop(k)
                        prev_course = course

            return courses

        if 'gvSchedule' not in courses_str:
            return None

        remove = dict.fromkeys((ord(c) for c in u"\xa0"))
        [main] = re.findall('<table .*?id="gvSchedule".*?>([\s\S]*?)</table>', courses_str)
        main = html.unescape(main).translate(remove)
        [week] = re.findall('<table .*?id="gvScheduleAllWeek".*?>([\s\S]*?)</table>', courses_str)
        week = html.unescape(week).translate(remove)

        all = match(main) + match(week)
        return all

    @staticmethod
    def _parse(courses):
        if courses is None:
            return None

        days = {
            '星期日': 0,
            '星期天': 0,
            '星期一': 1,
            '星期二': 2,
            '星期三': 3,
            '星期四': 4,
            '星期五': 5,
            '星期六': 6,
        }
        courses_1 = []
        courses_2 = []

        for course in courses:
            week = course.pop('week').translate(str.maketrans({'第': '', '周': ''}))
            weeks = week.split('，')
            for week in weeks:
                if '-' in week:
                    s, e = week.split('-')
                    for i in range(int(s), int(e) + 1):
                        new_course = course.copy()
                        new_course['week'] = i
                        courses_1.append(new_course)
                elif week.isnumeric():
                    new_course = course.copy()
                    new_course['week'] = int(week)
                    courses_1.append(new_course)
                else:
                    new_course = course.copy()
                    new_course['week'] = -1
                    courses_1.append(new_course)

        for course in courses_1:
            if 'day' in course.keys():
                day = course.pop('day')
                course['day'] = days.get(day)

        for course in courses_1:
            range_ = course.pop('range').translate(str.maketrans({'第': '', '节': ''}))
            nodes = range_.split(',')
            for node in nodes:
                new_course = course.copy()
                if node.isnumeric():
                    new_course['node'] = int(node)
                else:
                    new_course['node'] = -1
                courses_2.append(new_course)

        def sorter(x):
            week, day, node = 0, 0, 0
            if isinstance(x['week'], int):
                week = x['week']
            if isinstance(x['day'], int):
                day = x['day']
            if isinstance(x['node'], int):
                node = x['node']
            return week * 100 + day * 10 + node

        courses_2 = sorted(courses_2, key=sorter)
        return courses_2
