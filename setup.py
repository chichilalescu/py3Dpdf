#! /usr/bin/env python2
#######################################################################
#                                                                     #
#  Copyright 2014 Cristian C Lalescu                                  #
#                                                                     #
#  This file is part of py3Dpdf.                                      #
#                                                                     #
#  py3Dpdf is free software: you can redistribute it and/or modify    #
#  it under the terms of the GNU General Public License as published  #
#  by the Free Software Foundation, either version 3 of the License,  #
#  or (at your option) any later version.                             #
#                                                                     #
#  py3Dpdf is distributed in the hope that it will be useful,         #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of     #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the      #
#  GNU General Public License for more details.                       #
#                                                                     #
#  You should have received a copy of the GNU General Public License  #
#  along with py3Dpdf.  If not, see <http://www.gnu.org/licenses/>    #
#                                                                     #
#######################################################################


########################################################################
#
# some global settings
#
AUTHOR = 'Cristian C Lalescu'
AUTHOR_EMAIL = ''
#
########################################################################



########################################################################
#
# define version
#
import datetime
now = datetime.datetime.now()
date_name = '{0:0>4}{1:0>2}{2:0>2}'.format(now.year, now.month, now.day)
VERSION = date_name
#
########################################################################



from setuptools import setup
setup(
        name = 'py3Dpdf',
        version = VERSION,
        packages = ['py3Dpdf'],
        install_requires = ['numpy>=1.8'],

        #### package description stuff goes here
        description = '3D PDF printing from python',
        long_description = open('README.rst', 'r').read(),
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        license = 'GNU GPLv3',
        classifiers = [
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'Natural Language :: English',
            'Programming Language :: Python'
            ],
        )

