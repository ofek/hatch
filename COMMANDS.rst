Commands
--------

For your convenience, anything after a ``--`` will be treated as arguments.

.. contents:: **Table of Contents**
    :backlinks: none

``config``
^^^^^^^^^^

Locates, updates, or restores the config file.

.. code-block:: bash

    $ hatch config
    Settings location: /home/ofek/.local/share/hatch/settings.json

..

    **Options:**

*-u/--update*
    Updates the config file with any new fields.

*--restore*
    Restores the config file to default settings.

``new``
^^^^^^^

Creates a new Python project.

Values from your config file such as ``name`` and ``pyversions`` will be used
to help populate fields. You can also specify things like the readme format
and which CI service files to create. All options override the config file.

By default a virtual env will be created in the project directory and will
install the project locally so any edits will auto-update the installation.
You can also locally install the created project in other virtual envs using
the --env option.

Here is an example using an unmodified config file:

.. code-block:: bash

    $ hatch new -ne my-app
    Created project `my-app`
    $ tree --dirsfirst my-app
    my-app
    ├── my_app
    │   └── __init__.py
    ├── tests
    │   └── __init__.py
    ├── LICENSE-APACHE
    ├── LICENSE-MIT
    ├── MANIFEST.in
    ├── README.rst
    ├── requirements.txt
    ├── setup.py
    └── tox.ini

    2 directories, 8 files

..

    **Arguments:**

*name*
    The desired name of package.

..

    **Options:**

*-ne/--no-env*
    Disables the creation of a dedicated virtual env.

*-py/--python*
    A named Python path to use when creating a virtual
    env. This overrides --pypath.

*-pp/--pypath*
    An absolute path to a Python executable to use when
    creating a virtual env.

*-g/--global-packages*
    Gives created virtual envs access to the global site-packages.

*-e/--env*
    Forward-slash-separated list of named virtual envs to be
    installed in. Will create any that don't already exist.

*--basic*
    Disables third-party services and readme badges.

*--cli*
    Creates a ``cli.py`` in the package directory and an entry point in
    ``setup.py`` pointing to the properly named function within. Also, a
    ``__main__.py`` is created so it can be invoked via ``python -m pkg_name``.

*-l/--licenses*
    Comma-separated list of licenses to use.

``init``
^^^^^^^^

Same as ``new`` but the project target is the current directory.

``grow``
^^^^^^^^

Increments a project's version number using semantic versioning.
Valid choices for the part are ``major``, ``minor``, ``patch``
(``fix`` alias), ``pre``, and ``build``.

The path to the project is derived in the following order:

1. The optional argument, which should be the name of a package
   that was installed via ``hatch install -l`` or ``pip install -e``.
2. The --local flag.
3. The option --path, which can be a relative or absolute path.
4. The current directory.

If the path is a file, it will be the target. Otherwise, the path, and
every top level directory within, will be checked for a ``__version__.py``,
``__about__.py``, and ``__init__.py``, in that order. The first encounter of
a ``__version__`` variable that also appears to equal a version string will
be updated. Probable package paths will be given precedence.

The default tokens for the prerelease and build parts, *rc* and *build*
respectively, can be altered via the options ``--pre`` and ``--build``, or
the config entry ``semver``.

.. code-block:: bash

    $ git clone -q https://github.com/requests/requests && cd requests
    $ hatch grow build
    Updated /home/ofek/requests/requests/__version__.py
    2.18.4 -> 2.18.4+build.1
    $ hatch grow fix
    Updated /home/ofek/requests/requests/__version__.py
    2.18.4+build.1 -> 2.18.5
    $ hatch grow pre
    Updated /home/ofek/requests/requests/__version__.py
    2.18.5 -> 2.18.5-rc.1
    $ hatch grow minor
    Updated /home/ofek/requests/requests/__version__.py
    2.18.5-rc.1 -> 2.19.0
    $ hatch grow major
    Updated /home/ofek/requests/requests/__version__.py
    2.19.0 -> 3.0.0

..

    **Arguments:**

*part*
    The part of version to bump.

*package*
    The editable package to target (optional).

..

    **Options:**

*-l/--local*
    Shortcut to select the only available local (editable) package. If
    there are multiple, an error will be raised.

*-p/--path*
    A relative or absolute path to a project or file.

*--pre*
    The token to use for ``pre`` part, overriding the config file. Default: *rc*

