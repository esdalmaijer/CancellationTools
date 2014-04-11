# IMPORTS
# import every package we use, this prevents some errors
import matplotlib, numpy, pygame
# import everything we need to package stuff
from distutils.core import setup
import distutils.sysconfig as sysconfig
from py2exe.build_exe import py2exe
# import modules to to some file magic
import compileall
import os
import shutil
import sys


# # # # #
# PREPARATION

print("Starting setup, prepare for take-off...")

# PACKAGING
# packages that need to be copied rather than included in the library.zip archive, as that
# seems to fuck things up somehow
copy_packages = ['pygame',
                 'numpy',
                 'libcancellation']
# packages that are not part of standard packages, and are not copied, but should be included
include_packages = []
# packages that need to be excluded
exclude_packages = ['idlelib',
                    'antigravity',
                    'test']
# DLLs that cannot be included
exclude_dll = ['MSVCP90.dll',
               'libzmq.dll']
# Python folder (from which some packages need to be copied)
python_folder = r"C:\Anaconda"

# LIBZMQ.DLL ERROR
if not 'libzmq.dll' in exclude_dll:
    # libzmq.dll is in same directory as zmq's __init__.py
    import zmq
    os.environ["PATH"] = os.environ["PATH"] + os.path.pathsep + os.path.split(zmq.__file__)[0]
    zmqfiles = ["zmq.utils", "zmq.utils.jsonapi","zmq.utils.strtypes"]
else:
    zmqfiles = []

# DIRECTORIES
directory = os.path.dirname(os.path.abspath(__file__))
resdir = os.path.join(directory, 'resources')

# FUNCTIONS
# filter to ignore non-relevant package files
def ignore_package_files(folder, files):
    l = []
    for f in files:
        if os.path.splitext(f)[1] in [".pyo", ".pyc"]:
            l.append(f)
    return l
# function to strip non-compiled scripts and backup files
def strip_py(folder):
    print("Woohoo, stripping! (folder '%s')" % folder)
    for path in os.listdir(folder):
        path = os.path.join(folder, path)
        if os.path.isdir(path):
            strip_py(path)
            continue
        base, ext = os.path.splitext(path)
        if (ext in ('.py', '.pyc') and os.path.exists(base+'.pyo')) or path[-1] == '~':
            print('stripping %s' % path)
            os.remove(path)
# filter to ignore non-relevant resource files
def ignore_resources(folder, files):
    l = []
    print("... %s" % folder)
    for f in files:
        if os.path.splitext(f)[1] in [".csv", ".pyc"]:
            l.append(f)
        return l


# # # # #
# RUN SETUP

print("Please note that this will take forever, and if an error occurs before finishing, you'll have to start ALL over!\n\n")

# DIST AND BUILD
print("deleting old shit...")
# delete existing directory trees
if os.path.exists(os.path.join(directory,'dist')):
    shutil.rmtree(os.path.join(directory,'dist'))
if os.path.exists(os.path.join(directory,'build')):
    shutil.rmtree(os.path.join(directory,'build'))
# create new dist directory
print("creating new dist directory...")
os.mkdir(os.path.join(directory,'dist'))

# COPY PACKAGES
for pkg in copy_packages:
    print("copying packages '%s' ... " % pkg)
    exec('import %s as _pkg' % pkg)
    pkg_folder = os.path.dirname(_pkg.__file__)
    print("\tfrom '%s'" % pkg_folder)
    pkg_target = os.path.join("dist", pkg)
    shutil.copytree(pkg_folder, pkg_target, symlinks=True, ignore=ignore_package_files)
    compileall.compile_dir(pkg_target, force=True)
    strip_py(pkg_target)

# LIST STANDARD PACKAGES
# create a list of standard pakcages that should be included
# http://stackoverflow.com/questions/6463918/how-can-i-get-a-list-of-all-the-python-standard-library-modules
print("detecting standard Python packages and modules ... ")
std_pkg = []
std_lib = sysconfig.get_python_lib(standard_lib=True)
for top, dirs, files in os.walk(std_lib):
    for nm in files:
        prefix = top[len(std_lib)+1:]
        if prefix[:13] == 'site-packages':
            continue
        if nm == '__init__.py':
            pkg = top[len(std_lib)+1:].replace(os.path.sep,'.')
        elif nm[-3:] == '.py':
            pkg = os.path.join(prefix, nm)[:-3].replace(os.path.sep,'.')
        elif nm[-3:] == '.so' and top[-11:] == 'lib-dynload':
            pkg = nm[0:-3]
        if pkg[0] == '_':
            continue
        exclude = False
        for _pkg in exclude_packages:
            if pkg.find(_pkg) == 0:
                exclude = True
                break
        if exclude:
            continue
        try:
            exec('import %s' % pkg)
        except:
            continue
        print(pkg)
        std_pkg.append(pkg)
for pkg in sys.builtin_module_names:
    print(pkg)
    std_pkg.append(pkg)

# SETUP
setup(
    name="CancellationTools",
    version="1.0.0",
    description="run and analyse cancellation tasks",
    author="Edwin Dalmaijer",
    author_email="e.s.dalmaijer@pygaze.org",
    url="http://www.pygaze.org/cancellation",
    windows=[{'script':'CancellationTools', 'icon_resources':[(0,os.path.join(resdir,'cancellationtools.ico'))]}],
    options={
          'py2exe': {
                    "compressed":True,
                    "optimize":2,
                    "bundle_files":3,
                    "excludes":copy_packages,
                    "includes":std_pkg + include_packages + zmqfiles,
                    "dll_excludes" : exclude_dll,
                    "packages":['matplotlib', 'pytz']
                    }
         },
    data_files=matplotlib.get_py2exe_datafiles()
    )

# COPY PACKAGES
# PyGame
print("copying PyGame/SDLL dll's...")
shutil.copyfile(r"%s\Lib\site-packages\pygame\SDL_ttf.dll" % python_folder, r"dist\SDL_ttf.dll")
shutil.copyfile(r"%s\Lib\site-packages\pygame\libfreetype-6.dll" % python_folder, r"dist\libfreetype-6.dll")
shutil.copyfile(r"%s\Lib\site-packages\pygame\libogg-0.dll" % python_folder, r"dist\libogg-0.dll")
# PIL (for Matplotlib)
print("copying PIL.pth...")
shutil.copyfile(r"%s\Lib\site-packages\PIL.pth" % python_folder, r"dist\PIL.pth")

# CREATE DATA DIRECTORY
print("creating new (empty) data directory...")
datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'data')
os.mkdir(datadir)
os.mkdir(os.path.join(datadir,'raw'))
os.mkdir(os.path.join(datadir,'output'))

# COPY RESOURCES DIRECTORY
print("copying resources...")
newresdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'resources')
shutil.copytree(resdir, newresdir)

print('Traceback (most recent call last):\n  File "setup.py", line 185, in (module)\n    error = LOL!\nFakeError: You actually made it to the end!')
