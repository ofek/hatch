import os
from collections import OrderedDict

import toml
from sortedcontainers import SortedDict

from hatch.utils import find_project_root, is_setup_managed, parse_setup
from hatch.commands.utils import echo_success, echo_failure
from hatch.files.setup import SetupFile
from hatch.files.licenses import LICENSES


class Project(object):
    def __init__(self, filename='pyproject.toml'):
        self.project_root = project_root = find_project_root()
        self.project_file = os.path.join(project_root, filename)
        self.lock_file = os.path.join(project_root, '{}.lock'.format(filename))
        self.setup_file = os.path.join(project_root, 'setup.py')
        self.setup_is_managed = is_setup_managed(self.setup_file)
        self.setup_user_section_error = None
        self.setup_user_section = ''
        if self.setup_is_managed:
            try:
                self.setup_user_section = parse_setup(self.setup_file)
            except Exception as e:
                self.setup_user_section_error = str(e)

        self.raw = OrderedDict()
        try:
            with open(self.project_file) as f:
                self.raw = toml.load(f, OrderedDict)
            self.packages = SortedDict(self.raw.get('packages'))
            self.dev_packages = SortedDict(self.raw.get('dev-packages'))
            self.metadata = self.raw.get('metadata')
            self.commands = self.raw.get('tool', {}).get('hatch', {}).get('commands', OrderedDict())
            self.pyversions = self.raw.get('requires', []).get('python_version', [])
        except (FileNotFoundError, IOError, ValueError):
            self.packages = SortedDict()
            self.dev_packages = SortedDict()
            self.metadata = OrderedDict()
            self.commands = OrderedDict()
            self.pyversions = []

    def structure(self):
        final = self.raw
        final['metadata'] = self.metadata
        final['packages'] = self.packages
        final['dev-packages'] = self.dev_packages
        if final.get('tool') is None:
            final['tool'] = OrderedDict()
        if final['tool'].get('hatch') is None:
            final['tool']['hatch'] = OrderedDict()
        if final['tool']['hatch'].get('commands') is None:
            final['tool']['hatch']['commands'] = OrderedDict()

        final['tool']['hatch']['commands'] = self.commands
        return final

    @property
    def name(self):
        return self.metadata.get('name')

    @property
    def description(self):
        return self.metadata.get('description')

    @property
    def author(self):
        return self.metadata.get('author')

    @property
    def author_email(self):
        return self.metadata.get('author_email')

    @property
    def readme(self):
        return self.metadata.get('readme')

    @property
    def user_defined(self):
        return self.setup_user_section

    @property
    def url(self):
        return self.metadata.get('url')

    @property
    def license(self):
        return self.metadata.get('license')

    @property
    def cli(self):
        return self.metadata.get('cli')

    @property
    def version(self):
        return self.metadata.get('version')

    @version.setter
    def version(self, version):
        self.metadata['version'] = version
        self.write_files()

    def add_package(self, package, version, dev=False):
        packages = self.packages if not dev else self.dev_packages
        packages[package] = version
        self.write_files()

    def write_files(self):
        if not self.write_project_file():
            echo_failure('{} was NOT updated.'.format(self.project_file))
        if not self.write_setup_file():
            echo_failure('{} was NOT updated.'.format(self.setup_file))

    def write_project_file(self):
        with open(self.project_file, 'w') as f:
            toml.dump(self.structure(), f)
            f.write('\n')
        return True

    def write_setup_file(self):
        if not self.setup_is_managed:
            return False
        try:
            licenses = [LICENSES[li](self.author) for li in self.license.split('/')]
            setup = SetupFile(self.author, self.author_email, self.name,
                    self.pyversions, licenses, self.readme, self.url,
                    self.cli, list(self.packages), self.user_defined)
            setup.write(self.project_root)
            return True
        except Exception:
            return False