*--build*
    The token to use for ``build`` part, overriding the config file. Default: *build*

``test``
^^^^^^^^

Runs tests using ``pytest``, optionally checking coverage.

The path is derived in the following order:

1. The optional argument, which should be the name of a package
   that was installed via ``hatch install -l`` or ``pip install -e``.
2. The --local flag.
3. The option --path, which can be a relative or absolute path.
4. The current directory.

If the path points to a package, it should have a ``tests`` directory.

If a project is detected but there is no dedicated virtual env, it
will be created and any dev requirements will be installed in it.

.. code-block:: bash

    $ git clone https://github.com/ofek/privy && cd privy
    $ hatch test -c
    ========================= test session starts ==========================
    platform linux -- Python 3.5.2, pytest-3.2.1, py-1.4.34, pluggy-0.4.0
    rootdir: /home/ofek/privy, inifile:
    plugins: xdist-1.20.0, mock-1.6.2, httpbin-0.0.7, forked-0.2, cov-2.5.1
    collected 10 items

    tests/test_privy.py ..........

    ====================== 10 passed in 4.34 seconds =======================

    Tests completed, checking coverage...

    Name                  Stmts   Miss Branch BrPart  Cover   Missing
    -----------------------------------------------------------------
    privy/__init__.py         1      0      0      0   100%
    privy/core.py            30      0      0      0   100%
    privy/utils.py           13      0      4      0   100%
    tests/__init__.py         0      0      0      0   100%
    tests/test_privy.py      57      0      0      0   100%
    -----------------------------------------------------------------
    TOTAL                   101      0      4      0   100%

..

    **Arguments:**

*package*
    The editable package to target (optional).

..

    **Options:**

*-l/--local*
    Shortcut to select the only available local (editable) package. If
    there are multiple, an error will be raised.

*-p/--path*
    A relative or absolute path to a project or test directory.

*-c/--cov*
    Computes, then outputs coverage after testing.

*-m/--merge*
    If --cov, coverage will run using --parallel-mode and combine the results.

*-ta/--test-args*
    Pass through to ``pytest``, overriding defaults. Example: ``hatch test -ta "-k test_core.py -vv"``

*-ca/--cov-args*
    Pass through to ``coverage run``, overriding defaults. Example: ``hatch test -ca "--timid --pylib"``

*-g/--global*
    Uses the ``pytest`` and ``coverage`` shipped with Hatch instead of environment-aware modules.
    This is useful if you just want to run a quick test without installing these again in a
    virtual env. Keep in mind these will be the Python 3 versions.

*-nd/--no-detect*
    Does not run the tests inside a project's dedicated virtual env.

``pypath``
^^^^^^^^^^

Names an absolute path to a Python executable. You can also modify
these in the config file entry ``pypaths``.

Hatch can then use these paths by name when creating virtual envs, building
packages, etc.

.. code-block:: bash

    $ hatch pypath -l
    There are no saved Python paths. Add one via `hatch pypath NAME PATH`.
    $ hatch pypath py2 /usr/bin/python
    Successfully saved Python `py2` located at `/usr/bin/python`.
    $ hatch pypath py3 /usr/bin/python3
    Successfully saved Python `py3` located at `/usr/bin/python3`.
    $ hatch pypath -l
    py2 -> /usr/bin/python
    py3 -> /usr/bin/python3

..

    **Arguments:**

*name*
    The desired name of the Python path.

*path*
    An absolute path to a Python executable.

..

    **Options:**

*-l/--list*
    Shows available Python paths.

``env``
^^^^^^^

Creates a new virtual env that can later be utilized with the ``shell`` command.

.. code-block:: bash

    $ hatch pypath -l
    py2 -> /usr/bin/python
    py3 -> /usr/bin/python3
    $ hatch env -l
    No virtual environments found in /home/ofek/.virtualenvs. To create one do `hatch env NAME`.
    $ hatch env my-app
    Already using interpreter /usr/bin/python3
    Successfully saved virtual env `my-app` to `/home/ofek/.virtualenvs/my-app`.
    $ hatch env -py py2 old
    Successfully saved virtual env `old` to `/home/ofek/.virtualenvs/old`.
    $ hatch env -pp ~/pypy3/bin/pypy fast
    Successfully saved virtual env `fast` to `/home/ofek/.virtualenvs/fast`.
    $ hatch env -ll
    Virtual environments found in /home/ofek/.virtualenvs:

    fast ->
      Version: 3.5.3
      Implementation: PyPy
    my-app ->
      Version: 3.5.2
      Implementation: CPython
    old ->
      Version: 2.7.12
      Implementation: CPython

