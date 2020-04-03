# Originally contributed by Lorne McIntosh.
# Modified by Eric Xu
# Further modification by random internet people.

# You will probably have to edit this file in unpredictable ways
# if you want pyipopt to work for you, sorry.

# When I installed Ipopt from source, I used the
# --prefix=/usr/local
# option, so this is where I want pyipopt to look for my ipopt installation.
# I only installed from source because the ipopt packaging
# for my linux distribution was buggy,
# so by the time you read this the bugs have probably been fixed
# and you will want to specify a different directory here.
IPOPT_DIR = '/usr/'

import os
from distutils.core import setup
from distutils.extension import Extension

# NumPy is much easier to install than pyipopt,
# and is a pyipopt dependency, so require it here.
# We need it to tell us where the numpy header files are.
#import numpy
#numpy_include = numpy.get_include()

# I personally do not need support for lib64 but I'm keeping it in the code.
def get_ipopt_lib():
    for lib_suffix in ('lib', 'lib64'):
        d = os.path.join(IPOPT_DIR, lib_suffix)
        if os.path.isdir(d):
            return d

IPOPT_LIB = get_ipopt_lib()
if IPOPT_LIB is None:
    raise Exception('failed to find ipopt lib')

IPOPT_INC = os.path.join(IPOPT_DIR, 'include/coin/')

PYIPOPT_CORE_FILES = ['src/callback.c', 'src/pyipoptcoremodule.c']

# this is from: https://stackoverflow.com/questions/19919905/how-to-bootstrap-numpy-installation-in-setup-py
from setuptools.command.build_ext import build_ext as _build_ext

class build_ext(_build_ext):
    def run(self):
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

# The extra_link_args is commented out here;
# that line was causing my pyipopt install to not work.
# Also I am using coinmumps instead of coinhsl.
pyipopt_extension = Extension(
        'pyipoptcore',
        PYIPOPT_CORE_FILES,
        library_dirs=[IPOPT_LIB],
        libraries=[
            'ipopt',
            'dl',
            'm',
            ],
        include_dirs=[IPOPT_INC],
        )

setup(
        name="pyipopt",
        version="0.9",
        description="An IPOPT connector for Python",
        author="Morten Olsen Lysgaard",
        author_email="molysgaard@gmail.com",
        url="https://github.com/molysgaard/pyipopt",
        cmdclass={'build_ext':build_ext},
        setup_requires=['numpy',],
        packages=['pyipopt'],
        ext_modules=[pyipopt_extension],
        #install_requires=['numpy',],
        )

