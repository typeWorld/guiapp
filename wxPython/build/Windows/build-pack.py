import os, sys

from subprocess import Popen,PIPE,STDOUT

from ynlib.web import GetHTTP
version = GetHTTP('https://api.type.world/latestUnpublishedVersion/world.type.guiapp/windows/')
if version == 'n/a':
    print('Can’t get version number')
    sys.exit(1)


def executeCommands(commands):
	for description, command, mustSucceed in commands:

		# Print which step we’re currently in
		print(description, '...')

		# Execute the command, fetch both its output as well as its exit code
		out = Popen(command, stderr=STDOUT,stdout=PIPE, shell=True)
		output, exitcode = out.communicate()[0], out.returncode

		# If the exit code is not zero and this step is marked as necessary to succeed, print the output and quit the script.
		if exitcode != 0 and mustSucceed:
			print(output)
			print()
			print(command)
			print()
			print('Step "%s" failed! See above.' % description)
			print('Command used: %s' % command)
			print()
			sys.exit(666)


executeCommands([
	['Create InnoSetup .iss file', 'python "Z:\\Code\\py\\git\\typeworld\\guiapp\\wxPython\\build\\Windows\\createissfile.py"', True],
	['Create InnoSetup Installer', '"C:\\Program Files (x86)\\Inno Setup 5\\ISCC.exe" "Z:\\Code\\py\\git\\typeworld\\guiapp\\wxPython\\build\\Windows\\TypeWorld.iss"', True],
	['Signing Installer Package', f'"C:\\Program Files (x86)\\Windows Kits\\10\\bin\\10.0.17134.0\\x64\\signtool.exe" sign /tr http://timestamp.digicert.com /debug /td sha256 /fd SHA256 /a /n "Jan Gerner" "Z:\\Code\\TypeWorldApp\\dmg\\TypeWorldApp.{version}.exe"', True],
	['Verify signature', f'"C:\\Program Files (x86)\\Windows Kits\\10\\bin\\10.0.17134.0\\x64\\signtool.exe" verify /pa /v "Z:\\Code\\TypeWorldApp\\dmg\\TypeWorldApp.{version}.exe"', True],
])


print ('Done.')