..

    **Arguments:**

*name*
    The desired name of the virtual environment.

..

    **Options:**

*-py/--python*
    The named Python path to use. This overrides --pypath.

*-pp/--pypath*
    An absolute path to a Python executable.

*-g/--global-packages*
    Gives the virtual environment access to the global site-packages.

*-c/--clone*
    Specifies an existing virtual env to clone. (Experimental)

*-r/--restore*
    Attempts to make all virtual envs in the venvs directory usable by fixing the
    executable paths in scripts and removing  all compiled ``*.pyc`` files. (Experimental)

*-v/--verbose*
    Increases verbosity.

*-l/--list*
    Shows available virtual envs. Can stack up to 3 times to show more info.

``shed``
^^^^^^^^

Removes named Python paths or virtual environments.

.. code-block:: bash

    $ hatch pypath -l
    py2 -> /usr/bin/python
    py3 -> /usr/bin/python3
    invalid -> :\/:
    $ hatch env -ll
    Virtual environments found in /home/ofek/.virtualenvs:

    duplicate ->
      Version: 3.5.2
      Implementation: CPython
    fast ->
      Version: 3.5.3
      Implementation: PyPy
    my-app ->
      Version: 3.5.2
      Implementation: CPython
    old ->
      Version: 2.7.12
      Implementation: CPython
    $ hatch shed -p invalid -e duplicate/old
    Successfully removed Python path named `invalid`.
    Successfully removed virtual env named `duplicate`.
    Successfully removed virtual env named `old`.

..

    **Options:**

*-p/-py/--pypath*
    Forward-slash-separated list of named Python paths.

*-e/--env*
    Forward-slash-separated list of named virtual envs.

``shell``
^^^^^^^^^

Activates or sends a command to a virtual environment. A default shell
name (or command) can be specified in the config file entry ``shell`` or the
environment variable ``SHELL``. If there is no entry, env var, nor shell
option provided, a system default will be used: ``cmd`` on Windows, ``bash``
otherwise.

Any arguments provided after the first will be sent to the virtual env as
a command without activating it. If there is only the env without args,
it will be activated similarly to how you are accustomed. The name of
the virtual env to use must be omitted if using the --temp env option.
If no env is chosen, this will attempt to detect a project and activate
its virtual env. To run a command in a project's virtual env, use ``.`` as
the env name.

Activation will not do anything to your current shell, but will rather
spawn a subprocess to avoid any unwanted strangeness occurring in your
current environment. If you would like to learn more about the benefits
of this approach, be sure to read `<https://gist.github.com/datagrok/2199506>`_.
To leave a virtual env, type ``exit``, or you can do ``Ctrl+D`` on non-Windows
machines.

``use`` is an alias for this command.

Activation:

.. code-block:: bash

    $ hatch env -ll
    Virtual environments found in `/home/ofek/.virtualenvs`:

    fast ->
      Version: 3.5.3
      Implementation: PyPy
    my-app ->
      Version: 3.5.2
      Implementation: CPython
    old ->
      Version: 2.7.12
      Implementation: CPython
    $ which python
    /usr/bin/python
    $ hatch shell my-app
    (my-app) $ which python
    /home/ofek/.virtualenvs/my-app/bin/python

Commands:

.. code-block:: bash

    $ hatch shell my-app pip list --format=columns
    Package    Version
    ---------- -------
    pip        9.0.1
    setuptools 36.3.0
    wheel      0.29.0
    $ hatch shell my-app hatch install -q requests six
    $ hatch shell my-app pip list --format=columns
    Package    Version
    ---------- -----------
    certifi    2017.7.27.1
    chardet    3.0.4
    idna       2.6
    pip        9.0.1
    requests   2.18.4
    setuptools 36.3.0
    six        1.10.0
    urllib3    1.22
    wheel      0.29.0

Temporary env:

.. code-block:: bash

    $ hatch shell -t
    Already using interpreter /usr/bin/python3
    Using base prefix '/usr'
    New python executable in /tmp/tmpzg73untp/Ihqd/bin/python3
    Also creating executable in /tmp/tmpzg73untp/Ihqd/bin/python
    Installing setuptools, pip, wheel...done.
    $ which python
    /tmp/tmpzg73untp/Ihqd/bin/python

