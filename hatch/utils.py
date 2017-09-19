import glob
import os
import platform
import re
import shutil
from base64 import urlsafe_b64encode
from datetime import datetime
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
import click

ON_WINDOWS = False
if os.name == 'nt' or platform.system() == 'Windows':  # no cov
    ON_WINDOWS = True

NEED_SUBPROCESS_SHELL = ON_WINDOWS

VENV_FLAGS = {
    '_HATCHING_',
    'VIRTUAL_ENV',
    'CONDA_PREFIX'
}

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help'],
}

UNKNOWN_OPTIONS = {
    'ignore_unknown_options': True,
    **CONTEXT_SETTINGS
}


def echo_success(text, nl=True):
    click.secho(text, fg='cyan', bold=True, nl=nl)


def echo_failure(text, nl=True):
    click.secho(text, fg='red', bold=True, nl=nl)


def echo_warning(text, nl=True):
    click.secho(text, fg='yellow', bold=True, nl=nl)


def echo_waiting(text, nl=True):
    click.secho(text, fg='magenta', bold=True, nl=nl)


def echo_info(text, nl=True):
    click.secho(text, fg='white', bold=True, nl=nl)


def venv_active():
    return bool(VENV_FLAGS & set(os.environ))


def get_random_venv_name():
    # Will be length 4, so 16777216 possibilities.
    return urlsafe_b64encode(os.urandom(3)).decode()


def get_proper_python():  # no cov
    if not venv_active():
        default_python = os.environ.get('_DEFAULT_PYTHON_', None)
        if default_python:
            return default_python
        elif not ON_WINDOWS:
            return 'python3'
    return 'python'


def get_proper_pip():  # no cov
    if not venv_active():
        default_pip = os.environ.get('_DEFAULT_PIP_', None)
        if default_pip:
            return default_pip
        elif not ON_WINDOWS:
            return 'pip3'
    return 'pip'


def get_admin_command():  # no cov
    if ON_WINDOWS:
        return [
            'runas', r'/user:{}\{}'.format(
                platform.node() or os.environ.get('USERDOMAIN', ''),
                os.environ.get('_DEFAULT_ADMIN_', 'Administrator')
            )
        ]
    # Should we indeed use -H here?
    else:
        admin = os.environ.get('_DEFAULT_ADMIN_', '')
        return ['sudo', '-H'] + (['--user={}'.format(admin)] if admin else [])


def get_requirements_file(d, dev=False):
    d = d or os.getcwd()

    reqs = os.path.join(d, 'requirements.txt')
    if dev or not os.path.exists(reqs):
        paths = set(glob.iglob(os.path.join(d, '*requirements*.txt')))
        paths.discard(reqs)
        if not paths:
            return
        reqs = sorted(paths)[0]

    return reqs


def ensure_dir_exists(d):
    if not os.path.exists(d):
        os.makedirs(d)


def create_file(fname):
    ensure_dir_exists(os.path.dirname(os.path.abspath(fname)))
    with open(fname, 'a'):
        os.utime(fname, times=None)


def copy_path(path, d):
    if os.path.isdir(path):
        shutil.copytree(
            path,
            os.path.join(d, basepath(path)),
            copy_function=shutil.copy
        )
    else:
        shutil.copy(path, d)


def remove_path(path):
    try:
        shutil.rmtree(path)
    except (FileNotFoundError, OSError):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass


def resolve_path(path):
    try:
        path = str(Path(path).resolve())
    # FUTURE: Remove this when we drop 3.5.
    except FileNotFoundError:  # no cov
        return ''
    return path if os.path.exists(path) else ''


def basepath(path):
    return os.path.basename(os.path.normpath(path))


def get_current_year():
    return str(datetime.now().year)


def normalize_package_name(package_name):
    return re.sub(r"[-_.]+", "_", package_name).lower()


@contextmanager
def chdir(d, cwd=None):
    origin = cwd or os.getcwd()
    os.chdir(d)

    try:
        yield
    finally:
        os.chdir(origin)


@contextmanager
def temp_chdir(cwd=None):
    with TemporaryDirectory() as d:
        origin = cwd or os.getcwd()
        os.chdir(d)

        try:
            yield resolve_path(d)
        finally:
            os.chdir(origin)


@contextmanager
def env_vars(evars):
    old_evars = {}

    for ev in evars:
        if ev in os.environ:
            old_evars[ev] = os.environ[ev]
        os.environ[ev] = evars[ev]

    try:
        yield
    finally:
        for ev in evars:
            if ev in old_evars:
                os.environ[ev] = old_evars[ev]
            else:
                os.environ.pop(ev)


@contextmanager
def temp_move_path(path, d):
    if os.path.exists(path):
        dst = shutil.move(path, d)

        try:
            yield dst
        finally:
            try:
                os.replace(dst, path)
            except OSError:  # no cov
                shutil.move(dst, path)
    else:
        try:
            yield
        finally:
            remove_path(path)
