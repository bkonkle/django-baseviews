VERSION = (0, 5, 0, "f", 0) # following PEP 386
DEV_N = 1 # for PyPi releases, set this to None


def get_version(short=False):
    version = "%s.%s" % (VERSION[0], VERSION[1])
    if short:
        return version
    if VERSION[2]:
        version = "%s.%s" % (version, VERSION[2])
    if VERSION[3] != "f":
        version = "%s%s%s" % (version, VERSION[3], VERSION[4])
        if DEV_N:
            version = "%s.dev%s" % (version, DEV_N)
    return version

__version__ = get_version()