..

    **Arguments:**

*env_name*
    The name of the desired virtual environment to use.

*command*
    The command to send to the virtual environment (optional).

..

    **Options:**

*-s/--shell*
    The name of shell to use e.g. ``bash``. If the shell name is not
    supported, e.g. ``bash -O``, it will be treated as a command and
    no custom prompt will be provided. This overrides the config file
    entry ``shell``.

*-t/--temp*
    Use a new temporary virtual env.

*-py/--python*
    A named Python path to use when creating a temporary virtual
    env. This overrides --pypath.

*-pp/--pypath*
    An absolute path to a Python executable to use when creating
    a temporary virtual env.

*-g/--global-packages*
    Gives created virtual envs access to the global site-packages.

``clean``
^^^^^^^^^

Removes a project's build artifacts.

The path to the project is derived in the following order:

1. The optional argument, which should be the name of a package
   that was installed via ``hatch install -l`` or ``pip install -e``.
2. The --local flag.
3. The option --path, which can be a relative or absolute path.
4. The current directory.

All ``*.pyc``/``*.pyd``/``*.pyo`` files and ``__pycache__`` directories will be removed.
Additionally, the following patterns will be removed from the root of the path:
``.cache``, ``.coverage``, ``.eggs``, ``.tox``, ``build``, ``dist``, and ``*.egg-info``.

If the path was derived from the optional package argument, the pattern
``*.egg-info`` will not be applied so as to not break that installation.

..

    **Arguments:**

*package*
    The editable package to target (optional).

..

    **Options:**

*-l/--local*
    Shortcut to select the only available local (editable) package. If
    there are multiple, an error will be raised.

*-p/--path*
    A relative or absolute path to a project.

*-c/--compiled-only*
    Removes only .pyc files.

*-nd/--no-detect*
    Disables the detection of a project's dedicated virtual env. By default,
    it will not be considered.

*-v/--verbose*
    Shows removed paths.

``build``
^^^^^^^^^

Builds a project, producing a source distribution and a wheel.

The path to the project is derived in the following order:

1. The optional argument, which should be the name of a package
   that was installed via ``hatch install -l`` or ``pip install -e``.
2. The --local flag.
3. The option --path, which can be a relative or absolute path.
4. The current directory.

The path must contain a ``setup.py`` file.

..

    **Arguments:**

*package*
    The editable package to target (optional).

..

    **Options:**

*-l/--local*
    Shortcut to select the only available local (editable) package. If
    there are multiple, an error will be raised.

*-p/--path*
    A relative or absolute path to a project.

*-py/--python*
    The named Python path to use. This overrides --pypath.

*-pp/--pypath*
    An absolute path to a Python executable.

*-u/--universal*
    Indicates compatibility with both Python 2 and 3.

*-n/--name*
    Forces a particular platform name, e.g. linux_x86_64.

*-d/--build-dir*
    A relative or absolute path to the desired build directory.

*-c/--clean*
    Removes build artifacts before building.

*-v/--verbose*
    Increases verbosity.

``release``
^^^^^^^^^^^

Uploads all files in a directory to PyPI using Twine.

The path to the build directory is derived in the following order:

1. The optional argument, which should be the name of a package
   that was installed via ``hatch install -l`` or ``pip install -e``.
2. The --local flag.
3. The option --path, which can be a relative or absolute path.
4. The current directory. If the current directory has a ``dist``
   directory, that will be used instead.

If the path was derived from the optional package argument, the
files must be in a directory named ``dist``.

The PyPI username can be saved in the config file entry ``pypi_username``.
If the ``TWINE_PASSWORD`` environment variable is not set, a hidden prompt
will be provided for the password.

..

    **Arguments:**

*package*
    The editable package to target (optional).

..

    **Options:**

*-l/--local*
    Shortcut to select the only available local (editable) package. If
    there are multiple, an error will be raised.

*-p/--path*
    A relative or absolute path to a build directory.

*-u/--username*
    The PyPI username to use.

*-t/--test*
    Uses the test version of PyPI.

*-s/--strict*
    Aborts if a distribution already exists.

``install``
^^^^^^^^^^^

If the option --env is supplied, the install will be applied using
that named virtual env. Unless the option --global is selected, the
install will only affect the current user. Of course, this will have
no effect if a virtual env is in use. The desired name of the admin
user can be set with the ``_DEFAULT_ADMIN_`` environment variable.

