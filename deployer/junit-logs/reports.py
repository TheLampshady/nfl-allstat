#!/usr/bin/env python

from xml.dom.minidom import parse
import re
import argparse
from os import listdir
from os.path import isdir, isfile
import logging


def junit_rename(filename, suffix, mode):
    f = open(filename, 'r')
    content = f.read()
    content = content.replace('&', '&amp;')

    regex_find = "<testsuite\serrors=.+name=\"(.+)\"\sskipped"

    result = re.search(regex_find, content, re.M)

    if not result:
        return None

    test_name = result.group(1)

    if mode == 's':
        name_new = str(test_name)+suffix
    elif mode == 'p':
        name_new = str(suffix) + test_name
    elif mode == 'r':
        name_new = str(suffix)

    regex_replace = "name=\"%s\"\s" % test_name

    content_new = re.sub(regex_replace, "name=\"%s\" " % name_new, content)


    f.close()
    f = open(filename, 'w')
    f.write(content_new)

    f.close()


class ReportsParser(object):

    def __init__(self, reports_dir='reports', prefix='TESTS'):
        self.reports_dir = reports_dir
        self.prefix = prefix
        self.allowed_browsers = ['firefox', 'chrome', 'phantomjs']
        self.allowed_breakpoints = ['small', 'medium', 'large']

        self.setup_logger()

        self.parse_reports()

    def setup_logger(self):
        logger = logging.getLogger('reports parser')
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)
        self.logger = logger

    def parse_reports(self):
        browsers = listdir(self.reports_dir)
        for browser in browsers:
            browser_dir = '{0}/{1}'.format(self.reports_dir, browser)
            if browser in self.allowed_browsers and isdir(browser_dir):
                self.parse_browser(browser)
            elif isfile(browser_dir):
                self.logger.warn("You've got a loose file in your test reports {0}".format(browser_dir))
            else:
                self.logger.warn("Found this browser - {0} -  which is not permitted".format(browser))

    def parse_browser(self, browser):
        browser_dir = '{0}/{1}'.format(self.reports_dir, browser)
        breakpoints = listdir(browser_dir)
        for breakpoint in breakpoints:
            breakpoint_dir = '{0}/{1}'.format(browser_dir, breakpoint)
            if breakpoint in self.allowed_breakpoints and isdir(browser_dir):
                self.parse_breakpoint(browser, breakpoint)
            elif isfile(breakpoint_dir):
                self.logger.warn("You've got a loose file in your test reports {0}".format(breakpoint_dir))
            else:
                self.logger.warn("You've got a bad breakpoint {0}".format(breakpoint))

    def parse_breakpoint(self, browser, breakpoint):
        breakpoint_dir = '{0}/{1}/{2}'.format(self.reports_dir, browser, breakpoint)
        report_files = listdir(breakpoint_dir)
        for report_file in report_files:
            if report_file.endswith('.xml'):
                report_file_path = '{0}/{1}'.format(breakpoint_dir, report_file)
                suffix = ' - {0} - {1}'.format(browser, breakpoint)
                junit_rename(report_file_path, suffix, 's')


def main():
    parser = argparse.ArgumentParser(prog='bdd reports utility')
    parser.add_argument('--reports_dir', default='reports', help='reports directory')
    parser.add_argument('--prefix', default='TESTS')

    args = parser.parse_args()
    parser = ReportsParser(args.reports_dir, args.prefix)

if __name__ == "__main__":
    main()
