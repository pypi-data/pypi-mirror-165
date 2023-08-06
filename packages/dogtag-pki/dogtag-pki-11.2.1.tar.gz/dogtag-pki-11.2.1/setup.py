# Authors:
#     Christian Heimes <cheimes@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (C) 2015 Red Hat, Inc.
# All rights reserved.
#
"""Dogtag client library

In order to build wheels the wheel and setuptools packages are required:

  $ sudo yum install python-wheel python-setuptools

The 'release' alias builds and uploads a source distribution and universal
wheel. The version and release number are taken from pki.spec file.

  $ python setup.py release

The 'packages' alias just creates the files locally:

  $ python setup.py packages

For a complete list of all available commands (except for aliases):

  $python setup.py --help-commands
"""

from setuptools import setup

setup(
    author='Dogtag Certificate System Team',
    author_email='devel@lists.dogtagpki.org',
    name='dogtag-pki',
    version="11.2.1",
    description='Client library for Dogtag Certificate System',
    long_description="""\
This package contains the REST client for Dogtag PKI.

The Dogtag Certificate System is an enterprise-class open source
Certificate Authority (CA). It is a full-featured system, and has been
hardened by real-world deployments. It supports all aspects of certificate
lifecycle management, including key archival, OCSP and smartcard management,
and much more. The Dogtag Certificate System can be downloaded for free
and set up in less than an hour.""",
    license='LGPLv3+',
    keywords='pki x509 cert certificate',
    url='https://www.dogtagpki.org',
    packages=['pki', 'pki.cli'],
    install_requires=['requests', 'six', 'cryptography'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU Lesser General Public License ' +
            'v3 or later (LGPLv3+)',
        'Topic :: Security :: Cryptography',
    ],
)
