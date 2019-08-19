from setuptools import setup

# global package constants
packageName     = 'colory'
packageVersion  = '0.1'              # provide a version tag as fallback
fullVersion     = packageVersion
strVersionFile  = "%s/version.py" %(packageName)

def getCurrentVersion():
    '''
    Determine package version and put it in the signatures.
    '''
    global packageVersion
    global fullVersion

    # check if there is a manual version override
    if os.path.isfile(".version"):
        with open(".version", "r") as f:
            stdout = f.read().split('\n')[0]
        print("Override of version string to '%s' (from .version file )" % (
            stdout))

        fullVersion = stdout

    else:
        # check if source directory is a git repository
        if not os.path.exists(".git"):
            print(("Installing from something other than a Git repository; " +
                   "Version file '%s' untouched.") % (strVersionFile))
            return

        # fetch current tag and commit description from git
        try:
            p = subprocess.Popen(
                ["git", "describe", "--tags", "--dirty", "--always"],
                stdout=subprocess.PIPE
            )
        except EnvironmentError:
            print("Not a git repository; Version file '%s' not touched." % (
                strVersionFile))
            return

        stdout = p.communicate()[0].strip()
        if stdout is not str:
            stdout = stdout.decode()

        if p.returncode != 0:
            print(("Unable to fetch version from git repository; " +
                   "leaving version file '%s' untouched.") % (strVersionFile))
            return

        fullVersion = stdout

    # output results to version string, extract package version number from
    # `fullVersion` as this string might also contain additional tags (e.g.
    # commit hashes or `-dirty` flags from git tags)
    versionMatch = re.match(r"[.+\d+]+\d*[abr]\d*", fullVersion)
    if versionMatch:
        packageVersion = versionMatch.group(0)
        print("Fetched package version number from git tag (%s)." % (
            packageVersion))
            
setup(
    author='Sebastian Semper',
    version=packageVersion,
    name=packageName,
    url='https://ems-tu-ilmenau.github.io/colorfy/',
    license='GNU General Public License 3',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
    ],
    packages=['colorfy'],
    scripts=['bin/colorfyScript'],

)
