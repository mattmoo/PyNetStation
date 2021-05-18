#!/usr/bin/env python

"""
This file is part of egi.
PyGaze is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
PyGaze is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with qnotero.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import glob
import pynetstation
from setuptools import setup

#print("Running setup for PyGaze version {}".format(pygaze.__version__))


def files(path):

	l = [fname for fname in glob.glob(path) if os.path.isfile(fname) \
		and not fname.endswith('.pyc')]
	print(l)
	return l


def data_files():

	"""
	desc:
		The OpenSesame plug-ins are installed as additional data. Under Windows,
		there is no special folder to put these plug-ins in, so we skip this
		step.
	returns:
		desc:	A list of data files to include.
		type:	list
	"""

	return [
		("share/opensesame_plugins/pynetstation_begin_trial",
			files("opensesame_plugins/pynetstation_begin_trial/*")),
		("share/opensesame_plugins/pynetstation_end",
			files("opensesame_plugins/pynetstation_end/*")),
		("share/opensesame_plugins/pynetstation_init",
			files("opensesame_plugins/pynetstation_init/*")),
		("share/opensesame_plugins/pynetstation_pause_recording",
			files("opensesame_plugins/pynetstation_pause_recording/*")),
		("share/opensesame_plugins/pynetstation_reinit",
			files("opensesame_plugins/pynetstation_reinit/*")),
		("share/opensesame_plugins/pynetstation_send_tags",
			files("opensesame_plugins/pynetstation_send_tags/*")),
		("share/opensesame_plugins/pynetstation_start_recording",
			files("opensesame_plugins/pynetstation_start_recording/*"))
		]

setup(
	name="PyNetStation",
	python_requires=">=3",
	version="0.2", #pygaze.__version__,
	description="A Python library for use with the EGI Net Station EEG recording software.",
	author=["Matthew Moore", "Joshua Zosky"],
	author_email="matthew.moore@auckland.ac.nz",
	url="https://github.com/imnotamember/pynetstation/",
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'Environment :: MacOS X',
		'Environment :: Win32 (MS Windows)',
		'Environment :: X11 Applications',
		'License :: MIT',
		'Programming Language :: Python :: 3',
	],
	include_package_data=True,
	packages = [
		"pynetstation"
		],
	data_files=data_files()
	)