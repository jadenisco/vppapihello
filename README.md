# VPP API Hello Example

This is an simple example of how to use the VPP API. VPP runs in Linux user space. This example will use an installed version of VPP. The VPP API can also be used on with versions of VPP from a build tree. This example will use python3 and an installed version of VPP

The VPP wiki also has a description of how to use the VPP API. 

The Wiki version of this document is at [VPP/Python API](https://wiki.fd.io/view/VPP/Python_API).

## Install the Python virtual environment package

``` console
$ sudo apt-get install python3-pip
$ sudo pip3 install virtualenv

```

## Install the virtual environment for this app

I did this from the VSCode terminal. With VSCode after you create the environment you should be asked if you want to use this environment. Say yes.

``` console
$ python3 -m venv .venv

```

## Build and install the vpp python api

``` console
$ export VPP="Some VPP root directory"
$ pushd $VPP/src/vpp-api/python/
$ python setup.py install
$ popd
```

## LD_LIBRARY_PATH

The LD_LIBRARY_PATH is set in the vpp_api_hello.py program. LD_LIBRARY_PATH needs to point to libvppapiclient.so. If VPP is installed LD_LIBRARY_PATH should point to '/usr/lib/x86_64-linux-gnu/'.

## Run the script

The vpp_api_hello script needs to be run as root. It can be run like so:

``` console

$ cd vppapihello
$ sudo bash
# source ./.venv/bin/activate
(.venv) # python ./vpp_api_hello.py -h
usage: arg-test [-h] [--debug] {connect} ...

An example of how to use the VPP API

positional arguments:
  {connect}
    connect    Test the VPP connection

optional arguments:
  -h, --help   show this help message and exit
  --debug, -d  Print debug messages

See "arg-test help COMMAND" for help on a specific command.
(.venv) #
(.venv) # python ./vpp_api_hello.py connect
VPP Version: 22.02-release
(.venv) #
(.venv) # python ./vpp_api_hello.py -d connect
DEBUG:root:connect(Namespace(debug=1, func=<function connect at 0x7f1cc8c8e4c0>))
DEBUG:root:initialize_env()
DEBUG:root:  vpp_json_dir: /usr/share/vpp/api/core/
DEBUG:root:  LD_LIBRARY_PATH: /usr/lib/x86_64-linux-gnu/
DEBUG:root:Connecting to VPP...
DEBUG:vpp_papi.vpp_papi.VPPApiClient:Calling show_version('context':1,'_vl_msg_id':1348,'client_index':2147483649)
DEBUG:vpp_papi.vpp_papi.VPPApiClient:Return value: show_version_reply(_0=1349, context=1, retval=0, program='vpe', ve...
INFO:root:VPP Version: show_version_reply(_0=1349, context=1, retval=0, program='vpe', version='22.02-release', build_date='2022-02-23T14:16:58', build_directory='/w/workspace/vpp-merge-2202-ubuntu2004-x86_64')
VPP Version: 22.02-release
DEBUG:vpp_papi:Cleaning up VPP on exit
DEBUG:vpp_papi.vpp_papi.VPPApiClient:Calling sockclnt_delete('index':2147483649,'context':2,'_vl_msg_id':17,'client_index':2147483649)
DEBUG:vpp_papi.vpp_papi.VPPApiClient:Return value: sockclnt_delete_reply(_0=18, context=2, response=1)
(.venv) #

# Some thoughts 

Look at def _call_vpp(self, i, msgdef, service, **kwargs):

The call is made using the index i and the message definition msgdef

Use type(), vars(), dir()