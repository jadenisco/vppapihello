#!/bin/env python
'''
vpp_hello_world.py

This module will demostrate how to use VPP Python API (VPPAPI) 

'''

from vpp_papi import VPPApiClient
import argparse
import logging
import os
import fnmatch

ld_library_path = '/usr/lib/x86_64-linux-gnu/'
vpp_json_dir = '/usr/share/vpp/api/core/'
vpp_json_files = []

def initialize_env(args):
    global vpp_json_files

    logging.debug("initialize_env()")
    logging.debug("  vpp_json_dir: {}".format(vpp_json_dir))

    os.environ["LD_LIBRARY_PATH"] = ld_library_path
    logging.debug("  LD_LIBRARY_PATH: {}".format(os.environ["LD_LIBRARY_PATH"]))  

    vpp_json_files = []
    for root, dirnames, filenames in os.walk(vpp_json_dir):
        for filename in fnmatch.filter(filenames, '*.api.json'):
            vpp_json_files.append(os.path.join(vpp_json_dir, filename))

    if not vpp_json_files:
        logging.error('No json api files found.')
        exit(-1)

def disconnect(vpp):
    logging.debug("disconnect({})".format(vpp))

    vpp.disconnect()
    logging.debug('Disconnected from VPP...')

def connect(args):
    logging.debug("connect({})".format(args))

    # Initialize the environment
    initialize_env(args)

    # Start the connection
    vpp = VPPApiClient(apifiles=vpp_json_files)
    logging.debug("Connecting to VPP...")
    vpp.connect("VPP Hello")
    v = vpp.api.show_version()
    logging.info("VPP Version: {}".format(v))
    print("VPP Version: {}".format(v.version))

def main():

    description = "An example of how to use the VPP API"
    parser = argparse.ArgumentParser(prog='arg-test', description=description,
        epilog='See "%(prog)s help COMMAND" for help on a specific command.')
    parser.add_argument('--debug', '-d', action='count', help='Print debug messages')
    subparsers = parser.add_subparsers()
    conn_parser = subparsers.add_parser('connect', help='Test the VPP connection')
    conn_parser.set_defaults(func=connect)
    args = parser.parse_args()

    if (args.debug):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    if "func" in args:
        return(args.func(args))
    else:
        print("No Arguments were specified. Use -h for help.")

if __name__ == '__main__':

    exit(main())
