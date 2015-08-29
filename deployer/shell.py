#!/usr/bin/env python
"""
For help/usage run: python shell.py -h
"""

import os
import sys
import logging
import argparse
from observer import Observer
from deployer import GAEDeployer

sys.path.append(os.path.join(os.path.dirname(__file__), '../deployer'))

parser = argparse.ArgumentParser(prog='Newsletter Deployment CLI')

parser.add_argument('--build_path', required=True,
                    help='location of current build path, relative to shell script')

parser.add_argument('--gae_path', default=None,
                    help='Path to GAE Python SDK')

parser.add_argument('--app', required=True,
                    help='The GAE App being Deployed (e.g. <app-name>.appspot.com)')

parser.add_argument('--app_version', required=True,
                    help='The GAE app version to use in app.yaml')

parser.add_argument('--modules', nargs='*', default=[],
                    help='the GAE Modules. More than one can be listed (e.g. app.yaml)')

parser.add_argument('-v', '--verbose',
                    dest='verbose', action='store_true',
                    help='Toggling Verbosity.')

parser.add_argument('-q', '--queue',
                    dest='queue', action='store_true',
                    help='Toggling Queue Uploading.')

parser.add_argument('-i', '--index',
                    dest='index', action='store_true',
                    help='Toggling Index Uploading.')

parser.add_argument('-d', '--dispatch',
                    dest='dispatch', action='store_true',
                    help='Toggling Dispatch Uploading.')

parser.add_argument('-c', '--cron',
                    dest='cron', action='store_true',
                    help='Toggling Cron Uploading.'
                    )

parser.add_argument('-m', '--make_live',
                    dest='make_live', action='store_true',
                    help='Makes this GAE version Default.')



args = parser.parse_args()


def main():
    """
    Handles Arguments pass and runs the deployment process for Google App Engine
    :return:
    """

    # Create an Observer that logs progress updates from the deployment process
    class LoggingObserver(Observer):
        def observeEvent(self, event):
            logging.info('Update: %s at: %s %%', event.type, event.percent)

    deployer = GAEDeployer(build_path=args.build_path,
                           app=args.app,
                           app_version=args.app_version,
                           gae_path=args.gae_path,
                           modules=args.modules or [],
                           verbose=args.verbose,
                           queue=args.queue,
                           index=args.index,
                           dispatch=args.dispatch,
                           cron=args.cron,
                           make_live=args.make_live
                           )

    observer = LoggingObserver()
    deployer.subscribe(observer)

    deployer.deploy_to_gae()

    sys.exit(0)


if __name__ == "__main__":
    main()  # Calls main
