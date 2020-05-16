from setuptools import setup
import os

version = open('/Users/yanone/Code/py/git/typeworld/guiapp/currentVersion.txt', 'r').read().strip()

os.system('rm -rf ~/Code/TypeWorldApp/apps/Mac/Type.World.%s.app' % version)

options = {'py2app': {'argv_emulation': False, # this puts the names of dropped files into sys.argv when starting the app.
           'iconfile': '/Users/yanone/Code/py/git/typeworld/guiapp/wxPython/icon/tw.icns',
           'includes': ['ynlib', 'importlib_metadata', 'os'],#, 'os', 'webbrowser', 'urllib', 'base64', 'keyring'],
           'frameworks': ['Python.framework'],
           'resources': [
                '/Users/yanone/Code/py/git/typeworld/guiapp/wxPython/build/Mac/InternetAccessPolicy.plist', 
                '/Users/yanone/Code/py/git/typeworld/guiapp/wxPython/build/Mac/Little Snitch Translations', 
                '/Users/yanone/Code/py/git/typeworld/guiapp/wxPython/htmlfiles', 
                '/Users/yanone/Code/py/git/typeworld/guiapp/wxPython/patrons', 
                '/Users/yanone/Code/py/git/typeworld/guiapp/wxPython/locales', 
                # Sparkle < 1.12.0
                '/Users/yanone/Code/Certificates/Type.World Sparkle/dsa_pub.pem',
            ], #, 'appbadge.docktileplugin'
           'packages': ['certifi', 
              'encodings', 'codecs', 'io', 'abc', 'os', 'stat', 'typeworld', 'keyring', 'importlib', 'pystray', 'markdown2', 'pkg_resources', '_collections_abc', 'posixpath', 'genericpath', 'linecache', 'functools', 'collections', 'operator', 'keyword', 'heapq', 'reprlib', 'tokenize', 're', 'enum', 'types', 'sre_compile', 'sre_parse', 'sre_constants', 'copyreg', 'token', 'ctypes', 'struct', 'webbrowser', 'shlex', 'shutil', 'fnmatch', 'subprocess', 'signal', 'warnings', 'selectors', 'threading', 'traceback', '_weakrefset', 'urllib', 'base64', 'bisect', 'email', 'hashlib', 'http', 'string', 'quopri', 'random', 'socket', 'datetime', 'calendar', 'locale', 'uu', 'tempfile', 'weakref', 'contextlib', 'plistlib', 'xml', 'json', 'semver', '__future__', 'argparse', 'gettext', 'platform', 'logging', 'wx', 'multiprocessing', 'pickle', '_compat_pickle', 'ynlib', 'ssl', 'inspect', 'dis', 'opcode', 'copy', 'zipfile', 'markdown2', 'optparse', 'textwrap', 'AppKit', 'objc', 'pkgutil', 'ntpath', 'pyparsing', 'pkg_resources', 'pprint', 'sysconfig', '_osx_support', '_sysconfigdata_m_darwin_darwin', 'typing', 'Foundation', 'six', 'grpc', 'concurrent', 'requests', 'urllib3', 'queue', 'hmac', 'mimetypes', 'chardet', 'idna',  'stringprep', 'pyasn1', 'pyasn1_modules', 'rsa', 'cachetools', 'pytz', 'uuid', 'configparser', 'importlib_metadata', 'csv', 'zipp', 'more_itertools', 'pathlib', '_strptime', 

              # Dependencies of deepdiff
              'deepdiff', 'difflib', 'jsonpickle', 'decimal', '_pydecimal', 'numbers', 'ordered_set', 'ast'],

              
           'bdist_base': '%s/Code/TypeWorldApp/build/' % os.path.expanduser('~'),
           'dist_dir': '%s/Code/TypeWorldApp/dist/' % os.path.expanduser('~'),
           'plist': {
                'CFBundleName': 'Type.World',
                'CFBundleShortVersionString':version, # must be in X.X.X format
                'CFBundleVersion': version,
                'CFBundleIdentifier':'world.type.guiapp', #optional
                'NSHumanReadableCopyright': '@ Yanone 2020', #optional
                'CFBundleDevelopmentRegion': 'English', #optional - English is default
                # 'NSDockTilePlugIn': '@executable_path/../Resources/AppBadge.docktileplugin',
                'CFBundleURLTypes': [{'CFBundleURLName': 'Type.World Font Installation Protocols', 'CFBundleURLSchemes': ['typeworld', 'typeworldapp']}],
#                'LSUIElement': True, # No dock icon

                # Sparkle
                'SUFeedURL': 'https://type.world/static/guiapp/appcast.xml',
                'SUEnableAutomaticChecks': True,

                # Sparkle < 1.20.0
                'SUPublicDSAKeyFile': 'dsa_pub.pem',
                # Sparkle >= 1.20.1
                'SUPublicEDKey': 'IqLvpa980dAYzn9P6ttJiBgMQTpI58G6lchzLC9Q8aA=',

                'SUAllowsAutomaticUpdates': True,
                },
           'strip': True,
#           'debug-skip-macholib': True,
           'optimize': 1,
#     'semi_standalone': False,
#     'no-chdir': True,
           }}


# Little Snitch Translations
folder = '/Users/yanone/Code/py/git/typeworld/guiapp/wxPython/build/Mac/Little Snitch Translations'
options['py2app']['resources'].extend([os.path.join(folder, x) for x in next(os.walk(folder))[1]])


setup(
    app=['/Users/yanone/Code/py/git/typeworld/guiapp/wxPython/app.py'],
    data_files=[],
    options=options,
    setup_requires=['py2app'],
)




# # Attention: Hack!
# os.chdir('/Users/yanone/Code/TypeWorldApp/dist/Type.World.app/Contents/Resources/lib/python3.7/lib-dynload/wx/')
# for file in ['libwx_baseu-3.0.0.4.0.dylib', 'libwx_osx_cocoau_core-3.0.0.4.0.dylib', 'libwx_osx_cocoau_webview-3.0.0.4.0.dylib', 'libwx_baseu_net-3.0.0.4.0.dylib']:
#     assert os.system('ln -s ../../../../../Frameworks/%s %s' % (file, file)) == 0