With no packages selected, this will install using a ``setup.py`` in the
current directory.

If no --env is chosen, this will attempt to detect a project and use its
virtual env before resorting to the default pip. No project detection
will occur if a virtual env is active.

..

    **Arguments:**

*packages*
    The packages to install (optional).

..

    **Options:**

*-nd/--no-detect*
    Disables the use of a project's dedicated virtual env. This is useful if
    you need to be in a project root but wish to not target its virtual env.

*-e/--env*
    The named virtual env to use.

*-l/--local*
    Corresponds to ``pip``'s --editable option, allowing a local package to be
    automatically updated when modifications are made.

*-g/--global*
    Installs globally, rather than on a per-user basis. This has no effect if
    a virtual env is in use.

*--admin*
    When --global is selected, this assumes admin rights are already enabled
    and therefore sudo/runas will not be used.

*-q/--quiet*
    Decreases verbosity.

``uninstall``
^^^^^^^^^^^^^

If the option --env is supplied, the uninstall will be applied using
that named virtual env. Unless the option --global is selected, the
uninstall will only affect the current user. Of course, this will have
no effect if a virtual env is in use. The desired name of the admin
user can be set with the ``_DEFAULT_ADMIN_`` environment variable.

With no packages selected, this will uninstall using a ``requirements.txt``
or a dev version of that in the current directory.

If no --env is chosen, this will attempt to detect a project and use its
virtual env before resorting to the default pip. No project detection
will occur if a virtual env is active.

..

    **Arguments:**

*packages*
    The packages to uninstall (optional).

..

    **Options:**

*-nd/--no-detect*
    Disables the use of a project's dedicated virtual env. This is useful if
    you need to be in a project root but wish to not target its virtual env.

*-e/--env*
    The named virtual env to use.

*-g/--global*
    Uninstalls globally, rather than on a per-user basis. This has no effect if
    a virtual env is in use.

*--admin*
    When --global is selected, this assumes admin rights are already enabled
    and therefore sudo/runas will not be used.

*-d/--dev*
    When locating a requirements file, only use the dev version.

*-y/--yes*
    Confirms the intent to uninstall without a prompt.

*-q/--quiet*
    Decreases verbosity.

``update``
^^^^^^^^^^

If the option --env is supplied, the update will be applied using
that named virtual env. Unless the option --global is selected, the
update will only affect the current user. Of course, this will have
no effect if a virtual env is in use. The desired name of the admin
user can be set with the ``_DEFAULT_ADMIN_`` environment variable.

When performing a global update, your system may use an older version
of pip that is incompatible with some features such as --eager. To
force the use of these features, use --force.

With no packages nor options selected, this will update packages by looking
for a ``requirements.txt`` or a dev version of that in the current directory.

If no --env is chosen, this will attempt to detect a project and use its
virtual env before resorting to the default pip. No project detection
will occur if a virtual env is active.

To update this tool, use the --self flag. All other methods of updating will
ignore ``hatch``. See: `<https://github.com/pypa/pip/issues/1299>`_

..

    **Arguments:**

*packages*
    The packages to update (optional).

..

    **Options:**

*-nd/--no-detect*
    Disables the use of a project's dedicated virtual env. This is useful if
    you need to be in a project root but wish to not target its virtual env.

*-e/--env*
    The named virtual env to use.

*--eager*
    Updates all dependencies regardless of whether they still satisfy the
    new parent requirements. See: `<https://github.com/pypa/pip/pull/3972>`_

*--all*
    Updates all currently installed packages. The packages ``pip``,
    ``setuptools``, and ``wheel`` are excluded.

*--infra*
    Updates only the packages ``pip``, ``setuptools``, and ``wheel``.

*-g/--global*
    Updates globally, rather than on a per-user basis. This has no effect if
    a virtual env is in use.

*--admin*
    When --global is selected, this assumes admin rights are already enabled
    and therefore sudo/runas will not be used.

*-f/--force*
    Forces the use of newer features in global updates.

*-d/--dev*
    When locating a requirements file, only use the dev version.

*-m/--module*
    Invokes ``pip`` as a module instead of directly, i.e. ``python -m pip``.

*--self*
    Updates ``hatch`` itself.

*-q/--quiet*
    Decreases verbosity.
