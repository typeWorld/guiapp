import os, sys

from subprocess import Popen,PIPE,STDOUT


version = open('/Users/yanone/Code/py/git/typeWorld/guiapp/currentVersion.txt', 'r').read().strip()
findSymlinks = 'find -L ~/Code/TypeWorldApp/dist/Type.World.app -type l'
sparkle = '/Users/yanone/Code/Sparkle-1.21.2/Sparkle.framework'

flavour = sys.argv[-1]


_list = [
['Remove old build folder', 'rm -rf /Users/yanone/Code/TypeWorldApp/build/*', None, ''],
['Remove old dist folder', 'rm -rf /Users/yanone/Code/TypeWorldApp/dist/*', None, ''],
# ['Remove old dist folder', 'rm -rf //Users/yanone/Code/py/git/typeWorld/guiapp/wxPython/dist', None, ''],
# ['Python build', '/Users/yanone/Library/Python/3.6/bin/pyinstaller --windowed --onedir /Users/yanone/Code/py/git/typeWorld/guiapp/wxPython/build/Mac/setup_pyinstaller.spec', None, ''],

# Agent
['Agent build', '/usr/local/bin/python3 /Users/yanone/Code/py/git/typeWorld/guiapp/wxPython/build/Mac/setup_daemon.py py2app', None, ''],
['Signing inner components', 'codesign -s "Jan Gerner" -f "/Users/yanone/Code/TypeWorldApp/dist/Type.World Agent.app/Contents/Frameworks/Python.framework/Versions/3.6"', None, 'nosign'],
['Signing inner components', 'codesign -s "Jan Gerner" -f "/Users/yanone/Code/TypeWorldApp/dist/Type.World Agent.app/Contents/MacOS/python"', None, 'nosign'],
['Signing app', 'codesign -s "Jan Gerner" -f "/Users/yanone/Code/TypeWorldApp/dist/Type.World Agent.app"', None, 'nosign'],
['Zipping agent', 'tar -cjf /Users/yanone/Code/TypeWorldApp/dist/agent.tar.bz2 -C "/Users/yanone/Code/TypeWorldApp/dist/" "Type.World Agent.app"', None, ''],

# Main app
['Main App build', '/usr/local/bin/python3 /Users/yanone/Code/py/git/typeWorld/guiapp/wxPython/build/Mac/setup.py py2app', None, ''],
['Copying Sparkle', 'cp -R %s /Users/yanone/Code/TypeWorldApp/dist/Type.World.app/Contents/Frameworks/' % sparkle],
['Copying agent', 'cp /Users/yanone/Code/TypeWorldApp/dist/agent.tar.bz2 /Users/yanone/Code/TypeWorldApp/dist/Type.World.app/Contents/Resources/', None, ''],
['Unlink site.pyo', 'unlink ~/Code/TypeWorldApp/dist/Type.World.app/Contents/Resources/lib/python3.6/site.pyo', None, ''],
['Signing inner components', 'codesign -s "Jan Gerner" -f /Users/yanone/Code/TypeWorldApp/dist/Type.World.app/Contents/Frameworks/libwx_baseu-3.0.0.4.0.dylib', None, 'nosign'],
['Signing inner components', 'codesign -s "Jan Gerner" -f /Users/yanone/Code/TypeWorldApp/dist/Type.World.app/Contents/Frameworks/libwx_osx_cocoau_core-3.0.0.4.0.dylib', None, 'nosign'],
['Signing inner components', 'codesign -s "Jan Gerner" -f /Users/yanone/Code/TypeWorldApp/dist/Type.World.app/Contents/Frameworks/libwx_osx_cocoau_webview-3.0.0.4.0.dylib', None, 'nosign'],
['Signing inner components', 'codesign -s "Jan Gerner" -f /Users/yanone/Code/TypeWorldApp/dist/Type.World.app/Contents/Frameworks/libwx_baseu_net-3.0.0.4.0.dylib', None, 'nosign'],
['Signing inner components', 'codesign -s "Jan Gerner" -f /Users/yanone/Code/TypeWorldApp/dist/Type.World.app/Contents/Frameworks/Python.framework/Versions/3.6', None, 'nosign'],
['Signing inner components', 'codesign -s "Jan Gerner" -f /Users/yanone/Code/TypeWorldApp/dist/Type.World.app/Contents/Frameworks/Sparkle.framework/Versions/A', None, 'nosign'],
['Signing inner components', 'codesign -s "Jan Gerner" -f /Users/yanone/Code/TypeWorldApp/dist/Type.World.app/Contents/MacOS/python', None, 'nosign'],
['Signing app', 'codesign -s "Jan Gerner" -f ~/Code/TypeWorldApp/dist/Type.World.app', None, 'nosign'],
['Verify signature', 'codesign -dv --verbose=4  ~/Code/TypeWorldApp/dist/Type.World.app', None, 'nosign'],
['Verify signature', 'codesign --verify --deep --strict --verbose=20 ~/Code/TypeWorldApp/dist/Type.World.app', findSymlinks, 'nosign'],
['Verify signature', 'spctl -a -t exec -vvvv ~/Code/TypeWorldApp/dist/Type.World.app', findSymlinks, 'nosign'],

['Move app to archive folder', 'cp -R /Users/yanone/Code/TypeWorldApp/dist/Type.World.app /Users/yanone/Code/TypeWorldApp/apps/Mac/Type.World.%s.app' % version],
]

for l in _list:

	alt = None
	excludeCondition = None
	if len(l) == 2:
		desc, cmd = l
	if len(l) == 3:
		desc, cmd, alt = l
	if len(l) == 4:
		desc, cmd, alt, excludeCondition = l


	if not excludeCondition or excludeCondition != flavour:

		print(desc, '...')

		out = Popen(cmd, stderr=STDOUT,stdout=PIPE, shell=True)
		output, exitcode = out.communicate()[0].decode(), out.returncode

		if exitcode != 0:
			print(output)
			print()
			print(cmd)
			print()
			print('%s failed! See above.' % desc)
			print()
			if alt:
				print('Debugging output:')
				os.system(alt)
			sys.exit(0)

print('Done.')
print()


# rm -rf ~/Code/TypeWorldApp/build
# rm -rf ~/Code/TypeWorldApp/dist


# # Build
# python3 /Users/yanone/Code/py/git/typeWorld/guiapp/wxPython/build/Mac/setup.py py2app

# # Copy Sparkle over
# cp -R ~/Code/Sparkle-1.19.0/Sparkle.framework ~/Code/TypeWorldApp/dist/Type.World.app/Contents/Frameworks/

# # Copy docktileplugin
# # cp -R /Users/yanone/Code/py/git/typeWorld/guiapp/appbadge/dist/appbadge.docktileplugin ~/Code/TypeWorldApp/dist/Type.World.app/Contents/Resources/

# # Move app to archive folder
# cp -R ~/Code/TypeWorldApp/dist/Type.World.app ~/Code/TypeWorldApp/apps/Mac/Type.World.`cat /Users/yanone/Code/py/git/typeWorld/guiapp/currentVersion.txt`.app

# exit 0