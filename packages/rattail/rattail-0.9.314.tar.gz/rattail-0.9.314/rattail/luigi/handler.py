# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Luigi utilities
"""

from __future__ import unicode_literals, absolute_import

import os
import logging
import shlex
import subprocess
import sys

import sqlalchemy as sa
import six
from six.moves.xmlrpc_client import ProtocolError

from rattail.app import GenericHandler


log = logging.getLogger(__name__)


class LuigiHandler(GenericHandler):
    """
    Base class and default implementation for Luigi handler.
    """

    def get_supervisor_process_name(self, require=False, **kwargs):
        getter = self.config.require if require else self.config.get
        return getter('luigi', 'scheduler.supervisor_process_name')

    def restart_supervisor_process(self, name=None, **kwargs):
        if not name:
            name = self.get_supervisor_process_name()

        try:
            proxy = self.app.make_supervisorctl_proxy()
        except:
            log.warning("failed to make supervisorctl proxy", exc_info=True)

        else:
            # we have our proxy, so use that, then return
            try:
                info = proxy.supervisor.getProcessInfo(name)
                if info['state'] != 0:
                    proxy.supervisor.stopProcess(name)
                proxy.supervisor.startProcess(name)
            except ProtocolError as error:
                raise self.app.safe_supervisor_protocol_error(error)
            return

        # no proxy, but we can still try command line
        # TODO: should rename this setting at some point?
        cmd = self.config.get('luigi', 'scheduler.restart_command')
        if cmd:
            cmd = self.config.parse_list(cmd)
        elif name:
            cmd = ['supervisorctl', 'restart', name]

        log.debug("attempting luigi scheduler restart with command: %s", cmd)

        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            log.warning("failed to restart luigi scheduler; output was:")
            log.warning(error.output)
            raise

    def get_all_overnight_tasks(self, **kwargs):
        tasks = []
        keys = self.config.getlist('rattail.luigi', 'overnight_tasks',
                                   default=[])
        for key in keys:
            lastrun = self.config.get(
                'rattail.luigi', 'overnight.{}.lastrun'.format(key))
            lastrun = self.app.parse_utctime(lastrun, local=True)
            tasks.append({
                'key': key,
                'description': self.config.get(
                    'rattail.luigi', 'overnight.{}.description'.format(key)),
                'script': self.config.get(
                    'rattail.luigi', 'overnight.{}.script'.format(key)),
                'notes': self.config.get(
                    'rattail.luigi', 'overnight.{}.notes'.format(key)),
                'lastrun': lastrun,
                'last_date': self.config.getdate(
                    'rattail.luigi', 'overnight.{}.last_date'.format(key)),
            })
        tasks.sort(key=lambda t: t['description'])
        return tasks

    def get_overnight_task(self, key, **kwargs):
        for task in self.get_all_overnight_tasks():
            if task['key'] == key:
                return task

    def launch_overnight_task(self, task, date, **kwargs):
        appdir = self.config.appdir()

        env = {
            'RATTAIL_CONFIG_FILES': os.path.join(appdir, 'silent.conf'),
        }

        cmd = '{} {}'.format(task['script'], date)

        cmd = [os.path.join(sys.prefix, 'bin', 'rattail'),
               '--config', os.path.join(appdir, 'silent.conf'),
               '--no-versioning',
               'run-n-mail',
               '-S', "Overnight for {}: {}".format(date, task['description']),
               cmd]

        cmd = ['echo', shlex.join(cmd)]
        cmd = shlex.join(cmd)

        cmd = "{} | at 'now + 1 minute'".format(cmd)

        # run command in subprocess
        log.debug("launching command in subprocess: %s", cmd)
        try:
            subprocess.check_output(cmd, shell=True, env=env,
                                    stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as error:
            log.warning("command failed with exit code %s!  output was:",
                        error.returncode)
            log.warning(error.stderr.decode('utf_8'))
            raise

    def record_overnight_last_date(self, task, date, session=None, **kwargs):
        name = 'rattail.luigi.overnight.{}.last_date'.format(task['key'])
        with self.app.short_session(session=session, commit=True) as s:
            self.app.save_setting(s, name, six.text_type(date))

    def get_all_backfill_tasks(self, **kwargs):
        tasks = []
        keys = self.config.getlist('rattail.luigi', 'backfill_tasks',
                                   default=[])
        for key in keys:
            lastrun = self.config.get(
                'rattail.luigi', 'backfill.{}.lastrun'.format(key))
            lastrun = self.app.parse_utctime(lastrun, local=True)
            tasks.append({
                'key': key,
                'description': self.config.get(
                    'rattail.luigi', 'backfill.{}.description'.format(key)),
                'script': self.config.get(
                    'rattail.luigi', 'backfill.{}.script'.format(key)),
                'forward': self.config.getbool(
                    'rattail.luigi', 'backfill.{}.forward'.format(key),
                    default=False),
                'notes': self.config.get(
                    'rattail.luigi', 'backfill.{}.notes'.format(key)),
                'lastrun': lastrun,
                'last_date': self.config.getdate(
                    'rattail.luigi', 'backfill.{}.last_date'.format(key)),
                'target_date': self.config.getdate(
                    'rattail.luigi', 'backfill.{}.target_date'.format(key)),
            })
        tasks.sort(key=lambda t: t['description'])
        return tasks

    def get_backfill_task(self, key, **kwargs):
        for task in self.get_all_backfill_tasks():
            if task['key'] == key:
                return task

    def launch_backfill_task(self, task, start_date, end_date, **kwargs):
        if not start_date or not end_date:
            raise ValueError("must specify both start_date and end_date")

        appdir = self.config.appdir()
        luigi = os.path.join(sys.prefix, 'bin', 'luigi')
        logging_conf = os.path.join(appdir, 'luigi', 'logging.conf')
        cmd = [luigi, '--logging-conf-file', logging_conf,
               '--module', 'rattail.luigi.backfill_runner']

        if task['forward']:
            cmd.append('ForwardBackfillRange')
        else:
            cmd.append('BackwardBackfillRange')

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        cmd.extend([
            '--key', task['key'],
            '--start-date={}'.format(start_date),
            '--end-date={}'.format(end_date),
        ])

        env = {
            'RATTAIL_CONFIG_FILES': os.path.join(appdir, 'silent.conf'),
        }

        last_date = end_date if task['forward'] else start_date
        cmd = [os.path.join(sys.prefix, 'bin', 'rattail'),
               '--config', os.path.join(appdir, 'silent.conf'),
               '--no-versioning',
               'run-n-mail',
               '-S', 'Backfill thru {}: {}'.format(last_date, task['description']),
               shlex.join(cmd)]

        cmd = ['echo', shlex.join(cmd)]
        cmd = shlex.join(cmd)

        cmd = "{} | at 'now + 1 minute'".format(cmd)

        # run command in subprocess
        log.debug("launching command in subprocess: %s", cmd)
        try:
            subprocess.check_output(cmd, shell=True, env=env,
                                    stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as error:
            log.warning("command failed with exit code %s!  output was:",
                        error.returncode)
            log.warning(error.stderr.decode('utf_8'))
            raise

    def record_backfill_last_date(self, task, date, session=None, **kwargs):
        name = 'rattail.luigi.backfill.{}.last_date'.format(task['key'])
        with self.app.short_session(session=session, commit=True) as s:
            self.app.save_setting(s, name, six.text_type(date))
