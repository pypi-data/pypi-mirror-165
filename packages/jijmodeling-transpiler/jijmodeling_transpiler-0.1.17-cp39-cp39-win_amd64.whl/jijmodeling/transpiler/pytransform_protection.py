# platforms: windows.x86_64.11.py39
# advanced: 2
# suffix: _vax_001333
# license: licenses/jijmodelingtranspiler/license.lic
def protect_pytransform():

    def assert_builtin(func):
        type = ''.__class__.__class__
        builtin_function = type(''.join)
        if type(func) is not builtin_function:
            raise RuntimeError('%s() is not a builtin' % func.__name__)

    def check_obfuscated_script():
        from sys import _getframe
        CO_SIZES = 30, 39
        CO_NAMES = set(['pytransform_vax_001333', 'pyarmor',
                        '__name__', '__file__'])
        co = _getframe(3).f_code
        if not ((set(co.co_names) <= CO_NAMES)
                and (len(co.co_code) in CO_SIZES)):
            raise RuntimeError('unexpected obfuscated script')

    def check_lib_pytransform():
        from sys import platform
        if platform == 'darwin':
            return
        import pytransform_vax_001333 as pytransform
        filename = pytransform.__file__
        with open(filename, 'rb') as f:
            buf = bytearray(f.read())
        value = sum(buf)
        sys = __import__('sys')
        if hasattr(sys, 'frozen') and sys.platform == 'darwin':
            major, minor = sys.version_info[:2]
            if '_vax_001333':
                value += 886 - sum(b'_vax_001333') + (
                      1151 if major == 2 else (1161 + minor))
            else:
                value += 2069 if major == 2 else (2079 + minor)
        if value not in [113591304]:
            raise RuntimeError('unexpected %s' % filename)

    assert_builtin(sum)
    assert_builtin(open)
    assert_builtin(len)

    check_obfuscated_script()
    check_lib_pytransform()


protect_pytransform()
