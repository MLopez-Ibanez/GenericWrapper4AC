import os
import shutil
import subprocess
import sys
import traceback
import setuptools
from setuptools.command.install import install

RUNSOLVER_LOCATION = os.path.join(os.path.dirname(__file__), 'runsolver',
                                  'runsolver-3.3.4-patched', 'src')
BINARIES_DIRECTORY = 'genericWrapper4AC/binaries'
TEST_DIRECTORY = os.path.join(os.path.dirname(__file__), 'test',
                              'test_binaries')


class InstallRunsolver(install):

    def run(self):
        # Build the runsolver
        sys.stdout.write('Building runsolver\n')
        cur_pwd = os.getcwd()
        print(cur_pwd)
        os.chdir(RUNSOLVER_LOCATION)
        subprocess.check_call('make')
        os.chdir(cur_pwd)

        # Create a fresh binaries directory
        try:
            shutil.rmtree(BINARIES_DIRECTORY)
        except Exception:
            pass

        try:
            os.makedirs(BINARIES_DIRECTORY)
        except Exception:
            pass

        # Copy the runsolver into the test directory so tests can be run
        try:
            os.makedirs(TEST_DIRECTORY)
        except Exception:
            pass
        shutil.copy(os.path.join(RUNSOLVER_LOCATION, 'runsolver'),
                        os.path.join(TEST_DIRECTORY, 'runsolver'))

        # Copy the runsolver into the sources so it gets copied
        shutil.move(os.path.join(RUNSOLVER_LOCATION, 'runsolver'),
                    os.path.join(BINARIES_DIRECTORY, 'runsolver'))


        #install.do_egg_install(self)
        install.run(self)

        try:
            shutil.rmtree(BINARIES_DIRECTORY)
        except OSError:
            pass


setuptools.setup(
    name='GenericWrapper4AC',
    description='Generic Wrapper to interface between algorithm configurators and algorithms to tune',
    version='2.0.0',
    python_requires='>=3.5',
    test_suite='nose.collector',
    tests_require=["nose", "numpy", "scipy", "scikit-learn"],
    cmdclass={'install': InstallRunsolver},
    include_package_data=True,
    package_data={"genericWrapper4AC": ["binaries/runsolver"]},
    author='Marius Lindauer',
    author_email='lindauer@informatik.uni-freiburg.de',
    license='BSD',
    platforms=['Linux'],
    classifiers=[],
    url='www.ml4aad.org')