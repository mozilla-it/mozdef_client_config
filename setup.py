#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright (c) 2018 Mozilla Corporation
""" Packaging script """

import os
import subprocess
from setuptools import setup

VERSION = '0.0.5'


def git_version():
    """ Return the git revision as a string """
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for envvar in ['SYSTEMROOT', 'PATH']:
            val = os.environ.get(envvar)
            if val is not None:
                env[envvar] = val
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        git_revision = out.strip().decode('ascii')
    except OSError:
        git_revision = u"Unknown"

    return git_revision


def read(fname):
    """ Contents of a single filename """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mozdef-client-config',
    py_modules=['mozdef_client_config'],
    version=VERSION,
    author='Greg Cox',
    author_email='gcox@mozilla.com',
    description=('Wrapper to mozdef_client with one unified config\n' +
                 'This package is built upon commit '+git_version()),
    license='MPL',
    keywords='mozilla ldap',
    url='https://github.com/mozilla-it/mozdef_client_config',
    long_description=read('README.rst'),
    install_requires=['mozdef_client>=1.0.11'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    ],
)
