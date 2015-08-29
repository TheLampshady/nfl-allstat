from lxml import html
import urllib2
import logging

from utils import best_match
from apps.crime.configs.crime_catagories import crime_category_list


class HunterAbstract(object):
    """
    Parser for multiple source. Content for each source is differnet
    """
    site = ''
    content = ''

    def __init__(self):
        raise NotImplementedError("Constructor Not Implemented")

    def get_content(self):
        raise NotImplementedError("Get Not Implemented")

    def request_content(self):
        response = urllib2.urlopen(self.site)
        if response.code != 200:
            raise ValueError('Request Error: Status Code: %s' % response.code)

        return response.read()

    def parse_content(self):
        raise NotImplementedError("Parser Not Implemented")


class CrimeHunterUSA(HunterAbstract):

    def __init__(self):
        self.site = 'http://www.usatoday.com/sports/nfl/arrests/'
        self.search_table = '//tbody/tr'
        self.category_choices = crime_category_list

        self.td_classes = dict(
            date='td[1]',
            team='td[2]',
            name='td[3]',
            pos='td[4]',
            case='td[5]',
            category='td[6]',
            description='td[7]',
            outcome='td[8]',
        )

    def get_content(self):
        self.content = self.request_content()
        return self.parse_content()

    def parse_content(self):
        record_list = list()

        page = html.fromstring(self.content)
        table_rows = page.xpath(self.search_table)

        for row in table_rows:
            record = dict()
            for key, value in self.td_classes.items():
                try:
                    content = row.xpath(value)[0].text_content()
                    if key == 'category':
                        content = [best_match(x.strip().lower(), self.category_choices)
                                   for x in content.split(',')]
                    record[key] = content
                except:
                    logging.warning("Missing Element: %s" % row.text_content())
            record_list.append(record)

        return record_list

