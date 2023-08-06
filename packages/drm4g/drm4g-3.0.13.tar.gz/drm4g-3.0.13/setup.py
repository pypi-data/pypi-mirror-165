# Copyright 2021 Santander Meteorology Group (UC-CSIC)
#
# Licensed under the EUPL, Version 1.1 only (the
# "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
#
# http://ec.europa.eu/idabc/eupl
#
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
#

import os
import subprocess
import sys
import stat
from pprint import pprint

from importlib.util import module_from_spec, spec_from_file_location
from setuptools import setup, Extension, find_packages
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext
from setuptools.command.develop import develop

#To ensure a script runs with a minimal version requirement of the Python interpreter
assert sys.version_info >= (3, 5), "The version number of Python has to be >= 3.5"

HERE_PATH = os.path.abspath(os.path.dirname(__file__))
GRIDWAY_SRC = "gridway-5.8"
MAKE_CLEAN = False

def build():
    current_path = os.getcwd()
    if not os.path.exists(GRIDWAY_SRC) :
        raise Exception("The specified directory %s doesn't exist" % GRIDWAY_SRC)

    #setting same mtime to gridway sources
    mtime_ref = os.path.getmtime(GRIDWAY_SRC)
    for root, dirs, files in os.walk(GRIDWAY_SRC):
        for name in files + dirs:
            os.utime(os.path.join(root, name), (mtime_ref, mtime_ref))
    os.utime(GRIDWAY_SRC, (mtime_ref, mtime_ref))

    os.chdir( GRIDWAY_SRC )
    #to avoid re-run configure each time.
    if(not os.path.isfile('config.log') or
           os.path.getmtime('config.log') <= os.path.getmtime('configure') ):
        os_st = os.stat('configure')
        os.chmod('configure', os_st.st_mode | stat.S_IEXEC)
        os.makedirs('build',exist_ok = True)
        build_path = os.path.abspath('build')
        exit_code = subprocess.call('./configure --prefix="%s"' % build_path, shell=True)
        if exit_code:
            raise Exception("Configure failed - check config.log for more detailed information")

    exit_code = subprocess.call('make', shell=True)
    if exit_code:
        raise Exception("make failed")
    exit_code = subprocess.call('make install', shell=True)
    if exit_code:
        raise Exception("make install failed")
    if MAKE_CLEAN:
        exit_code = subprocess.call('make clean', shell=True)
        if exit_code:
            raise Exception("make clean failed")
    os.chdir( current_path )

GW_FILES = ('bin',
    [
      GRIDWAY_SRC + '/build/bin/gwuser',
      GRIDWAY_SRC + '/build/bin/gwacct',
      GRIDWAY_SRC + '/build/bin/gwwait',
      GRIDWAY_SRC + '/build/bin/gwhost',
      GRIDWAY_SRC + '/build/bin/gwhistory',
      GRIDWAY_SRC + '/build/bin/gwsubmit',
      GRIDWAY_SRC + '/build/bin/gwps',
      GRIDWAY_SRC + '/build/bin/gwkill',
      GRIDWAY_SRC + '/build/bin/gwd',
      GRIDWAY_SRC + '/build/bin/gw_flood_scheduler',
      GRIDWAY_SRC + '/build/bin/gw_sched',
    ])

class build_ext_wrapper(build_ext):
    def run(self):
        print("[running build_ext_wrapper.run() ...]")
        if self.verbose:
            pprint(vars(self))
        build()
        build_ext.run(self)

class install_wrapper(install):
    def run(self):
        print("[running install_wrapper.run() ...]")
        if self.verbose:
            pprint(vars(self))
        build()
        install.run(self)

class develop_wrapper(develop):
    def run(self):
        print("[running develop_wrapper.run() ...]")
        develop.run(self)
        if self.verbose:
            pprint(vars(self))
        for filename in GW_FILES[1]:
            dst = os.path.join(self.script_dir, os.path.basename(filename))
            if os.path.lexists(dst):
                if self.verbose:
                    print("[removing %s]" % dst)
                os.remove(dst)
            src = os.path.abspath(filename)
            if not self.uninstall:
                if self.verbose:
                    print("[creating symlink: %s -> %s]" % (dst, src))
                os.symlink(src,dst)

# FROM: https://github.com/jbweston/miniver
def get_version_and_cmdclass(package_name):
    spec = spec_from_file_location(
             'version',
             os.path.join(package_name, '_version.py')
           )
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__, module.cmdclass
version, cmdclass = get_version_and_cmdclass('drm4g')

# read the contents of your README file
with open(os.path.join(HERE_PATH, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'drm4g',
    version = version,
    python_requires = ">=3.5",
    packages = find_packages(),
    include_package_data = True,
    package_data = {'drm4g' : ['conf/*']},
    data_files = [GW_FILES],
    author = 'Santander Meteorology Group (UC-CSIC)',
    author_email = 'antonio.cofino@unican.es',
    url = 'https://github.com/SantanderMetGroup/DRM4G',
    project_urls = {
      'Documentation' : 'https://github.com/SantanderMetGroup/DRM4G/wiki'   ,
      'Source'        : 'https://github.com/SantanderMetGroup/DRM4G'        ,
      'Tracker'       : 'https://github.com/SantanderMetGroup/DRM4G/issues' ,
      'Download'      : 'https://pypi.org/project/drm4g/#files'             ,
      'Twitter'       : 'https://twitter.com/SantanderMeteo'
    },
    description = 'Meta-scheduling framework for distributed computing infrastructures',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    classifiers = [
      "Development Status :: 4 - Beta",
      "Environment :: Console",
      "Intended Audience :: Science/Research",
      "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
      "Operating System :: POSIX",
      "Topic :: Scientific/Engineering",
      "Topic :: Office/Business :: Scheduling",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.5",
      "Programming Language :: Python :: 3.6",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
    ],
    install_requires = [ 'paramiko>=2.4', 'scp', 'fabric' ],
    entry_points = {
      'console_scripts': [
          'drm4g=drm4g.commands.main:main',
          'gw_im_mad_drm4g.py=drm4g.core.im_mad:main',
          'gw_em_mad_drm4g.py=drm4g.core.em_mad:main',
          'gw_tm_mad_drm4g.py=drm4g.core.tm_mad:main',
        ],
    },
    ext_modules = [
        Extension(
            name = 'drm4g.gridway',
            sources = []
        )
    ],
    cmdclass = {
      'build_ext' : build_ext_wrapper,
      'install'   : install_wrapper,
      'develop'   : develop_wrapper,
      'sdist'     : cmdclass['sdist'],
      'build_py'  : cmdclass['build_py'],
    },
  )
