import ctypes
# api = ctypes.cdll.LoadLibrary('.\\aardvark.dll')
try:
    import aardvark as api
except ImportError, ex1:
    import imp, platform
    ext = platform.system() in ('Windows', 'Microsoft') and '.dll' or '.so'
    try:
        api = imp.load_dynamic('aardvark', 'aardvark' + ext)
    except ImportError, ex2:
        import_err_msg  = 'Error importing aardvark%s\n' % ext
        import_err_msg += '  Architecture of aardvark%s may be wrong\n' % ext
        import_err_msg += '%s\n%s' % (ex1, ex2)
        raise ImportError(import_err_msg)

# version = api.py_version
# print(api.py_version)
print(dir(api))
