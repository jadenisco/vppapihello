#!/bin/env python
'''
vpp_hello_world.py

This module will demonstrate how to use VPP Python API (VPPAPI) 

'''

from http.client import REQUEST_URI_TOO_LONG
from vpp_papi import VPPApiClient
import asyncio
import argparse
import logging
import os
import fnmatch
import time
import json
import re

ld_library_path = '/usr/lib/x86_64-linux-gnu/'
vpp_json_dir = '/usr/share/vpp/api/core/'
vpp_json_files = []

api_db = {}

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

def papi_event_handler(msg_name, result):
    print(msg_name)
    print(result)


def _show_stats(args):
    logging.debug("_show_stats()")

    vpp = _connect()

    r=vpp.register_event_callback(papi_event_handler)
    
    pid=os.getpid()
    r = vpp.api.want_interface_events(enable_disable=True, pid=pid)
    logging.debug(r)

    # Wait for some stats                                                                                                                                                                                    
    time.sleep(60)

    exit(_disconnect(vpp))

def show_stats(args):
    logging.debug("show_stats({})".format(args))

    asyncio.run(_show_stats(args))

def _show_api(jl):
    logging.debug("_show_api(jl)")

    logging.debug("  keys: {}".format(jl.keys()))
    for m in jl['messages']:
        print("  messages: {}".format(m[0]))

        reply = re.search(r'_reply', m[0])
        if reply != None:
            print("REPLY: {}".format(reply))

def _build_api_db():
    global api_db

    logging.debug("_build_api_db()")

    for file in vpp_json_files:
        module = os.path.basename(file).split('.')[0]
        with open(file) as f:
            jl = json.loads(f.read())

            for m in jl['messages']:
                api_db[m[0]] = {"module": module, "vars": m[4:len(m)-1]}

def _show_method(method, message):
    logging.debug("_show_method({})".format(method))

    print("  Method: {}:".format(method))
    vars = message['vars']
    if len(vars) > 0:
        print("    Vars: <type>, <variable>, [size | default]")
        for v in vars:
            if len(v) == 2:
                print("        {}, {}".format(v[0], v[1]))
            else:
                print("        {}, {}, {}".format(v[0], v[1], v[2]))
    else:
        print("  Vars: None")

def show_api(args):
    global api_db
    module_name = ''

    logging.debug("show_api({})".format(args))

    _initialize_env()

    _build_api_db()

    if args.method != None:
        try:
            message = api_db[args.method]
        except:
            logging.error("The method \"{}\" does not exist.".format(args.method))

        module_name = message['module']
        print("\nModule: {}".format(module_name))
        _show_method(args.method, message)

        reply_method = args.method + '_reply'
        try:
            message = api_db[reply_method]
            _show_method(reply_method, message)
        except:
            print("  There is no reply method.")

        sp = args.method.split('_')

        if sp[len(sp)-1] == 'dump':
            details_method = '_'.join(sp[0:len(sp)-1]) + '_details'
        try:
            message = api_db[details_method]
            _show_method(details_method, message)
        except:
            print("  There is no details method.")

        return

    for method, message in api_db.items():
        if module_name != message['module']:
            m = message['module']
            print("\nModule: {}".format(m))
            module_name = m
        print("  ------")
        _show_method(method, message)

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
    api_parser.add_argument('--method', '-m', help='Show only the specified method.')
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
