#!/bin/env python
'''
vpp_hello_world.py
'''
from __future__ import print_function
 
import os
import fnmatch
 
from vpp_papi import VPP 
 
# first, construct a vpp instance from vpp json api files
# this will be a header for all python vpp scripts
 
# directory containing all the json api files.
# if vpp is installed on the system, these will be in /usr/share/vpp/api/
vpp_json_dir = os.environ['VPP'] + '/build-root/install-vpp_debug-native/vpp/share/vpp/api/core'
 
# construct a list of all the json api files
jsonfiles = []
for root, dirnames, filenames in os.walk(vpp_json_dir):
    for filename in fnmatch.filter(filenames, '*.api.json'):
        jsonfiles.append(os.path.join(vpp_json_dir, filename))
 
if not jsonfiles:
    print('Error: no json api files found')
    exit(-1)
 
# use all those files to create vpp.
# Note that there will be no vpp method available before vpp.connect()
vpp = VPP(jsonfiles)
r = vpp.connect('papi-example')
print(r)
# None
 
# You're all set.
# You can check the list of available methods by calling dir(vpp)
 
# show vpp version
rv = vpp.api.show_version()
print('VPP version =', rv.version.decode().rstrip('\0x00'))
# VPP version = 17.04-rc0~192-gc5fccc0c
 
# disconnect from vpp
r = vpp.disconnect()
print(r)
# 0
 
exit(r)