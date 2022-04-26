# VPP API Hello Example

This is an simple example of how to use the VPP API. VPP runs in Linux user space. This example will use an installed version of VPP. The VPP API can also be used on with versions of VPP from a build tree. This example will use python3.

The VPP wiki also has a description of how to use the VPP API. 

[VPP/Python API](https://wiki.fd.io/view/VPP/Python_API)

## Install the Python virtual environment packages

``` console
$ sudo apt-get install python3-pip
$ sudo pip3 install virtualenv

```

## Install the virtual environment for this app

I did this from the VSCode terminal. After this you should be asked if you want to use this environment. Say yes.

``` console
$ python3 -m venv .venv

```

# install vpp python api
pushd $VPP/src/vpp-api/python/
$VPP/virtualenv/bin/python setup.py install
popd
 
# Now set the LD_LIBRARY_PATH such that it points to the directory containing libvppapiclient.so
export LD_LIBRARY_PATH=`find $VPP -name "libvppapiclient.so" -exec dirname {} \; | grep install-vpp | head -n 1`
 
# You will now need two windows :
# one for vpp, and the other for python
 
# VPP
cd $VPP
make run
 
# python
# (as root, as vpp.connect() requires root privileges)
# Note that sudo cannot not preserve LD_LIBRARY_PATH
cd $VPP
 
# you can run a script 
sudo -E LD_LIBRARY_PATH=$LD_LIBRARY_PATH $VPP/virtualenv/bin/python vpp-api/python/tests/vpp_hello_world.py.py
 
# or get a python prompt
sudo -E LD_LIBRARY_PATH=$LD_LIBRARY_PATH $VPP/virtualenv/bin/python
VPP python'