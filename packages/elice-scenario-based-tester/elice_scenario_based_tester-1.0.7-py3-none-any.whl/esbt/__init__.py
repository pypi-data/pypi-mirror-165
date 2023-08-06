try:
    from setuptools_scm import get_version
    __version__ = get_version(root='..', relative_to=__file__)
except LookupError:
    try:
        from ._version import version
        __version__ = version
    except ModuleNotFoundError:
        raise RuntimeError('Cannot determine version : check git repository or _version.py fle')
