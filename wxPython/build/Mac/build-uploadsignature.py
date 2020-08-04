# -*- coding: utf-8 -*-

import os, sys

version = sys.argv[-1]

def http(url, data=None):
    if data:
        data = urllib.parse.urlencode(data).encode('ascii')
    request = urllib.request.Request(url, data=data)
    sslcontext = ssl.create_default_context(cafile=certifi.where())
    response = urllib.request.urlopen(request, context=sslcontext)
    return response.read().decode()

def execute(command):
	out = Popen(command, stderr=STDOUT,stdout=PIPE, shell=True)
	output, exitcode = out.communicate()[0].decode(), out.returncode
	return output, exitcode


def getEdDSA(file):
	path = '"sparkle/bin/sign_update" "%s"', file)
	dsa = Execute(path).decode()
	return dsa

signature = getEdDSA(f'dmg/TypeWorldApp.{version}.dmg')

response = http('https://api.type.world/setSparkleSignature', data = {'appKey': 'world.type.guiapp', 'version': version, 'platform': 'mac', 'signature': signature})
if not response == 'ok':
	print('Uploading Sparkle signature failed:', response)
	sys.exit(1)
