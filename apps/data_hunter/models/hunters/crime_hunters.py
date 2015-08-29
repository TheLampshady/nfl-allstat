import urllib2
import logging
from lxml import html

from apps.common.utils import best_match
from apps.data_hunter.configs.crime_catagories import crime_category_list
from apps.data_hunter.models.hunters.base_hunter import HunterAbstract


class CrimeHunterUSA(HunterAbstract):

    def __init__(self):
        self.site = 'http://www.usatoday.com/sports/nfl/arrests/'
        self.search_table = '//tbody/tr'
        self.category_choices = crime_category_list
        self.type = 'crime'

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

    def request_content(self):
        response = urllib2.urlopen(self.site)
        if response.code != 200:
            raise ValueError('Request Error: Status Code: %s' % response.code)

        return response.read()

    def parse_content(self, content):
        record_list = list()

        page = html.fromstring(content)
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