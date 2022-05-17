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
import time
import json

ld_library_path = '/usr/lib/x86_64-linux-gnu/'
vpp_json_dir = '/usr/share/vpp/api/core/'
vpp_json_files = []

def _initialize_env():
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

def _disconnect(vpp):
    logging.debug("disconnect({})".format(vpp))

    vpp.disconnect()
    logging.debug('Disconnected from VPP...')

def _connect():
    logging.debug("connect()")

    # Initialize the environment
    _initialize_env()

    # Start the connection
    vpp = VPPApiClient(apifiles=vpp_json_files)
    logging.debug("Connecting to VPP...")
    vpp.connect("VPP Hello")

    return vpp
 
def show_version(args):
    logging.debug("show_version({})".format(args))
    
    vpp = _connect()

    v = vpp.api.show_version()
    logging.info("VPP Version: {}".format(v))
    print("VPP Version: {}".format(v.version))

    exit(_disconnect(vpp))

def dump_interfaces(args):
    logging.debug("dump_interfaces({})".format(args))

    vpp = _connect()

    for interface in vpp.api.sw_interface_dump():
        logging.debug("Interface: {}".format(interface))
        print(interface.interface_name)

    exit(_disconnect(vpp))

def papi_event_handler(msgname, result):
    print(msgname)
    print(result)

def show_stats(args):
    logging.debug("dump_stats({})".format(args))

    vpp = _connect()

    r=vpp.register_event_callback(papi_event_handler)
    
    pid=os.getpid()
    sw_ifs = [1,2,3,4,5,6,7]

    # Need to find api calls

    vpp.api                                                                                                                                                                          
    r = vpp.api.want_per_interface_simple_stats(enable_disable=True, sw_ifs=sw_ifs, num=len(sw_ifs), pid=pid)
    logging.debug(r)

    # Wait for some stats                                                                                                                                                                                    
    time.sleep(60)
    r = vpp.api.want_per_interface_simple_stats(enable_disable=False)

    exit(_disconnect(vpp))

def show_api(args):
    logging.debug("show_api({})".format(args))

    _initialize_env()

    for file in vpp_json_files:
        print("file: {}".format(os.path.basename(file)).split('.')[0])
        with open(file) as f:
            jl = json.loads(f.read())
            logging.debug("  keys: {}".format(jl.keys()))
            for m in jl['messages']:
                print("  messages: {}".format(m[0]))
            f.close()

    return

def main():

    description = "An example of how to use the VPP API"
    parser = argparse.ArgumentParser(prog='arg-test', description=description,
        epilog='See "%(prog)s help COMMAND" for help on a specific command.')
    parser.add_argument('--debug', '-d', action='count', help='Print debug messages')
    subparsers = parser.add_subparsers()
    version_parser = subparsers.add_parser('version', help='Get the VPP Version')
    version_parser.set_defaults(func=show_version)
    dump_parser = subparsers.add_parser('dump', help='Dump VPP interface information')
    dump_parser.set_defaults(func=dump_interfaces)
    stats_parser = subparsers.add_parser('stats', help='Get VPP interface statistics')
    stats_parser.set_defaults(func=show_stats)
    api_parser = subparsers.add_parser('api', help='How the VPP api')
    api_parser.set_defaults(func=show_api)
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
