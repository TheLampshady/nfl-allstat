"""An observable process that runs various steps to export content from Goro,
version it in your GAE app's repo, and deploy it to App Engine.

"""
import sys
import logging
import subprocess

from observer import Observable


class GAEDeployer(Observable):
    """
    Uses the GAE SDK command, for example:
    appcfg.py -v --oauth2 --noauth_local_webserver update -A gthink-insights /srv/gthink-insights/
    """
    def __init__(self, build_path, app, app_version, gae_path=None, modules=[],
                 verbose=False, queue=False, make_live=False, index=False, dispatch=False,
                 cron=False):
        """
        Initializes variables for deployment
        :return:
        """
        super(self.__class__, self).__init__()
        self.windows = sys.platform == 'win32'
        self.build_path = build_path

        self.app = app
        self.app_version = app_version
        self.make_live = make_live
        self.modules = modules
        self.queue = queue
        self.index = index
        self.dispatch = dispatch
        self.gae_path = gae_path
        self.cron = cron

        if not gae_path:
            if self.windows:
                self.gae_path = 'C:\\Program Files (x86)\\Google\\google_appengine\\'
            else:
                self.gae_path = '/usr/local/bin/'

        self.line_print = '---------------------------------------------------------------------------'

        logging.basicConfig(level=logging.DEBUG)

        v = ' -v ' if verbose else ' '
        self.app_cfg = '"{0}appcfg.py"{1}--oauth2 --noauth_local_webserver'.format(self.gae_path, v)
        self.override_app = ' -A '+self.app
        self.override_version = ' -V '+self.app_version

    def deploy_to_gae(self):
        """
        Master function for uploading to GAE
        """

        # GAE update command for front end module
        self.upload_module_yaml(self.modules)

        # GAE standard command
        if self.dispatch:
            self.upload_dispatch_yaml()
        if self.queue:
            self.upload_queue_yaml()
        if self.index:
            self.upload_indexes_yaml()
        if self.cron:
            self.upload_cron_yaml()

        logging.info("GAE Deployment Successful: <%s-dot-%s>." % (self.app_version, self.app))

        if self.make_live:
            self.set_default_version_in_gae()
        else:
            logging.info('GAE Version Default: Manual update required for version: {0}'.format(self.app_version))

    def upload_module_yaml(self, modules):
        """
        :param modules: List of YAML files to be uploaded to GAE
        """
        for module in modules:
            command = self.app_cfg + ' update{0}{1} {2}{3}.yaml'.format(
                self.override_app, self.override_version, self.build_path, module)
            self.run_command(command)

    def upload_dispatch_yaml(self):
        command = self.app_cfg + ' update_dispatch{0}{1} {2}'.format(
            self.override_app, self.override_version, self.build_path)
        self.run_command(command)

    def upload_queue_yaml(self):
        command = self.app_cfg + ' update_queues{0}{1} {2}'.format(
            self.override_app, self.override_version, self.build_path)
        self.run_command(command)

    def upload_cron_yaml(self):
        command = self.app_cfg + ' update_cron{0}{1} {2}'.format(
            self.override_app, self.override_version, self.build_path)
        self.run_command(command)

    def upload_indexes_yaml(self):
        command = self.app_cfg + ' update_indexes{0} {1}'.format(self.override_app, self.build_path)
        self.run_command(command)

    def set_default_version_in_gae(self):
        """
        Sets the deployed app as the default version
        """
        logging.info('Setting the default version to: {0} ...'.format(self.app_version))

        # GAE set_default_version command
        for module in self.modules:
            module = 'default' if module.lower() is 'app' else module
            command = self.app_cfg + ' set_default_version -A {0} -V {1} -M {2}'.format(
                self.app, self.app_version, module)

            logging.info('set default command is: ')
            logging.info(command)
            subprocess.check_call(command, shell=True)

        logging.info(self.line_print)
        logging.info('[VERSION][SUCCESS] Enabled default version {0} for app {1}'.format(self.app_version, self.app))
        logging.info(self.line_print)

    def run_command(self, command):
        logging.info('Command Executed: %s' % command)
        logging.info(command)
        if self.windows:
            subprocess.Popen("python "+command, shell=True).communicate()
        else:
            subprocess.check_call(command, shell=True)
